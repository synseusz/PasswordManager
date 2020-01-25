import sys
from tkinter import *


class PasswordManager:
    
    def __init__(self, root):


    #######################################################################
    #                        LABELS AND BUTTONS                           #     
    #######################################################################


# 1. MASTER PASSWORD PROMPT.
        self.ADMIN_PASSWORD = "123"

        self.root=root
        
        self.label1 = Label(self.root, text = "Welcome to Password Manager!\n")
        self.label2 = Label(self.root, text = "Please enter master password to gain access")

        self.master_pass = Entry(self.root, show = '*', width = 35)
        self.submit_button = Button(self.root, text = "Submit", command = self.submit)

        self.Access_check()

# 2. COMMAND FUNCTIONS.
    def submit(self):
        MPget = self.master_pass.get()
        if MPget == self.ADMIN_PASSWORD:
            self.Access_forget()
            self.label1.pack()
        else:
            self.label4 = Label(self.root, text = "Wrong Password!").pack()


# 3. VIEWS
    def Access_check(self):
        self.label2.pack(pady = 5)
        self.master_pass.pack(pady = 4)
        self.submit_button.pack(pady = 4)


# 4. REMOVE FUNCTIONS
    def Access_forget(self):
        self.label2.pack_forget()
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