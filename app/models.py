from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'tb_user'
    id = db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String,nullable=False)
    password = db.Column(db.String,nullable=False)
    role = db.Column(db.String,nullable=False)

    data = db.Column(db.String,nullable=False)
    def __repr__(self) -> str:
        return f'<username : {self.username}>'

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls,id):
        return cls.query.get_or_404(id)
    @classmethod
    def get_by_name(cls,username):
        return cls.query.filter_by(username=username).first()
    def save(self):
        db.session.add(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Produk(db.Model):
    __tablename__ = 'tb_produk'
    id = db.Column(db.Integer,primary_key=True)
    kode_produk = db.Column(db.Integer,nullable=False,unique=True)
    jenis_produk = db.Column(db.String,nullable=False)
    data  = db.Column(db.String)

    def __repr__(self) -> str:
        return f'<kode produk : {self.kode_produk}>'
class Transaksi(db.Model):
    __tablename__ = 'tb_transaksi'
    id = db.Column(db.Integer,primary_key=True)
    resi = db.Column(db.String,nullable=False)
    status = db.Column(db.String,nullable=False)
    created_at = db.Column(db.DateTime,default=datetime.now())
    data = db.Column(db.String,nullable=False)

 




