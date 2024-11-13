from flask import Blueprint, jsonify, make_response
from .services.dashboard_service import DashboardService
from .services.report_service import ReportService
from .services.analysis_service import AnalysisService

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')
dashboard_service = DashboardService()

# Get the total number of services
@dashboard_bp.route('/services', methods=['GET'])
def get_services_count():
    count = dashboard_service.get_services_count()
    return jsonify({"total_services": count}), 200

# Get the number of incidents per service
@dashboard_bp.route('/incidents/per-service', methods=['GET'])
def get_incidents_per_service():
    incidents = dashboard_service.get_incidents_per_service()
    return jsonify({"incidents_per_service": incidents}), 200

# Get the number of incidents by service and status
@dashboard_bp.route('/incidents/by-service-and-status', methods=['GET'])
def get_incidents_by_service_and_status():
    incidents = dashboard_service.get_incidents_by_service_and_status()
    print("incidents: ", incidents)
    print("type incidents: ", type(incidents))
    return jsonify({"incidents_by_service_and_status": incidents}), 200

# Get all teams with their related services
@dashboard_bp.route('/teams', methods=['GET'])
def get_teams_and_services():
    teams_services = dashboard_service.get_teams_and_services()
    return jsonify({"teams": teams_services}), 200

# Get escalation policies and their service and teams
@dashboard_bp.route('/escalation-policies', methods=['GET'])
def get_escalation_policies():
    escalation_policies = dashboard_service.get_escalation_policies()
    return jsonify({"escalation_policies": escalation_policies}), 200

# Get a CSV report of other routes
@dashboard_bp.route('/report/csv/<report_type>', methods=['GET'])
def generate_report(report_type):
    report_service = ReportService(dashboard_service)
    try:
        report_type = report_type.replace('-', '_')
        csv_content = report_service.generate_csv_file(report_type)
        
        # Create a response with the CSV content
        response = make_response(csv_content)
        response.headers["Content-Disposition"] = f"attachment; filename={report_type}_report.csv"
        response.headers["Content-Type"] = "text/csv"
        
        return response
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    

# Get analysis of: service with more incidents, breakdown of incidents by status
@dashboard_bp.route('/analysis/service-most-incidents', methods=['GET'])
def get_analysis():
    analysis_service = AnalysisService(dashboard_service)
    analysis_data = analysis_service.get_service_with_incident_breakdown()

    if analysis_data:
        return jsonify(analysis_data), 200
    return jsonify({"message": "No service found."}), 404

@dashboard_bp.route('/analysis/service-most-incidents/graph', methods=['GET'])
def get_incident_breakdown_graph():
    analysis_service = AnalysisService(dashboard_service)
    graph_html = analysis_service.generate_incident_breakdown_html()

    if graph_html:
        return make_response(graph_html), 200, {"Content-Type": "text/html"}
    
    return jsonify({"message": "No incidents found to generate graph."}), 404

# Get analysis of inactive users
@dashboard_bp.route('/analysis/inactive-users', methods=['GET'])
def get_inactive_users():
    analysis_service = AnalysisService(dashboard_service)
    inactive_users_data = analysis_service.get_inactive_users()

    if inactive_users_data["inactive_users"]:
        return jsonify(inactive_users_data), 200
    return jsonify({"message": "No inactive users found."}), 404