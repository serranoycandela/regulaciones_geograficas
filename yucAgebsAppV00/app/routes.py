# Importamos el objeto app, las funciones de flask  así como las formas y
# modelos de la aplicación

from app import app
from .models import *

from flask import render_template,jsonify, redirect, url_for, request, Response, make_response, send_file

import geoalchemy2,shapely
from geoalchemy2.shape import to_shape

from shapely.geometry import shape
import geopandas as gpd
import matplotlib.pyplot as plt
import json
from sqlalchemy import func
import requests

# Esta url redirecciona a la URL dibuja_poligono
@app.route('/', methods=['GET'])
def home():
    return redirect(url_for('inicio'))

@app.route('/inicio', methods=['GET','POST'])
def inicio():
    return render_template('index.html')


@app.route('/getfile', methods=['GET','POST'])
def getfile():
    if request.method == 'POST':

        # for secure filenames. Read the documentation.
        file = request.files['myfile']
        mipoligono=gpd.read_file(file)

        poligono_shp={"Poligono_shp":shapely.geometry.geo.mapping(mipoligono.iloc[0,0])}

        poligono_dict={"type": "Feature",
                        "properties":{"id":"01"},
                    "geometry":{"type":"Polygon",
                    "coordinates":poligono_shp["Poligono_shp"]["coordinates"]},
                    }

        return render_template('prueba.html',gjson=json.dumps(poligono_dict))

    return render_template('prueba.html',gjson=jsonify(poligono_dict))
