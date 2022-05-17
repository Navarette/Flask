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

comuni = gpd.read_file('/workspace/Flask/CorrezioneVerA2/static/Com01012021_g-20220419T124103Z-001.zip')

# ES1
@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/selezione", methods=["GET"])
def selezione():
    scelta = request.args['scelta']

    if scelta == 'es1':
        return redirect(url_for('input'))
    elif scelta == 'es2':
        return redirect(url_for('dropdown'))
    else:
        return redirect(url_for('dropdown1'))

@app.route("/input", methods=["GET"])
def input():  
    return render_template('input.html')

@app.route("/ricerca", methods=["GET"])
def ricerca():
    global comuneUtente
    nomeCom = request.args['comune']
    comuneUtente = comuni[comuni['COMUNE'] == nomeCom]
    comunilimitrofi = comuni[comuni.touches(comuneUtente.geometry.squeeze())]
    area = comuneUtente.geometry.area
    return render_template('elenco.html',risultato=comunilimitrofi.to_html(),area=area)

@app.route("/mappa", methods=["GET"])
def mappa():
    
    fig, ax = plt.subplots(figsize = (12,8))

    comuneUtente.to_crs(epsg=3857).plot(ax=ax,edgecolor='black',facecolor='none')
    comuni.to_crs(epsg=3857).plot(ax=ax,alpha=0.3,edgecolor='k')
    contextily.add_basemap(ax=ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    FigureCanvas(fig).print_png(output)
    
    return Response(output.getvalue(), mimetype='image/png')



if __name__ == '__main__':
  app.run(host='0.0.0.0', port=1235, debug=True)