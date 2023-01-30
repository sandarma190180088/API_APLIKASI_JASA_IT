from flask import Flask,request,jsonify,make_response,redirect,session
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api,Resource
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from config import Config
import jwt
from functools import wraps


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
api = Api(app)
ma = Marshmallow(app)


migrate = Migrate(app,db)

from app.models import *
from app.schema import *
from app.api import *



