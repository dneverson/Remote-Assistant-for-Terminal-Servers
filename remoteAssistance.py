#!/usr/bin/python
import subprocess
from os import system

def getUsers(name):
    p = subprocess.Popen("dsquery user -name *"+name+"* | DSGET USER -samid", stdout=subprocess.PIPE, shell=True)
    p_status = p.wait()
    (output, err) = p.communicate()
    output = output.split()
    return output[1:-2]

def getUserIDFromTerminal(name, terminal):
    p = subprocess.Popen("query user "+name+" /server:"+terminal, stdout=subprocess.PIPE, shell=True)
    p_status = p.wait()
    (output, err) = p.communicate()
    output = output.split()
    if(p_status):
        return output[10:-5]

def getDomain():
    p = subprocess.Popen("ECHO %USERDOMAIN%", stdout=subprocess.PIPE, shell=True)
    p_status = p.wait()
    (output, err) = p.communicate()
    return output.strip()

def searchAllServers(name, servers):
    for server in servers:
        result = getUserIDFromTerminal(name, server)
        domain = getDomain()
        if(result):
            return [domain,server,name,result[0]]

def startRemoteAssistance(arr):
    p = subprocess.Popen("msra.exe /offerra "+arr[1]+" "+arr[0]+"\\"+arr[2]+":"+arr[3], shell=True)
    p_status = p.wait()
    if(p):
        ## REMOTE SESSION IS OVER DO SOMTHING
        clear()
        print("\nRemote Assistance Has Ended")

def logUserOut(arr):
    if(arr):
        p = subprocess.Popen("logoff "+arr[3]+" /server:"+arr[1])
        p_status = p.wait()
        if(p):
            print(arr[2]+" has been logged off")
    else: return 0

def clear():
    system('cls')

def selectUser(name):
    users = getUsers(name)
    if(len(users)>1):
        for i in range(len(users)):
            print(str(i)+" "+users[i])
        try:
            num = int(raw_input("\nSelect User: "))
            return users[num]
        except:
            print("\nInvalid Entry")
            return 0
    else:
        try: return users[0]
        except:
            clear()
            print("\nUser Not Found")


if __name__ == "__main__":
    servers = ["rds-sh01","rds-sh02","rds-sh03","rds-sh04","rds-sh05","rds-sh07","rds-sh08","rds-sh-rec01","rds-sh-rec02","rds-sh-dragon01","cmg-rds-loa1","cmg-rds-loa2"]
    name = selectUser(raw_input("\nUser Name: "))
    found = searchAllServers(name, servers)
    clear()

    if(not found): print("\nUser is not logged in")
    else:
        print("\n1 Remote Assistance")
        #print("\n2 Log User Off")
        option = int(raw_input("\nSelect Option: "))
        if(option==1):
            startRemoteAssistance(found)
        #if(option==2):
        #    logUserOut(found)
