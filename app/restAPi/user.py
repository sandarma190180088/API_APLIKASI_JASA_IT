from app import (
    app,
    Resource,
    request,
    User,
    check_password_hash,
    generate_password_hash,
    jwt,datetime,
    session,
    token_required,
    users_schema,
    user_schema,
    json,
    db,
    api,
    make_response,jsonify
)
import datetime



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
                        "exp":datetime.datetime.utcnow()+datetime.timedelta(days=1)
                    },app.config['SECRET_KEY'],algorithm="HS256"

                    )
                    session['token']= token
                    session['username'] = u.username
                    return {"msg":"berhasil Login",'token':token},200
                else:
                    return {'msg':'password anda salah ! '},404
                
            else :

                return {'msg':'username anda tidak ditemukan'},404
        else:
            return {'msg':'gagal Login'},400



class User_(Resource): 
    @token_required
    def get(self):
        q = User.get_all()
        return users_schema.dump(q),200
    def post(self):
        username = request.form['username']
        password = request.form['password']
        role = ''
        data  = json.dumps({})
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
        u = User.get_by_id(id)
        username = session.get('username')
        if id :
            try:
                u = User.get_by_id(id)
                u.delete()
                if u.username == username:
                    session.clear()
                return {'msg':'succes deleted !','u':username},200

            except Exception as e:
                return {'msg':'id anda tidak ditemukan !'},404
        else:
            return {'msg':'isi id anda'},400



class UserData(Resource):
    def get(self,id):
        q = User.get_data(id)
        return {'data':q},200
    def post(self,id):
        try:
            q = User.query.filter_by(id=id).first()
            data = json.loads(q.data)
            nama_lengkap = request.form['nama_lengkap']
            nip = request.form['nip']
            alamat = request.form['alamat']
            no_telp = request.form['no_telp']
            data['dataPersonal'] = {
                'nama_lengkap':nama_lengkap,
                'nip':nip,
                'alamat':alamat,
                'no_telp':no_telp,
            }
            q.data = json.dumps(data)
            db.session.commit()
            return {'msg':'success !'},200
        except Exception as e:
            return {'msg':str(e)},400
@app.route('/api/logout')
def logout():
    session.clear()
    return make_response(jsonify({
        'msg':'anda sudah keluar'
    }),200)

# API Route
api.add_resource(Login,'/api/login') 
api.add_resource(User_,'/api/user')
api.add_resource(UserData,'/api/user/data/<id>')