import os
import json
import base64

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


if __name__ == '__main__':
    users = [{"id":"f7c8bd66-0044-4256-829c-c74291424ec5", "name": "Tizio", "surname": "Caio", "email": "tiziocaio@gmail.com", "created": "2021-03-26T18:37:03.840852", "password": "$2b$12$.nq4Puod5u5ZHr3jYaSoYuhnKdJwOWtAOe5DrItm5yhzeCRD3TLje"}, {"id": "25c25b85-ed8a-4975-90c7-f77a1e29bb9d", "name": "Sempronio", "surname": "Pippo", "email": "semproniopippo@yahoo.it", "created": "2021-03-26T18:37:12.593265", "password": "$2b$12$esj0nwFy7vXOcldeRHi0wOz/QDHMzinUaPR7IiQ7Az4SOxc9eWET."}]
    written = fileDbWrite('users.json',users)
    data = []
    if written:
        data = fileDbReader('users.json')

    print(data)
    print(type(data))