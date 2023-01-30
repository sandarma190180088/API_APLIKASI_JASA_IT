from app import ma,User 


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id","username","role",'data')

user_schema = UserSchema()
users_schema = UserSchema(many=True)


    




