from flask_restplus import fields
from app.posts import api

# show Post
postList = api.model('Post',
                    {
                   'id' : fields.Integer(description='post id'),
                    'post' : fields.String(description='post body'),
                    'uploaded' : fields.DateTime(description='post uploaded date'),
                    'thumbnail' : fields.String(description='Small image url'),
                    'large' : fields.String(description='HD image url')
                    }
                )

# post Post
postInsert = api.model('Insert Post',
                        {
                            'story' : fields.String(description='post body'),
                            'latitude': fields.String(description='user gps'),
                            'longitude': fields.String(description='user gps'),
                            'premium': fields.String(description='0 or 1'),
                            'convert': fields.String(description='0 or 1')
                        }
                      )
