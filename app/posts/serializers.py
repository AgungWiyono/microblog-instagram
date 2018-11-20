from flask import request
from flask_restplus import fields
from app.posts import api


# Show user in post
miniUser = api.model('Post Author',
                    {
                        'id': fields.Url('user_other_user_list', absolute=True),
                        'username': fields.String(),
                        'about': fields.String()
                    }
                    )

class hdimage(fields.Raw):
    def format(self, value):
        return request.host_url+'/media/hd/' + value


# show Post
postList = api.model('Post',
                    {
                    'story' : fields.String(description='Post body'),
                    'uploaded' : fields.DateTime(description='Uploaded date'),
                    'image': hdimage(),
                    'author': fields.Nested(miniUser)
                    }
                )

# post Post
postInsert = api.model('Insert Post',
                        {
                            'story' : fields.String(description='post body'),
                            'premium': fields.String(description='0 or 1'),
                            'convert': fields.String(description='0 or 1')
                        }
                      )
