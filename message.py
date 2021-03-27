import uuid
from user import findUserByEmail
from datetime import datetime as dt
from resultmsg import Result
from flask import jsonify
import json
import utils

messages = []
# I messaggi sono memorizzati come dizionari.
# message = {
#    'id': 'a123ba2'
#    'chatId': 'ba4313c123',
#    'seq': 1,
#    'mitt': 'peppino',
#    'dest': 'carmine',
#    'msg': 'testo del messaggio',
#    'created': '5-03-2024', 
# }


def SaveMessage(mitt: str, dest: str, msg: str, chat_id=None) -> (Result, dict):
    # check auth 
    # check if the chatId is 
    if not chat_id:
        chat_id = uuid.uuid4()   

    msg_id = uuid.uuid4()        

    muser = findUserByEmail(mitt)
    duser = findUserByEmail(dest)
    if not muser or not duser:
        print("one of the users has not been found")
        return Result.NOT_FOUND, None
    
    message = {
        'id': msg_id,
        'chatId': chat_id,
        'mitt': muser['email'],
        'dest': duser['email'],
        'msg': msg,
        'created': dt.utcnow().isoformat()
    }

    messages.append(message.copy())
    message['mitt'] = muser['email']
    message['dest'] = duser['email']

    #store
    written = utils.fileDbWrite('messages.db',messages)
    if not written:
        return Result.NOT_FOUND, None
    
    return Result.OK, message

def GetMessages(email: str) -> (Result, dict):
    usr_data = findUserByEmail(email)
    if not usr_data:
        return Result.NOT_FOUND, None
    usr_msgs=[]
    for msg in messages:
        if msg['dest'] == usr_data['email']:
            # modificare i tag di ritorno e risolvere le email
            usr_msgs.append(msg)
    
    return Result.OK, jsonify(usr_msgs)