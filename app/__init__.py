from flask import Flask,request,jsonify,make_response,redirect,session
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api,Resource
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from config import Config
import jwt
from functools import wraps
from werkzeug.security import generate_password_hash,check_password_hash




app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
api = Api(app)
ma = Marshmallow(app)


migrate = Migrate(app,db)

def token_required(func=None):
    @wraps(func)
    def wrapper(*args,**kwargs):
        _ = func(*args,**kwargs)
        token = session.get('token')
        if not token :
            return make_response(
                jsonify(
                    {'msg':'token tidak ada !'},404
                )
            )
        else:
            try:
                output = jwt.decode(token,app.config['SECRET_KEY'],algorithms=['HS256']
                )
                print(output)
                print(request.user_agent)
                
                return _
            
            except Exception as e:
                return make_response(jsonify(
                    {
                        "output":f'{e}'
                    }
                ),404)
    return wrapper

from app.models import *
from app.schema import *
from app.restAPi import user,transaksi,product



