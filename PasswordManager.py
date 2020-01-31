import sys
from tkinter import *
import sqlite3

class PasswordManager:
    
    def __init__(self, root):


    #######################################################################
    #                        LABELS AND BUTTONS                           #     
    #######################################################################


# 1. MASTER PASSWORD PROMPT.
        self.ADMIN_PASSWORD = "123"

        self.root=root
        
        self.label1 = Label(self.root, text = "Please enter master password to gain access")

        self.master_pass = Entry(self.root, show = '*', width = 35)
        self.submit_button = Button(self.root, text = "Submit", command = self.submit)
        self.error_label = Label(self.root, text = "Wrong Password!")

        self.Access_check()

# MAIN MENU
        self.label2 = Label(self.root, text = "Welcome to Password Manager!")

        self.store_passw_btn = Button(self.root, text = "Store Password", command = self.store_passwd_menu) #change function name
        self.get_passw_btn = Button(self.root, text = "Get Password", command = self.get_passwd_menu)
        self.exit_btn = Button(self.root, text = "Exit", command = self.exit)
        
# DB call
        try:
            self.conn = sqlite3.connect("password_manager.db")
        except:
            pass
        
# DB cursor
        self.cursor = self.conn.cursor()


# Service & Password entries
        self.label3 = Label(self.root, text = "What's the name of the service you'd like to store password for?")
        self.service_entry = Entry(self.root)

        self.label4 = Label(self.root, text = "Enter password")
        self.passw_entry = Entry(self.root, show = "*")

        self.store_passw_btn2 = Button(self.root, text = "Store password", command = self.add_to_db)
        
        self.error_label2 = Label(self.root, text = "This service already has a password assigned!")

# All passwd menu
        self.label5 = Label(self.root, text = "Password Storage")

# 2. COMMAND FUNCTIONS.
    def submit(self):
        MPget = self.master_pass.get()
        #self.wrong_passwd = ["Yes", "No"]
        #self.wp_current_status = []
        if MPget == self.ADMIN_PASSWORD:
            try:
                self.cursor.execute(''' 
                CREATE TABLE PASSKEYS (
                    SERVICE TEXT PRIMARY KEY NOT NULL,
                    PASSWD TEXT VARCHAR(100)
                );
                ''') 

            except:
                pass
            
            self.Access_forget()
            self.main_menu()
        else:
            try:
                self.error_label.pack()

            except:
                pass

    def store_passw(self):
        pass
        #self.store_passwd_menu()


    def add_to_db(self):
        self.service = self.service_entry.get()
        self.password = self.passw_entry.get()

        self.command = "INSERT INTO PASSKEYS(SERVICE,PASSWD) VALUES(?,?);"
        self.cursor.execute(self.command, [self.service, self.password])
        self.conn.commit()

        # Unique service name check
        #self.query = "SELECT SERVICE FROM PASSKEYS;"
        #self.cursor.execute(self.query)

        #self.results = self.cursor.fetchall()

        #if self.service in self.results:
            #self.error_label2.pack()
        #else:
            #pass

        self.store_passwd_menu_forget()
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

        for x in self.results:
            self.service_btn = Button(self.root, text = x, width = 50, command = None)
            self.service_btn.pack(pady = 4)

    def get_passwd(self,):


    def exit(self):
        self.root.destroy()


# 3. VIEWS
    def Access_check(self):
        self.label1.pack(pady = 5, padx=10)
        self.master_pass.pack(pady = 4)
        self.submit_button.pack(pady = 4)

    def main_menu(self):
        self.label2.pack(pady = 10)
        self.store_passw_btn.pack()
        self.get_passw_btn.pack()
        self.exit_btn.pack(pady = 10)

    def store_passwd_menu(self):
        self.main_menu_forget()
        self.label3.pack(padx = 10, pady = 10)
        self.service_entry.pack()
        self.label4.pack(pady = 6)
        self.passw_entry.pack()
        self.store_passw_btn2.pack(pady = 5)

    def get_passwd_menu(self):
        self.main_menu_forget()
        self.all_passwd_menu()

    def all_passwd_menu(self):
        self.label5.pack()
        self.get_safe_status()
        self.get_services()


# 4. REMOVE VIEWS FUNCTIONS
    def Access_forget(self):
        self.label1.pack_forget()
        self.error_label.pack_forget()
        self.master_pass.pack_forget()
        self.submit_button.pack_forget()

    def main_menu_forget(self):
        self.label2.pack_forget()
        self.store_passw_btn.pack_forget()
        self.get_passw_btn.pack_forget()
        self.exit_btn.pack_forget()

    def store_passwd_menu_forget(self):
        self.label3.pack_forget()
        self.service_entry.pack_forget()
        self.label4.pack_forget()
        self.passw_entry.pack_forget()
        self.store_passw_btn2.pack_forget()

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