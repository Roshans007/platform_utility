from rich.console import Console
from rich.table import Table

class Dashboard:
    def __init__(self):
        self.console = Console()

    def display_failing_jobs(self, jobs):
        table = Table(title="Failing Jenkins Jobs")
        table.add_column("Job Name", justify="left")
        table.add_column("Instance", justify="left")
        table.add_column("Last Build URL", justify="left")

        for job in jobs:
            table.add_row(job['name'], job['instance'], job['last_build'] or "N/A")

        self.console.print(table)

    def display_service_status(self, services):
        table = Table(title="Service Health Status")
        table.add_column("Service Name", justify="left")
        table.add_column("Status", justify="center")

        for service in services:
            table.add_row(service['name'], service['status'])

        self.console.print(table)
