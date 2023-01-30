from app import (api,Resource,request,app,jwt,user_schema,users_schema,db,User,wraps,session,make_response,jsonify
)
import json
from werkzeug.security import generate_password_hash,check_password_hash
import datetime


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





class User_(Resource): 
    @token_required
    def get(self):
        q = User.query.all()
        return users_schema.dump(q),200
    def post(self):
        username = request.form['username']
        password = request.form['password']
        role = 'client'
        data  = {"data":None}
        data = json.dumps(data)
        pas_g = generate_password_hash(password)
        try :
            q = User(username=username,password=pas_g,role=role,data=data)
            db.session.add(q)
            db.session.commit()
            return {'msg':'success !','status':True},200
        except Exception as e:
            return {'msg':f'{e}','status':False},404
    def delete(self):
        id = request.args['id']
        if id :
            try:
                u = User.get_by_id(id)
                u.delete()
                return {'msg':'succes deleted !'},200

            except Exception as e:
                return {'msg':'id anda tidak ditemukan !'},404
        else:
            return {'msg':'isi id anda'},400
                
class Login(Resource):
    def get(self):
        return {'msg':'anda harus login menggunakan method POST'},400
    def post(self):
        username = request.form['username']
        password = request.form['password']
        if username and password:
            u = User.get_by_name(username)
            if u:
                if check_password_hash(u.password,password):
                    token = jwt.encode(
                    {
                        "username":username,
                        "exp":datetime.datetime.utcnow()+datetime.timedelta(minutes=4)
                    },app.config['SECRET_KEY'],algorithm="HS256"

                    )
                    session['token']= token
                    return {"msg":"berhasil Login",'token':token},200
                else:
                    return {'msg':'password anda salah ! '},404
                
            else :

                return {'msg':'username anda tidak ditemukan'},404
        else:
            return {'msg':'gagal Login'},400
        
api.add_resource(User_,'/api')
api.add_resource(Login,'/api/login')
