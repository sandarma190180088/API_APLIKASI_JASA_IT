from app import (
    Produk,
    api,
    request,
    token_required,
    json,
    db,session,
    Resource,User,reqparse
)

parser = reqparse.RequestParser()
parser.add_argument('dataProduct',location='json',type=dict)

class Product_(Resource):
    @token_required
    def get(self):
        q = Produk.get_dataJson()
        return q,200
        
    @token_required
    def post(self):
        args = parser.parse_args()
        try:
            username= session.get('username')
            role = session.get('role')
            if role == '':
                return {'msg':'anda tidak bisa menambahkan produk <role : {}>'.format(role)},400
            dataProduct = args['dataProduct']
            kode_produk = f'{dataProduct["jenis_produk"]}/{username}/{len(dataProduct["nama_produk"])}{len(dataProduct["catatan"])}{len(dataProduct["harga"])}'
            created_by = username

            data = json.dumps(dataProduct)
            
            q = Produk(kode_produk=kode_produk,created_by=created_by,jenis_produk=dataProduct['jenis_produk'],data=data)
            db.session.add(q)
            db.session.commit()

            return {'msg':'success add Product ! ,created by : <username:{}>'.format(username)},200
        except Exception as e:
            return {'msg':str(e)},404
    @token_required
    def put(self):
        args = parser.parse_args()
        kode_product = request.args['kode_product']
        username = session.get('username')
        role = session.get('role')
        if role == '':
            return {'msg':'anda tidak bisa menambahkan produk <role : {}>'.format(role)},400
        try:
            p = Produk.query.filter_by(kode_produk=kode_product).first()
            if p.created_by == username:

                dataProduct = args['dataProduct']
                p.data = json.dumps(dataProduct)
                db.session.commit()
                return {'msg':'success update !'},200
                
            else:
                return {'msg':'auth denied !'},400
        except Exception as e:
            return {'msg':str(e)},400
        
    # Belum Selesai 
    def delete(self):
        username = session.get('username')
        kode_produk = request.args['kode_product']
        try:
            if kode_produk == 'all':
                p = Produk.query.filter_by(created_by=username).all()
                db.session.delete(p)
                db.session.commit()
            else:
                p = Produk.query.filter_by(kode_produk=kode_produk).first()
                db.session.delete(p)
                db.session.commit()
            return {'msg':'success delete'},200
        except Exception as e:
            return {'msg':str(e)},404



        

    



api.add_resource(Product_,'/api/product')

















# Produk ada 3 yaitu (Mobile,Web,UI/UX)
