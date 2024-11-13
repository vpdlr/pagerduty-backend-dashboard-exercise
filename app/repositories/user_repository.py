from .base_repository import BaseRepository
from ..models import User

class UserRepository(BaseRepository):
    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)
    
    @staticmethod
    def get_users_by_ids(user_ids):
        return User.query.filter(User.id.in_(user_ids)).all()