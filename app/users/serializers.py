from flask_restplus import fields
from app.users import api

# Schema: User Database Model
userSchema = api.model('User',{
                 'username' : fields.String(required=True, description='user name'),
                 'password' : fields.String(required=True, description='password'),
                 'phone' : fields.Integer(required=True, description='phone')
                }
)

# Schema: User Login
userLoginSchema = api.model('User Login', {
                'username' : fields.String(required=True),
                'password' : fields.String(required=True)
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
