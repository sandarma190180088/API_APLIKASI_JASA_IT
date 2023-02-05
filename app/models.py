from app import db
from datetime import datetime
import json


class User(db.Model):
    __tablename__ = 'tb_user'
    id = db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String,nullable=False,unique=True)
    password = db.Column(db.String,nullable=False)
    role = db.Column(db.String,nullable=False)

    data = db.Column(db.Text)
    def __repr__(self) -> str:
        return f'<username : {self.username}>'

    @classmethod
    def get_by_name(cls,username):
        q = cls.query.filter_by(username=username).first()

        data ={
                'username':q.username,
                'role':q.role,
                'data':json.loads(q.data)
        }
        return data
    
    @classmethod
    def get_dataJsonId(cls,id):
        q = cls.query.get_or_404(id)
        data ={
            'username':q.username,
            'role':q.role,
            'data':json.loads(q.data)
        }
        return data

    @classmethod
    def get_dataJson(cls):
        q = cls.query.all()
        data = []
        for i in q:
            v ={
                'id':i.id,
                'username':i.username,
                'role':i.role,
                'data':json.loads(i.data)
            }
            data.append(v)
        return data
    @classmethod
    def post_data(cls,id,data):
        data = json.dumps(data)
        q =  User.query.filter_by(id=id).first()
        q.data = data
        
    def save(self):
        db.session.add(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()



class Produk(db.Model):
    __tablename__ = 'tb_produk'
    id = db.Column(db.Integer,primary_key=True)
    kode_produk = db.Column(db.String,nullable=False,unique=True)
    # Jenis Produk ada 3 yaitu (MD,WD,UI/UX/)
    jenis_produk = db.Column(db.String,nullable=False)
    data  = db.Column(db.Text)

    @classmethod
    def get_dataJson(cls):
        q = cls.query.all()
        data = []
        for i in q:
            v = {
                'kode_produk':i.kode_produk,
                'jenis_produk':i.jenis_produk,
                'data':json.loads(i.data)
            }
            data.append(v)
        return data
    @classmethod
    def get_dataJsonByKode(cls,kode_produk):
        q = cls.query.filter_by(kode_produk=kode_produk).first()
        v = {
            'kode_produk':q.kode_produk,
            'jenis_produk':q.jenis_produk,
            'data':json.loads(q.data)
        }
        
        return v
    def __repr__(self) -> str:
        return f'<kode produk : {self.kode_produk}>'

    
class Transaksi(db.Model):
    __tablename__ = 'tb_transaksi'
    id = db.Column(db.Integer,primary_key=True)
    resi = db.Column(db.String,nullable=False)
    status = db.Column(db.String,nullable=False)
    created_at = db.Column(db.DateTime,default=datetime.now())
    data = db.Column(db.Text,nullable=False)

    def __repr__(self) -> str:
        return self.resi



class Chat(db.Model):
    __tablename__ = 'tb_chat'
    id = db.Column(db.Integer,primary_key=True)
    kode_produk = db.Column(db.String,nullable=False)
    from_chat = db.Column(db.String,nullable=False)
    to_chat = db.Column(db.String,nullable=False)
    data = db.Column(db.Text)





 




