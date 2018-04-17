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
groups = {}
files = {}

# Initialize audit and account file. Overwrites files
auditFile = open('audit.txt','w')
acctFile = open('accounts.txt','w')
acctFile.close() # I close the accounts writer because I want to separate when I'm reading and writing into separate processes that I can call when needed

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
            auditFile.write('Error: unknown command encountered\n')
            print('Error: unknown command encountered')
            
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

def WriteUserInfo(username,password):
    acctWrite = open('accounts.txt','a') # Open accounts file to append
    acctWrite.write('{0} {1}\n'.format(username,password)) # Write to file using 'username password' format
    acctWrite.close()
	
    return;
	
def GetUserInfo(username):
    acctRead = open('accounts.txt','r') # Open accounts file to read
    lines = [line.strip() for line in acctRead.readlines()] # Read all lines in file
	
    for line in lines:
	userInfo = line.split()
		
	if userInfo[0] == username:
	    acctRead.close() # Close reader
	    return userInfo[1]; # Return password if the username read equals the input username
	
    acctRead.close() # Close reader
	
    return ' '; # Return empty password, nothing found

def CheckUser(username):
    return GetUserInfo(username) != ' '; # Check if returned password isn't empty
	
def Useradd(username,password):
    if loggedInUser == root:
        if not CheckUser(username):
            WriteUserInfo(username,password) # Write user information to accounts
			
            auditFile.write('User {0} created\n'.format(username))
	    print('User {0} created'.format(username))
        
	else:
	    auditFile.write('Error: user {0} already exists\n'.format(username))
            print('Error: user {0} already exists'.format(username))
    
    else:
        auditFile.write('Error: only the root user may issue the useradd command\n')
	print('Error: only the root user may issue the useradd command')
    
    return;

def Login(username,password):
    global loggedInUser
    if not CheckLogin():
        if CheckUser(username):
            if GetUserInfo(username) != password:
                auditFile.write('Login failed: invalid username or password\n')
		print('Login failed: invalid username or password')
            
	    else:
                loggedInUser = username; # Set logged in user
                
		auditFile.write('{0} logged in\n'.format(username))
		print('{0} logged in'.format(username))
        
	else:
            auditFile.write('Login failed: invalid username or password\n')
	    print('Login failed: invalid username or password')
    
    else:
        auditFile.write('Login failed: simultaneous login not permitted\n')
	print('Login failed: simultaneous login not permitted')
    
    return;

def Logout():
    global loggedInUser
    if loggedInUser != ':':
        auditFile.write('User {0} logged out\n'.format(loggedInUser))
	print('User {0} logged out'.format(loggedInUser))
        
	loggedInUser = ':'
		
    else:
        auditFile.write('Logout error: no users are logged in\n')
	print('Logout error: no users are logged in')
    
    return;

def Groupadd(groupName):
    if loggedInUser == root:
        if groupName not in groups:
            if groupName != 'nil':
                groups[groupName] = []
                
		auditFile.write('Group {0} created\n'.format(groupName))
		print('Group {0} created'.format(groupName))
            
	    else:
                auditFile.write('Error: group name cannot be "nil"\n')
		print('Error: group name cannot be "nil"')
        
	else:
            auditFile.write('Error: group {0} already exists\n'.format(groupName))
	    print('Error: group {0} already exists'.format(groupName))
    
    else:
        auditFile.write('Error: only the root user may issue the groupadd command\n')
	print('Error: only the root user may issue the groupadd command')
    
    return;

def Usergrp(username, groupName):
    if loggedInUser == root:
        if CheckUser(username) and groupName in groups:
            if username not in groups[groupName]:
                groups[groupName].append(username)
                
		auditFile.write('User {0} added to group {1}\n'.format(username,groupName))
		print('User {0} added to group {1}'.format(username,groupName))
            
	    else:
                auditFile.write('Error: user {0} is already in group {1}\n'.format(username,groupName))
		print('Error: user {0} is already in group {1}'.format(username,groupName))
        
	else:
            auditFile.write('Error with usergrp: username or group could not be found\n')
	    print('Error with usergrp: username or group could not be found')
    
    else:
        auditFile.write('Error: only the root user may issue the usergrp command\n')
	print('Error: only the root user may issue the usergrp command')
    
    return;

def Mkfile(filename):
    if CheckLogin():
        if filename not in files:
            files[filename] = [loggedInUser, 'nil', 'rw-', '---', '---']
            
	    auditFile.write('File {0} with owner {1} and default permissions created\n'.format(filename,loggedInUser))
	    print('File {0} with owner {1} and default permissions created'.format(filename,loggedInUser))
        
	else:
            auditFile.write('Error: the file {0} already exists\n'.format(filename))
	    print('Error: the file {0} already exists'.format(filename))
    
    else:
        auditFile.write('Error: user must be logged in to issue the mkfile command\n')
	print('Error: user must be logged in to issue the mkfile command')
    
    return;

def Chmod(filename,permissions):
    if CheckLogin():
        if filename in files:
            if (loggedInUser == root or loggedInUser == files[filename][0]):
                perm = permissions.split() # Split the permissions input to get the owner, group, and other permissions
				
		# Check if permissions follow correct format
                if ValidPermissions(perm):
                    auditFile.write('Permissions for {0} set to {1} {2} {3} by {4}\n'.format(filename,perm[0],perm[1],perm[2],loggedInUser))
		    print('Permissions for {0} set to {1} {2} {3} by {4}'.format(filename,perm[0],perm[1],perm[2],loggedInUser))
					
                    files[filename] = [files[filename][0],files[filename][1],perm[0],perm[1],perm[2]]
                
		else:
                    auditFile.write('Error: the file permissions do not follow the correct format\n')
		    print('Error: the file permissions do not follow the correct format')
            
	    else:
                auditFile.write('Error: only the root user or file owner may issue the chmod command\n')
		print('Error: only the root user or file owner may issue the chmod command')
        
	else:
            auditFile.write('Error with chmod: file {0} not found\n'.format(filename))
	    print('Error with chmod: file {0} not found'.format(filename))
    
    else:
        auditFile.write('Error: user must be logged in to issue the chmod command\n')
	print('Error: user must be logged in to issue the chmod command')
    
    return;

def Chown(filename,username):
    if loggedInUser == root:
        if CheckUser(username) and filename in files:
            files[filename][0] = username
            
	    auditFile.write('Owner of {0} changed to {1}\n'.format(filename,username))
	    print('Owner of {0} changed to {1}'.format(filename,username))
        
	else:
            auditFile.write('Error with chown: file {0} not found\n'.format(filename))
	    print('Error with chown: file {0} not found'.format(filename))
    
    else:
        auditFile.write('Error: only the root user may issue the chown command\n')
	print('Error: only the root user may issue the chown command')
    
    return;

def Chgrp(filename,groupName):
    if CheckLogin():
        if filename in files and groupName in groups:
            if loggedInUser == root:
                files[filename][1] = groupName # Re-assign the group name to file info
                
		auditFile.write('Group for {0} set to {1} by {2}\n'.format(filename,groupName,loggedInUser))
		print('Group for {0} set to {1} by {2}'.format(filename,groupName,loggedInUser))

            elif loggedInUser == files[filename][0]:
                
		# Check if user is in the group specified
		if loggedInUser in groups[groupName]:
                    files[filename][1] = groupName # Re-assign the group name to file info
                    
		    auditFile.write('Group for {0} set to {1} by {2}\n'.format(filename,groupName,loggedInUser))
		    print('Group for {0} set to {1} by {2}'.format(filename,groupName,loggedInUser))

                else:
                    auditFile.write('Error with chgrp: user {0} is not a member of group {1}\n'.format(loggedInUser,groupName))
		    print('Error with chgrp: user {0} is not a member of group {1}'.format(loggedInUser,groupName))

            else:
                auditFile.write('Error: only the root user or file owner may issue the chmod command\n')
		print('Error: only the root user or file owner may issue the chmod command')
        
	else:
            auditFile.write('Error with chgrp: filename or group was not found\n')
	    print('Error with chgrp: filename or group was not found')
   
    else:
        auditFile.write('Error: user must be logged in to issue the chgrp command\n')
	print('Error: user must be logged in to issue the chgrp command')
    
    return;

def ReadText(filename):
    inputText = open(filename,'r')
    lines = [line.strip() for line in inputText.readlines()]
	
    auditFile.write('User {0} reads {1} as:\n'.format(loggedInUser,filename))
    print('User {0} reads {1} as:'.format(loggedInUser,filename))
	
    # Print each line
    for line in lines:
	auditFile.write(line + '\n')
	print(line)

    return;
	
def ReadCmd(filename):
    if CheckLogin():
        if filename in files:
            fileInfo = files[filename] # Get file info from files dictionary
			
            if loggedInUser == fileInfo[0]:
                if fileInfo[2][0] == 'r':
                    ReadText(filename)
                
		else:
                    auditFile.write('User {0} denied read access to {1}\n'.format(loggedInUser,filename))
		    print('User {0} denied read access to {1}'.format(loggedInUser,filename))

            elif fileInfo[1] != 'nil' and loggedInUser in groups[fileInfo[1]]:
                if fileInfo[3][0] == 'r':
                    ReadText(filename)
                    
		else:
                    auditFile.write('User {0} denied read access to {1}\n'.format(loggedInUser,filename))
		    print('User {0} denied read access to {1}'.format(loggedInUser,filename))

            else:
                if fileInfo[4][0] == 'r':
                    ReadText(filename)
                
		else:
                    auditFile.write('User {0} denied read access to {1}\n'.format(loggedInUser,filename))
		    print('User {0} denied read access to {1}'.format(loggedInUser,filename))

        else:
            auditFile.write('User {0} denied read access to {1}\n'.format(loggedInUser,filename))
	    print('User {0} denied read access to {1}'.format(loggedInUser,filename))

    else:
        auditFile.write('Error: user must be logged in to issue the read command\n')
	print('Error: user must be logged in to issue the read command')
    
    return;
	
def WriteText(filename,text):
    outputFile = open(filename,'a') # Open file
    outputFile.write(text + '\n') # Write text
    outputFile.close() # Close file
	
    return;

def WriteCmd(filename,text):
    if CheckLogin():
        if filename in files:
            fileInfo = files[filename] # Get file info from files dictionary
            
	    if loggedInUser == fileInfo[0]:
                if fileInfo[2][1] == 'w':
                    auditFile.write('User {0} wrote to {1}: {2}\n'.format(loggedInUser,filename,text))
		    print('User {0} wrote to {1}: {2}'.format(loggedInUser,filename,text))
                
		    WriteText(filename,text)
		else:
                    auditFile.write('User {0} denied write access to {1}\n'.format(loggedInUser,filename))
		    print('User {0} denied write access to {1}'.format(loggedInUser,filename))

            elif fileInfo[1] != 'nil' and loggedInUser in groups[fileInfo[1]]:
                if fileInfo[3][1] == 'w':
                    auditFile.write('User {0} wrote to {1}: {2}\n'.format(loggedInUser,filename,text))
		    print('User {0} wrote to {1}: {2}'.format(loggedInUser,filename,text))
                
		    WriteText(filename,text)
		else:
                    auditFile.write('User {0} denied write access to {1}\n'.format(loggedInUser,filename))
		    print('User {0} denied write access to {1}'.format(loggedInUser,filename))

            else:
                if fileInfo[4][1] == 'w':
                    auditFile.write('User {0} wrote to {1}: {2}\n'.format(loggedInUser,filename,text))
		    print('User {0} wrote to {1}: {2}'.format(loggedInUser,filename,text))
                
		    WriteText(filename,text)
		else:
                    auditFile.write('User {0} denied write access to {1}\n'.format(loggedInUser,filename))
		    print('User {0} denied write access to {1}'.format(loggedInUser,filename))
                    
        else:
            auditFile.write('User {0} denied write access to {1}\n'.format(loggedInUser,filename))
	    print('User {0} denied write access to {1}'.format(loggedInUser,filename))

    else:
        auditFile.write('Error: user must be logged in to issue the write command\n')
	print('Error: user must be logged in to issue the write command')
    
    return;

def ExecuteCmd(filename):
    if CheckLogin():
        if filename in files:
            fileInfo = files[filename] # Get file info from files dictionary
            
	    if loggedInUser == fileInfo[0]:
                if fileInfo[2][2] == 'x':
                    auditFile.write('File {0} executed by {1}\n'.format(filename,loggedInUser))
		    print('File {0} executed by {1}'.format(filename,loggedInUser))
                
		else:
                    auditFile.write('User {0} denied execute access to {1}\n'.format(loggedInUser,filename))
		    print('User {0} denied execute access to {1}'.format(loggedInUser,filename))

            elif fileInfo[1] != 'nil' and loggedInUser in groups[fileInfo[1]]:
                if fileInfo[3][2] == 'x':
                    auditFile.write('File {0} executed by {1}\n'.format(filename,loggedInUser))
		    print('File {0} executed by {1}'.format(filename,loggedInUser))
                
		else:
                    auditFile.write('User {0} denied execute access to {1}\n'.format(loggedInUser,filename))
		    print('User {0} denied execute access to {1}'.format(loggedInUser,filename))

            else:
                if fileInfo[4][2] == 'x':
                    auditFile.write('File {0} executed by {1}\n'.format(filename,loggedInUser))
		    print('File {0} executed by {1}'.format(filename,loggedInUser))
                
		else:
                    auditFile.write('User {0} denied execute access to {1}\n'.format(loggedInUser,filename))
		    print('User {0} denied execute access to {1}'.format(loggedInUser,filename))

        else:
            auditFile.write('User {0} denied execute access to {1}\n'.format(loggedInUser,filename))
	    print('User {0} denied execute access to {1}'.format(loggedInUser,filename))

    else:
        auditFile.write('Error: user must be logged in to issue the execute command\n')
	print('Error: user must be logged in to issue the execute command')
    
    return;

def LSCmd(filename):
    if filename in files:
        fileInfo = files[filename] # Get file info from file dictionary
        
	auditFile.write('{0}: {1} {2} {3} {4} {5}\n'.format(filename, fileInfo[0], fileInfo[1], fileInfo[2], fileInfo[3], fileInfo[4]))
	print('{0}: {1} {2} {3} {4} {5}'.format(filename, fileInfo[0], fileInfo[1], fileInfo[2], fileInfo[3], fileInfo[4]))

    else:
        auditFile.write('Error: the file {0} could not be found\n'.format(filename))
	print('Error: the file {0} could not be found'.format(filename))
    
    return;

def EndCmd():
    auditFile.close() # Close audit file writer
	
    # Write all the group info
    groupFile = open('groups.txt','w')
	
    for group, members in groups.iteritems():
	groupFile.write('{0}: {1}\n'.format(group,' '.join(members)))
		
    groupFile.close()
	
    # Write all the file info
    fileInfoFile = open('files.txt','w')
	
    for filename, fileInfo in files.iteritems():
	fileInfoFile.write('{0}: {1} {2} {3} {4} {5}\n'.format(filename, fileInfo[0], fileInfo[1], fileInfo[2], fileInfo[3], fileInfo[4]))
	
    fileInfoFile.close()
	
    return;

# -------------------------------------------------------------------------------------------------
# MAIN PROGRAM AFTER ALL METHODS ARE DEFINED

args = sys.argv
if len(args) == 2:
    # open input and read all lines
    fIn = open(args[1],'r') 
    lines = [line.strip() for line in fIn.readlines()]

    # Read the first line
    rootTokens = lines[0].split(' ',2)
    if (len(rootTokens) == 3 and rootTokens[0] == 'useradd' and ValidUsername(rootTokens[1]) and ValidPassword(rootTokens[2])):
        auditFile.write('User {0} created\n'.format(rootTokens[1]))
        print('User {0} created'.format(rootTokens[1]))
        
	root = rootTokens[1] # Set the root username to username provided
	WriteUserInfo(rootTokens[1],rootTokens[2]) # Write user info to accounts
        
	# Initiate the main process
	MainProcess(lines[1:])
    else:
        # First line was incorrect
        auditFile.write('Error: first command line did not follow the correct format\n')
	print('Error: first command line did not follow the correct format')
		
	auditFile.close() # Close the audit file since the end command won't be reached here
    
else:
    print('Error: the commandline arguments are incorrect. Enter "python executableFilename commandTextFilename"')
