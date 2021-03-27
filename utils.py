import os
import json
import ast

# create a dir
def createDir(path,dirmode=0o666):       
    try:
        if os.path.exists(path):
            print("createDir - The folder "+str(path)+" already exists. Nothing to create.")
            return True
        else:
            os.mkdir(path=path,mode=dirmode)
            print("createDir - The folder "+str(path)+" has been succesfully created.")
        return True
    except OSError as oserr:
        print("createDir - An error occurred while creating folder "+str(oserr))
        return False

# write file
def writeFile(txtFile, text):
    try:
        #fileName = os.path.basename(txtFile)
        '''
        path = os.path.dirname(txtFile)
        if not os.path.exists(path):
            createDir(path)
        '''
        with open(txtFile,"w+") as wfile:
            if isinstance(text,list) or isinstance(text,dict):
                for el in text:
                    wfile.write(el)
            else:
                wfile.write(text)
        print("writeFile - File "+str(txtFile)+" has been succesfully written.")
        return True
    except Exception as e:    
        print("writeFile - An error occurred while trying to write "+str(txtFile)+ ": "+str(e)+".")
        return False

'''
def fileDbWrite(toWrite, data):
    try:
    
        dbfile = '{\n'
        for el in data:
            dbfile = dbfile + ' ' + json.dumps(el) +',\n'
        dbfile = dbfile +'}\n'
        print(dbfile)

        with open(toWrite,"w+") as wfile:
            wfile.write(dbfile)
        print("fileDbWrite - File "+str(toWrite)+" has been succesfully written.")
        
        return True
    except Exception as e:    
        print("fileDbWrite - An error occurred while trying to write "+str(toWrite)+ ": "+str(e)+".")
        return False
'''

# read the content of the file which is a list of dictionaries and return the list

def fileDbReader(toRead):
    data=[]
    if os.path.exists(toRead):
        try:
            with open(toRead, 'r') as content:
                for line in content:
                    data.append(json.loads(line))
        except Exception as e:
            print("fileDbReader - An error occurred while reading the "+ str(toRead)+"file "+str(e))
            return False
    else:
        print("jsonReader - The json file "+str(toRead)+" has not been found.")
    return data


def fileDbWrite(toWrite, data):
    cnt = ''
    try:
        for dic in data:
            cnt = cnt + str(dic).replace("'",'"') +"\n"

        with open(toWrite,"w+") as wfile:
            wfile.write(str(cnt))
        print("fileDbWrite - File "+str(toWrite)+" has been succesfully written.")
        return True
    except Exception as e:    
        print("fileDbWrite - An error occurred while trying to write "+str(toWrite)+ ": "+str(e)+".")
        return False