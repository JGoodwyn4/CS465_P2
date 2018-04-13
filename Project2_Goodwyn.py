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

# Define global variables/lists/dictionaries
root = ""
loggedInUser = ":" # Default is : since that's an illigal character for passwords
users = {}
groups = {}
files = {}

def MainProcess(commands):
    for line in commands:
        tokens = line.split(' ',2)

        if tokens[0] == 'useradd':
            Useradd(tokens[1],tokens[2])
            
        elif tokens[0] == 'login':
            Login(tokens[1],tokens[2])
            
        elif tokens[0] == 'logout':
            Logout()
            
        elif tokens[0] == 'groupadd':
            Groupadd(tokens[1])
            
        elif tokens[0] == 'usergrp':
            Usergrp(tokens[1],tokens[2])
            
        elif tokens[0] == 'mkfile':
            Mkfile(tokens[1])
            
        elif tokens[0] == 'chmod':
            Chmod(tokens[1],tokens[2])
            
        elif tokens[0] == 'chown':
            Chown(tokens[1],tokens[2])
            
        elif tokens[0] == 'chgrp':
            Chgrp(tokens[1],tokens[2])
            
        elif tokens[0] == 'read':
            ReadCmd(tokens[1])
            
        elif tokens[0] == 'write':
            WriteCmd(tokens[1],tokens[2])
            
        elif tokens[0] == 'execute':
            ExecuteCmd(tokens[1])
            
        elif tokens[0] == 'ls':
            LSCmd(tokens[1])
            
        elif tokens[0] == 'end':
            EndCmd()
            return;
            
        else:
            print('Invalid Command\n')

        print('\n')
            
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
            print('The user {0} was added'.format(username))
        else:
            print('The user {0} could not be added'.format(username))
    else:
        print('Root user must be logged in to add a new user')
    return;

def Login(username,password):
    global loggedInUser
    if not CheckLogin():
        if username in users:
            if users[username] != password:
                print('One of the user credentials was incorrect')
            else:
                loggedInUser = username;
                print('{0} logged in'.format(username))
        else:
            print('One of the user credentials was incorrect')
    else:
        print('A user is already logged in')
    return;

def Logout():
    global loggedInUser
    if loggedInUser != ':':
        print('Logging out current user {0}'.format(loggedInUser))
        loggedInUser = ':'
    else:
        print('No user is logged in')
    return;

def Groupadd(groupName):
    if loggedInUser == root:
        if groupName not in groups:
            if groupName != 'nil':
                groups[groupName] = []
                print('The group {0} was added'.format(groupName))
            else:
                print('A group cannot be called "nil"')
        else:
            print('Could not add the group {0}'.format(groupName))
    else:
        print('Root user must be logged in to execute this command')
    return;

def Usergrp(username, groupName):
    if loggedInUser == root:
        if username in users and groupName in groups:
            if username not in groups[groupName]:
                groups[groupName].append(username)
                print('{0} was added to {1}'.format(username,groupName))
            else:
                print('{0} is already in {1}'.format(username,groupName))
        else:
            print('One of the supplied arguments was incorrect')
    else:
        print('Root user must be logged in to execute this command')
    return;

def Mkfile(filename):
    if CheckLogin():
        if filename not in files:
            files[filename] = [loggedInUser, 'nil', 'rw-', '---', '---']
            print('{0} was created'.format(filename))
        else:
            print('The file could not be created')
    else:
        print('A user must be logged in to execute this command')
    return;

def Chmod(filename,permissions):
    if CheckLogin():
        if filename in files:
            if (loggedInUser == root or loggedInUser == files[filename][0]):
                perm = permissions.split()
                if ValidPermissions(perm):
                    print('File permissions for {0} are set'.format(filename))
                    files[filename] = [files[filename][0],files[filename][1],perm[0],perm[1],perm[2]]
                else:
                    print('File arguments are incorrect')
            else:
                print('Only the file owner or root user may execute this command')
        else:
            print('The command could not be executed')
    else:
        print('A user must be logged in to execute this command')
    return;

def Chown(filename,username):
    if loggedInUser == root:
        if username in users and filename in files:
            files[filename][0] = username
            print('{0} was set as the owner of {1}'.format(username,filename))
        else:
            print('The command was unable to be executed')
    else:
        print('Only the root user may execute this command')
    return;

def Chgrp(filename,groupName):
    if CheckLogin():
        if filename in files and groupName in groups:
            if loggedInUser == root:
                files[filename][1] = groupName
                print('{0} was assigned to {1}'.format(groupName,filename))

            elif loggedInUser == files[filename][0]:
                if loggedInUser in groups[groupName]:
                    files[filename][1] = groupName
                    print('{0} was assigned to {1}'.format(groupName,filename))

                else:
                    print('The file owner must belong to the group specified')

            else:
                print('Only the file owner or root user may execute this command')
        else:
            print('The command could not be executed')
    else:
        print('Must be logged in to execute command')
    return;

def ReadCmd(filename):
    if CheckLogin():
        if filename in files:
            fileInfo = files[filename]
            if loggedInUser == fileInfo[0]:
                if fileInfo[2][0] == 'r':
                    # Allow to read file
                    print('{0} read file {1}'.format(loggedInUser,filename))
                else:
                    print('Permission denied')

            elif fileInfo[1] != 'nil' and loggedInUser in groups[fileInfo[1]]:
                if fileInfo[3][0] == 'r':
                    print('{0} read file {1}'.format(loggedInUser,filename))
                else:
                    print('Permission denied')

            else:
                if fileInfo[4][0] == 'r':
                    print('{0} read file {1}'.format(loggedInUser,filename))
                else:
                    print('Permission denied')

        else:
            print('Permission denied')

    else:
        print('User must be logged in to execute command')
    return;

def WriteCmd(filename,text):
    if CheckLogin():
        if filename in files:
            fileInfo = files[filename]
            if loggedInUser == fileInfo[0]:
                if fileInfo[2][1] == 'w':
                    print('{0} wrote "{1}" to file {2}'.format(loggedInUser,text,filename))
                else:
                    print('Permission denied')

            elif fileInfo[1] != 'nil' and loggedInUser in groups[fileInfo[1]]:
                if fileInfo[3][1] == 'w':
                    print('{0} wrote "{1}" to file {2}'.format(loggedInUser,text,filename))
                else:
                    print('Permission denied')

            else:
                if fileInfo[4][1] == 'w':
                    print('{0} wrote "{1}" to file {2}'.format(loggedInUser,text,filename))
                else:
                    print('Permission denied')
                    
        else:
            print('Permission denied')

    else:
        print('User must be logged in to execute command')
    return;

def ExecuteCmd(filename):
    if CheckLogin():
        if filename in files:
            fileInfo = files[filename]
            if loggedInUser == fileInfo[0]:
                if fileInfo[2][2] == 'x':
                    print('{0} executed successfully'.format(filename))
                else:
                    print('Permission denied')

            elif fileInfo[1] != 'nil' and loggedInUser in groups[fileInfo[1]]:
                if fileInfo[3][2] == 'x':
                    print('{0} executed successfully'.format(filename))
                else:
                    print('Permission denied')

            else:
                if fileInfo[4][2] == 'x':
                    print('{0} executed successfully'.format(filename))
                else:
                    print('Permission denied')

        else:
            print('Permission denied')

    else:
        print('User must be logged in to execute command')
    return;

def LSCmd(filename):
    if filename in files:
        fileInfo = files[filename]
        print('{0}: {1} {2} {3} {4} {5}'.format(filename, fileInfo[0], fileInfo[1], fileInfo[2], fileInfo[3], fileInfo[4]))

    else:
        print('The command could not be executed')
    return;

def EndCmd():
    print('End command reached')
    return;

# MAIN PROGRAM AFTER ALL METHODS ARE DEFINED

args = sys.argv
if len(args) == 2:
    fIn = open(args[1],'r')
    lines = [line.strip() for line in fIn.readlines()]

    # Read the first line
    rootTokens = lines[0].split(' ',2)
    if (len(rootTokens) == 3 and rootTokens[0] == 'useradd' and ValidUsername(rootTokens[1]) and ValidPassword(rootTokens[2])):
        # Normal Operations
        print('Added root user {0}'.format(rootTokens[1]))
        root = rootTokens[1]
        users[root] = rootTokens[2]
        MainProcess(lines[1:])
    else:
        # First line was incorrect
        print('First line incorrect')
    
else:
    print('Incorrect arguments')
