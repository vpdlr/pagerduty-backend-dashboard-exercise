import io
import pandas as pd
import plotly.express as px


class AnalysisService:
    def __init__(self, dashboard_service):
        self.dashboard_service = dashboard_service

    def get_service_with_incident_breakdown(self):
        # Get the service with the most incidents
        service_info = self.dashboard_service.get_service_with_most_incidents()
        
        # If service exists, get breakdown by status
        if service_info:
            service_id = service_info["service_id"]
            incident_breakdown = self.dashboard_service.get_incident_breakdown_by_status(service_id)
            return {
                "service_with_most_incidents": service_info,
                "incident_breakdown": incident_breakdown
            }
      
        return None


    def generate_incident_breakdown_html(self):
        breakdown_data = self.get_service_with_incident_breakdown()
        
        if breakdown_data:
            incident_breakdown = breakdown_data["incident_breakdown"]
            service_id = breakdown_data["service_with_most_incidents"]["service_id"]
            df = pd.DataFrame(incident_breakdown)

            # Generate a bar chart with Plotly, modifying bar width and title
            fig = px.bar(
                df,
                x="status",
                y="incident_count",
                title=f"Incidents by Status for Service ID: {service_id}",
                labels={"status": "Status", "incident_count": "Incident Count"}
            )

            fig.update_traces(width=0.3)  # Set bar width

            fig.update_layout(
                title_x=0.5,
                yaxis=dict(range=[0, max(df["incident_count"]) * 1.1])
            )

            return fig.to_html(full_html=False)  # Returns the HTML string

        return None
    
    def get_inactive_users(self):
        """Retrieve inactive users from the dashboard repository."""
        inactive_users = self.dashboard_service.get_inactive_users()
        return {"inactive_users": [user.id for user in inactive_users]}