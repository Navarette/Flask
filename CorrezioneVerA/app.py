from flask import Flask, render_template, send_file, make_response, url_for, Response,request
app = Flask(__name__)

import io
import geopandas as gpd
import contextily
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

stazioni = pd.read_csv('/workspace/Flask/CorrezioneVerA/static/coordfix_ripetitori_radiofonici_milano_160120_loc_final.csv',sep=';')


@app.route("/", methods=["GET"])
def home():
    return render_template("home1.html")

@app.route("/selezione", methods=["GET"])
def selezione():
    scelta = request.args['scelta']
    if scelta == 'es1':
        return redirect(url_for('/num'))
    elif scelta == 'es2':
        return redirect(url_for('/input'))
    else:
        return redirect(url_for('/dropdown'))
        





@app.route("/num", methods=["GET"])
def numero():
    global risultato
#numero stazioni per ogni municipio
    risultato = stazioni.groupby('MUNICIPIO')['OPERATORE'].count().reset_index()

    return render_template("elenco.html",risultato=risultato.to_html())

@app.route("/grafico", methods=["GET"])
def grafico():
    #costruzione del grafico
    fig, ax = plt.subplots(figsize = (5,5))
    x = risultato.MUNICIPIO
    y = risultato.OPERATORE

    ax.bar(x,y,)
    #visualizzazione grafico
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    
    return Response(output.getvalue(), mimetype='image/png')
    




if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)