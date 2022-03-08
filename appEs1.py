#realizzare un server web che permetta di effetuare il login
#l'utente inserisce lo username e la password:
#se il username è admin e la password è xxx123## il sito ci saluta con un messaggio di benvenuto altrimenti ci da un messaggio di errore
from flask import Flask, render_template,request
app = Flask(__name__)
@app.route('/' , methods=['GET'])
def home():
    return render_template('form2.html')
    
@app.route('/data' , methods=['GET'])
def data():

   if request.args['Username'] == 'admin' and request.args['Password'] == 'xxx123##':
    return render_template('wellcome2.html',benvenuto = 'Benvenuto')

   else:
    return 'errore'

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)