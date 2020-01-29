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

        self.Access_check()

# MAIN MENU
        self.label2 = Label(self.root, text = "Welcome to Password Manager!\n")

        self.store_passw_btn = Button(self.root, text = "Store Password", command = self.store_passw) #change function name
        self.get_passw_btn = Button(self.root, text = "Get Password", command = self.get_passw)
        self.exit_btn = Button(self.root, text = "Exit", command = self.exit)
        
# DB call
        try:
            self.conn = sqlite3.connect("password_manager.db")
        except:
            pass
        
# db functions
        self.cursor = self.conn.cursor()
        self.service_entry = Entry(self.root)
        self.test_submit = Button(self.root, text = "insert into db", command = self.add_to_db)



# 2. COMMAND FUNCTIONS.
    def submit(self):
        MPget = self.master_pass.get()
        #self.wrong_passwd = ["Yes", "No"]
        #self.wp_current_status = []
        if MPget == self.ADMIN_PASSWORD:
            try:
                self.cursor.execute(''' 
                CREATE TABLE PASSKEYS (
                    PASSWD TEXT VARCHAR(100)
                );
                ''') 

            except:
                pass
            
            self.Access_forget()
            self.main_menu()
        else:
            self.label3 = Label(self.root, text = "Wrong Password!")
            try:
                self.label3.pack()

            except:
                pass

            #self.wp_current_status = self.wrong_passwd[0]
            #for x in self.wrong_passwd:
                #if x in self.wp_current_status:
                    #self.label3.pack()
                    #print("1 - " + str(self.wrong_passwd))
                #elif x == 1:
                    #pass
                #else:
                    #print("2 - " + str(self.wrong_passwd))
                    #pass

    def store_passw(self):
        self.service_entry.pack()
        self.test_submit.pack()


    def add_to_db(self):
        self.service = self.service_entry.get()

        self.command = "INSERT INTO PASSKEYS(PASSWD) VALUES(?);"
        self.cursor.execute(self.command, [self.service])
        self.conn.commit()

    def get_passw(self):
        self.cursor = self.conn.cursor()
        self.command2 = "SELECT * FROM 'PASSKEYS';"
        self.test_get = self.cursor.execute(self.command2)
        
        self.results = self.cursor.fetchall()

        for x in self.results:
            print(x)

    def exit(self):
        self.root.destroy()


# 3. VIEWS
    def Access_check(self):
        self.label1.pack(pady = 5, padx=10)
        self.master_pass.pack(pady = 4)
        self.submit_button.pack(pady = 4)

    def main_menu(self):
        self.label2.pack()
        self.store_passw_btn.pack()
        self.get_passw_btn.pack()
        self.exit_btn.pack(pady = 10)


# 4. REMOVE VIEWS FUNCTIONS
    def Access_forget(self):
        self.label1.pack_forget()
        self.master_pass.pack_forget()
        self.submit_button.pack_forget()

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