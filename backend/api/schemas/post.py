from api.ma import ma, MethodField
from api.models.post import PostModel
from api.models.user import UserModel
from marshmallow import fields
from api.schemas.user import AuthorSchema


class PostSchema(ma.SQLAlchemyAutoSchema):
    """
    게시물 모델에 관한 직렬화 규칙 정의
    """
    image = fields.String(required=True)
    created_at = fields.DateTime(format="%Y-%m-%d,%H:%M:%S")
    updated_at = fields.DateTime(format="%Y-%m-%d,%H:%M:%S")
    author = fields.Nested(AuthorSchema)

    class Meta:
        model = PostModel
        exclude = ("author_id",)
        include_fk = True
        load_instance = True
        ordered = True
