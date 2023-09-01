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

quartieri = gpd.read_file('/workspace/Flask/Navarette.es5/templates/ds964_nil_wm-20220322T104418Z-001 (1).zip')


@app.route('/', methods=['GET'])
def home_page():

    return render_template('home1.html')

@app.route('/quartieri.png', methods=['GET'])
def plot_png():

    fig, ax = plt.subplots(figsize = (12,8))

    imgUtente.to_crs(epsg=3857).plot(ax=ax, alpha=0.5,edgecolor='k')
    contextily.add_basemap(ax=ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/quartieri', methods=("POST", "GET"))
def mpl():

    global imgUtente

    qrt = request.args['quartiere']
    imgUtente = quartieri[quartieri['NIL']==qrt]

    return render_template('risultato2.html',PageTitle = "Matplotlib")

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)