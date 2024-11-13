# PagerDuty Dashboard

PagerDuty Backend Exercise to get data using the Pagerduty API to feed a dashboard with information related to services, incidents, teams and escalation policies

## Prerequisites

- **Python 3.10+**
- **MySQL**: Make sure you have MySQL installed and running.
- **Docker** (optional, for containerized deployment)

## Setup

1. **Create a MySQL Database and User**:

   - Create a new database (eg. `pagerduty_db`).
   - Create a user (e.g., `pagerduty_user`) with a password (e.g., `root`) and grant them access to the database.

   Update the `DATABASE_URL` in the `.env` file accordingly:

2. **Create a `.env` file** in the root directory of the project and add the following environment variables:

```bash
DATABASE_URL=mysql+pymysql://<PAGERDUTY_USER>:<PAGERDUTY_USER_PASSWORD>@localhost/<PAGERDUTY_DB>
PAGERDUTY_API_KEY=<PAGERDUTY_API_KEY>
```

Ensure the `DATABASE_URL` starts with `mysql+pymysql` as this is required for the application to connect to MySQL.

3. **Install dependencies**:

```bash
pip install -r requirements.txt
```

## Running the Application

### Using Docker Compose

1. **Start the application:**

```bash
docker-compose up --build
```

### Without Docker

1. **Run the application:**

```bash
flask run
```

The app will be accessible at http://localhost:5000.

## CLI Command

After the application is up and running, you can synchronize data from PagerDuty by running:

```bash
flask sync-pagerduty
```

This command will fetch and store the latest data from the PagerDuty API into the database.

## API Endpoints

You can access the following endpoints to get data:

### Dashboard Data Endpoints

These endpoints provide access to various dashboard data:

`GET /api/dashboard/services`

`GET /api/dashboard/incidents/per-service`

`GET /api/dashboard/incidents/by-service-and-status`

`GET /api/dashboard/teams`

`GET /api/dashboard/escalation-policies`

### CSV Report Endpoints

Generate CSV reports for different datasets:

`GET /api/dashboard/report/csv/services`

`GET /api/dashboard/report/csv/incidents_per_service`

`GET /api/dashboard/report/csv/incidents_by_service_and_status`

`GET /api/dashboard/report/csv/teams_and_services`

`GET /api/dashboard/report/csv/escalation_policies`

### Analysis Endpoints 

Perform analysis on the data: 

Service with more incidents, breakdown of incidents by status

`GET /api/dashboard/analysis/service-most-incidents`

Analysis of inactive users

`GET /api/dashboard/analysis/inactive-users`

#### Analysis Graph

Graph of: Service with more incidents, breakdown of incidents by status

`GET /api/dashboard/analysis/service-most-incidents/graph`



## Features

- Synchronize data from PagerDuty
- Access data through API endpoints for services, incidents, teams, and escalation policies
- Generate CSV reports for services, incidents, teams, and escalation policies
