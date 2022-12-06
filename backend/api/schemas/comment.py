from api.ma import ma
from api.models.comment import CommentModel
from marshmallow import fields
from api.ma import ma, MethodField


class CommentSchema(ma.SQLAlchemyAutoSchema):
    """
    댓글 모델에 대한 직렬화 규칙을 정의합니다.
    """

    created_at = fields.DateTime(format="%Y-%m-%d,%H:%M:%S")
    updated_at = fields.DateTime(format="%Y-%m-%d,%H:%M:%S")

    author_name = MethodField("get_author_name")

    def get_author_name(self, obj):
        return obj.author.username

    class Meta:
        model = CommentModel
        dump_only = [
            "author_name",
        ]
        exclude = ("author_id", "post_id")
        load_instance = True
        include_fk = True
        ordered = True
