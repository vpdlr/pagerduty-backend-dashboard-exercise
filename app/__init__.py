import os
from flask import Flask
import click
import asyncio
from dotenv import load_dotenv
from .db import db
from .routes import dashboard_bp
from .services.data_service import DataSyncService

# Load environment variables
load_dotenv()

from .config import Config

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(dashboard_bp)

    # Initialize the database
    db.init_app(app)

    with app.app_context():
        # Import routes and create all tables
        from . import routes
        db.create_all()

        # Register CLI command
        @app.cli.command("sync-pagerduty")
        def sync_pagerduty():
            """Synchronize data from PagerDuty"""
            click.echo("Syncing data from PagerDuty...")

            # Create an event loop and run the async sync_all_data function
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            data_sync_service = DataSyncService()

            try:
                result = loop.run_until_complete(data_sync_service.sync_all_data())
                if result is None:
                    click.echo("No data was synchronized.")
                else:
                    click.echo("Data sync complete.")
            finally:
                loop.close()

            click.echo("Data sync complete.")

    return app
