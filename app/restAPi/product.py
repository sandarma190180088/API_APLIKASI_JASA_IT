from app import (
    Produk,
    api,
    request,
    token_required,
    product_schema,products_schema,
    json,
    db,session,
    Resource,User
)

class Product_(Resource):
    @token_required
    def get(self):
        try:
            que = request.args['kode_product']
            p = Produk.query.filter_by(kode_produk=que).first()
            return product_schema.dump(p),200
        except:
            p = Produk.query.all()
            return products_schema.dump(p),200
    @token_required
    def post(self):
        try:
            username= session.get('username')
            u = User.query.filter_by(username=username).first()
            jenis_produk = request.form['jenis_produk']
            nama_produk = request.form['nama_produk']
            catatan = request.form['catatan']
            harga = request.form['harga']
            r_data = {
                'nama_produk' : nama_produk,
                'harga' : harga,
                'catatan':catatan
            }
            
            kode_produk = f'{jenis_produk}/{u.username}/{len(nama_produk)}{len(catatan)}{len(harga)}'

            data = json.loads(u.data)
            
            if 'dataProduct' not in data:
                
                data['dataProduct'] = [kode_produk]
                
            else:
                if kode_produk in data['dataProduct']:
                    return {'msg':'data produk anda sudah ada'},400
                else:
                    data['dataProduct'].append(kode_produk)
            data = json.dumps(data)
            u.data = data
            q = Produk(kode_produk=kode_produk,jenis_produk=jenis_produk,data=json.dumps(r_data))
            db.session.add(q)
            db.session.commit()

            return {'msg':'added !','data':data},200
        except Exception as e:
            return {'msg':str(e)},404

    



api.add_resource(Product_,'/api/product')

















# Produk ada 3 yaitu (Mobile,Web,UI/UX)