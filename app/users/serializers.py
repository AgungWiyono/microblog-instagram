from flask_restplus import fields
from flask import request
from app.users import api


class thumbimage(fields.Raw):
    def format(self,value):
        return request.host_url + '/media/thumb/' + value

login_response = api.model(
                'Login Response',{
                    'username': fields.String,
                    'phone': fields.String,
                    'token': fields.String
                }
)

# Schema: User Database Model
user_schema= api.model('User',{
                 'username' : fields.String(required=True, description='user name'),
                 'password' : fields.String(required=True, description='password'),
                 'phone' : fields.String(required=True, description='phone')
                }
)


# Schema: User Login
user_login = api.model('User Login', {
                'username' : fields.String(required=True, description='Registered username'),
                'password' : fields.String(required=True, description='password')
                }
)

subs_response = api.model(
                'Subscribe/Unsubscribe Response',{
                    'status': fields.String,
                    'name': fields.String,
                    'target': fields.String
                }
)

# User id schema
user_id = api.model('User ID receiver', {
                'user_id' : fields.String(required=True)
})

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
                    'image': thumbimage(),
                    'user_id': fields.Integer(description='Author')
                }
                )

# Schema: user profile
user_profile = api.model(
                'User Profile', {
                    'id': fields.String(description="User's id"),
                    'username': fields.String(description="User's name"),
                    #'photo': fields.Url('media_profile_image', absolute=True),
                    'about': fields.String(description="User's bio"),
                    'poin': fields.Integer(description="User's total poin"),
                    'subscribing': fields.Integer,
                    'subscribers': fields.Integer,
                    'post': fields.Integer,
                    'status': fields.Integer,
                    'posts': fields.List(fields.Nested(userPostList)),
                }
)

#Show posts on other user's profile
miniPostSch = api.model(
    'Mini posts', {
        'id': fields.Url('post_show_post', absolute=True, attribute='post'),
        'image': thumbimage()
    }
)

# Show other user profile
otherUserProfileSch = api.model(
    'Show another user profile',{
                    'id': fields.String(description="User's id"),
                    'username': fields.String(description="User's name"),
                    'photo': fields.Url('media_profile_image', absolute=True),
                    'about': fields.String(description="User's bio"),
                    'poin': fields.Integer(description="User's total poin"),
                    'subscribing': fields.Integer,
                    'subscribers': fields.Integer,
                    'post': fields.Integer,
                    'posts': fields.List(fields.Nested(userPostList)),
    }
    )

# Show mini profile in subbed section
mini_profile = api.model("User's Mini Profile",
                           {
                               'username': fields.String(),
                               'phone': fields.String(),
                               'posts': fields.List(
                                        fields.Nested(miniPostSch)
                               )
                           }
                )

register_response = api.model('Register Response', {
                    'username': fields.String,
                    'phone': fields.String,
                    'token': fields.String
                    }
)
