from service import BaseService
from posts.repository import PostRepository

class PostService(BaseService):
    repository = PostRepository