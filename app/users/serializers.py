from flask_restplus import fields
from flask import request
from app.users import api


class thumbimage(fields.Raw):
    def format(self,value):
        return request.host_url + '/media/thumb/' + value

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

# User id schema
userId = api.model('User ID receiver', {
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
myProfile = api.model(
                'Logged in User Profile', {
                    'id' : fields.String(description="User's id"),
                    'username' : fields.String(description="User's name"),
                    'photo': fields.Url('media_profile_image', absolute=True),
                    'about' : fields.String(description="User's bio"),
                    'poin' : fields.Integer(description="User's total poin"),
                    'photo' : fields.String(description="User's photo. \
                                             Not implemented yet"),
                    'posts' : fields.List(fields.Nested(userPostList)),
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
        'username': fields.String(),
        'phone': fields.String(),
        'about': fields.String(),
        'poin': fields.Integer,
        'subscribing': fields.Integer,
        'subscribers': fields.Integer,
        'posts': fields.List(fields.Nested(miniPostSch))
    }
    )

# Show mini profile in subbed section
miniProfileSch = api.model("User's Mini Profile",
                           {
                               'username': fields.String(),
                               'phone': fields.String(),
                               'posts': fields.List(
                                        fields.Nested(miniPostSch)
                               )
                           }
                )
