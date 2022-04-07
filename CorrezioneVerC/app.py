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

# ES 1
@app.route("/numero", methods=["GET"])
def numero():
    return render_template('elenco.html')

@app.route("/ricerca", methods=["GET"])
def ricerca():
    global lunghezzautente
    linea =  min(request.args["val1"], request.args["val2"])
    linea1 =  max(request.args["val1"], request.args["val2"])
    linee_distanza = tram[(tram["lung_km"] > linea) & (tram["lung_km"] < linea1)].sort_values("linea")
    return  render_template('risultato.html',risultato=linee_distanza.to_html())

# ES 2
@app.route("/input", methods=["GET"])
def input():
    return render_template('input.html')

@app.route("/ricerca1", methods=["GET"])
def ricerca1():
    #dichiarazione globale di due variabili
    global stazioniQuartiere ,quartiere
    #controlla quello che l'utente ha inserito nella textbox
    nomeQuar = request.args['quartiere']
    #cerca nel dataframe quartieri il quartiere corrispondente al quartiere inserito dall'utente 
    quartiere = quartieri[quartieri.NIL.str.contains(nomeQuar)]
    #controlla i quartieri che intersecano con il geodataframe stazionigeo
    tramQuar = tram[tram.intersects(quartiere.geometry.squeeze())]
    
    return render_template('elenco1.html',risultato = tramQuar.to_html())

# ES 3
@app.route("/dropdown", methods=["GET"])
def dropdown():
    linea = tram.linea.to_list()
     
    linea = list(set(linea))
    
    linea.sort()

    return render_template('dropdown.html',linee=linea)

@app.route("/sceltalinea", methods=["GET"])
def sceltastazione():
    global quartiere1,lineaUtente
   
    linea = request.args['linea']  
    
    lineaUtente = tram[tram.linea== linea] 

    quartiere1 = quartieri[quartieri.contains(lineaUtente.geometry.squeeze())]

    return render_template('sceltalinea.html')

@app.route("/mappaquar", methods=["GET"])
def mappaquar():
    fig, ax = plt.subplots(figsize = (12,8))

    lineaUtente.to_crs(epsg=3857).plot(ax=ax,color='black')
    quartiere1.to_crs(epsg=3857).plot(ax=ax,alpha=0.3,edgecolor='k')
    contextily.add_basemap(ax=ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    FigureCanvas(fig).print_png(output)
    
    return Response(output.getvalue(), mimetype='image/png')


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=1234, debug=True)