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

def area_interseccion(ageb, poligono):
    # Geometría de la intersección del polígono de entrada con el ageb
    interseccion=session.scalar(ageb.geom.ST_Intersection(WKTElement(str(shape(poligono)), srid=4326)))
    # Convertimos la geometría de la intersección en formato WKTElement
    interseccion_wkte=WKTElement(str(to_shape(interseccion)),srid=4326)
    # Obtenemos el área de la geometría de la interseccion
    area_interseccion=session.scalar(select([func.ST_Area(func.ST_Transform(interseccion_wkte,4486))]))

    return area_interseccion

def area_poligono(ageb):
    # Obtenemos el área de ageb
    area_ageb=session.scalar(ageb.geom.ST_Transform(4486).ST_Area())

    return area_ageb

@app.route('/', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_api():
        return redirect('/fomix/api/v0.1')

@app.route('/fomix/api/v0.1/interseccion/<string:poligono>', methods=['GET'])
def interseccion(poligono):

        # Convertimos el string recibido del polígono en un diccionario
        poligono = json.loads(poligono)

        # Realizamos la consulta con geoalchemy2
        query= session.query(TbDbagebsyucatan).filter(TbDbagebsyucatan.geom.ST_Intersects(WKTElement(str(shape(poligono)), srid=4326)))

        # Iteramos sobre los agebs que hace intersección el polígono recibido
        for unidad in query:
            # Imprimimos la cvegeo y la clave de la ageb
            print(unidad.cvegeo+"  "+unidad.cve_ageb)
            # Imprimimos el área del ageb
            #print(session.scalar(unidad.geom.ST_Transform(4486).ST_Area()))
            # Geometría de la intersección de polígono de entrada con el ageb
            #interseccion=session.scalar(unidad.geom.ST_Intersection(WKTElement(str(shape(poligono)), srid=4326)))
            #area_interseccion=session.scalar(select([func.ST_Area(func.ST_Transform(WKTElement(str(to_shape(session.scalar(unidad.geom.ST_Intersection(WKTElement(str(shape(poligono)), srid=4326))))),srid=4326),4486))]))
            #print(str(area_interseccion/session.scalar(unidad.geom.ST_Transform(4486).ST_Area())))
        # Convertimos la geometría de los agebs y los almacenamos en un diccionario
        geoms = {ageb.cvegeo:shapely.geometry.geo.mapping(to_shape(ageb.geom)) for ageb in query}

        # Iteramos sobre la consulta de las intersecciones del polígono con las agebs para generar un diccionario,
        # el cual se regresará en formato geojson en la consulta REST
        agebs = [{"type": "Feature",
            "properties":{"cvegeo":ageb.cvegeo,
                          "area":round(area_poligono(ageb),2),
                          "area_interseccion": round(area_interseccion(ageb, poligono),2),
                          "porcentaje_interseccion": round((area_interseccion(ageb, poligono)/area_poligono(ageb))*100,4)
                          },
            "geometry":{"type":"MultiPolygon",
            "coordinates":geoms[ageb.cvegeo]["coordinates"]},
            } for ageb in query]


        return jsonify({"type": "FeatureCollection","features":agebs})
@app.route('/fomix/api/v0.1/municipios/coneval/<anio>/<indicador>', methods=['GET'])
def municipios(anio,indicador):
        # Realizamos una consulta de la cvegeo y la geometría de los municipios de Yucatán
        muni_yucatan = pd.read_sql(session.query(TbMunicipiosyucatan.cvegeo,TbMunicipiosyucatan.geom).statement,session.bind)

        # Convertimos la geometría de los municipios
        muni_yucatan['geom'] = muni_yucatan['geom'].apply(lambda x: shapely.geometry.geo.mapping(to_shape(x)))

        # Realizamos una consulta para obtener la tabla tb_yuc_coneval
        coneval_yuc = pd.read_sql(session.query(t_tb_yuc_coneval).filter(t_tb_yuc_coneval.c.anio==anio,t_tb_yuc_coneval.c.indicador==indicador).statement,session.bind)
        print(coneval_yuc)
        # Hacemos un left join para agregar la geometría a coneval_yuc
        coneval_yuc_geom = pd.merge(left=coneval_yuc, right=muni_yucatan, how='left', left_on='cvegeo', right_on='cvegeo')

        # Nos quedamos con la geometría del polígono del municipio
        coneval_yuc_geom['geom'] = coneval_yuc_geom['geom'].apply(lambda x: x['coordinates'])

        # Iteramos sobre la reunión para generar un diccionario el cual se regresará en formato geojson en la consulta REST
        coneval_yuc_dict = [{"type": "Feature",
            "properties":{"cvegeo": row['cvegeo'],
                          "anio": row['anio'],
                          "indicador": row['indicador'],
                          "valor_indicador": row['valor_indicador']
                          },
            "geometry":{"type":"MultiPolygon",
            "coordinates":row['geom']},
            } for index, row in coneval_yuc_geom.iterrows()]

        return jsonify({"type": "FeatureCollection","features":coneval_yuc_dict})
