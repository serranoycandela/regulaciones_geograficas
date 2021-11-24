# Importamos el objeto app, las funciones de flask y el modelo
from app import app
from flask import render_template,jsonify, redirect, url_for, request, Markup
from .models import *
import geoalchemy2,shapely
from geoalchemy2.shape import to_shape
from flask_cors import CORS, cross_origin
from shapely.geometry import shape
import json
from sqlalchemy import func
import shapely.wkt
from geoalchemy2.elements import WKTElement

from sqlalchemy import create_engine, select, func
from geoalchemy2 import functions  # NOQA

import pandas as pd
import geojson
from utm_zone import epsg


def area_interseccion(ageb, poligono,utm):
    # Geometría de la intersección del polígono de entrada con el ageb
    interseccion=session.scalar(ageb.geom.ST_Intersection(WKTElement(str(shape(poligono)), srid=4326)))
    # Convertimos la geometría de la intersección en formato WKTElement
    interseccion_wkte=WKTElement(str(to_shape(interseccion)),srid=4326)
    # Obtenemos el área de la geometría de la interseccion
    area_interseccion=session.scalar(select([func.ST_Area(func.ST_Transform(interseccion_wkte,utm))]))/10000

    return area_interseccion

def area_poligono(f,utm):
    # Obtenemos el área de ageb
    
    area_f = session.scalar(f.geom.ST_Transform(utm).ST_Area())/10000

    return area_f

def get_UTM_from_WKT(wkt):
    g1 = shapely.wkt.loads(wkt)
    g2 = geojson.Feature(geometry=g1, properties={})
    return epsg(g2)


@app.route('/', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_api():
        return redirect('/fomix/api/v0.1')

@app.route('/fomix/api/v0.1/interseccion/<string:poligono>', methods=['GET'])
def interseccion(poligono):

        # Convertimos el string recibido del polígono en un diccionario
        poligono = json.loads(poligono)

        # Realizamos la consulta con geoalchemy2
        query= session.query(UgasLineamiento).filter(UgasLineamiento.geom.ST_Intersects(WKTElement(str(shape(poligono)), srid=4326)))

        geoms = {uga.id_uga:shapely.geometry.geo.mapping(to_shape(uga.geom)) for uga in query}
        poligono_wkt = WKTElement(str(shape(poligono)), srid=4326)
        utm = get_UTM_from_WKT(poligono_wkt.desc)
        area_poligono_wkt = session.scalar(select([func.ST_Area(func.ST_Transform(poligono_wkt,utm))]))/10000
        #print(type(poligono_wkt).__name__)
        # Iteramos sobre la consulta de las intersecciones del polígono con las agebs para generar un diccionario,
        # el cual se regresará en formato geojson en la consulta REST
        ugas = [{"type": "Feature",
            "properties":{"clave_uga":uga.clave_uga,
                          "lineamiento_uga":uga.lineamiento_uga,
                          "area_uga":round(area_poligono(uga, utm), 1),
                          "area_poligono":round(area_poligono_wkt, 1),
                          "area_interseccion": round(area_interseccion(uga, poligono, utm),1),
                          "porcentaje_interseccion": round((area_interseccion(uga, poligono, utm)/area_poligono_wkt)*100, 1)
                          },
            "geometry":{"type":"MultiPolygon",
            "coordinates":geoms[uga.id_uga]["coordinates"]},
            } for uga in query]


        return jsonify({"type": "FeatureCollection","features":ugas})



