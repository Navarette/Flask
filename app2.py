#realizzare un server web che visualizzi l'ora e colori lo sfondo in base all'orario:un colore per la mattina,uno per il pomeriggio,uno per la sera ,e uno per la notte
from flask import Flask, render_template 
app = Flask(__name__)
from datetime import datetime

@app.route('/')
def time():
    now = datetime.now().hour + 1
    if now < 7:
       return   render_template("index2.html", color="yellow",testo='È notte,sono le: ' + str(now))
    elif now < 13:
      return render_template("index2.html", color="red",testo= 'È mattino,sono le: ' +str(now))
    elif now < 18:
      return  render_template("index2.html", color="orange",testo= 'È pomeriggio,sono le: ' +str(now))
    else:
       return render_template("index2.html", color="blue",testo= 'È sera,sono le: ' + str(now))

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3001, debug=True)