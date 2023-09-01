#si vuole realizzare un sito web per memorizzare le squadre di uno sport a scelta.
#l'utente deve poter inserire il nome della squadra,la data di fondazione e la città.
#deve inoltre poter effetuare delle ricerche inserendo uno dei valori delle colonne e ottenendo i dati presenti.

from flask import Flask, render_template,request
app = Flask(__name__)
import pandas as pd

@app.route('/', methods=['GET'])
def home():
    return render_template('squadraHome.html')

@app.route('/inserisci', methods=['GET'])
def inserisci():
    return render_template('inserisci.html')

@app.route('/dati', methods=['GET'])
def dati():
    # inserimento dei dati nel file csv
    # lettura dei dati dal form html 
    squadra = request.args['Squadra']
    anno = request.args['Anno']
    citta = request.args['Citta']
    # lettura dei dati daal file nel dataframe
    df1 = pd.read_csv('/workspace/Flask/Navarette.es4/templates/dati.csv')
    # aggiungiamo i nuovi dati nel dataframe 
    nuovi_dati = {'squadra':squadra,'anno':anno,'citta':citta}
    
    df1 = df1.append(nuovi_dati,ignore_index=True)
    # salviamo il dataframe sul file dati.csv
    df1.to_csv('/workspace/Flask/Navarette.es4/templates/dati.csv', index=False)
    return df1.to_html()

@app.route('/formricerca', methods=['GET'])
def formricerca():
    return render_template('formricerca.html')

@app.route('/ricerca', methods=['GET'])
def ricerca():
    indice = request.args['indice']
    radio = request.args['sel']
    df1 = pd.read_csv('/workspace/Flask/Navarette.es4/templates/dati.csv')
    if indice not in df1[radio]:
        return '<h1>Errore</h1>'
    if radio == 'squadra':
        return df1[df1['squadra'].str.contains(indice)].to_html()
    if radio == 'anno':
        return df1[df1['anno'].str.contains(indice)].to_html()
    if radio == 'citta':
        return df1[df1['citta'].str.contains(indice)].to_html()

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3246, debug=True)