from api.ma import ma, Method
from api.models.post import PostModel
from api.models.user import UserModel
from marshmallow import fields

class PostSchema(ma.SQLAlchemyAutoSchema):
    """
    게시물 모델에 관한 직렬화 규칙 정의
    """
    
    image = fields.String(required=True)
    
    created_at = fields.DateTime(format="%Y-%m=%d,%H:%M:%S")
    updated_at = fields.DateTime(format="%Y-%m=%d,%H:%M:%S")
    
    author_name = Method("get_author_name")
    
    def get_author_name(self, obj):
        return obj.author.username
    
    class Meta:
        model = PostModel
        # 보기 전용 필드들의 정의
        dump_only = [
            "author_name",
        ]
        # 쓰기 전용 필드들의 정의
        # load_only = [
        #     "author_id",    
        # ]
        exclude = ("author_id",)
        load_instance = True
        include_fk = True
        ordered = True
