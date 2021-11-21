# Servicio REST de información geográfica

Se desarrolla una aplicación  REST(Representational State Transfer) en el framework Flask de Python que sirve datos geográficos en formato GeoJSON. Usamos el ORM GeoAlchemy.

La aplicación sirve datos a nivel ageb y municipio para el estado de Yucatán. Para el nivel de ageb, el cliente envía en la petición al servidor un campo en el que especifica el las geometría de un poligono de interés. El servidos regresa la los agebs que hacen intersección con la geometría de polígono así como infomación relacionada con el porcentaje del area de intersección. Un ejemplo de solicitud es la siguiente:

```
localhost:4000/fomix/api/v0.1/interseccion/POLYGON ((-99.05746600000001 19.388907, -99.054934 19.387227, -99.055148 19.389686, -99.05746600000001 19.388907))
```
Para el caso de datos a nivel municipal, el campo de la solicitud es algún indicador particular (e.g., indicadores de rezago social) y el año. Por ejemplo

```
localhost:4000/fomix/api/v0.1/municipios/coneval/2010/nopob_novul
```
## Configuación de la base de datos 

El manejador de bases de datos que se utiliza el Postgres y su extención PostGIS, que nos permite realizar consultas geográficas. 

 Creamos  la base de datos ```dbagebsyucatan```

```
 CREATE DATABASE dbagebsyucatan;
```

 Incorporamos la extensión PostGIS

```
 CREATE EXTENSION  postgis;
```
Usamos el comando ```shp2pgsql``` para generar el archivo SQL del shapefile de los agebs de Yucatán. Podemos usar a opción -G para generar una tabla espacial de PostGIS que use el tipo geography y -I para generar el índice espacial de la columna geometric:

```
 shp2pgsql -G -I 31a.shp tb_dbagebsyucatan > dbagebsyucatan.sql
```

 Para generar la tabla espacial con el tipo geometry en vez de geography, y para que la columna de geometric se llame ```the_geom```
, usamos el comando:

```
 shp2pgsql -I -g the_geom  31a.shp tb_dbagebsyucatan > dbagebsyucatan.sql
```

 Para agregar el sistema de referencia usamos la opción -s. El siguiente comando es el que finalmente utilizamos:
 
```
 shp2pgsql -I -s 4326  31a.shp tb_dbagebsyucatan > dbagebsyucatan.sql
```

 Si está interesado en las distintas opciones del comando shp2pgsql vea la liga https://manpages.debian.org/stretch/postgis/shp2pgsql.1.en.html

 Se ejecuta  el script:

```
 psql -U postgres -d dbagebsyucatan -a -f dbagebsyucatan.sql
```

 Para generar nuestro ORM de ORM GeoAlchemy, usamos el siguiente comando :
 
```
  sqlacodegen postgresql://usuario:clave@localhost/dbagebsyucatan --outfile dbagebsyucatan.py
```
Repetimos los mismos paso para el shapefile de municipios.

Creamos la tabla que albergará los datos de rezago social a nivel municipal

```
CREATE TABLE tb_yuc_coneval
(
  cvegeo VARCHAR(5),
  anio integer,
  indicador VARCHAR(100),
  valor_indicador double precision
  );

  \copy tb_yuc_coneval(cvegeo,anio,indicador,valor_indicador) FROM '/tmp/yuc_coneval_10_15.csv' DELIMITERS ',' CSV HEADER;
```
