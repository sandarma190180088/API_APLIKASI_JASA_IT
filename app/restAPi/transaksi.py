from app import (
    app,
    api,
    Transaksi,
    reqparse,
    request,
    json,session,
    token_required,
    Resource,reqparse,Produk
)
parser = reqparse.RequestParser()
parser.add_argument('resi',type=str,location='args',help="harap isi kode produk !")



class Transaksi_(Resource):
    @token_required
    def get(self):
        args = parser.parse_args()
        resi = args['resi']
        data = Transaksi.get_dataJsonByResi(resi=resi)
        if data['data'] == None:
            return data,404
        else:
            return data,200
        
    def post(self):
        args = parser.parse_args()
        username = session.get('username')
        kode_produk = args['kode_produk']
        try:
            p = Produk.query.filter_by(kode_produk=kode_produk).first()
            uJasa = p.created_by
            resi = f'{kode_produk}/{uJasa}/{username}'
            
            t = Transaksi()
        except Exception as e:
            return {'msg':str(e)},404
        
api.add_resource(Transaksi_,'/api/transaksi')