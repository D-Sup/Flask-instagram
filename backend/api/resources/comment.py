
from flask_restful import Resource, request
from ..models.post import PostModel
# from models.post import PostModel
from ..models.user import UserModel
from ..models.comment import CommentModel
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..schemas.comment import CommentSchema

comment_schema = CommentSchema()
comment_list_schema = CommentSchema(many=True)


class CommentList(Resource):
    @classmethod
    def get(cls, post_id):
        post = PostModel.find_by_id(post_id)
        ordered_comment_list = post.comment_set.order_by(CommentModel.id.desc())
        return comment_list_schema.dump(ordered_comment_list)
    
    @classmethod
    @jwt_required()
    def post(cls, post_id):
        comment_json = request.get_json()
        username = get_jwt_identity()
        author_id = UserModel.find_by_username(username).id
        try:
            new_comment = comment_schema.load(comment_json)
            new_comment.author_id = author_id
            new_comment.post_id = post_id
        except ValidationError as err:
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
        '''
        댓글 수정
        '''
        comment_json = request.get_json()
        validate_result = comment_schema.validate(comment_json)
        if validate_result:
            return validate_result, 400

        username = get_jwt_identity()
        author_id = UserModel.find_by_username(username).id
        comment = CommentModel.find_by_id(comment_id)

        if not comment:
            return {"Error": "댓글을 찾을 수 없습니다."}, 404

        if comment.author_id == author_id and comment.post_id == post_id:
            comment.update_to_db(comment_json)
        else:
            return {"Error": "댓글은 작성자만 수정할 수 있습니다."}, 403

        return comment_schema.dump(comment), 200
        
        
    @classmethod
    @jwt_required()
    def delete(cls, post_id, comment_id):
        '''
        댓글 삭제
        '''
        username = get_jwt_identity()
        author_id = UserModel.find_by_username(username).id

        post = PostModel.find_by_id(post_id)
        comment = CommentModel.find_by_id(comment_id)

        if comment:
            if comment.author_id == author_id and comment.post_id == post_id:
                comment.delete_from_db()
                return {"message": "댓글이 성공적으로 삭제되었습니다."}, 200
            else:
                return {"Error": "댓글은 작성자만 삭제할 수 있습니다."}, 403
        return {"Error": "댓글을 찾을 수 없습니다."}, 404
    
    
    
    