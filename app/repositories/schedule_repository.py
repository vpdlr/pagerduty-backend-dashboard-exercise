from .base_repository import BaseRepository
from ..models import Schedule

class ScheduleRepository(BaseRepository):
    @staticmethod
    def get_schedule_by_id(schedule_id):
        return Schedule.query.get(schedule_id)
    
    @staticmethod
    def get_schedules_by_ids(schedule_ids):
        return Schedule.query.filter(Schedule.id.in_(schedule_ids)).all()