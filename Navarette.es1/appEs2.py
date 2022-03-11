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
    
    return render_template('login.html')
   

@app.route('/login' , methods=['GET'])
def login():
    username = request.args['Username']
    password = request.args['Password']

    for utente1 in lst:
        if utente1['Username'] == username and utente1['Password'] == password:

          if utente1['Sex'] == 'M':
            saluto ='Benvenuto ' + utente1['Nome']
          elif utente1['Sex'] == 'F':
            saluto ='Benvenuta ' + utente1['Nome']
          else:
            saluto = 'Benvenut* ' + utente1['Nome']
    return render_template('welcome2.html',benvenuto=saluto)

 

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)