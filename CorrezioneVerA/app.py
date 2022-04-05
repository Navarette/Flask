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

stazioni = pd.read_csv('/workspace/Flask/CorrezioneVerA/static/coordfix_ripetitori_radiofonici_milano_160120_loc_final.csv',sep=';')
stazionigeo = gpd.read_file('/workspace/Flask/CorrezioneVerA/static/ds710_coordfix_ripetitori_radiofonici_milano_160120_loc_final.geojson')
quartieri = gpd.read_file('/workspace/Flask/CorrezioneVerA/static/ds964_nil_wm-20220322T104418Z-001 (1).zip')
@app.route("/", methods=["GET"])
def home():
    return render_template("home1.html")

@app.route("/selezione", methods=["GET"])
def selezione():
    scelta = request.args['scelta']
    if scelta == 'es1':
        return redirect(url_for('numero'))
    elif scelta == 'es2':
        return redirect(url_for('input'))
    else:
        return redirect(url_for('dropdown'))
        


@app.route("/numero", methods=["GET"])
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

@app.route("/input", methods=["GET"])
def input():
    
    return render_template('input.html')

@app.route("/ricerca", methods=["GET"])
def ricerca():
    global stazioniQuartiere ,quartiere
    nomeQuar = request.args['quartiere']
    quartiere = quartieri[quartieri.NIL.str.contains(nomeQuar)]
    stazioniQuartiere = stazionigeo[stazionigeo.intersects(quartiere.geometry.squeeze())]
    
    return render_template('elenco1.html',risultato=stazioniQuartiere.to_html())

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

@app.route("/dropdown", methods=["GET"])
def dropdown():
    nomi_Stazioni = stazioni.OPERATORE.to_list()
    nomi_Stazioni = list(set(nomi_Stazioni))
    nomi_Stazioni.sort()

    return render_template('dropdown.html',stazioni=nomi_Stazioni)

@app.route("/sceltastazione", methods=["GET"])
def sceltastazione():
    global quartiere1,stazioneUtente
    #controlla quello che l'utente ha selezionato nel menu a tendina
    stazione = request.args['stazione']  
    #cerca nel geodataframe la stazionec corrispondente alla stazione selezionata dall'utente
    stazioneUtente = stazionigeo[stazionigeo.OPERATORE== stazione] 
    # 
    quartiere1 = quartieri[quartieri.contains(stazioneUtente.geometry.squeeze())]

    return render_template('vistastazione.html',quartiere = quartiere1)

@app.route("/mappaquar", methods=["GET"])
def mappaquar():
    fig, ax = plt.subplots(figsize = (12,8))

    stazioneUtente.to_crs(epsg=3857).plot(ax=ax,color='black')
    quartiere1.to_crs(epsg=3857).plot(ax=ax,alpha=0.3,edgecolor='k')
    contextily.add_basemap(ax=ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    FigureCanvas(fig).print_png(output)
    
    return Response(output.getvalue(), mimetype='image/png')




if __name__ == '__main__':
  app.run(host='0.0.0.0', port=1234, debug=True)