from flask import request
from flask_restplus import fields
from app.posts import api


# Show user in post
mini_user = api.model('Post Author',
                    {
                        'id': fields.Url('user_profile', absolute=True),
                        'username': fields.String(),
                        'about': fields.String(),
                        'phone': fields.String()
                    }
                    )

# Show user in post
mini_user2= api.model('Post Author',
                    {
                        'id': fields.Url('user_user_profile', absolute=True),
                        'username': fields.String(),
                        'phone': fields.String()
                    }
                    )

class hdimage(fields.Raw):
    def format(self, value):
        return request.host_url+'media/hd/' + value

class thumbimage(fields.Raw):
    def format(self, value):
        return request.host_url + 'media/thumb' + value


# show Post
post_list= api.model('Post',
                    {
                    'story' : fields.String(description='Post body'),
                    'uploaded' : fields.DateTime(description='Uploaded date'),
                    'image': hdimage(),
                    'author': fields.Nested(mini_user)
                    }
                )

# Posts Fedd
post_feed= api.model('Posts Feed',
                    {
                    'story' : fields.String(description='Post body'),
                    'uploaded' : fields.DateTime(description='Uploaded date'),
                    'image': hdimage(),
                    'author': fields.Nested(mini_user2)
                    }
                )

# post Post
post_insert = api.model('Insert Post',
                        {
                            'status':fields.String,
                        }
                      )
