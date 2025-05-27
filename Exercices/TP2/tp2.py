import mysql.connector
from tabulate import tabulate
from dotenv import load_dotenv
from mysql.connector import Error
import os

load_dotenv()

connection = mysql.connector.connect(
    host='mysql',
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
    print("Erreur de connexion à la base de données.")
    exit(1)


def updateDb(connection, folder_path="scripts"):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(base_dir, "scripts")

    scripts = sorted([
        f for f in os.listdir(folder_path)
        if f.endswith(".sql")
    ])

    cursor = connection.cursor()
    
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

    cursor.close()

updateDb(connection)

def addUser(connection):
    nom = None
    while nom is None or nom.strip() == "":
        nom = input("Merci de saisir le nom de l'utilisateur : ")
        if nom.strip() == "":
            print("Le nom ne peut pas être vide. Veuillez réessayer.")
    email = None
    while email is None or email.strip() == "":
        email = input("Merci de saisir l'email de l'utilisateur : ")
        if email.strip() == "":
            print("L'email ne peut pas être vide. Veuillez réessayer.")
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO utilisateurs (nom, email) VALUES (%s, %s)", (nom, email))
        connection.commit()
        print(f"Utilisateur {nom} ajouté avec succès.")
    except mysql.connector.Error as err:
        print(f"Erreur lors de l'ajout de l'utilisateur : {err}")
        connection.rollback()
    finally:
        cursor.close()
        
def addLivre(connection):
    titre = None
    while titre is None or titre.strip() == "":
        titre = input("Merci de saisir le titre du livre : ")
        if titre.strip() == "":
            print("Le titre ne peut pas être vide. Veuillez réessayer.")
    auteur = None
    while auteur is None or auteur.strip() == "":
        auteur = input("Merci de saisir l'auteur du livre : ")
        if auteur.strip() == "":
            print("L'auteur ne peut pas être vide. Veuillez réessayer.")
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO livres (titre, auteur) VALUES (%s, %s)", (titre, auteur))
        connection.commit()
        print(f"Livre '{titre}' ajouté avec succès.")
    except mysql.connector.Error as err:
        print(f"Erreur lors de l'ajout du livre : {err}")
        connection.rollback()
    finally:
        cursor.close()
        
def addEmprunt(connection):
    idUtilisateur = None
    while idUtilisateur is None:
        idUtilisateur = input("Merci de saisir l'ID de l'utilisateur : ")
        if not idUtilisateur.isdigit():
            print("L'ID de l'utilisateur doit être un nombre. Veuillez réessayer.")
            idUtilisateur = None
    idLivre = None
    while idLivre is None:
        idLivre = input("Merci de saisir l'ID du livre : ")
        if not idLivre.isdigit():
            print("L'ID du livre doit être un nombre. Veuillez réessayer.")
            idLivre = None
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO emprunts (id_utilisateur, id_livre) VALUES (%s, %s)", (idUtilisateur, idLivre))
        connection.commit()
        print(f"Emprunt ajouté avec succès pour l'utilisateur ID {idUtilisateur} et le livre ID {idLivre}.")
    except mysql.connector.Error as err:
        print(f"Erreur lors de l'ajout de l'emprunt : {err}")
        connection.rollback()
    finally:
        cursor.close()
        
def displayEmprunts(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("""
            SELECT
                e.id,
                u.nom,
                l.titre,
                e.date_emprunt,
                e.date_retour
            FROM emprunts e
            INNER JOIN utilisateurs u ON u.id = e.id_utilisateur
            INNER JOIN livres l ON l.id = e.id_livre
            WHERE e.date_retour IS NULL OR e.date_retour < NOW()
        """)
        emprunts = cursor.fetchall()
        if emprunts:
            print(tabulate(emprunts, headers=["ID", "Utilisateur", "Livre", "Date d'emprunt", "Date de retour"], tablefmt="fancy_grid"))
        else:
            print("Aucun emprunt trouvé.")
    except mysql.connector.Error as err:
        print(f"Erreur lors de la récupération des emprunts : {err}")
    finally:
        cursor.close()
        
def displayUsers(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT id, nom, email FROM utilisateurs")
        users = cursor.fetchall()
        if users:
            print(tabulate(users, headers=["ID", "Nom", "Email"], tablefmt="fancy_grid"))
        else:
            print("Aucun utilisateur trouvé.")
    except mysql.connector.Error as err:
        print(f"Erreur lors de la récupération des utilisateurs : {err}")
    finally:
        cursor.close()
        
def displayLivres(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT id, titre, auteur FROM livres")
        livres = cursor.fetchall()
        if livres:
            print(tabulate(livres, headers=["ID", "Titre", "Auteur"], tablefmt="fancy_grid"))
        else:
            print("Aucun livre trouvé.")
    except mysql.connector.Error as err:
        print(f"Erreur lors de la récupération des livres : {err}")
    finally:
        cursor.close()
        
def displayMenu():
    print("1. Ajouter un utilisateur")
    print("2. Afficher les utilisateurs")
    print("3. Ajouter un livre")
    print("4. Afficher les livres")
    print("5. Enregistrer un emprunt")
    print("6. Afficher les emprunts en cours")
    print("7. Quitter")
    choice = input("Veuillez choisir une option : ")
    if choice == "1":
        addUser(connection)
    elif choice == "2":
        displayUsers(connection)
    elif choice == "3":
        addLivre(connection)
    elif choice == "4":
        displayLivres(connection)
    elif choice == "5":
        addEmprunt(connection)
    elif choice == "6":
        displayEmprunts(connection)
    elif choice == "5":
        print("Au revoir !")
        connection.close()
        exit(0)
    else:
        print("Choix invalide. Veuillez réessayer.")
    displayMenu()
    
displayMenu()