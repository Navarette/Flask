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
    immagine ='static/pioggia.jfif'
  elif i < 5:
    immagine ='static/nuvoloso.jfif'
  else:
    immagine ='static/sole.jfif'
  return render_template('meteo.html',meteo=immagine)

@app.route('/frasicelebri')
def frasi():
  i = random.randrange(0,len(frasilst))
  return render_template('frasi.html',frase = frasilst[i]['frase'],autore = frasilst[i]['autore'])

@app.route('/quantomanca')
def tempo_mancante():
  oggi = datetime.now()
  finescuola = datetime(2022, 6, 8)
 
  return render_template('calendario.html',data = (finescuola - oggi).days)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3001, debug=True)