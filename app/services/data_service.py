from ..services.pagerduty_service import PagerDutyService
from ..repositories.service_repository import ServiceRepository
from ..repositories.incident_repository import IncidentRepository
from ..repositories.team_repository import TeamRepository
from ..repositories.user_repository import UserRepository
from ..repositories.schedule_repository import ScheduleRepository
from ..repositories.escalation_policy_repository import EscalationPolicyRepository
from ..models import Service, IncidentStatus, Incident, Team, EscalationPolicy, User, Schedule
import asyncio


class DataSyncService:
    """Handles fetching and syncing data to the database"""

    def __init__(self):
        self.pagerduty_service = PagerDutyService()

    
    async def fetch_all_data(self):
        """Fetches all data from API 

        Returns:
            tuple: arrays of all fetched entities (teams, services, incidents and escalation_policies)
        """
        teams, services, incidents, escalation_policies, users, schedules = await asyncio.gather(
            self.pagerduty_service.fetch_teams(),
            self.pagerduty_service.fetch_services(),
            self.pagerduty_service.fetch_incidents(),
            self.pagerduty_service.fetch_escalation_policies(),
            self.pagerduty_service.fetch_users(),
            self.pagerduty_service.fetch_schedules()
        )
        return teams, services, incidents, escalation_policies, users, schedules

    async def sync_all_data(self):
        """Syncs data: fetches the API and stores into the database
        """
        try:
            teams, services, incidents, escalation_policies, users, schedules = await self.fetch_all_data()
            print("teams: ", len(teams), ", services: ", len(services), ", incidents: ", len(incidents),
                   ", escalation policies: ", len(escalation_policies), ", users: ", len(users), ", schedules: ", len(schedules))
            
            self.store_teams(teams)
            self.store_services(services)
            self.store_incidents(incidents)
            self.store_escalation_policies(escalation_policies)
            self.store_users(users)
            self.store_schedules(schedules)

            print("Data synchronization completed successfully.")
        except Exception as e:
            print(f"Error during data synchronization: {str(e)}")

    def store_teams(self, teams):
        if teams:
            team_objects = [Team(id=team['id']) for team in teams]
            TeamRepository.add_all(team_objects)
        
    def store_services(self, services):
        print("storing services------")
        if services:
            service_objects = []
            for service in services:
                service_obj = Service(id=service['id'])
                team_ids = [team['id'] for team in service.get('teams', [])]
                if team_ids:
                    team_objects = TeamRepository.get_teams_by_ids(team_ids)
                    service_obj.teams.extend(team_objects)
                service_objects.append(service_obj)
            ServiceRepository.add_all(service_objects)

    def store_incidents(self, incidents):
        if incidents:
            incident_objects = []
            for incident in incidents:
                service = ServiceRepository.get_service_by_id(incident['service']['id'])
                status = IncidentStatus[incident['status'].upper()]
                incident_obj = Incident(id=incident['id'], status=status, service=service)
                incident_objects.append(incident_obj)
            IncidentRepository.add_all(incident_objects)

    def store_escalation_policies(self, escalation_policies):
        if escalation_policies:
            escalation_policy_objects = []
            for policy in escalation_policies:
                escalation_policy_obj = EscalationPolicy(id=policy['id'])
                if policy['teams']:
                    policy_id = policy['teams'][0]["id"]
                    team = TeamRepository.get_team_by_id(policy_id)
                    escalation_policy_obj.team = team
                services_id = [service['id'] for service in policy.get('services', [])]
                if services_id:
                    service_objects = ServiceRepository.get_services_by_ids(services_id)
                    escalation_policy_obj.services.extend(service_objects)
                escalation_policy_objects.append(escalation_policy_obj)
            EscalationPolicyRepository.add_all(escalation_policy_objects)


    def store_users(self, users):
        if users:
            user_objects = [User(id=user['id']) for user in users]
            UserRepository.add_all(user_objects)
    
    def store_schedules(self, schedules):
        if schedules:
            schedule_objects = []
            for schedule in schedules:
                schedule_obj = Schedule(id=schedule['id'])
                schedule_objects.append(schedule_obj)
                # Optionally associate users with schedules if that data is present
                if 'users' in schedule:
                    for user in schedule['users']:
                        user_obj = UserRepository.get_user_by_id(user['id'])
                        if user_obj:
                            schedule_obj.users.append(user_obj)
            ScheduleRepository.add_all(schedule_objects)