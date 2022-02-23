from flask import Flask, render_template 
app = Flask(__name__)
import random
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
 return render_template()

@app.route('/quantomanca')
def tempo_mancante():
 return render_template()


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3001, debug=True)