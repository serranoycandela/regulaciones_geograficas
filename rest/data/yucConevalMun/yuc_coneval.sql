/*
 Para abrir sesión de postgresql
 sudo -u postgres psql

 Para ejecutar el script
 psql -U postgres -d dbagebsyucatan -a -f yuc_coneval.sql

*/

-- Creamos la tabla que albergará los datos de rezago social a nivel municipal

CREATE TABLE tb_yuc_coneval
(
  cvegeo VARCHAR(5),
  anio integer,
  indicador VARCHAR(100),
  valor_indicador double precision
  );

  \copy tb_yuc_coneval(cvegeo,anio,indicador,valor_indicador) FROM '/tmp/yuc_coneval_10_15.csv' DELIMITERS ',' CSV HEADER;
