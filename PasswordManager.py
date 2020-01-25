import sys
from tkinter import *


class PasswordManager:
    
    def __init__(self, root):


    #######################################################################
    #                        LABELS AND BUTTONS                           #     
    #######################################################################


# 1. MASTER PASSWORD PROMPT.
        ADMIN_PASSWORD = "n3fXXFZjrw"

        self.root=root
        
        self.label1 = Label(self.root, text = "Welcome to Password Manager!\n")
        self.label2 = Label(self.root, text = "Please enter master password to gain access")

        self.master_pass = Entry(self.root, show = '*', width = 35)
        self.submit_button = Button(self.root, text = "Submit", command = self.submit)

        self.Access()
# 2. COMMAND FUNCTIONS.
    def submit(self):
        MPget = self.master_pass.get()
        print(MPget)


# 3. VIEWS
    def Access(self):
        self.label1.pack()
        self.label2.pack()
        self.master_pass.pack()
        self.submit_button.pack()


    #######################################################################
    #                             MAIN CONFIG                             #
    #######################################################################

       
def main():
    root = Tk()
    gui = PasswordManager(root)
    root.wm_title("Password Manager")
    root.minsize(300,150)
    root.mainloop()
    
if __name__ == '__main__':
    sys.exit(main())