import sys
import os
from tkinter import *
import sqlite3
import bcrypt
from cryptography.fernet import Fernet

class PasswordManager:
    
    def __init__(self, root):


    #######################################################################
    #                        LABELS AND BUTTONS                           #     
    #######################################################################

        self.root=root

# DB call
        try:
            self.conn = sqlite3.connect("password_manager.db")
        except:
           pass

# DB cursor
        self.cursor = self.conn.cursor()

# MASTER PASSWORD SETUP
        self.MPsetupLabel = Label(self.root, text = "Setup your new Master Password")
        self.MP = Entry(self.root, show = '*', width = 35)
        self.MPsubmit = Button(self.root, text = "Submit", command = self.add_MP_to_db)

        try:
            self.cursor.execute(''' 
            CREATE TABLE MasterPasswd (
                MP TEXT VARCHAR(100) NOT NULL
            );
            ''') 
        except:
            pass

# MASTER PASSWORD PROMPT  
        self.label1 = Label(self.root, text = "Please enter master password to gain access")

        self.master_pass = Entry(self.root, show = '*', width = 35)
        self.submit_button = Button(self.root, text = "Submit", command = self.submit)
        self.error_label = Label(self.root, text = "Wrong Password!")

        self.MP_check()

# MAIN MENU
        self.label2 = Label(self.root, text = "Welcome to Password Manager!", font = ("Arial", 14, "bold"))

        self.store_passw_btn = Button(self.root, text = "Store Password", width = 15, command = self.store_passwd_menu)
        self.get_passw_btn = Button(self.root, text = "Get Password", width = 15, command = self.all_passwd_menu)
        self.exit_btn = Button(self.root, text = "Exit", width = 15, command = self.exit)


# Service & Password entries
        self.label3 = Label(self.root, text = "What's the name of the service you'd like to store password for?")
        self.service_entry = Entry(self.root)

        self.label4 = Label(self.root, text = "Enter password")
        self.passw_entry = Entry(self.root, show = "*")

        self.store_passw_btn2 = Button(self.root, text = "Store password", width = 15, command = self.add_to_db)
        self.show_passwd_btn = Button(self.root, text = "Show password", command = self.show_password)
        #self.error_label2 = Label(self.root, text = "This service already has a password assigned!")

# All passwd menu
        self.label5 = Label(self.root, text = "Password Storage", font = ("Arial", 14, "bold"))
        self.back_btn = Button(self.root, text = "Back", width = 15, command = self.main_menu)

# Get passwd menu
        self.back_btn2 = Button(self.root, text = "Back", width = 15, command = self.all_passwd_menu)

# Cryptography
    def generate_key(self, service):
        # Create keys directory
        self.filename = "keys/" + service + '.key'
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        # Generating key and writing into the file
        self.key = Fernet.generate_key()
        self.file = open(self.filename, 'wb')
        self.file.write(self.key)
        self.file.close()
        return self.key

    def get_key(self, service):
        self.file = open('keys/' + service + '.key', 'rb')
        self.decrypt_key = self.file.read()
        self.file.close()
        return self.decrypt_key

# 2. COMMAND FUNCTIONS.

    def MP_check(self):
        self.MP_check_query = "SELECT * FROM MasterPasswd;"
        self.cursor.execute(self.MP_check_query)
        
        self.results = self.cursor.fetchall()
        self.results_lenght = len(self.results)

        if self.results_lenght == 0:
            self.master_password_setup()
        elif self.results_lenght == 1:
            self.Access_check()
        else:
            print("You currently have " + str(self.results_lenght) + " Master Passwords assigned!")

    def add_MP_to_db(self):
        self.MPget = self.MP.get()
        self.bMPget = self.MPget.encode('utf-8')

        #passwd hashing
        self.MP_hashed = bcrypt.hashpw(self.bMPget, bcrypt.gensalt())

        self.MPinsertQuery = "INSERT INTO MasterPasswd(MP) VALUES(?);"
        self.cursor.execute(self.MPinsertQuery, [self.MP_hashed])
        self.conn.commit()

        self.MP_check()

    def submit(self):
        self.master_pass_get = self.master_pass.get()
        self.b_master_pass_get = self.master_pass_get.encode('utf-8')
       
        self.MP_get_query = "SELECT * FROM MasterPasswd;"
        self.cursor.execute(self.MP_get_query)
        
        self.results = self.cursor.fetchall()

        for MP_hashed in self.results:
            self.MP_hashed = MP_hashed[0]

            self.MP_hash_check = bcrypt.checkpw(self.b_master_pass_get, self.MP_hashed)

            if self.MP_hash_check:
                try:
                    self.cursor.execute(''' 
                    CREATE TABLE PASSKEYS (
                        SERVICE TEXT VARCHAR(100) NOT NULL,
                        PASSWD TEXT VARCHAR(100)
                    );
                    ''') 

                except:
                    pass
                
                self.main_menu()
            else:
                try:
                    self.error_label.pack()

                except:
                    pass

    def add_to_db(self):
        self.service = self.service_entry.get()
        self.password = self.passw_entry.get()
        
        # Generate crypto key for service
        self.crypto_key = self.generate_key(self.service)
        
        # Encode password
        self.encoded_passwd = self.password.encode('utf-8')

        # Encrypt password
        self.f = Fernet(self.crypto_key)
        self.encrypted_passwd = self.f.encrypt(self.encoded_passwd)

        self.command = "INSERT INTO PASSKEYS(SERVICE,PASSWD) VALUES(?,?);"
        self.cursor.execute(self.command, [self.service, self.encrypted_passwd])

        self.conn.commit()

        # Unique service name check
        #self.query = "SELECT SERVICE FROM PASSKEYS;"
        #self.cursor.execute(self.query)

        #self.results = self.cursor.fetchall()

        #for x in self.results:
        #    self.x = x[0]
        #    print("jajebix" + str(self.x))
        #    if self.x == self.service_entry.get():
        #        self.error_label2.pack()
        #    else:
        #        pass

        self.all_passwd_menu()

    def get_safe_status(self):
        self.get_safe_status_cmd = "SELECT SERVICE FROM PASSKEYS;"
        self.cursor.execute(self.get_safe_status_cmd)
        
        self.results = self.cursor.fetchall()
        self.lenght = len(self.results)

        self.label_text = "You currently store passwords for %s Service(s)"%(self.lenght)
        self.safe_status_label = Label(self.root, text = self.label_text)
        self.safe_status_label.pack()

    def get_services(self):
        self.query = "SELECT SERVICE FROM PASSKEYS;"
        self.cursor.execute(self.query)

        self.results = self.cursor.fetchall()
        self.results_length = len(self.results)
        print(self.results)

        for service in self.results:
            print("elko2" + str(service))
            self.service_btn = Button(self.root, text = service, width = 50, command = lambda s=service: self.get_passwd(s))
            self.service_btn.pack(pady = 4)


    def get_passwd(self, service):
        self.clear()
    
        self.service = service[0]

        # Get crypto key for service        
        self.decrypt_key = self.get_key(self.service)

        self.query2 = "SELECT PASSWD FROM PASSKEYS WHERE SERVICE = ?;"
        self.cursor.execute(self.query2, [self.service])

        self.results = self.cursor.fetchall()

        self.string = "The password for %s is: " % (service)
        self.label6 = Label(self.root, text = self.string)
        self.label6.pack()


        print(self.string + str(self.results))

        for password in self.results:
            self.password = password[0]

            # Decrypt encrypted passwd 
            self.f2 = Fernet(self.decrypt_key)
            self.decrypted_passw = self.f2.decrypt(self.password)

            self.passwd_label = Label(self.root, text = self.decrypted_passw, font = ("Helvetica", 15, "bold"))
            self.passwd_label.pack(pady = 4)
            self.copy_btn = Button(self.root, text = "Copy to Clipboard", width = 15, command = lambda pw=self.decrypted_passw: self.copy_to_clipboard(pw))
            self.copy_btn.pack()
            self.delete_passwd_btn = Button(self.root, text = "Delete", width = 15, command = lambda enc_pw = self.password: self.delete_passwd(enc_pw, self.service))
            self.delete_passwd_btn.pack()
            
        self.back_btn2.pack(side = LEFT, padx = 10, pady = 10)
        self.exit_btn.pack(side = RIGHT, padx = 10, pady = 10)
    
    def copy_to_clipboard(self, password):
        self.root.clipboard_clear()
        self.root.clipboard_append(password)

    def show_password(self):
        if self.passw_entry['show'] == "":
            self.show_passwd_btn['text'] = "Show Password"
            self.passw_entry['show'] = "*"
        else:
            self.show_passwd_btn['text'] = "Hide Password"
            self.passw_entry['show'] = ""

    def delete_passwd(self, password, service):
        print(password)
        print(service)
        self.delete_query = "DELETE FROM PASSKEYS WHERE PASSWD = ?;"
        self.cursor.execute(self.delete_query, [password])

        self.conn.commit()

        self.label_text = "Password for %s has been successfully deleted"%(service)
        self.delete_passwd_label = Label(self.root, text = self.label_text)
        self.delete_passwd_label.pack()


        # TO BE ADDED - REMOVE KEY FILE ON PASSWD DELETION FUNCTION



    def exit(self):
        self.conn.close()
        self.root.destroy()


# 3. VIEWS

    def master_password_setup(self):
        self.MPsetupLabel.pack(pady = 5, padx=10)
        self.MP.pack(pady = 4)
        self.MPsubmit.pack()

    def Access_check(self):
        self.clear()
        self.label1.pack(pady = 5, padx=10)
        self.master_pass.pack(pady = 4)
        self.submit_button.pack(pady = 4)

    def main_menu(self):
        self.clear()
        self.label2.pack(padx = 10, pady = 10)
        self.store_passw_btn.pack()
        self.get_passw_btn.pack()
        self.exit_btn.pack(pady = 10)

    def store_passwd_menu(self):
        self.passw_entry['show'] = "*"
        self.show_passwd_btn['text'] = "Show Password"
        self.clear()
        self.clear_entries()
        self.label3.pack(padx = 10, pady = 10)
        self.service_entry.pack()
        self.label4.pack(pady = 6)
        self.passw_entry.pack()
        self.show_passwd_btn.pack(pady = 5)
        self.back_btn.pack(side = LEFT, padx = 10, pady = 10)
        self.store_passw_btn2.pack(side = RIGHT, padx = 10, pady = 10)

    def all_passwd_menu(self):
        self.clear()
        self.label5.pack()
        self.get_safe_status()
        self.get_services()
        self.back_btn.pack(side = LEFT, padx = 10, pady = 10)
        self.exit_btn.pack(side = RIGHT, padx = 10, pady = 10)


# CLEAR ALL CURRENTLY DISPLAYED WIDGETS
    def clear(self):
        self.all_widgets = self.root.pack_slaves()
        for w in self.all_widgets:
            w.pack_forget()

# CLEAR ENTRIES

    def clear_entries(self):
        self.service_entry.delete(0, "end")
        self.passw_entry.delete(0, "end")

    #######################################################################
    #                             MAIN CONFIG                             #
    #######################################################################

       
def main():
    root = Tk()
    gui = PasswordManager(root)
    root.wm_title("Password Manager")
    root.minsize(300,100)
    root.mainloop()
    
if __name__ == '__main__':
    sys.exit(main())