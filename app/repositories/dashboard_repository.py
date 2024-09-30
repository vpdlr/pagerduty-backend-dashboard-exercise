from ..models import Service, Incident, Team, EscalationPolicy
from ..db import db

class DashboardRepository:
    def get_services_count(self):
        return Service.query.count()

    def get_incidents_per_service(self):
        results = Incident.query.with_entities(
            Incident.service_id,
            db.func.count(Incident.id).label('incident_count')
        ).group_by(Incident.service_id).all()

        return results

    def get_incidents_by_service_and_status(self):
        results = (
            Incident.query.with_entities(
                Incident.service_id,
                Incident.status,
                db.func.count(Incident.id).label('incident_count')
            )
            .group_by(Incident.service_id, Incident.status)
            .all()
        )

        return results
    
    def get_teams(self):
        return Team.query.all()
    
    def get_escalation_policies(self):
        return EscalationPolicy.query.options(
            db.joinedload(EscalationPolicy.team),
            db.joinedload(EscalationPolicy.services)
        ).all()

    def get_service_with_most_incidents(self):
        return (
            Incident.query
            .with_entities(Incident.service_id, db.func.count(Incident.id).label('incident_count'))
            .group_by(Incident.service_id)
            .order_by(db.func.count(Incident.id).desc())
            .first()
        )

    def get_incident_breakdown_by_status(self, service_id):
        return (
            Incident.query
            .filter(Incident.service_id == service_id)
            .with_entities(Incident.status, db.func.count(Incident.id).label('incident_count'))
            .group_by(Incident.status)
            .all()
        )

