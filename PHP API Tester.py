#import dependencies
import tkinter as tk
from tkinter import ttk

#set global variables
root = tk.Tk()
screenWidth = 1280
screenHeight = 720
table = ttk.Treeview(root)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=table.yview)
table.configure(yscrollcommand=scrollbar.set)

#Set application title and sixe
root.title("Validation GUI")
root.geometry(f"{screenWidth}x{screenHeight}")
root.resizable(False, False)

#Set main menu buttons
uploadsBtn = tk.Button(root, text='Upload file(s)', command=lambda:upload_file(), height=2, width=11)
startBtn = tk.Button(root, text='Start test', command=lambda:start_test(), height=2, width=11)
exitBtn = tk.Button(root, text='Exit', command=lambda:exit_program(), height=2, width=11)
settingsBtn = tk.Button(root, text='Settings', command=lambda:settings_menu(), height=2, width=11)

#Set upload file(s) menu buttons
exitUploadsBtn = tk.Button(root, text='Main Menu', command=lambda:exit_upload(), height=2, width=11)

#Set test interface buttons
exitTestBtn = tk.Button(root, text='Main Menu', command=lambda:exit_test(), height=2, width=11)

#Set buttons for settings menu
exitSettingsBtn = tk.Button(root, text='Main Menu', command=lambda:exit_settings(), height=2, width=11)

#Function is called to create the main menu
def create_main_menu():
    width = (screenWidth/2)-50
    uploadsBtn.place(x=width,y=int((screenHeight/2)-100))
    startBtn.place(x=width, y=int((screenHeight/2)-50))
    settingsBtn.place(x=width, y=int(screenHeight/2))
    exitBtn.place(x=width, y=int((screenHeight/2)+50))
create_main_menu()

#Function is called to exit the program
def exit_program():
    root.destroy()

#Function is called to clear the main menu
def clear_main_menu():
    uploadsBtn.place_forget()
    startBtn.place_forget()
    settingsBtn.place_forget()
    exitBtn.place_forget()

#Function is called to exit the upload file(s) menu and return to the main menu
def exit_upload():
    exitUploadsBtn.place_forget()
    create_main_menu()

#Function is called to navigate to the upload file(s) menu
def upload_file():
    clear_main_menu()
    exitUploadsBtn.place(x=0, y=screenHeight-40)

#Function is called to exit the test interface and return to the main menu
def exit_test():
    table.place_forget()
    scrollbar.place_forget()
    exitTestBtn.place_forget()
    create_main_menu()

#Function is called to navigate to the test interface
def start_test():
    clear_main_menu()
    #Define the columns
    table["columns"] = ("ID","URL","Test Data")
    #Hidden index column
    table.column("#0", width=0, stretch=tk.NO)
    #Table columns
    table.column("ID", anchor=tk.W, width=int((screenWidth/16)*1.7))
    table.column("URL", anchor=tk.W, width=int((screenWidth/16)*7))
    table.column("Test Data", anchor=tk.W, width=int((screenWidth/16)*7))
    #Table headings
    table.heading("#0", text="", anchor=tk.W)
    table.heading("ID", text="ID", anchor=tk.W)
    table.heading("URL", text="URL", anchor=tk.W)
    table.heading("Test Data", text="Test Data", anchor=tk.W)
    #Insert records
    #table.insert("", 0, values=(i, "localhost/moodle/user/login.index.php", 22))
    #Place the table and scroll bar
    table.place(x=0,y=0)
    scrollbar.place(x=int((screenWidth/16)*15.7), y=0, width=30, height=225)
    #Place Main Menu button
    exitTestBtn.place(x=0, y=screenHeight-40)

def exit_settings():
    exitSettingsBtn.place_forget()
    create_main_menu()

def settings_menu():
    clear_main_menu()
    exitSettingsBtn.place(x=0, y=screenHeight-40)

root.mainloop()