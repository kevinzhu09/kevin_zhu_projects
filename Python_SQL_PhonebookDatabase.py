# Completely done by Kevin Zhu

import psycopg2
# PLEASE READ to SET UP:
# 1. PostgreSQL and pgAdmin must first be set up and installed on the system 
# 2. in pgAdmin, set up the user/password and create the database. I believe the default username is postgres. 

# Change these values below to the username/password/database name you chose. 
databasename='postgres' 
username='postgres' 
password='SamplePassword'
# The host should stay as localhost and does not need to be changed unless there are special circumstances. 
host='localhost'

# 3. run the command "pip install psycopg2" in the terminal to use the package.
# 4. The application will take care of the rest so just run this application.
# 
# Please do not use this application and the postgreSQL database at the same time.



from functools import total_ordering

def findUsers(cur):
    while(True):
        answer = int(input("""\nLooking up a user(s)? You will need to provide either the user's first name, last name, or phone number.

(1) I know the user's first name
(2) I know the user's last name
(3) I know the user's phone number
(4) Go back to the main menu\n
"""))
        if (answer==1):
            knownInfo = "first name"
            modifyingSQL = "first_name"
        elif (answer==2):
            knownInfo = "last name"
            modifyingSQL = "last_name"
        elif (answer==3):
            knownInfo = "phone number"
            modifyingSQL = "phone_number"
        elif(answer==4):
            return
        else:
            print("That was not a possible choice. Enter a number(1,2,3 or 4)")

        if (knownInfo=="phone number"):
            lookupValue = input("\nWhat is the user's phone number? Use the format ###-###-####. ")
        else:
            lookupValue = input("\nWhat is the user's %s? This is case-sensitive. " % (knownInfo))
        confirmation = input("\nLooking up users with the %s: %s." % (knownInfo, lookupValue)
            + " Is this correct? Enter 'no' if this is wrong.\nTo confirm this is correct and modify this user, just press Enter.\n")
        if (confirmation.lower()=="no" or confirmation.lower()=="'no'"):
            continue
        try:
            cur.execute("SELECT * FROM users WHERE %s = '%s';" % (modifyingSQL,lookupValue))
        except Exception as e:
            print("There was an issue, and the user could not be found. It could be because the %s is invalid or does not exist within the database. " % (knownInfo)
            + "\nError info: " + e)
            continue
        else:
            print("The user(s) was successfully found in the phonebook database. Here are the results.\n")
            data_records = cur.fetchall() 
            
            for row in data_records:
                print("Id: " + str(row[0]) + " | First name: " + row[1] + " | Last name: " + row[2] + " | Phone number: " + row[3])
            
            input("\nPress Enter to continue.")
            return


def addUsers(cur):
    while(True):
        answer = int(input("""\nAdding a user? How will you do this? (Keep in mind, phone numbers must be unique.)

(1) Manually enter their first and last name, and phone number.
(2) Go back to the main menu\n
"""))
        if (answer==1):
            firstName = input("What is the first name? Enter /leave to go back to the previous menu.\n").capitalize()
            if (firstName.lower()=="/leave" or firstName.lower()=="\\leave"):
                continue
            lastName = input("What is the last name? Enter /leave to go back to the previous menu.\n").capitalize()
            if (lastName.lower()=="/leave" or lastName.lower()=="\\leave"):
                continue
            phoneNumber = input("What is the phone number? Use the format ###-###-####. Enter /leave to go back to the previous menu.\n")
            if (phoneNumber.lower()=="/leave" or phoneNumber.lower()=="\\leave"):
                continue
            confirmation = input("\n%s %s has the phone number: %s. Is this correct? Enter 'no' if this is wrong. To confirm this is correct and add this user, just press Enter.\n" % (firstName,lastName,phoneNumber))
            if (confirmation.lower()=="no" or confirmation.lower()=="'no'"):
                continue
            try:
                cur.execute("INSERT INTO users(first_name, last_name, phone_number) VALUES ('%s', '%s', '%s');" % (firstName,lastName,phoneNumber))
            except Exception as e:
                print("There was an issue, and the user could not be added. It could be because a duplicate phone number would have been added. Error info: " + e)
                continue
            else:
                print("The user was successfully added to the phonebook database.")
                return
        elif (answer==2):
            return
        else:
            print("That was not a possible choice. Enter a number(1 or 2)")

def deleteUsers(cur):
    while(True):
        answer = int(input("""\nDeleting a user? You will need to provide the user's phone number. Use "find a user" in the main menu if you need to get their phone number.

(1) Delete a user by providing their phone number
(2) Go back to the main menu\n
"""))
        if (answer==1):
            phoneNumber = input("What is the phone number? Use the format ###-###-####. Enter /leave to go back to the previous menu.\n")
            if (phoneNumber.lower()=="/leave" or phoneNumber.lower()=="\\leave"):
                continue
            confirmation = input("\nDeleting the user with the phone number: %s. Is this correct? Enter 'no' if this is wrong. To confirm this is correct and delete this user, just press Enter.\n" % (phoneNumber))
            if (confirmation.lower()=="no" or confirmation.lower()=="'no'"):
                continue
            try:
                cur.execute("DELETE FROM users WHERE phone_number = '%s'" % (phoneNumber))
            except Exception as e:
                print("There was an issue, and the user could not be deleted. It could be because the phone number is invalid. Error info: " + e)
                continue
            else:
                print("The user was successfully deleted from the phonebook database.")
                return
        elif (answer==2):
            return
        else:
            print("That was not a possible choice. Enter a number(1 or 2)")

def modifyUsers(cur):
    while(True):
        answer = int(input("""\nModifying a user? You will need to provide the user's phone number. Use "find a user" in the main menu if you need to get their phone number.

(1) Modify a user by providing their phone number
(2) Go back to the main menu\n
"""))
        if (answer==1):
            phoneNumber = input("\nWhat is the phone number? Use the format ###-###-####. Enter /leave to go back to the previous menu.\n\n")
            if (phoneNumber.lower()=="/leave" or phoneNumber.lower()=="\\leave"):
                continue
            changeAnswer = int(input("""\nWhat would you like to change about this user? You can only change one thing.

(1) Modify the user's first name
(2) Modify the user's last name
(3) Modify the user's phone number
(4) Go back to the previous menu\n
"""))
            if (changeAnswer==1):
                whatToChange = "first name"
                modifyingSQL = "first_name"
            elif (changeAnswer==2):
                whatToChange = "last name"
                modifyingSQL = "last_name"
            elif (changeAnswer==3):
                whatToChange = "phone number"
                modifyingSQL = "phone_number"
            elif (changeAnswer==4):
                continue
            if (whatToChange=="phone number"):
                newValue = input("\nWhat is the new phone number? Use the format ###-###-####. ")
            else:
                newValue = input("\nWhat is the new %s? " % (whatToChange))
            confirmation = input("\nModifying the user with the phone number: %s and changing their %s to: %s." % (phoneNumber, whatToChange, newValue)
             + " Is this correct? Enter 'no' if this is wrong.\nTo confirm this is correct and modify this user, just press Enter.\n")
            if (confirmation.lower()=="no" or confirmation.lower()=="'no'"):
                continue
            try:
                cur.execute("UPDATE users SET %s = '%s' WHERE phone_number = '%s';" % (modifyingSQL, newValue, phoneNumber))
            except Exception as e:
                print("There was an issue, and the user could not be modified. It could be because the phone number is invalid. Error info: " + e)
                continue
            else:
                print("The user was successfully modified in the phonebook database.")
                return
        elif (answer==2):
            return
        else:
            print("That was not a possible choice. Enter a number(1 or 2)")

def main():
    print("Welcome to Kevin's Phonebook Database!")
    
    try:
        conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (databasename,username,host,password))
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id serial PRIMARY KEY,
        first_name VARCHAR (50) NOT NULL,
        last_name VARCHAR (50) NOT NULL,
        phone_number VARCHAR (20) NOT NULL,
        CONSTRAINT UX_users_phone_number UNIQUE (phone_number)
        );''')
    except Exception as inst:
        print ("There was an error connecting to the database. \nDetails: " + inst)
        exit()

    while(True):
        answer = int(input("""\nWhat would you like to do next? Enter the number(1,2,3,4 or 5) corresponding to your choice.

(1) (Find a user) Look up and Display information about a user you know something about
(2) Add users to the phonebook
(3) Remove existing users from the phonebook
(4) Modify existing users in the phonebook
(5) Exit the phonebook database\n
"""))
        if (answer==1):
            findUsers(cur)
        elif (answer==2):
            addUsers(cur)
        elif (answer==3):
            deleteUsers(cur)
        elif (answer==4):
            modifyUsers(cur)
        elif (answer==5):
            print("\nThank you for using Kevin's Phonebook Database!")
            break
        else:
            print("That was not a possible choice. Enter a number(1,2,3,4 or 5)")
            

@total_ordering
class User:
    def __init__(self, line):
        self._firstName = ''
        self._lastName = ''
        self._number = ''

        first = True
        for word in line.split():
            if word[0].isalpha():
                if first == True:
                    self._firstName = word
                    first = False
                else:
                    self._lastName = word
            else:
                self._number = word

    def standardize(self):
        self._firstName = self._firstName.capitalize()
        self._lastName = self._lastName.capitalize()
        self._number = (self._number[:3] + '-' + self._number[3:6] + '-' + self._number[6:])
        return self


    def __str__(self):
        return self._firstName + ' ' + self._lastName + ' ' + self._number

    def __gt__(self, other):

        return self._lastName > other._lastName

    def getFirstName(self):
        return self._firstName

    def getLastName(self):
        return self._lastName

    def getNumber(self):
        return self._number

    def __eq__(self, other):
        return self._lastName == other._lastName

main()
