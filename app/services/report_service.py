import pandas as pd
from flask import make_response

class ReportService:
    def __init__(self, dashboard_service):
        self.dashboard_service = dashboard_service

    def generate_services_report(self):
        services_count = self.dashboard_service.get_services_count()
        return pd.DataFrame({"Services": [services_count]})

    def generate_incidents_per_service_report(self):
        incidents = self.dashboard_service.get_incidents_per_service()
        df = pd.DataFrame(incidents)
        df.columns = ["Service ID", "Incidents"]
        return df

    def generate_incidents_by_service_and_status_report(self):
        incidents = self.dashboard_service.get_incidents_by_service_and_status()
        df = pd.DataFrame(incidents)
        df.columns = ["Service ID", "Status", "Incidents"]
        return df

    def generate_teams_and_services_report(self):
        teams_services = self.dashboard_service.get_teams_and_services()
        return pd.DataFrame([
            {"Team ID": team["team_id"], "Services": "-".join(team["services"])}
            for team in teams_services
        ])

    def generate_escalation_policies_report(self):
        escalation_policies = self.dashboard_service.get_escalation_policies()
        return pd.DataFrame([
            {
                "Escalation Policy ID": policy["escalation_policy_id"],
                "Team ID": policy["team"]["id"],
                "Services": "-".join(policy["services"])
            }
            for policy in escalation_policies
        ])

    def generate_csv_file(self, report_type):
        if report_type == "services":
            df = self.generate_services_report()
        elif report_type == "incidents_per_service":
            df = self.generate_incidents_per_service_report()
        elif report_type == "incidents_by_service_and_status":
            df = self.generate_incidents_by_service_and_status_report()
        elif report_type == "teams_and_services":
            df = self.generate_teams_and_services_report()
        elif report_type == "escalation_policies":
            df = self.generate_escalation_policies_report()
        else:
            raise ValueError("Invalid report type specified.")

        return df.to_csv(index=False)