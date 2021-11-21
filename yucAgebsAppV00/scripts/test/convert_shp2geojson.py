import geopandas as gpd
import geoalchemy2,shapely
from flask import jsonify
from shapely.geometry import shape

mipoligono=gpd.read_file('poligono_prueba.shp')


poligono_shp={"Poligono_shp":shapely.geometry.geo.mapping(mipoligono.iloc[0,1])}

poligono_dict={"type": "Feature",
            "geometry":{"type":"Polygon",
            "coordinates":poligono_shp["Poligono_shp"]["coordinates"]},
            }
poligono_dict
