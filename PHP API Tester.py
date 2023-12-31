#import dependencies
import tkinter as tk
from tkinter import ttk
import urllib.request
from random import randint

#set global variables
root = tk.Tk()
screenWidth = 1280
screenHeight = 720
table = ttk.Treeview(root)
firstTable = False
scrollbarV = ttk.Scrollbar(root, orient="vertical", command=table.yview)
table.configure(yscrollcommand=scrollbarV.set)
data = []
currentData = []
results = []
recordNum = 1
cookie = ''
inputError = tk.Label(root, text='', fg='red')
inputSuccess = tk.Label(root, text='Success', fg='green')
textHeight = 5
inputWidth = 50
btnWidth = 11
btnHeight = 2
#Variable stores all the options for parameters
options = ['1) integer','2) A-Z','3) a-z','4) float','5) date','6) base64 image','7) encoded HTML','8) email']
#Variable used to temporarily store variable keys
varArray = [[],[]]
optArray = [[],[]]

#Set application title and size
root.title("PHP API Tester")
root.geometry(f"{screenWidth}x{screenHeight}")
root.resizable(False, False)

#Set main menu buttons
uploadsBtn = tk.Button(root, text='Upload File(s)', command=lambda:upload_file(), height=btnHeight, width=btnWidth)
setupBtn = tk.Button(root, text='Setup Test', command=lambda:setup_test(), height=btnHeight, width=btnWidth)
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
#Set options for variables
optDDText = [tk.StringVar(root, "Select a Get Variable"), tk.StringVar(root, "Select a Post Variable")]
optDropDowns = [ttk.Combobox(root, textvariable=optDDText[0], state='readonly'), ttk.Combobox(root, textvariable=optDDText[1], state='readonly')]
optCheckBoxes = [[],[]]
optCheckBoxesVar = [[],[]]
for i in options:
    for y in range(2):
        optCheckBoxesVar[y].append(tk.IntVar())
        optCheckBoxes[y].append(tk.Checkbutton(root, text=i, variable=optCheckBoxesVar[y][-1]))
optCheckSub = [tk.Button(root, text='Submit Selection', height=1, width=int(btnWidth*1.2)), tk.Button(root, text='Submit Selection', height=1, width=int(btnWidth*1.2))]
optSubmit = tk.Button(root, text='Submit Test', height=1, width=btnWidth)
startSubmit = tk.Button(root, text='Start Test', height=btnHeight, width=btnWidth)

#Set buttons for settings menu
submitTestInputBtn = tk.Button(root, text='Validate', height=1, width=btnWidth)
cookieBtn = tk.Button(root, text='Submit', height=btnHeight, width=btnWidth)
#Set input and label for setting menu
inputCookie = tk.Text(root, height=textHeight, width=100)
labelCookie = tk.Label(root, text='Cookie')
labelCurrentCookie = tk.Label(root, text='Current Cookie: ', wraplength=800)

#Function is called to create the main menu
def create_main_menu():
    width = (screenWidth/2)-50
    uploadsBtn.place(x=width,y=int((screenHeight/2)-100))
    setupBtn.place(x=width, y=int((screenHeight/2)-50))
    settingsBtn.place(x=width, y=int(screenHeight/2))
    exitBtn.place(x=width, y=int((screenHeight/2)+50))
create_main_menu()

#Function is called to exit the program
def exit_program():
    root.destroy()

#Function is called to clear the main menu
def clear_main_menu():
    uploadsBtn.place_forget()
    setupBtn.place_forget()
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
def setup_test():
    global firstTable
    clear_main_menu()
    #Place Main Menu button
    exitSubBtn.config(command=lambda:exit_test())
    exitSubBtn.place(x=0, y=screenHeight-40)
    #Function is called to remove variable option selection and set the checkboxes to the default value
    def remove_var_options():
        optSubmit.place_forget()
        for i in optCheckSub:
            i.place_forget()
        for i in range(len(optCheckBoxes[0])):
            for y in range(2):
                optCheckBoxesVar[y][i].set(0)
                optCheckBoxes[y][i].place_forget()
        i = 1
        for i in range(3):
            optDropDowns[i-1].place_forget()
    #Function is called to remove error and success labels
    def remove_temp_labels():
        inputError.place_forget()
        inputSuccess.place_forget()
    #Function is called to exit the test interface and return to the main menu
    def exit_test():
        table.place_forget()
        scrollbarV.place_forget()
        exitSubBtn.place_forget()
        submitTestInputBtn.place_forget()
        for i in inputArray:
            i[0].place_forget()
            i[1].place_forget()
        remove_var_options()
        optSubmit.place_forget()
        startSubmit.place_forget()
        remove_temp_labels()
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
    #Function is called to get the x position for a speicified position
    def xPos(num):
        return int(((screenWidth/3)*num)+(-15*num)+(-5*(num-1)))
    #Place input boxes, labels and submit button
    num = 0
    for i in inputArray:
        i[0].place(x=xPos(num), y=265)
        i[1].place(x=xPos(num), y=240)
        num += 1
    #   Submit
    submitTestInputBtn.place(x=int(screenWidth*0.9), y=355)
    submitTestInputBtn.config(command=lambda:validate_test_input())
    placedSub = False
    startSubmit.place(x=int(screenWidth*0.935), y=screenHeight-40)
    startSubmit.config(command=lambda:start_test())
    #Check if input data is stored and if it is, display the relevant options
    for y in range(2):
        if len(varArray[y]) > 0:
            optDropDowns[y].place(x=xPos(y+1), y=375)
            num = 0
            for i in range(len(optCheckBoxes[y])):
                optCheckBoxes[y][i].place(x=xPos(y+1), y=400+(25*num))
                num += 1
            optCheckSub[y].place(x=xPos(y+1), y=int(400+(25*len(optCheckBoxes[y]))))
            if optDropDowns[y].get() in varArray[y]:
                for i in range(len(optCheckBoxesVar[y])):
                    if (i+1) in optArray[y][varArray[y].index(optDropDowns[y].get())]:
                        optCheckBoxesVar[y][i].set(1)
            if placedSub == False:
                optSubmit.place(x=int(screenWidth*0.9), y=int(400+(25*len(optCheckBoxes[0]))))
                placedSub = True
    #Function is called to start the test
    def start_test():
        global results
        remove_temp_labels()
        #Check if data is avaiable for the test, if not display an error else proceed
        if data == []:
            inputError.config(text='No test data available.')
            inputSuccess.place(x=int(screenWidth*0.9), y=screenHeight-60)
        elif data != []:
            inputSuccess.config(text='Test Started')
            inputSuccess.place(x=int(screenWidth*0.94), y=screenHeight-60)
            #Send requests and store the results
            results = []
            for i in range(len(data)):
                tempResult = [data[i][0],[]]
                #Create requests for each variable and each option and put the get and post in seperate arrays
                maxLength = 0
                requestData = [[],[]]
                b = 1
                while b < 3:
                    for y in data[i][b]:
                        tmpData = []
                        for x in y[1]:
                            if x == 1:
                                tmpData.append([x, y[0]+'=0123456789'])
                                j = 0
                                while j < 10:
                                    tmpData.append([x, y[0]+'='+str(j)])
                                    j += 1
                            elif x == 2:
                                tmpData.append([x, y[0]+'=ABCDEFGHIJKLMNOPQRSTUVWXYZ'])
                                for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                                    tmpData.append([x, y[0]+'='+letter])
                            elif x == 3:
                                tmpData.append([x, y[0]+'=abcdefghijklmnopqrstuvwxyz'])
                                for letter in 'abcdefghijklmnopqrstuvwxyz':
                                    tmpData.append([x, y[0]+'='+letter])
                            elif x == 4:
                                tmpData.append([x, y[0]+'=1%2E1'])
                            elif x == 5:
                                tmpData.append([x, y[0]+'=2022%2D01%2D02'])
                            elif x == 6:
                                tmpData.append([x, y[0]+'=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAIAAAACUFjqAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAAYSURBVChTY%2Fz%2F%2Fz8DbsAEpXGAkSnNwAAApeMDEUEua14AAAAASUVORK5CYII%3D'])
                            elif x == 7:
                                tmpData.append([x, y[0]+'=%26lt%3Bscript%26gt%3B%26lt%3B%2Fscript%26gt%3B'])
                            elif x == 8:
                                tmpData.append([x, y[0]+'=email%40email%2Ecom'])
                        maxLength = max(maxLength, len(tmpData))
                        requestData[b-1].append(tmpData)
                    b += 1
                #Send the requests and add the results to the results array
                for y in range(maxLength):
                    #Get the get requests and options and add it to a string and array
                    getRequest = ''
                    getOptions = []
                    for x in requestData[0]:
                        getRequest += x[y%len(x)][1]+'&'
                        if x[y%len(x)][0] not in getOptions:
                            getOptions.append(x[y%len(x)][0])
                    if len(getRequest) > 0:
                        if getRequest[-1] == '&':
                            getRequest = getRequest[:-1]
                    #Get the post requests and options and add it to a string and array 
                    postRequest = ''
                    postOptions = []
                    for x in requestData[1]:
                        postRequest += x[y%len(x)][1]+'&'
                        if x[y%len(x)][0] not in postOptions:
                            postOptions.append(x[y%len(x)][0])
                    if len(postRequest) > 0:
                        if postRequest[-1] == '&':
                            postRequest = postRequest[:-1]
                    #Create the request
                    requestUrl = data[i][0]
                    if len(getRequest) > 0:
                        requestUrl += '?'+getRequest
                    request = urllib.request.Request(requestUrl, data=postRequest.encode('utf-8'))
                    if cookie != '':
                        request.add_header('Cookie', cookie)
                    #Try to send the request and catch any errors
                    try:
                        #Send the response
                        with urllib.request.urlopen(request) as response:
                            #Decode the response and determine if it passes
                            responseData = response.read().decode('utf-8')
                            passFail = 'Fail'
                            #Need change validation to allow the user to input their pass paramaters, current if is temporary
                            if responseData.find('[') == 0 and responseData.rfind(']') == len(responseData)-1 or responseData.find('No search results') != -1:
                                passFail = 'Pass'
                            tempResult[1].append([[getOptions, getRequest], [postOptions, postRequest], [passFail, responseData]])
                    except Exception as e:
                        #Check for UnicodeError and put it into a string
                        if str(e).find('UnicodeError: ') != -1:
                            e = str(e).split('UnicodeError: ')[1].split(')')[0]
                        #Check for URLError and put it into a string
                        if str(e).find('>') != -1 and str(e).find('] ') != -1:
                            e = str(e).split('] ')[1].split('>')[0]
                        #Get for HTTP Error and put it into a string
                        if str(e).find('HTTP Error ') != -1:
                            e = str(e).split(": ")[1]
                        tempResult[1].append([[getOptions, getRequest], [postOptions, postRequest], ['Fail', e]])
                results.append(tempResult)
            print(results)
    #Function is called when the dropdown value is changed
    def changed_drop_down(num):
        remove_temp_labels()
        i = 0
        #Load saved selection if it exists
        for i in range(len(optCheckBoxesVar[num])):
            if optDropDowns[num].get() in varArray[num]:
                if (i+1) in optArray[num][varArray[num].index(optDropDowns[num].get())]:
                    optCheckBoxesVar[num][i].set(1)
                else:
                    optCheckBoxesVar[num][i].set(0)
            else:
                optCheckBoxesVar[num][i].set(0)
    #Function is called to validate the the selected options for a variable, and if it passes submit it
    def sub_selection(num):
        global optArray
        remove_temp_labels()
        optChosen = []
        i = 0
        #Get the options selected and add them to an array
        for i in range(len(optCheckBoxesVar[num])):
            if optCheckBoxesVar[num][i].get() == 1:
                optChosen.append(i+1)
        if len(optChosen) == 0:
            inputError.config(text='No option selected.')
            inputError.place(x=xPos(num+1), y=430+(25*len(optCheckBoxes[num])))
        elif len(optChosen) >= 1:
            #Add selected values to an array
            try:
                optArray[num][varArray[num].index(optDropDowns[num].get())] = optChosen
                inputSuccess.config(text='Success')
                inputSuccess.place(x=xPos(num+1), y=430+(25*len(optCheckBoxes[num])))
            except:
                return
    #Function is called to submit the current test
    def validate_current_test():
        global data
        global currentData
        global varArray
        global optArray
        global recordNum
        remove_temp_labels()
        #Validate the current test
        #Check if all variables have a option chosen and if not display an error message
        valid = True
        for i in optArray:
            for y in i:
                if y == []:
                    valid = False
        if valid == False:
            inputError.config(text='No options chosen for variable(s)')
            inputError.place(x=int(screenWidth*0.85), y=430+(25*len(optCheckBoxes[0])))
        elif valid == True:
            #proceed to saving the options chosen for each variable, then add them to the table and an array
            newArray = [[],[]]
            pos = 0
            #Add options to an array
            for i in varArray:
                num = 0
                for y in i:
                    newArray[pos].append([y, optArray[pos][num]])
                    num += 1
                pos += 1
            if newArray != []:
                #Add data to the table
                data.append([currentData[0], newArray[0], newArray[1]])
                table.insert("", 0, values=(recordNum, data[-1][0], data[-1][1], data[-1][2]))
                recordNum += 1
                #Set the varArray and optArray to default values
                varArray = [[],[]]
                optArray = [[],[]]
                currentData = []
                #Reset check boxes to default
                remove_var_options()
                #Display success text
                inputSuccess.config(text='Success')
                inputSuccess.place(x=int(screenWidth*0.9), y=430+(25*len(optCheckBoxes[0])))
            else:
                #Display error text
                inputError.config(text='Error creating test.')
                inputError.place(x=int(screenWidth*0.9), y=430+(25*len(optCheckBoxes[0])))
    #Function is called to validate the user input
    def validate_test_input():
        global currentData
        global varArray
        global optArray
        #Reset the options section to default layout
        remove_temp_labels()
        remove_var_options()
        #Store user input into variables
        url = inputArray[0][0].get("1.0","end")
        getT = inputArray[1][0].get("1.0","end")
        post = inputArray[2][0].get("1.0","end")
        errorText = ''
        #Validate url
        if (url.count('.') >= 2 and url.count('http') == 1 and url.count('://') == 1) == False:
            errorText += "Invalid Url Provided, the format should be http://www.site.com. "
        #Validate get
        if (getT.count('=') == 0 or (getT.count('=') >= 1 and getT.count('=') == (getT.count('&')+1))) == False:
            errorText += "Invalid Get Provided, the format should be name=&nametwo=. "
        #Validate post
        if (post.count('=') == 1 and post.count('&') == 0 or (post.count('=') >= 2 and post.count('=') == (post.count('&')+1)) or post.count('=') == 0) == False:
            errorText += "Invalid Post Provided, the format should be name=&nametwo=. "
        #Save the data if the errorText varaiable is empty, else output an error
        if errorText == '':
            url = url.replace('\n','').replace('\t','').replace('\r','').replace("\'","").replace('\"','').replace('\\','')
            if url.count('?') >= 1:
                url = url.split('?')[0]
            getT = getT.replace('\n','').replace('\t','').replace('\r','').replace("\'","").replace('\"','').replace('\\','')
            post = post.replace('\n','').replace('\t','').replace('\r','').replace("\'","").replace('\"','').replace('\\','')
            if len(getT) == 0 and len(post) == 0:
                errorText += 'No Post or Get provided. '
            else:
                optArray = [[],[]]
                varArray = [[],[]]
                i = 0
                #Validate get and post input and place each variable into an array
                for params in [getT, post]:
                    if params != '':
                        #Validate input and place each varaible into an array
                        if params.count('=') == 1 and params.count('&') == 0:
                            pair = params.split('=')
                            if pair[0] == '':
                                if i == 0:
                                    errorText += 'No get variable provided. '
                                elif i == 1:
                                    errorText += 'No post varaible provided. '
                            else:
                                if pair[0] not in varArray[i]:
                                    varArray[i].append(pair[0])
                                    optArray[i].append([])
                        elif params.count('=') > 1 and params.count('&') >= 1 and params.count('&') + 1 == params.count('='):
                            pairs = params.split('&')
                            for pair in pairs:
                                key = pair.split('=')[0]
                                if key != '':
                                    if key not in varArray[i]:
                                        varArray[i].append(key)
                                        optArray[i].append([])
                            if len(varArray[i]) == 0 and i == 0:
                                errorText += 'No get variables provided. '
                            if len(varArray[i]) == 0 and i == 1:
                                errorText += 'No Post variable provided. '
                    i += 1
                if errorText == '':
                    #Set drop downs to default and then reset
                    optDDText[0].set("Select a Get Variable")
                    optDDText[1].set("Select a Post Variable")
                    i = 1
                    for i in range(3):
                        if len(varArray[i-1]) > 0:
                            optDropDowns[i-1].config(values=varArray[i-1])
                            optDropDowns[i-1].place(x=xPos(i), y=375)
                            optDropDowns[i-1].bind("<<ComboboxSelected>>", lambda event, index=i-1: changed_drop_down(index))
                            optCheckSub[i-1].place(x=xPos(i), y=400+(25*len(optCheckBoxes[i-1])))
                            optCheckSub[i-1].config(command=lambda index=i-1:sub_selection(index))
                    num = 0
                    #Place check boxes
                    for i in range(len(optCheckBoxes[0])):
                        for y in range(2):
                            if len(varArray[y]) > 0:
                                optCheckBoxes[y][i].place(x=xPos(y+1), y=400+(25*num))
                        num += 1
                    currentData = [url, varArray[0], varArray[1]]
                    inputSuccess.config(text='Success')
                    inputSuccess.place(x=int((screenWidth/2)-500), y=350)
                    optSubmit.place(x=int(screenWidth*0.9), y=int(400+(25*len(optCheckBoxes[0]))))
                    optSubmit.config(command=lambda:validate_current_test())
        if errorText != '':
            #Display the error text
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
        #Validate the input provided
        if cookieInp.count('\n') > 1:
            errorText += 'Please only use a single line for the cookie. '
        elif cookieInp.find('=') == -1:
            errorText += 'Missing the character ='
        elif cookieInp.find(';') == -1:
            errorText += 'Missing the character ;'
        if errorText == '':
            #Output success text and add the cookie to the current cookie label
            cookie = cookieInp.replace('\n','')
            inputSuccess.config(text='Success')
            inputSuccess.place(x=int((screenWidth/2)+45), y=int((screenHeight/4)+95))
            labelCurrentCookie.config(text="Current Cookie: "+cookie)
        elif errorText != '':
            #Output error message text
            inputError.config(text=errorText)
            inputError.place(x=int((screenWidth/2)+45), y=int((screenHeight/4)+95))

root.mainloop()