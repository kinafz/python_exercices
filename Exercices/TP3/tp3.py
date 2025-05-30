import mysql.connector
from tabulate import tabulate
from dotenv import load_dotenv
from mysql.connector import Error
import os
from datetime import datetime
import time
import random
import argparse
import pymongo
from pymongo.errors import ConnectionFailure, ConfigurationError, InvalidURI

load_dotenv()

try:
    mongoClient = pymongo.MongoClient(
        host=os.getenv('MONGO_HOST', 'localhost'),
        port=27017,
    )
    mongo_db = mongoClient[os.getenv('MONGO_DATABASE')]
    logs_collection = mongo_db['audit_logs']
except (ConnectionFailure, ConfigurationError, InvalidURI) as conn_err:
    print(f"Erreur de connexion à MongoDB : {conn_err}")
    logs_collection = None
except ValueError as ve:
    print(f"Erreur de configuration : {ve}")
    logs_collection = None
except Exception as e:
    print(f"Erreur inconnue : {e}")
    logs_collection = None

connection = mysql.connector.connect(
    host=os.getenv('MYSQL_HOST', 'localhost'),
    user=os.getenv('MYSQL_USER'),
    password=os.getenv('MYSQL_PASSWORD'),
    database=os.getenv('MYSQL_DATABASE'),
    auth_plugin='mysql_native_password',
    port=3306
)
if connection.is_connected():
    db_Info = connection.server_info
    print("Connecté à MySQL, version :", db_Info)
    with connection.cursor() as cursor:
        cursor.execute("SELECT DATABASE();")
        record = cursor.fetchone()
        print("Base de données actuelle :", record)
else:
    print("Erreur de connexion à la base de données MySQL.")
    exit(1)

def updateDb(connection, folder_path="scripts"):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(base_dir, "scripts")

    scripts = sorted([
        f for f in os.listdir(folder_path)
        if f.endswith(".sql")
    ])

    with connection.cursor() as cursor:
        for script_file in scripts:
            script_path = os.path.join(folder_path, script_file)
            print(f"\nExécution du script : {script_file}")
            
            with open(script_path, "r", encoding="utf-8") as file:
                sql_commands = file.read()
            
            try:
                for statement in sql_commands.strip().split(";"):
                    if statement.strip():
                        cursor.execute(statement)
                connection.commit()
                print("Terminé avec succès.")
            except mysql.connector.Error as err:
                print(f"Erreur dans {script_file} : {err}")
                connection.rollback()
                exit(1)

updateDb(connection)

def log_action(action, **kwargs):
    logs_collection.insert_one({
        "action": action,
        **kwargs,
        "timestamp": datetime.now()
    })

def create_release(version, tag):
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO releases (version, tag_git, date_creation) VALUES (%s, %s, %s)",
                  (version, tag, datetime.now()))
        connection.commit()
        print("Release created.")
        
def deploy_release(release_id, env_name):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id FROM environnements WHERE nom = %s", (env_name,))
        env = cursor.fetchone()
        if not env:
            print("Invalid environment.")
            return
        cursor.execute("INSERT INTO deploiements (id_release, id_env, etat, date_deploiement) VALUES (%s, %s, %s, %s)",
                  (release_id, env[0], 'planifié', datetime.now()))
        connection.commit()
        print("Deployment planned.")
        
def validate_and_execute(deploy_id):
    try:
        connection.start_transaction()
        with connection.cursor() as cursor:
            cursor.execute("SELECT id_env, etat FROM deploiements WHERE id = %s", (deploy_id,))
            row = cursor.fetchone()
            if not row:
                print("Deployment not found.")
                return
            env_id, state = row
            cursor.execute("SELECT COUNT(*) FROM deploiements WHERE id_env = %s AND etat = 'en_cours'", (env_id,))
            if cursor.fetchone()[0] > 0:
                print("Another deployment is already in progress.")
                return

            cursor.execute("UPDATE deploiements SET etat = 'en_cours' WHERE id = %s", (deploy_id,))
            print("Deployment started...")
            time.sleep(2)

            if random.choice([True, False]):
                cursor.execute("UPDATE deploiements SET etat = 'réussi' WHERE id = %s", (deploy_id,))
                log_action("DEPLOY_SUCCESS",
                           message=f"Deployment {deploy_id} succeeded.",
                           deploy_id=deploy_id,
                           etat_initial=state,
                           etat_final='réussi',
                           source='cli')
                print("Deployment successful.")
            else:
                cursor.execute("UPDATE deploiements SET etat = 'annulé' WHERE id = %s", (deploy_id,))
                log_action("DEPLOY_FAIL",
                           message=f"Deployment {deploy_id} failed and was rolled back.",
                           deploy_id=deploy_id,
                           etat_initial=state,
                           etat_final='annulé',
                           source='cli')
                print("Deployment failed and rolled back.")

            connection.commit()
    except Exception as e:
        connection.rollback()
        log_action("ERROR",
            message=f"Error during deployment.",
            deploy_id=deploy_id,
            etat_initial=state,
            etat_final='annulé',
            source='cli')
    finally:
        connection.close()
        
def status(env_name):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                e.nom, r.version, d.etat, d.date_deploiement
            FROM deploiements d
                INNER JOIN releases r ON d.id_release = r.id
                INNER JOIN environnements e ON d.id_env = e.id
            WHERE e.nom = %s
            ORDER BY d.date_deploiement DESC
            LIMIT 1
        """, (env_name,))
        row = cursor.fetchone()
        if row:
            print(f"Env: {row[0]}, Version: {row[1]}, State: {row[2]}, Date: {row[3]}")
        else:
            print("No deployment found for this environment.")
            
def display_logs_mongo():
    try:
        cursor = logs_collection.find().sort("timestamp", pymongo.DESCENDING)
        logs = list(cursor)
        if not logs:
            print("No logs found.")
            return

        log_data = []
        for log in logs:
            log_data.append([
                log.get("action"),
                log.get("message", ""),
                log.get("deploy_id", ""),
                log.get("etat_initial", ""),
                log.get("etat_final", ""),
                log.get("source", ""),
                log.get("timestamp")
            ])

        headers = ["Action", "Message", "Deploy ID", "Etat Initial", "Etat Final", "Source", "Timestamp"]
        print(tabulate(log_data, headers=headers, tablefmt="grid"))
    except Exception as e:
        print(f"Error retrieving logs: {e}")
            
def display_menu():
    while True:
        print("\n=== MENU ===")
        print("1. Créer une release")
        print("2. Planifier un déploiement")
        print("3. Valider et exécuter un déploiement")
        print("4. Voir le statut d'un environnement")
        print("5. Annuler un déploiement")
        print("6. Afficher les logs de déploiement")
        print("7. Quitter")
        choice = input("Choisissez une option : ")

        if choice == "1":
            version = input("Version : ")
            tag = input("Tag Git : ")
            create_release(version, tag)
        elif choice == "2":
            release_id = int(input("ID Release : "))
            env = input("Environnement (dev, staging, prod) : ")
            deploy_release(release_id, env)
        elif choice == "3":
            deploy_id = int(input("ID du déploiement : "))
            validate_and_execute(deploy_id)
        elif choice == "4":
            env = input("Environnement : ")
            status(env)
        elif choice == "5":
            deploy_id = int(input("ID du déploiement à annuler : "))
            rollback(deploy_id)
        elif choice == "6":
            display_logs_mongo()
        elif choice == "7":
            print("Au revoir !")
            break
        else:
            print("Choix invalide.")
            
def rollback(deploy_id):
    with connection.cursor() as cursor:
        cursor.execute("UPDATE deploiements SET etat = 'annulé' WHERE id = %s", (deploy_id,))
        log_action("ROLLBACK",
            message=f"Rollback deployment {deploy_id}.",
            deploy_id=deploy_id,
            etat_final='annulé',
            source='cli')
        connection.commit()
        print("Rollback executed.")
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    release_parser = subparsers.add_parser('release')
    release_parser.add_argument('--create')
    release_parser.add_argument('--tag')

    deploy_parser = subparsers.add_parser('deploy')
    deploy_parser.add_argument('--release', type=int)
    deploy_parser.add_argument('--env')

    validate_parser = subparsers.add_parser('validate')
    validate_parser.add_argument('--deploy-id', type=int)

    status_parser = subparsers.add_parser('status')
    status_parser.add_argument('--env')

    rollback_parser = subparsers.add_parser('rollback')
    rollback_parser.add_argument('--deploy-id', type=int)
    
    rollback_parser = subparsers.add_parser('logs')
    rollback_parser.add_argument('--mongo', action='store_true')

    args = parser.parse_args()

    if args.command == 'release':
        create_release(args.create, args.tag)
    elif args.command == 'deploy':
        deploy_release(args.release, args.env)
    elif args.command == 'validate':
        validate_and_execute(args.deploy_id)
    elif args.command == 'status':
        status(args.env)
    elif args.command == 'rollback':
        rollback(args.deploy_id)
    elif args.command == 'logs':
        if args.mongo:
            display_logs_mongo()
        else:
            print("Option invalide pour les logs. Utilisez --mongo pour afficher les logs MongoDB.")
    elif args.command is None:
        display_menu()
    else:
        print("Commande invalide")
        parser.print_help()