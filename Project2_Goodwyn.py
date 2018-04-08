# ---------------------------------
# Programming Assignment 2
# 04/XX/2018
# Name: John Goodwyn
# Login-ID:
# Student ID:
# ---------------------------------
# Status:
# ---------------------------------


# Import stuff here
import sys

rootUser = ""
loggedInUser = ":" # Default is : since that's an illigal character for passwords
users = {}
groups = {}
fileGroups = {}
fileMod = {}

args = sys.argv
if len(args) == 2:
    fIn = open(args[1],'r')
    lines = [line.strip() for line in fIn.readlines()]

    # Read the first line
    rootTokens = lines[0].split('',2)
    if (len(rootTokens) == 3 && rootTokens[0] == 'useradd' && ValidUsername(rootTokens[1]) && ValidPassword(rootTokens[2])):
        # Normal Operations
        print('Added root user {0}',rootTokens[1])
        rootUser = rootTokens[1]
        users[rootUser] = rootTokens[2]
        MainProcess(lines[1:])
    else:
        # First line was incorrect
        print('First line incorrect')
        
        


    
else:
    print('Incorrect arguments')

def MainProcess(commands):
    for line in commands:
        tokens = line.split('',2)

        if tokens[0] == 'useradd':
            print()
        elif tokens[0] == 'login':
            print()
        elif tokens[0] == 'logout':
            print('x')
        elif tokens[0] == 'groupadd':
            print()
        elif tokens[0] == 'usergrp':
            print()
        elif tokens[0] == 'mkfile':
            print()
        elif tokens[0] == 'chmod':
            print()
        elif tokens[0] == 'chown':
            print()
        elif tokens[0] == 'chgrp':
            print()
        elif tokens[0] == 'read':
            print()
        elif tokens[0] == 'write':
            print()
        elif tokens[0] == 'execute':
            print()
        elif tokens[0] == 'ls':
            print()
        elif tokens[0] == 'end':
            print()
        else:
            print('Invalid Command')
            
    return;

def ValidUsername(name):
    # username is at most 30 characters, doesn't contain any whitespace, and does not contain / or :
    return (len(name) <= 30 && len(name.split()) == 1 && '/' not in name && ':' not in name);

def ValidPassword(password):
    # password is at most 30 chars and doesn't contain any whitespace
    return (len(password) <= 30 && len(password.split()) == 1);

def CheckLogin():
    # Check if logged in user is not default
    return loggedInUser != ':';

def Useradd(useraddArgs):
    
    return;

def Login(loginArgs):
    if not CheckLogin():
        if loginArgs[0] in users:
            if users[loginArgs[0]] != loginArgs[1]:
                print('One of the user credentials was incorrect')
            else:
                loggedInUser = loginArgs[1];
        else:
            print('One of the user credentials was incorrect')
    else:
        print('A user is already logged in')
    return;

def Logout():
    loggedInUser = ':'
    return;

def Groupadd(groupaddArgs):
    return;

def Usergrp(usergrpArgs):
    return;

def Mkfile(mkfileArgs):
    return;

def Chmod(chmodArgs):
    return;

def Chown(chownArgs):
    return;

def Chgrp(chgrpArgs):
    return;

def ReadCmd(readArgs):
    return;

def WriteCmd(writeArgs):
    return;

def ExecuteCmd(executeArgs):
    return;

def LSCmd(lsArgs):
    return;

def EndCmd():
    return;
