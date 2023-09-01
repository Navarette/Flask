#realizzare un sito web che restituisca la mappa dei quartieri di milano.
#ci deve essere una home page con un link'quartieri di  Milano':cliccando su questo link si deve visualizzare la mappa dei quartieri di Milano

from flask import Flask, render_template, send_file, make_response, url_for, Response
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

    return render_template('home.html')

@app.route('/quartieri.png', methods=['GET'])
def plot_png():

    fig, ax = plt.subplots(figsize = (12,8))

    quartieri.to_crs(epsg=3857).plot(ax=ax, alpha=0.5)
    contextily.add_basemap(ax=ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/quartieri', methods=("POST", "GET"))
def mpl():
    return render_template('risultato.html',PageTitle = "Matplotlib")

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)