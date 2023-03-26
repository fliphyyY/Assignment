import requests
import sqlite3
from bs4 import BeautifulSoup
import os.path

soup = ''
name = ''
surname = ''
office = ''
tel = ''
sites = []

def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

def sql_database():
    conn = sqlite3.connect('Client_data.db') #Opens Connection to SQLite database file.
    conn.execute('''CREATE TABLE Employee_db
                (NAME            BLOB NOT NULL,
                SURNAME         BLOB NOT NULL,
                PHONE           BLOB NOT NULL,
                OFFICE          BLOB NOT NULL  
                );''') #Creates the table
    conn.commit() # Commits the entries to the database
    conn.close()

def create_user(name, surname, phone, office):
    conn = sqlite3.connect('Client_data.db')
    cursor = conn.cursor()
    params = (name, surname, phone, office)
    cursor.execute("INSERT INTO Employee_db VALUES (?,?,?,?)",params)
    conn.commit()
    print('Employee inserted into the database!')
    conn.close()

def highest_number_employees():
    conn = sqlite3.connect('Client_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT OFFICE, COUNT(*) FROM Employee_db WHERE OFFICE != '' GROUP BY OFFICE ORDER BY COUNT(*) desc limit 1")
    result = cursor.fetchall()
    return result

def getOfficeEmployees(office):
    conn = sqlite3.connect('Client_data.db')
    params = (office)
    cursor = conn.cursor()
    cursor.execute("SELECT NAME, SURNAME FROM Employee_db WHERE OFFICE =?",(params,))
    result = cursor.fetchall()
    return result



def getLinks():

    url = "https://www.ics.muni.cz/en/about-us/employees"
    html = requests.get(url).content
    soup = BeautifulSoup(html, "html.parser")

    links = [a["href"] for a in soup.find_all("a", href=True)]
    for i in range(len(links)):
        if has_numbers(links[i]) and links[i] not in sites:
            sites.append('https://www.ics.muni.cz/' + links[i])


def getPageEmployee(urlEmployee):
    url = urlEmployee
    html = requests.get(url).content
    global soup
    soup = BeautifulSoup(html, "html.parser")
    soup = str(soup)

def nameSurname(urlEmployee):
    urlParse = urlEmployee.split('-')
    global name
    global surname
    name = urlParse[len(urlParse) - 2]
    surname = urlParse[len(urlParse) - 1]

def officeNumber():
    startIndex = soup.find("Office:")
    global office
    if startIndex != '-1':
        office = soup[startIndex:startIndex + 30]
        office = office[8:30].strip()


def phoneNumer():
    startIndex = soup.find("tel:")
    global tel
    if startIndex != '-1':
        tel = soup[startIndex:startIndex + 17]
        tel = tel[4:17].strip()

def createFile():
    path = './Client_data.db'
    check_file = os.path.exists(path)
    if check_file is False:
        sql_database()
    else: 
        os.remove("Client_data.db")
        sql_database()

def main():
    getLinks()
    createFile()
    text = ['EMPLOYEES']
    for i in range(len(sites)):
        getPageEmployee(sites[i])
        nameSurname(sites[i])
        officeNumber()
        phoneNumer()
        create_user(name, surname, tel, office)

    cursorResultHighestNumber = highest_number_employees()
    cursorResultEmployees = getOfficeEmployees(str(cursorResultHighestNumber[0][0]))
    print('\nThe name of the office with highest number employees is ' + cursorResultHighestNumber[0][0] + ' and the count of the employees is ' + str(cursorResultHighestNumber[0][1]) +'.\n')

    for i in range(len(cursorResultEmployees)):
        print(cursorResultEmployees[i][0].capitalize() + ' ' + cursorResultEmployees[i][1].capitalize())


if __name__=="__main__":
    main()






