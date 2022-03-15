#si vuole realizzare un sito web che permetta di visualizzare alcune informazioni sull'andamento dell'epidemia di covid nel nostro paese a partire dai dati presenti nel file 'https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/platea-dose-addizionale-booster.csv'
#l'utente sceglie la regione da un elenco (menu a tendina),clicca su un bottone e il sito deve visualizzare una tabella contenente le informazioni relative a quella regione 
#i dati da inserire nel menu a tendina devono essere caricati automaticamente dalla pagina 
from flask import Flask, render_template,request
app = Flask(__name__)
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/platea-dose-addizionale-booster.csv')


@app.route('/', methods=['GET'])
def index():
    reg = df['nome_area'].drop_duplicates().to_list() #droppa i duplicati della colonna nome_area e lo trasforma in una lista
    return render_template('vaccini.html', reg=reg) 

@app.route('/vaccini' , methods=['GET'])
def vaccini():
    regione = request.args['vaccini'] 
    df3 = df[df['nome_area']== regione] 
    return render_template('vaccini1.html', tables=[df3.to_html()], titles=[''])
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3246, debug=True)