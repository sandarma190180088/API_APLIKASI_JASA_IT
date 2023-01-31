from app import ma,User 
import json


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id","username","role")
        
        ordered=True
user_schema = UserSchema()
users_schema = UserSchema(many=True)




class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id','kode_produk','jenis_produk','data')
        ordered=True


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)



    




