from app import User,Produk,Transaksi,json,db

class qData():
    def __init__(self,username):
        
        self.username = username

    def postData(self,data,query):
        try:
            q = User.query.filter_by(username=self.username).first()
            dataQ = json.loads(q.data)
            if query in dataQ:
                return {'msg':'Data anda sudah ada, untuk mengubah silahkan menggunakan method PUT !','http_code':400}
            else:
                dataQ[query] = data
                q.data = json.dumps(dataQ)
                db.session.commit()
                return {'msg':f'Success Menambahkan {query}','http_code':200}
        except:
            return {'msg':'username anda tidak ada di database','http_code':404}
    def putData(self,data,query):
        try:
            q = User.query.filter_by(username=self.username).first()
            dataQ = json.loads(q.data)
            if query not in dataQ:
                return {'msg':'Data anda belum ada, untuk menambah data silahkan menggunakan method POST !','http_code':400}
            else:
                dataQ[query] = data
                q.data = json.dumps(dataQ)
                db.session.commit()
                return {'msg':f'Success Mengubah {query}','http_code':200}
        except:
            return {'msg':'username anda tidak ada di database','http_code':404}
    def postDataProductInUser(self,dataProduct):
        try:
            q = User.query.filter_by(username=self.username).first()
            dataQ = json.loads(q.data)
            p = Produk(kode_produk=dataProduct['kode_produk'],jenis_produk=dataProduct['jenis_produk'],data=dataProduct['data'])
            if 'dataProduk' in dataQ:
                if dataProduct['data']['kode_produk'] in dataQ['dataProduk']['kode_produk'] :
                    return {'msg':'data anda sudah ada !','http_code':400}
                else:
                    pass # break cape :(

            else:
                pass            
        except Exception as e:
            return {'msg':str(e),'http_code':400}
       
