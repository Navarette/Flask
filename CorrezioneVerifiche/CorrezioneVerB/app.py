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
# pip install flask geopandas matplotlib contextily pandas

stazioniRadio = gpd.read_file('/workspace/Flask/CorrezioneVerB/static/ds710_coordfix_ripetitori_radiofonici_milano_160120_loc_final.geojson')
quartieri = gpd.read_file('/workspace/Flask/CorrezioneVerB/static/ds964_nil_wm-20220406T112003Z-001.zip')

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/elenco", methods=["GET"])
def elenco(): 
    #crea una variabile contenente i quartieri in ordine alfabetico  
    quartiere_scelta = quartieri.NIL.sort_values()
    return render_template("elenco.html",quartiere = quartiere_scelta )

@app.route("/stazioniquartiere", methods=["GET"])
def stazioniquartiere():
    #controlla cosa l'utente ha selezionato
    quartiere = request.args['quartiere']
    #controlla se il quartiere selezionato è uguale a un quartiere esistente
    quartiereUtente = quartieri[quartieri.NIL.str.contains(quartiere)]
    #controlla se ci sono stazioni radio nel quartiere scelto attraverso la sua geometria
    stazioniquartiere = stazioniRadio[stazioniRadio.within(quartiereUtente.geometry.squeeze())]

    return render_template("risultato.html",risultato=stazioniquartiere.to_html())

# ES 2
@app.route("/input", methods=["GET"])
def input():
    
    return render_template('input.html')

@app.route("/ricerca", methods=["GET"])
def ricerca():
    #dichiarazione globale di due variabili
    global stazioniQuartiere ,quartiere
    #controlla quello che l'utente ha inserito nella textbox
    nomeQuar = request.args['quartiere']
    #cerca nel dataframe quartieri il quartiere corrispondente al quartiere inserito dall'utente 
    quartiere = quartieri[quartieri.NIL.str.contains(nomeQuar)]
    #controlla i quartieri che intersecano con il geodataframe stazionigeo
    stazioniQuartiere = stazioniRadio[stazioniRadio.intersects(quartiere.geometry.squeeze())]
    
    return render_template('elenco1.html')

@app.route("/mappa", methods=["GET"])
def mappa():
    
    fig, ax = plt.subplots(figsize = (12,8))

    stazioniQuartiere.to_crs(epsg=3857).plot(ax=ax,color='black')
    quartiere.to_crs(epsg=3857).plot(ax=ax,alpha=0.3,edgecolor='k')
    contextily.add_basemap(ax=ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    FigureCanvas(fig).print_png(output)
    
    return Response(output.getvalue(), mimetype='image/png')

# ES 3
@app.route("/numero", methods=["GET"])
def numero():
    global risultato
#numero stazioni per ogni municipio
    risultato = stazioniRadio.groupby('MUNICIPIO')['OPERATORE'].count().reset_index()

    return render_template("elenco3.html",risultato=risultato.to_html())

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
  app.run(host='0.0.0.0', port=1234, debug=True)