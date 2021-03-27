# Questo modulo utilizza Flask per realizzare un web server. L'applicazione può essere eseguita in vari modi
# FLASK_APP=server.py FLASK_ENV=development flask run
# python server.py se aggiungiamo a questo file app.run()

from flask import Flask, request, jsonify
import user
import message
import utils

# viene creata l'applicazione con il nome del modulo corrente.
app = Flask(__name__)


# inizializza le liste con i valori dei file
message.messages = utils.fileDbReader('messages.json')
user.users = utils.fileDbReader('users.json')




# getErrorCode è una funzione di utilità che mappa i valori ritornati dal modulo user con quelli del
# protocollo HTTP in caso di errore. 
# 404 - Not Found: una risorsa non è stata trovata sul server;
# 403 - Forbidden: accesso negato;
# 409 - Conflict: è violato un vincolo di unicità. Ad esempio, esiste già un utente con la stessa mail registrata;
# Come ultima spiaggia è buona norma ritornare "500 - Internal Server Error" per indicare che qualcosa è andato storto
def getErrorCode(result: user.Result)->int:
    
    if result is user.Result.NOT_FOUND:
        code = 404
    elif result is user.Result.NOT_AUTHORIZED:
        code = 403
    elif result is user.Result.DUPLICATED:
        code = 409
    else:
        code = 500

    return code

@app.route('/user', methods=['POST','DELETE'])
def manageUser():
    # POST
    if request.method == "POST":
        data = request.get_json()
        name = data['name']
        surname = data['surname']
        email = data['email']
        password = data['password']
        
        result, u = user.SaveUser(name, surname, email, password)

        if result is not user.Result.OK:
            code = getErrorCode(result)
            return '', code
        else:
            return u, 201

    # DELETE
    elif request.method == "DELETE":
        auth = request.authorization
        if auth is None:
            return '', 403

        email = auth['username']
        pwd = auth['password']
        authorized, usr = user.Login(email, pwd)

        if authorized is not user.Result.OK:
            code = getErrorCode(authorized)
            return '', code
        
        result = user.DeleteUser(usr['email'])
        if result is not user.Result.OK:
            code = getErrorCode(result)
            return '', code
        else:
            return '', 200
        
    # OTHER REQUESTS
    else:
        return '', 400

        

@app.route('/login', methods=['POST'])
def loginUser():
    data = request.get_json()
    email = data['email']
    password = data['password']
    print(password)
    res, log = user.Login(email,password)
    if res is not user.Result.OK:
        code = getErrorCode(res)
        return '', code
    else:
        return log, 200


@app.route('/inbox', methods=['POST','GET'])
def inboxMng():
    # POST
    if request.method == "POST":
        data = request.get_json()
        mitt = data['mitt']
        dest = data['dest']
        chatId = data['chatId']
        msg = data['msg']
        result, m = message.SaveMessage(mitt, dest, msg, chatId)

        if result is not message.Result.OK:
            code = getErrorCode(result)
            return '', code
        else:
            return m, 201

    # GET
    elif request.method == "GET":
        email = request.args.get('email')
        result, msgs = message.GetMessages(email)

        if result is not message.Result.OK:
            code = getErrorCode(result)
            return '', code
        else:
            return msgs, 200
    
    # OTHER REQUESTS
    else:
        return '', 400


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
    
