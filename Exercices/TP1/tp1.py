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

prioriteMap = {
    "1": "Faible",
    "2": "Moyenne",
    "3": "Haute"
}

statusMap = {
    "1": "Ouvert",
    "2": "En cours",
    "3": "Fermé"
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
            for key, label in prioriteMap.items():
                print(f"{key}. {label}")
            priorite = input("Entrez le numéro de la priorité : ")
            if priorite not in prioriteMap:
                print("Priorité invalide. Veuillez réessayer.")

        cursor.execute("INSERT INTO tickets (titre, description, priorite) VALUES (%s, %s, %s)", (titre, description, prioriteMap.get(priorite).lower()))
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
    
def updateTicketPriority(connection):
    ticketId = None
    while ticketId is None or not ticketId.isdigit():
        ticketId = input("Merci de saisir l'ID du ticket à modifier : ")
        if not ticketId.isdigit():
            print("ID invalide. Veuillez saisir un nombre entier.")
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM tickets WHERE id = %s", (ticketId,))
            if cursor.fetchone() is None:
                print("Aucun ticket trouvé avec cet ID. Veuillez réessayer.")
                return
        newPriority = None
        while newPriority not in prioriteMap:
            print("Merci de saisir la nouvelle priorité du ticket :")
            for key, label in prioriteMap.items():
                print(f"{key}. {label}")
            newPriority = input("Entrez le numéro de la nouvelle priorité : ")
            if newPriority not in prioriteMap:
                print("Priorité invalide. Veuillez réessayer.")
        
        with connection.cursor() as cursor:
            cursor.execute("UPDATE tickets SET priorite = %s WHERE id = %s", (prioriteMap.get(newPriority).lower(), ticketId))
            connection.commit()
            print("Priorité du ticket mise à jour avec succès.")
    displayMenu()

def updateTicketStatus(connection):
    ticketId = None
    while ticketId is None or not ticketId.isdigit():
        ticketId = input("Merci de saisir l'ID du ticket à modifier : ")
        if not ticketId.isdigit():
            print("ID invalide. Veuillez saisir un nombre entier.")
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM tickets WHERE id = %s", (ticketId,))
            if cursor.fetchone() is None:
                print("Aucun ticket trouvé avec cet ID. Veuillez réessayer.")
                return
        newStatus = None
        while newStatus not in statusMap:
            print("Merci de saisir le nouveau statut du ticket :")
            for key, label in statusMap.items():
                print(f"{key}. {label}")
            newStatus = input("Entrez le numéro du nouveau statut : ")
            if newStatus not in statusMap:
                print("Statut invalide. Veuillez réessayer.")
        with connection.cursor() as cursor:
            cursor.execute("UPDATE tickets SET statut = %s WHERE id = %s", (statusMap.get(newStatus).lower(), ticketId))
            connection.commit()
            print("Statut du ticket mis à jour avec succès.")
    displayMenu()

def deleteTicket(connection):
    with connection.cursor() as cursor:
        ticket_id = input("Merci de saisir l'ID du ticket à supprimer : ")
        cursor.execute("DELETE FROM tickets WHERE id = %s", (ticket_id,))
        connection.commit()
        print("Ticket supprimé avec succès.")
    displayMenu()
    
def exitProgram():
    connection.close()
    exit(0)
    
def displayMenu():
    print("1. Afficher les tickets")
    print("2. Ajouter un ticket")
    print("3. Modifier la priorité d'un ticket")
    print("4. Modifier le statut d'un ticket")
    print("5. Supprimer un ticket")
    print("6. Quitter")
    choice = input("Veuillez choisir une option : ")
    if choice == "1":
        displayTickets(connection)
    elif choice == "2":
        addTicket(connection)
    elif choice == "3":
        updateTicketPriority(connection)
        displayMenu()
    elif choice == "4":
        updateTicketStatus(connection)
        displayMenu()
    elif choice == "5":
        deleteTicket(connection)
    elif choice == "6":
        exitProgram()
    else:
        print("Choix invalide. Veuillez réessayer.")
        displayMenu()
displayMenu()