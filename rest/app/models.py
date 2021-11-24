# coding: utf-8
from app import app
# La conexión a la base de datos así como la administración de la sesión
# es administrada con SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Float,CHAR, CheckConstraint,Table, Text, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship

# La columna Geometry es agregada al ORM usando Geometry
from geoalchemy2 import Geometry

# Para conectarse a la base de datos dbagebsyucatan
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()
metadata = Base.metadata


t_geography_columns = Table(
    'geography_columns', metadata,
    Column('f_table_catalog', String),
    Column('f_table_schema', String),
    Column('f_table_name', String),
    Column('f_geography_column', String),
    Column('coord_dimension', Integer),
    Column('srid', Integer),
    Column('type', Text)
)


t_geometry_columns = Table(
    'geometry_columns', metadata,
    Column('f_table_catalog', String(256)),
    Column('f_table_schema', String),
    Column('f_table_name', String),
    Column('f_geometry_column', String),
    Column('coord_dimension', Integer),
    Column('srid', Integer),
    Column('type', String(30))
)


class SpatialRefSy(Base):
    __tablename__ = 'spatial_ref_sys'
    __table_args__ = (
        CheckConstraint('(srid > 0) AND (srid <= 998999)'),
    )

    srid = Column(Integer, primary_key=True)
    auth_name = Column(String(256))
    auth_srid = Column(Integer)
    srtext = Column(String(2048))
    proj4text = Column(String(2048))


class TbDbagebsyucatan(Base):
    __tablename__ = 'tb_dbagebsyucatan'

    gid = Column(Integer, primary_key=True, server_default=text("nextval('tb_dbagebsyucatan_gid_seq'::regclass)"))
    cvegeo = Column(String(13))
    cve_ent = Column(String(2))
    cve_mun = Column(String(3))
    cve_loc = Column(String(4))
    cve_ageb = Column(String(4))
    geom = Column(Geometry('MULTIPOLYGON', srid=4326), index=True)


class TbMunicipiosyucatan(Base):
    __tablename__ = 'tb_municipiosyucatan'

    gid = Column(Integer, primary_key=True, server_default=text("nextval('tb_municipiosyucatan_gid_seq'::regclass)"))
    cvegeo = Column(String(5))
    cve_ent = Column(String(2))
    cve_mun = Column(String(3))
    nomgeo = Column(String(80))
    geom = Column(Geometry('MULTIPOLYGON', srid=4326), index=True)


t_tb_yuc_coneval = Table(
    'tb_yuc_coneval', metadata,
    Column('cvegeo', String(5)),
    Column('anio', Integer),
    Column('indicador', String(100)),
    Column('valor_indicador', Float(53))
)

class Poligonoselect(Base):
    __tablename__ = 'poligonoselect'
    __table_args__ = (
        CheckConstraint("(geometrytype(the_geom) = 'POLYGON'::text) OR (the_geom IS NULL)"),
        CheckConstraint('st_srid(the_geom) = 4326')
    )

    gid = Column(Integer, primary_key=True, server_default=text("nextval('poligonoselect_gid_seq'::regclass)"))
    the_geom = Column(Geometry('POLYGON', srid=4326))

class UgasLineamiento(Base):
    __tablename__ = 'ugas_lineamientos'

    id = Column(Integer, primary_key=True, server_default=text("nextval('ugas_lineamientos_id_seq'::regclass)"))
    geom = Column(Geometry('POLYGON', srid=4326))
    id_uga = Column(Integer)
    clave_uga = Column(String)
    lineamiento_uga = Column(String)