from app import ma,User 
import json


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id","username","role")
        
        ordered=True

    

user_schema = UserSchema()
users_schema = UserSchema(many=True)


    




