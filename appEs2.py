#realizzare un sito web che permetta la registrazione degli utenti
#l'utente inserisce il nome,uno username,una password
#la conferma della password e il sesso.
#se le informazioni sono corrette il sito salva le informazioni in una struttura dati opportuna

#prevedere la possibilità di fare il login inserendo username e password
#se sono corrette fornire un messaggio di benvenuto diverso a secondo del sesso

from flask import Flask, render_template,request
app = Flask(__name__)

lst = []

@app.route('/' , methods=['GET'])
def home():
    return render_template('registrazione.html')

@app.route('/data' , methods=['GET'])
def data():

    nome = request.args['Nome']
    username = request.args['Username']
    password = request.args['Password']
    confPassword = request.args['Conferma Password']
    sesso = request.args['Sex']

    if password == confPassword:
     utente = {'Nome':nome,'Username':username,'Password':password,'Sex':sesso}
     lst.append(utente)
     print(lst)
     if sesso == 'M':
       saluto ='Benvenuto'
     elif sesso == 'F':
       saluto ='Benvenuta'
     else:
       saluto = 'Benvenut*'
       return render_template('welcome2.html',benvenuto=saluto)

@app.route('/login' , methods=['GET'])
def login():
    username = request.args['Username']
    password = request.args['Password']
    
    return render_template('login.html')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)