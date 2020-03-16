#!/usr/bin/python
import subprocess
from os import system

# Globals
servers = ["rds-sh01","rds-sh02","rds-sh03","rds-sh04","rds-sh05","rds-sh07","rds-sh08","rds-sh-rec01","rds-sh-rec02","rds-sh-dragon01","cmg-rds-loa1","cmg-rds-loa2"]

# Gets user names via DSQUERY and returns an array of users with matching input
def getUsers(name):
    p = subprocess.Popen("dsquery user -name *"+name+"* | DSGET USER -samid", stdout=subprocess.PIPE, shell=True)
    p_status = p.wait()
    (output, err) = p.communicate()
    output = output.split()
    return output[1:-2]

# Gets ID of user in terminal session if found, returns ID number
def getUserIDFromTerminal(name, terminal):
    p = subprocess.Popen("query user "+name+" /server:"+terminal, stdout=subprocess.PIPE, shell=True)
    p_status = p.wait()
    (output, err) = p.communicate()
    output = output.split()
    if(p_status):
        return output[10:-5]

# Gets current domain and returns string
def getDomain():
    p = subprocess.Popen("ECHO %USERDOMAIN%", stdout=subprocess.PIPE, shell=True)
    p_status = p.wait()
    (output, err) = p.communicate()
    return output.strip()

# Searches all servers for username if found returns array of users information
def searchAllServers(name, servers):
    for server in servers:
        result = getUserIDFromTerminal(name, server)
        domain = getDomain()
        if(result):
            return [domain,server,name,result[0]]

# Initiates Remote Assisstance to user bypassing anoying menus
def startRemoteAssistance(arr):
    p = subprocess.Popen("msra.exe /offerra "+arr[1]+" "+arr[0]+"\\"+arr[2]+":"+arr[3], shell=True)
    p_status = p.wait()
    if(p):
        menu("\n ** Remote Assistance Has Ended **")

# Logs out the given user from the array searchAllServers funtion returns
def logUserOut(arr):
    if(arr):
        p = subprocess.Popen("logoff "+arr[3]+" /server:"+arr[1])
        p_status = p.wait()
        if(p):
            menu("\n **"+arr[2]+" has been logged off **")
    else: return 0

# Clears the CLS Window
def clear():
    system('cls')

# If more than one user is found with "like" string given, will give options to
# select corect user Else returns user in array index 0
def selectUser(name):
    users = getUsers(name)
    if(len(users)>1):
        for i in range(len(users)):
            print("  ("+str(i)+") "+users[i])
        try:
            num = int(raw_input("\n Select User: "))
            return users[num]
        except:
            menu("\n ** Invalid Entry **")
    else:
        try: return users[0]
        except:
            pass

# Gets Computers with like name and parse options
def computerSearch(name, options):
    p = subprocess.Popen(["powershell.exe","get-adcomputer -filter 'name -like \"*"+name+"*\"' -properties * | ft "+options], stdout=subprocess.PIPE, shell=True)
    p_status = p.wait()
    (output, err) = p.communicate()
    clear()
    if(output): print(output)
    else: print("\n - Computer \""+name+"\" Not Found")
    print("\n Search Computer Again? (y/yes)/(n/no)/(exit)")
    option = raw_input("\n Input: ")
    if(option.lower()=="y" or option.lower()=="yes"): menuComputerSearch()
    else: menu()

# Menu for Remote Assistance
def menuRemoteAssistance(message=""):
    clear()
    print("\n -- REMOTE ASSISSTANCE --\n")
    if(message): print(message)
    print("\n type 'exit' to go to main menu")
    userInput = raw_input("\n User Name: ")
    if(userInput.lower()=="exit"): menu()
    else:
        name = selectUser(userInput)
        try: found = searchAllServers(name, servers)
        except: found = ""
        clear()
        if(not found): menuRemoteAssistance("\n User is not found")
        else:
            print("\n Start Remote Assistance? (y/yes)/(n/no)/(exit)")
            option = raw_input("\n Input: ")
            if(option.lower()=="y" or option.lower()=="yes"): startRemoteAssistance(found)
            elif(option.lower()=="n" or option.lower()=="no"): menuRemoteAssistance()
            else: menu()

# Menu for Log User Out
def menuLogUserOut(message=""):
    clear()
    print("\n -- USER LOG OUT --\n")
    if(message): print(message)
    print("\n type 'exit' to go to main menu")
    userInput = raw_input("\n User Name: ")
    if(userInput.lower()=="exit"): menu()
    else:
        name = selectUser(userInput)
        try: found = searchAllServers(name, servers)
        except: found = ""
        clear()
        if(not found): menuLogUserOut("\n User is not found")
        else:
            print("\n Log User Out? (y/yes)/(n/no)/(exit)")
            option = raw_input("\n Input: ")
            if(option.lower()=="y" or option.lower()=="yes"): logUserOut(found)
            elif(option.lower()=="n" or option.lower()=="no"): menuLogUserOut()
            else: menu()

# Menu for Computer Search
def menuComputerSearch(message=""):
    clear()
    print("\n -- COMPUTER SEARCH --\n")
    if(message): print(message)
    print("\n type 'exit' to go to main menu")
    userInputC = raw_input("\n Computer Name: ")
    if(userInputC.lower()=="exit"): menu()
    elif(not userInputC.lower()): menuComputerSearch("\n Computer Name Not Valid")
    else:
        print("\n  - Option Examples: \"*, name, description, ipv4address, operatingsystem)\" Note: seperate by commas or ")
        print("\n  - blank for DEFAULT: name, ipv4address, operatingsystem, description")
        userInputO = raw_input("\n Option(s): ")
        if(userInputO.lower()=="exit"): menu()
        elif(userInputO.lower()): computerSearch(userInputC, userInputO)
        elif(not userInputO.lower()): computerSearch(userInputC, "name, ipv4address, operatingsystem, description")
        else: menuComputerSearch()

# Main menu
def menu(message=""):
    clear()
    if(message): print(message)
    print("\n -- MAIN MENU --\n")
    print("\n (1) Remote Assistance")
    print("\n (2) Log Off User")
    print("\n (3) Computer Search")
    print("\n type 'exit' to go to close program")
    select = raw_input("\n Select Option: ")
    if(select=="1"): menuRemoteAssistance()
    elif(select=="2"): menuLogUserOut()
    elif(select=="3"): menuComputerSearch()
    elif(select.lower()=="exit"): return 0
    else:
        menu("\n ** Invalid Input Select Again **")

# Init
if __name__ == "__main__":
    menu()
