from flask_restplus import fields
from app.posts import api

# show Post
postList = api.model('Post',
                    {
                   'id' : fields.String(description='post id'),
                    'post' : fields.String(description='post body'),
                    'uploaded' : fields.DateTime(description='post uploaded date'),
                    'thumbnail' : fields.String(description='Small image url'),
                    'large' : fields.String(description='HD image url')
                    }
                )

# post Post
postInsert = api.model('Insert Post',
                        {
                            'post' : fields.String(description='post body')
                        }
                      )
