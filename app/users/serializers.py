from flask_restplus import fields
from app.users import api

# Schema: User Database Model
userSchema = api.model('User',{
                 'username' : fields.String(required=True, description='user name'),
                 'password' : fields.String(required=True, description='password'),
                 'phone' : fields.String(required=True, description='phone')
                }
)

# Schema: User Login
userLoginSchema = api.model('User Login', {
                'username' : fields.String(required=True, description='Registered username'),
                'password' : fields.String(required=True, description='password')
                }
)

# Schema: Resource for Testing JWT Auhentication
tesSecretResource = api.model('Secret Resource', {
                'message' : fields.String()
                                                            }
)

# Schema : Refresh Token
refreshToken = api.model('Refresh_Token',{
                'token' : fields.String()
})


# Listing user post's
userPostList = api.model(
                "User post's list",{
                    'id' : fields.Integer(description="Post's id"),
                    'story': fields.String(description="Post's story"),
                    'uploaded' : fields.DateTime(description="Uploaded date"),
                    'thumbnail' : fields.String(description="Not implemented yet"),
                    'large' : fields.String(description='Not implemented yet.'),
                    'user_id': fields.Integer(description='Author')
                }
                )

# Schema: user profile
myProfile = api.model(
                'Logged in User Profile', {
                    'id' : fields.String(description="User's id"),
                    'username' : fields.String(description="User's name"),
                    'about' : fields.String(description="User's bio"),
                    'poin' : fields.Integer(description="User's total poin"),
                    'photo' : fields.String(description="User's photo. \
                                             Not implemented yet"),
                    'posts' : fields.List(fields.Nested(userPostList)),
                }
)

