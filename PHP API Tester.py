#import dependencies
import tkinter as tk
from tkinter import ttk

#set global variables
root = tk.Tk()
screenWidth = 1280
screenHeight = 720
table = ttk.Treeview(root)
firstTable = False
scrollbarV = ttk.Scrollbar(root, orient="vertical", command=table.yview)
table.configure(yscrollcommand=scrollbarV.set)
data = []
recordNum = 1
cookie = ''
inputError = tk.Label(root, text='', fg='red')
inputSuccess = tk.Label(root, text='Success', fg='green')
textHeight = 5
inputWidth = 50
btnWidth = 11
btnHeight = 2
#Variable stores all the options for parameters
options = ['integer','A-Z','a-z','float','date','base64-image','custom']

#Set application title and size
root.title("Validation GUI")
root.geometry(f"{screenWidth}x{screenHeight}")
root.resizable(False, False)

#Set main menu buttons
uploadsBtn = tk.Button(root, text='Upload file(s)', command=lambda:upload_file(), height=btnHeight, width=btnWidth)
startBtn = tk.Button(root, text='Start test', command=lambda:start_test(), height=btnHeight, width=btnWidth)
exitBtn = tk.Button(root, text='Exit', command=lambda:exit_program(), height=btnHeight, width=btnWidth)
settingsBtn = tk.Button(root, text='Settings', command=lambda:settings_menu(), height=btnHeight, width=btnWidth)

#Set exit submenu button
exitSubBtn = tk.Button(root, text='Main Menu', height=btnHeight, width=btnWidth)

#Set upload file(s) menu buttons

#Set inputs and labels
inputTypes = ['URL', 'Get Variable(s)', 'Post Variable(s)']
inputArray = []
for i in inputTypes:
    inputArray.append([tk.Text(root, height=textHeight, width=inputWidth), tk.Label(root, text=i)])

#Set buttons for settings menu
submitTestInputBtn = tk.Button(root, text='Submit', height=1, width=btnWidth)
cookieBtn = tk.Button(root, text='Submit', height=btnHeight, width=btnWidth)
#Set input and label for setting menu
inputCookie = tk.Text(root, height=textHeight, width=100)
labelCookie = tk.Label(root, text='Cookie')
labelCurrentCookie = tk.Label(root, text='Current Cookie: ', wraplength=800)

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

#Function is called to navigate to the upload file(s) menu
def upload_file():
    clear_main_menu()
    exitSubBtn.config(command=lambda:exit_upload())
    exitSubBtn.place(x=0, y=screenHeight-40)
    #Function is called to exit the upload file(s) menu and return to the main menu
    def exit_upload():
        exitSubBtn.place_forget()
        create_main_menu()

#Function is called to navigate to the test interface
def start_test():
    global firstTable
    clear_main_menu()
    #Place Main Menu button
    exitSubBtn.config(command=lambda:exit_test())
    exitSubBtn.place(x=0, y=screenHeight-40)
    #Function is called to exit the test interface and return to the main menu
    def exit_test():
        table.place_forget()
        scrollbarV.place_forget()
        exitSubBtn.place_forget()
        submitTestInputBtn.place_forget()
        for i in inputArray:
            i[0].place_forget()
            i[1].place_forget()
        inputError.place_forget()
        inputSuccess.place_forget()
        create_main_menu()
    #Only generate the table if it hasn't been done already
    if firstTable == False:
        #Define the columns
        table["columns"] = ("ID", inputTypes[0], inputTypes[1], inputTypes[2])
        #Hidden index column
        table.column("#0", width=0, stretch=tk.NO)
        #Table columns
        table.column("ID", anchor=tk.W, width=int((screenWidth/16)))
        num = 0
        for i in inputTypes:
            table.column(i, anchor=tk.W, width=int(((screenWidth-(screenWidth/4))/5)*(num+1))+5)
            num += 1
        #Table headings
        table.heading("#0", text="", anchor=tk.W)
        table.heading("ID", text="ID", anchor=tk.W)
        num = 0
        for i in inputTypes:
            table.heading(i, text=i, anchor=tk.W)
            num += 1
        firstTable = True
    #Place the table and scroll bar
    table.place(x=0,y=0)
    scrollbarV.place(x=int((screenWidth/16)*15.7), y=0, width=30, height=225)
    #Place input boxes, labels and submit button
    num = 0
    for i in inputArray:
        i[0].place(x=int(((screenWidth/3)*num)+(-15*num)+(-5*(num-1))), y=265)
        i[1].place(x=int(((screenWidth/3)*num)+(-15*num)+(-5*(num-1))), y=240)
        num += 1
    #   Submit
    submitTestInputBtn.place(x=int(screenWidth*0.9), y=355)
    submitTestInputBtn.config(command=lambda:sub_test_input())
    #Function is called to validate the user input
    def sub_test_input():
        global recordNum
        global data
        inputSuccess.place_forget()
        inputError.place_forget()
        url = inputArray[0][0].get("1.0","end")
        getT = inputArray[1][0].get("1.0","end")
        post = inputArray[2][0].get("1.0","end")
        errorText = ''
        #Validate url
        if (url.count('.') >= 2 and url.count('http') == 1 and url.count('://') == 1 and url.count('\n') == 1) == False:
            errorText += 'Invalid Url Provided, the format should be http://www.site.com. '
        #Validate get
        if (getT.count('\n') == 1 and getT.count('=') == 0 or (getT.count('\n') == 1 and getT.count('=') >= 1 and getT.count('=') == (getT.count('&')+1))) == False:
            errorText += 'Invalid Get Provided, the format should be name=&nametwo=. '
        #Validate post
        if (post.count('=') == 1 and post.count('&') == 0 and post.count('\n') == 1 or (post.count('=') >= 2 and post.count('&') >= 1 and post.count('=') == (post.count('&')+1) and post.count('\n') == 1)) == False:
            errorText += 'Invalid Post Provided, the format should be name=&nametwo=. '
        #Save the data if the errorText varaiable is empty, else output an error
        if errorText == '':
            url = url.replace('\n','')
            getT = getT.replace('\n','')
            post = post.replace('\n','')
            table.insert("", 0, values=(recordNum, url, getT, post))
            data.append([recordNum, url, getT, post])
            print(data)
            recordNum += 1
            inputSuccess.place(x=int((screenWidth/2)-500), y=350)
        else:
            inputError.config(text=errorText)
            inputError.place(x=25, y=350)

#Function is called to display the settings menu
def settings_menu():
    clear_main_menu()
    exitSubBtn.config(command=lambda:exit_settings())
    exitSubBtn.place(x=0, y=screenHeight-40)
    #Function is called to exit the settings menu
    def exit_settings():
        exitSubBtn.place_forget()
        inputCookie.place_forget()
        labelCookie.place_forget()
        cookieBtn.place_forget()
        inputError.place_forget()
        inputSuccess.place_forget()
        labelCurrentCookie.place_forget()
        create_main_menu()
    inputCookie.place(x=int(screenWidth/6), y=int(screenHeight/4))
    labelCookie.place(x=int((screenWidth/2)-20), y=int((screenHeight/4)-25))
    cookieBtn.place(x=int((screenWidth/2)-40), y=int((screenHeight/4)+85))
    cookieBtn.config(command=lambda:sub_cookie_input())
    labelCurrentCookie.place(x=int(screenWidth/6), y=int((screenHeight/4)+125))
    #Function is called to validate the cookie and if it passes add it to the cookie variable
    def sub_cookie_input():
        global cookie
        inputError.place_forget()
        inputSuccess.place_forget()
        cookieInp = inputCookie.get("1.0", "end")
        errorText = ''
        if cookieInp.count('\n') > 1:
            errorText += 'Please only use a single line for the cookie. '
        elif cookieInp.find('=') == -1:
            errorText += 'Missing the character ='
        elif cookieInp.find(';') == -1:
            errorText += 'Missing the character ;'
        if errorText == '':
            cookie = cookieInp.replace('\n','')
            inputSuccess.place(x=int((screenWidth/2)+45), y=int((screenHeight/4)+95))
            labelCurrentCookie.config(text="Current Cookie: "+cookie)
        elif errorText != '':
            inputError.config(text=errorText)
            inputError.place(x=int((screenWidth/2)+45), y=int((screenHeight/4)+95))

root.mainloop()