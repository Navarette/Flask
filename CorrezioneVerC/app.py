from flask import Flask, render_template, send_file, make_response, url_for, Response,request,redirect
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

quartieri = gpd.read_file('/workspace/Flask/CorrezioneVerC/static/ds964_nil_wm-20220406T112003Z-001.zip')
tram = gpd.read_file('/workspace/Flask/CorrezioneVerC/static/tpl_percorsi.geojson')

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/selezione", methods=["GET"])
def selezione():
    scelta = request.args['scelta']
    #in base alla scelta del radio button ti porta a diverse rotte
    if scelta == 'es1':
        return redirect(url_for('numero'))
    elif scelta == 'es2':
        return redirect(url_for('input'))
    else:
        return redirect(url_for('dropdown'))

@app.route("/numero", methods=["GET"])
def numero():
    return render_template('elenco.html')

@app.route("/ricerca", methods=["GET"])
def ricerca():
    global lunghezzautente
    lunghezza = request.args['linea']
    lunghezza1 = request.args['linea']
    lunghezzautente = tram[(tram['linea']>lunghezza)&(tram['linea']<lunghezza1)]
    lunghezzautente = lunghezzautente.sort_values(by='linea',ascending=True)
    return  render_template('risultato.html',risultato=lunghezzautente.to_html())






if __name__ == '__main__':
  app.run(host='0.0.0.0', port=1234, debug=True)