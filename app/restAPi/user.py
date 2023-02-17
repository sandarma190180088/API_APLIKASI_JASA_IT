from app import (
    app,
    Resource,
    request,
    User,Produk,
    check_password_hash,
    generate_password_hash,
    jwt,datetime,
    session,
    token_required,
    json,
    db,
    api,
    make_response,jsonify,
    qData
)
import datetime
from flask_restful import reqparse

parser = reqparse.RequestParser()

parser.add_argument('username',type=str,location='args',help='username Cannot be blank !')




class Login(Resource):
    def get(self):
        return {'msg':"gunakan method POST untuk login"},400
        
    def post(self):
        username = request.form['username']
        password = request.form['password']
        if username and password:
            login = User.login(username=username,password=password)
            
            if login['status']:
                token = jwt.encode(
                {
                    "username":username,
                    "exp":datetime.datetime.utcnow()+datetime.timedelta(days=1)
                },app.config['SECRET_KEY'],algorithm="HS256"

                )
                session.clear()
                session['token']= token
                session['username'] = username
                return {"msg":"berhasil Login",'token':token},200
            else:
                return {'msg':login['msg']},404
        else:
            return {'msg':'gagal Login'},400
        



class User_(Resource): 
    @token_required
    def get(self):
        args = parser.parse_args()
        username = args.get('username')
        if username == 'all':
            q = User.get_dataJson()
            return q,200
        try:
            q = User.get_by_name(username=username)
            return q,200
        except Exception:
            return {'msg':'username tidak ada !'},404

    def post(self):
        username = request.form['username'].replace(' ','').lower()
        password = request.form['password']
        role = request.form['role']
        data  = json.dumps({})
        pas_g = generate_password_hash(password)
        try :
            q = User(username=username,password=pas_g,role=role,data=data)
            db.session.add(q)
            db.session.commit()
            return {'msg':'success !','status':True},200
        except Exception as e:
            return {'msg':f'{e}','status':False},404
    @token_required
    def delete(self):
        args = parser.parse_args()
        username = args['username']
        if username == 'all':
            q = User.query.delete()
            db.session.commit()
            session.clear()
            return {'msg':'all deleted !'},200
        try:
            u = User.query.filter_by(username=username).first()
            if username == session.get('username'):
                session.clear()
            db.session.delete(u)
            db.session.commit()
            return {'msg':'success deleting !'},200
        except Exception as e:
            return {'msg':str(e)},400





class UserData(Resource):
    def get(self):
        username = session.get('username')
        if not username:
            return {'msg':'Username anda tidak ada mohon login terlebih dahulu'},404
        q = User.query.filter_by(username=username).first()
        data = json.loads(q.data)
        if 'dataPersonal' not in data:
            return {'msg':'data anda kosong ! mohon mengisi data anda menggunakan method POST !'},404
        return data,200
    
    def post(self):
        username = session.get('username')
        if not username:
            return {'msg':'Username anda tidak ada mohon login terlebih dahulu'},404
        parser.add_argument('data',type=dict,location='get_json',help='data cannot is blank !')
        args = parser.parse_args()
        data = args['data']
        obj = qData(username=username)
        s = obj.postData(data=data,query='dataPersonal')        
        return s,s['http_code']
    
    def put(self):
        username = session.get('username')
        if not username:
            return {'msg':'Username anda tidak ada mohon login terlebih dahulu'},404
        parser.add_argument('data',type=dict,location='get_json',help='data cannot is blank !') 
        args = parser.parse_args()
        data =  args['data']
        obj = qData(username=username)
        s = obj.putData(data=data,query='dataPersonal')
        return s,s['http_code']
    def delete(self):
        username = session.get('username')
        if not username:
            return {'msg':'Username anda tidak ada, mohon login terlebih dahulu'},404
        try:
            q = User.query.filter_by(username=username).first()
            data = json.loads(q.data)
            if 'dataPersonal' in data:
                del data['dataPersonal']
                q.data = json.dumps(data)
                db.session.commit()
                return {'msg':'succes deleted !'},200
            else:
                return {'msg':'data Pribadi anda tidak ada !'},404
        except Exception as e:
            return {'msg':str(e)},400

    
                
                
                
            


@app.route('/api/logout',methods=['GET','POST'])
def logout():
    session.clear()
    return make_response(jsonify({
        'msg':'anda sudah keluar'
    }),200)





class CekCurrentUser(Resource):
    def get(self):
        username = session.get('username')
        if username:
            return {'username':username},200
        else:
            return {'msg':'username anda tidak ada !'},404
# API Route
api.add_resource(Login,'/api/login') 
api.add_resource(User_,'/api/user')
api.add_resource(UserData,'/api/user/data/')
api.add_resource(CekCurrentUser,'/api/user/cek')
