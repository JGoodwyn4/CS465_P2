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
files = {}

args = sys.argv
if len(args) == 2:
    fIn = open(args[1],'r')
    lines = [line.strip() for line in fIn.readlines()]

    # Read the first line
    rootTokens = lines[0].split('',2)
    if (len(rootTokens) == 3 and rootTokens[0] == 'useradd' and ValidUsername(rootTokens[1]) and ValidPassword(rootTokens[2])):
        # Normal Operations
        print('Added root user {0}\n',rootTokens[1])
        rootUser = rootTokens[1]
        users[rootUser] = rootTokens[2]
        MainProcess(lines[1:])
    else:
        # First line was incorrect
        print('First line incorrect\n')
        
        


    
else:
    print('Incorrect arguments')

def MainProcess(commands):
    for line in commands:
        tokens = line.split('',2)

        if tokens[0] == 'useradd':
            Useradd(tokes[1],tokens[2])
            
        elif tokens[0] == 'login':
            Login(tokens[1],tokens[2])
            
        elif tokens[0] == 'logout':
            Logout()
            
        elif tokens[0] == 'groupadd':
            Groupadd(tokens[1])
            
        elif tokens[0] == 'usergrp':
            Usergrp(tokens[1],tokens[2])
            
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
            print('Invalid Command\n')
            
    return;

def ValidUsername(name):
    # username is at most 30 characters, doesn't contain any whitespace, and does not contain / or :
    return (len(name) <= 30 and len(name.split()) == 1 and '/' not in name and ':' not in name);

def ValidPassword(password):
    # password is at most 30 chars and doesn't contain any whitespace
    return (len(password) <= 30 and len(password.split()) == 1);

def CheckLogin():
    # Check if logged in user is not default
    return loggedInUser != ':';

def ValidPermissions(permissions):
    return len(permissions) == 3 and len(permissions[0]) == 3 and len(permissions[1]) == 3 and len(permissions[2]) == 3 and ValidAccess(permissions[0]) and ValidAccess(permissions[1]) and ValidAccess(permissions[2]);

def ValidAccess(access):
    return (access[0] == 'r' or access[0] == '-') and (access[1] == 'w' or access[1] == '-') and (access[2] == 'x' or access[2] == '-');

def Useradd(username,password):
    if loggedInUser == root:
        if username not in users:
            users[username] = password
            print('The user {0} was added',username)
        else:
            print('The user {0} could not be added\n',username)
    else:
        print('Root user must be logged in to add a new user\n')
    return;

def Login(username,password):
    if not CheckLogin():
        if username in users:
            if users[username] != password:
                print('One of the user credentials was incorrect\n')
            else:
                loggedInUser = password;
                print('{0} Logged in', username);
        else:
            print('One of the user credentials was incorrect\n')
    else:
        print('A user is already logged in\n')
    return;

def Logout():
    print('Logging out current user {0}\n', loggedInUser);
    loggedInUser = ':'
    return;

def Groupadd(groupName):
    if loggedInUser == root:
        if groupName not in groups:
            if groupName != 'nil':
                groups[groupName] = []
                print('The group {0} was added',groupName)
            else:
                print('A group cannot be called "nil"')
        else:
            print('Could not add the group {0}\n',groupName)
    else:
        print('Root user must be logged in to add a new group\n')
    return;

def Usergrp(username, groupName):
    if username in users and groupName in groups:
        if username not in groups[groupName]:
            groups[groupName].append(username)
            print('{0} was added to {1}\n',username,groupName)
        else:
            print('{0} is already in {1}\n',username,groupName)
    else:
        print('One of the supplied arguments was incorrect\n')
    return;

def Mkfile(filename):
    if not CheckLogin():
        if filename not in files:
            files[filename] = (loggedInUser, 'nil', 'rw-', '---', '---')
            print('{0} was created\n',filename)
        else:
            print('The file could not be created\n')
    else:
        print('A user must be logged in to execute this command\n')
    return;

def Chmod(filename,permissions):
    if not CheckLogin():
        if filename in files:
            if (loggedInUser == root or loggedInUser == files[filename][0]):
                perm = permissions.split()
                if ValidPermissions(perm):
                    print('File permissions are set\n')
                    files[filename] = (files[filename][0],files[filename][1],perm[0],perm[1],perm[2])
                else:
                    print('File arguments are incorrect\n')
            else:
                print('Only the file owner or root user may execute this command\n')
        else:
            print('The command could not be executed/n')
    else:
        print('A user must be logged in to execute this command\n')
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
