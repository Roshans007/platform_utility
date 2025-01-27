import requests

class HealthChecker:
    def __init__(self, services):
        self.services = services

    def check_services(self):
        results = []
        for service in self.services:
            try:
                response = requests.get(service['url'], timeout=5)
                status = 'UP' if response.status_code == 200 else 'DOWN'
            except Exception:
                status = 'DOWN'
            results.append({'name': service['name'], 'status': status})
        return results
