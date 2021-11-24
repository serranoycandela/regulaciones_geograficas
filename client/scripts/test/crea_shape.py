import geopandas
from geopandas import GeoSeries
from shapely.geometry import Polygon
p1 = Polygon([(-99.06827,19.392125), (-99.053679,19.380385), (-99.042263,19.382733),(-99.06827,19.392125)])
g = GeoSeries(p1)
g.crs = "EPSG:4326"
g.to_file("poligono_prueba.shp")
g.to_file("poligono_prueba.geojson", driver='GeoJSON')
