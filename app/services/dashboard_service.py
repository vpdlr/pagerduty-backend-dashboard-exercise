from ..repositories.dashboard_repository import DashboardRepository
from ..services.report_service import ReportService

class DashboardService:
    def __init__(self):
        self.repository = DashboardRepository()

    def get_services_count(self):
        return self.repository.get_services_count()

    def get_incidents_per_service(self):
        results = self.repository.get_incidents_per_service()
        # Convert the results into a list of dictionaries
        incidents_per_service = [
            {"service_id": row.service_id, "incident_count": row.incident_count}
            for row in results
        ]
        
        return incidents_per_service
    
    def get_incidents_by_service_and_status(self):
        results = self.repository.get_incidents_by_service_and_status()
        # Convert the results into a list of dictionaries
        incidents_by_service_and_status = [
            {
                "service_id": row[0],
                "status": row[1].value,
                "incident_count": row.incident_count
            }
            for row in results
        ]
        return incidents_by_service_and_status

    def get_teams_and_services(self):
        teams = self.repository.get_teams()
        return [
            {
                "team_id": team.id,
                "services": [service.id for service in team.services]
            } for team in teams
        ]
    
    def get_escalation_policies(self):
        policies = self.repository.get_escalation_policies()
        return [
            {
                "escalation_policy_id": policy.id,
                "team": {
                    "id": policy.team_id
                },
                "services": [service.id for service in policy.services]
            } for policy in policies
        ]

    def generate_csv_report(self):
        report_service = ReportService(self)
        return report_service.generate_csv_file()


    def get_service_with_most_incidents(self):
        result = self.repository.get_service_with_most_incidents()
        if result:
            return {"service_id": result.service_id, "incident_count": result.incident_count}
        return None

    def get_incident_breakdown_by_status(self, service_id):
        results = self.repository.get_incident_breakdown_by_status(service_id)
        return [
            {"status": row.status.value, "incident_count": row.incident_count}
            for row in results
        ]
    
    def get_inactive_users(self):
        results = self.repository.get_inactive_users()
        return results