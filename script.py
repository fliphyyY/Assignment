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

#create_user(name, surname, tel, office)





def main():
    getLinks()
    createFile()
    # text = ['EMPLOYEES']
    # with open('textfile.txt', 'w', encoding="utf-8") as f:
    #         f.writelines('\n'.join(text) + '\n')
    for i in range(len(sites)):
        getPageEmployee(sites[i])
        nameSurname(sites[i])
        officeNumber()
        phoneNumer()
        create_user(name, surname, tel, office)

        # with open('textfile.txt', 'a', encoding="utf-8") as f:
        #     f.writelines('*****************************\n')
        #     f.writelines(name + '\n')
        #     f.writelines(surname + '\n')
        #     f.writelines(office + '\n')
        #     f.writelines(tel + '\n')
        #     f.writelines('*****************************\n')


if __name__=="__main__":
    main()






