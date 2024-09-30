from .base_repository import BaseRepository
from ..models import Team
from ..db import db

class TeamRepository(BaseRepository):
    @staticmethod
    def get_team_by_id(service_id):
        return Team.query.get(service_id)
    
    @staticmethod
    def get_teams_by_ids(team_ids):
        return Team.query.filter(Team.id.in_(team_ids)).all()