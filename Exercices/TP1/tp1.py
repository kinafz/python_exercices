import mysql.connector
from tabulate import tabulate
from dotenv import load_dotenv
from mysql.connector import Error
import os

load_dotenv()

password=os.getenv('DATABASE_PASSWORD')
connection = mysql.connector.connect(
    host='localhost',
    user='afilez',
    password=password,
    database='afilez',
    auth_plugin='mysql_native_password'
)
if connection.is_connected():
    db_Info = connection.get_server_info()
    print("Connecté à MySQL, version :", db_Info)
    with connection.cursor() as cursor:
        cursor.execute("SELECT DATABASE();")
        record = cursor.fetchone()
        print("Base de données actuelle :", record)
else:
    print("Erreur de connexion à la base de données.")
    exit(1)

prioriteMap = {
    "1": "faible",
    "2": "moyenne",
    "3": "haute"
}

def addTicket(connection):
    with connection.cursor() as cursor:
        titre = None
        while titre is None or titre.strip() == "":
            titre = input("Merci de saisir le titre du ticket : ")
            if titre.strip() == "":
                print("Le titre ne peut pas être vide. Veuillez réessayer.")
        description = None
        while description is None or description.strip() == "":
            description = input("Merci de saisir la description du ticket : ")
            if description.strip() == "":
                print("La description ne peut pas être vide. Veuillez réessayer.")
        priorite = None
        while priorite not in prioriteMap:
            print("Merci de saisir la priorité du ticket :")
            print("1. Faible")
            print("2. Moyenne")
            print("3. Haute")
            priorite = input("Entrez le numéro de la priorité : ")
            if priorite not in prioriteMap:
                print("Priorité invalide. Veuillez réessayer.")

        cursor.execute("INSERT INTO tickets (titre, description, priorite) VALUES (%s, %s, %s)", (titre, description, prioriteMap.get(priorite)))
        connection.commit()
        print("Ticket ajouté avec succès.")
        displayMenu()

def displayTickets(connection):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, titre, description, priorite, statut, date_creation FROM tickets")
        tickets = cursor.fetchall()
        if tickets:
            print("Liste des tickets :")
            headers = ["ID", "Titre", "Description", "Priorité", "Statut", "Date de création"]
            tickets = [(ticket[0], ticket[1], ticket[2], ticket[3], ticket[4], ticket[5].strftime("%Y-%m-%d %H:%M:%S")) for ticket in tickets]
            print(tabulate(tickets, headers=headers, tablefmt="fancy_grid"))
        else:
            print("Aucun ticket trouvé.")
    displayMenu()
    
def exitProgram():
    connection.close()
    exit(0)
    
def displayMenu():
    print("1. Afficher les tickets")
    print("2. Ajouter un ticket")
    print("3. Quitter")
    choice = input("Veuillez choisir une option : ")
    if choice == "1":
        displayTickets(connection)
    elif choice == "2":
        addTicket(connection)
    elif choice == "3":
        exitProgram()
    else:
        print("Choix invalide. Veuillez réessayer.")
        displayMenu()
displayMenu()