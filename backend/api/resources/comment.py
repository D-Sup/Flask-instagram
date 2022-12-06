from marshmallow import ValidationError
from api.models.post import PostModel
from api.models.comment import CommentModel
from api.schemas.comment import CommentSchema
from api.models.user import UserModel
from flask_restful import Resource, request
from flask_jwt_extended import jwt_required, get_jwt_identity

comment_list_schema = CommentSchema(many=True)
comment_schema = CommentSchema()  # 댓글 하나만 달 때 사용할 것..


class CommentList(Resource):
    @classmethod
    def get(cls, post_id):
        """
        1. 게시물 id를 URL로부터 얻어옵니다.
        2. 게시물 id에 달려 있는 전체 댓글을 조회합니다. 
        """
        post = PostModel.find_by_id(post_id)
        ordered_comment_list = post.comment_set.order_by(
            CommentModel.id.desc()
        )
        return comment_list_schema.dump(ordered_comment_list)

    @classmethod
    @jwt_required()
    def post(cls, post_id):
        """
        1. 게시물 id를 URL로부터 얻어옵니다.
        2. 게시물 id를 외래키로 하여 새로운 댓글을 작성합니다.
        """
        comment_json = request.get_json()
        username = get_jwt_identity()
        author_id = UserModel.find_by_username(username).id
        try:
            new_comment = comment_schema.load(comment_json)
            new_comment.author_id = author_id
            new_comment.post_id = post_id
        except ValidationErr as err:
            return err.messages, 400
        try:
            new_comment.save_to_db()
        except:
            return {"Error": "저장에 실패하였습니다."}, 500
        return comment_schema.dump(new_comment), 201


class CommentDetail(Resource):
    @classmethod
    @jwt_required()
    def put(cls, post_id, comment_id):
        comment_json = request.get_json()
        username = get_jwt_identity()
        author_id = UserModel.find_by_username(username).id
        comment = CommentModel.find_by_id(comment_id)
        post = PostModel.find_by_id(post_id)
        # 댓글 존재 여부 확인
        if not comment:
            return {"Error": "댓글을 찾을 수 없습니다."}, 404

        # 댓글의 저자와, 요청을 보낸 사용자가 같다면 수정을 진행할 수 있다.
        if comment.author_id == author_id:
            comment.update_to_db(comment_json)
        else:
            return {"Error": "댓글은 작성자만 수정할 수 있습니다."}, 403

        return comment_schema.dump(post), 200

    @classmethod
    @jwt_required()
    def delete(cls, post_id, comment_id):
        username = get_jwt_identity()
        author_id = UserModel.find_by_username(username).id
        post = PostModel.find_by_id(post_id)
        comment = CommentModel.find_by_id(comment_id)
        if comment:
            if (post.id == post_id) and (comment.author_id == author_id):
                comment.delete_from_db()
                return {"message": "댓글이 성공적으로 삭제되었습니다."}, 200
            else:
                return {"Error": "댓글은 작성자만 삭제할 수 있습니다."}, 403
        else:
            return {"Error": "댓글을 찾을 수 없습니다."}, 404
