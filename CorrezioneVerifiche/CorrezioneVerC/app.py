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

quartieri = gpd.read_file('/workspace/Flask/CorrezioneVerC/static/ds964_nil_wm-20220406T112003Z-001.zip')
linee = gpd.read_file('/workspace/Flask/CorrezioneVerC/static/tpl_percorsi.geojson')

#trafosrma la colonna lung_km in valori float
linee["lung_km"] = linee["lung_km"].astype(float) 
#trasforma la colonna linea in valori integer
linee["linea"] = linee["linea"].astype(int)
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
    return render_template('numero.html')

@app.route("/ricerca", methods=["GET"])
def ricerca():
    #trova il minimo tra il val1 e val2
    linea =  min(float(request.args["val1"]), float(request.args["val2"]))
    #trova il massimo tra il val1 e val2
    linea1 = max(float(request.args["val1"]), float(request.args["val2"]))
    #crea una variabile contenente i percorsi che si trovano tra i valori inseriti prima e li riordina in base alla colonna linea in ordine crescente
    linee_distanza = linee[(linee["lung_km"] > linea) & (linee["lung_km"] < linea1)].sort_values("linea")
    return  render_template('risultato.html',risultato=linee_distanza.to_html())

# ES 2
@app.route("/input", methods=["GET"])
def input():
    return render_template("input.html")

@app.route("/lineequart", methods=["GET"])
def lineequart():
    #controlla cosa l'utente ha inserito nella textbox
    quartiere = request.args["quartiere"]
    #controlla nella colonna 'NIL' il quartiere che corrisponde a quello che l'utente ha inserito
    quartiereUtente = quartieri[quartieri["NIL"].str.contains(quartiere)]
    #controlla nel dataframe 'linee' se qualcosa interseca con la geometria del quartiere inserito dall'utente
    linee_quartiere = linee[linee.intersects(quartiereUtente.geometry.squeeze())].sort_values("linea")
    return render_template("lineequart.html", tabella = linee_quartiere.to_html())

# ES 3
@app.route("/dropdown", methods=["GET"])
def dropdown():
                                           #crea una variabile contenente la colonna linea droppando i duplicati e mettendo in ordine crescente 
    return render_template('dropdown.html',linee = linee["linea"].drop_duplicates().sort_values(ascending=True))

@app.route("/sceltalinea", methods=["GET"])
def sceltastazione(): 
    global lineeUtente
    #controlla quello che l'utente sceglie nel menu a tendina 
    linea = int(request.args["linea"])
    #cerca nel geodataframe 'linee' nella colonna 'linea' quello che corrisponde a quello che l'utente ha selezionato
    lineeUtente = linee[linee["linea"] == linea]

    return render_template('sceltalinea.html',linea = linea)

@app.route("/mappaquar", methods=["GET"])
def mappaquar():

    fig, ax = plt.subplots(figsize = (12,8))

    lineeUtente.to_crs(epsg=3857).plot(ax=ax, edgecolor="k")
    quartieri.to_crs(epsg=3857).plot(ax=ax, alpha=0.5, edgecolor="k")
    contextily.add_basemap(ax=ax)   

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=1234, debug=True)