import requests
import sqlite3
from bs4 import BeautifulSoup
import os.path


soup = ''
name = ''
surname = ''
office = ''
tel = ''

class Employee:
  def __init__(self, name, surname, email, phone, office):
    self.name = name
    self.surname = surname
    self.email = email
    self.phone = phone
    self.office = office


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
    print('User Creation Successful')
    conn.close()


def getLinks():

    url = "https://www.ics.muni.cz/en/about-us/employees"
    html = requests.get(url).content
    soup = BeautifulSoup(html, "html.parser")
    sites = []

    links = [a["href"] for a in soup.find_all("a", href=True)]
    for i in range(len(links)):
        if has_numbers(links[i]) and links[i] not in sites:
            sites.append('https://www.ics.muni.cz/' + links[i])


def getPageEmployee():
    url = "https://www.ics.muni.cz/en/about-us/employees/255519-petr-velan"
    html = requests.get(url).content
    soup = BeautifulSoup(html, "html.parser")
    soup = str(soup)

def nameSurname():
    urlParse = url.split('-')
    name = urlParse[len(urlParse) - 2]
    surname = urlParse[len(urlParse) - 1]
    print(name)
    print(surname)

def office():
    startIndex = soup.find("Office")
    office = soup[startIndex:startIndex + 30]
    office = office[8:30].strip()
    print(office)


def phoneNumer():
    startIndex = soup.find("tel:")
    tel = soup[startIndex:startIndex + 17]
    tel = tel[4:17].strip()
    print(tel)

def createFile():
    path = './Client_data.db'
    check_file = os.path.exists(path)
    print(check_file)
    if check_file is False:
        sql_database()

#create_user(name, surname, tel, office)





def main():
    getLinks()





