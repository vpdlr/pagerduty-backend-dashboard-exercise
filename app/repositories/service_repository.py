from .base_repository import BaseRepository
from ..models import Service

class ServiceRepository(BaseRepository):
    @staticmethod
    def get_service_by_id(service_id):
        return Service.query.get(service_id)
    
    @staticmethod
    def get_services_by_ids(services_ids):
        return Service.query.filter(Service.id.in_(services_ids)).all()