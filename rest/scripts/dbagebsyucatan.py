# coding: utf-8
from sqlalchemy import CheckConstraint, Column, Float, Integer, String, Table, Text, text
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.ext.declarative import declarative_base

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
    geom = Column(NullType, index=True)


class TbMunicipiosyucatan(Base):
    __tablename__ = 'tb_municipiosyucatan'

    gid = Column(Integer, primary_key=True, server_default=text("nextval('tb_municipiosyucatan_gid_seq'::regclass)"))
    cvegeo = Column(String(5))
    cve_ent = Column(String(2))
    cve_mun = Column(String(3))
    nomgeo = Column(String(80))
    geom = Column(NullType, index=True)


t_tb_yuc_coneval = Table(
    'tb_yuc_coneval', metadata,
    Column('cvegeo', String(5)),
    Column('anio', Integer),
    Column('indicador', String(100)),
    Column('valor_indicador', Float(53))
)
