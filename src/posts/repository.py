from repository import BaseRepository
from posts.models import Post

class PostRepository(BaseRepository):
    model = Post