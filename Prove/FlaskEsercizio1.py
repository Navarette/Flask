from flask import Flask, render_template 
app = Flask(__name__)
import random
from datetime import date,datetime

frasilst = [{'autore':'Johann Wolfgang von Goethe','frase' : 'Il dubbio cresce con la conoscenza.'},
        {'autore':'Luis Sepùlveda','frase' : 'Vola solo chi osa farlo.'},
        {'autore':'Lucio Anneo Seneca','frase' : 'Se vuoi essere amato, ama.'},
        {'autore':'Voltaire','frase' : 'Chi non ha bisogno di niente non è mai povero.'},
        {'autore':'Confucio','frase' : "Non importa quanto vai piano, l' importante è non fermarsi."},
        {'autore':'Steve Jobs','frase' : 'Siate affamati, siate folli.'},
        {'autore':'Walt Disney','frase' : 'Pensa, credi, sogna e osa.'},
        {'autore':'Mark Twain','frase' : 'Il segreto per andare avanti è iniziare.'}]
@app.route('/')
def home():
 return render_template('index3.html')

@app.route('/meteo')
def meteo():
  i = random.randint(0,9)
  if i < 2:   
    meteo = "PIOVOSO"
    immagine ='static/pioggia.jpg'
  elif i < 5:
    meteo = "NUVOLOSO"
    immagine ='static/nuvole.jpg'
  else:
    meteo = "SOLEGGIATO"
    immagine ='static/sole.jpg'
  return render_template('meteo.html',meteo=immagine,testo='Le previsioni indicano che il tempo è: '+ meteo)

@app.route('/frasicelebri')
def frasi():
  i = random.randrange(0,len(frasilst))
  return render_template('frasi.html',frase = frasilst[i]['frase'],autore = frasilst[i]['autore'])

@app.route('/quantomanca')
def tempo_mancante():
  oggi = datetime.now()
  finescuola = datetime(2022, 6, 8)
  data = (finescuola - oggi).days
  return render_template('calendario.html',testo='Mancano'+' '+str(data)+' '+'giorni alla fine della scuola')


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3001, debug=True)