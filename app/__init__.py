from flask import Flask
from flask_cors import CORS, cross_origin

app = Flask(__name__)

conn_string = 'postgresql://usuario:clave@localhost:5432/dbagebsyucatan'
app.config['SQLALCHEMY_DATABASE_URI'] = conn_string
app.config['SECRET_KEY'] = "SECRET_KEY"

CORS(app, support_credentials=True)


from app import views
