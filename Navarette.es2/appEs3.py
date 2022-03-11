#realizzare un server web che permetta di conoscere capoluoghi di regione.
#l'utente inserisce il nome della regione e il programma restituisce il nome di capoluogo di regione.
#caricare i capoluoghi e le regioni in una opportuna struttura dati.

#modificare poi l'esercizio precedente per permettere all'utente di inserire un capoluogo e di avere la regione in cui si trova
#l'utente sceglie se avere la regione o il capoluogo selezionando un radio button

from flask import Flask, render_template,request
app = Flask(__name__)

dizionario = {"Lazio":"Roma","Lombardia":"Milano","Campania":"Napoli","Piemonte":"Torino","Sicilia":"Palermo","Liguria":"Genova","Emilia-Romagna":"Bologna","Toscana":"Firenze","Puglia":"Bari","Veneto":"Venezia","Friuli-Venezia Giulia":"Trieste","Umbria":"Perugia","Sardegna":"Cagliari","Trentino-Alto Adige":"Trento","Marche":"Ancona","Calabria":"Catanzaro","Abruzzo":"L'Aquila","Basilicata":"Potenza","Molise":"Campobasso","Valle d'Aosta":"Aosta"}

@app.route('/' , methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/data' , methods=['GET'])
def data():

    scelta = request.args["bottone"]
    if scelta == "R":
        capoluogo = request.args["Input"]
        for key, value in dizionario.items():
            if capoluogo == value:
                regione = key
                return render_template("risposta.html", risposta = regione)
        return '<h1>La regione o capoluogo inserito non esistono</h1>'
    else:      
        regione = request.args["Input"]
        for key, value in dizionario.items():
            if regione == key:
                capoluogo = value
                return render_template("risposta.html", risposta = capoluogo)
        return '<h1>La regione o capoluogo inserito non esistono</h1>'
        
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)