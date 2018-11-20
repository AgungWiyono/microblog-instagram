from flask_restplus import fields
from app.posts import api


# Show user in post
miniUser = api.model('Post Author',
                    {
                        'id': fields.Integer,
                        'username': fields.String(),
                        'about': fields.String()
                    }
                    )

# show Post
postList = api.model('Post',
                    {
                    'story' : fields.String(description='Post body'),
                    'uploaded' : fields.DateTime(description='Uploaded date'),
                    'image' : fields.String(description='Small image url'),
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
