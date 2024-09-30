import requests
from flask import current_app
import asyncio
import aiohttp

class PagerDutyService:
    def __init__(self):
        self.api_key = current_app.config['PAGERDUTY_API_KEY']
        self.headers = {
            'Authorization': f'Token token={self.api_key}',
            'Content-Type': 'application/json'
        }
        self.base_url = 'https://api.pagerduty.com/'

    async def fetch_list(self, endpoint):
        """Fetch all resources from a given endpoint, handling pagination."""
        resources = []
        limit = 25  # Default limit per page
        offset = 0  # Start from the beginning

        async with aiohttp.ClientSession() as session:
            while True:
                url = f'{self.base_url}{endpoint}?limit={limit}&offset={offset}'
                async with session.get(url, headers=self.headers) as response:
                    response.raise_for_status()
                    data = await response.json()

                    resources.extend(data[endpoint])

                    # Check if there are more records to fetch
                    if not data.get('more', False):
                        break

                    # Increment offset for the next page
                    offset += limit

        return resources

    async def fetch_services(self):
        return await self.fetch_list('services')

    async def fetch_incidents(self):
        return await self.fetch_list('incidents')

    async def fetch_teams(self):
        return await self.fetch_list('teams')

    async def fetch_escalation_policies(self):
        return await self.fetch_list('escalation_policies')