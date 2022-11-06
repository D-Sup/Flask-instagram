from flask_restful import Resource, request
from api.models.post import PostModel, db
from api.schemas.post import PostSchema
from marshmallow import ValidationError

post_schema = PostSchema()
post_list_schema = PostSchema(many=True)

class Post(Resource):
    @classmethod
    def get(cls, id):
        post = PostModel.find_by_id(id)
        if post:
            return post_schema.dump(post), 200
        return {"Error" : "게시물을 찾을 수 없습니다."}, 404   
    
    @classmethod
    def put(cls, id):
        post_json = request.get_json()
        post = PostModel.find_by_id(id)
        # 게시물의 존재 여부를 먼저 체크한다.
        if post:
            post.title = post_json["title"]
            post.content = post_json["content"]
        # 게시물이 존재한지 않는다면 새 게시물을 생성한다.
        else:
            try:
                post = post_schema.load(post_json)
            except ValidationError as err:
                return err.messages, 400
            
        post. save_to_db()
        
        return post_schema.dump(post), 200
        
    @classmethod
    def delete(cls, id):
        post = PostModel.find_by_id(id)
        if post:
            post.delete_from_db()
            return {"message": "게시물이 성공적으로 삭제되었습니다."}, 200
        return {"Error" : "게시물을 찾을 수 없습니다."}, 404
   
class PostList(Resource):
    @classmethod
    def get(cls):     
        page = request.args.get("page", type=int, default=1)
        ordered_posts = PostModel.query.order_by(PostModel.id.desc())
        pagination = ordered_posts.paginate(page=page, per_page=10, error_out=False)
        result = post_list_schema.dump(pagination)
        return result
        # print(type(post_list_schema.dump(PostModel.find_all())))
        # return {"posts" : post_list_schema.dump(PostModel.find_all())}, 200    
    
    @classmethod
    def post(cls):
        pass
        post_json = request.get_json()  #json 데이터를 받아옴
        try:         
            new_post = post_schema.load(post_json)  #게시물 인스턴스로 변환
        except ValidationError as err:
            return err.messages, 400
        try:
            new_post.save_to_db()   #변환한 것을 데이터베이스에 저장
        except:
            return {"Error" : "저장에 실패하였습니다."}, 500
        return post_schema.dump(new_post), 201