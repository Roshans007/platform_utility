from rich.console import Console
from rich.table import Table

class Dashboard:
    def __init__(self):
        self.console = Console()

    def display_failing_jobs(self, jobs):
        """
        Displays the failing Jenkins jobs in a table with indexing starting from 1.
        """
        table = Table(title="Failing Jenkins Jobs")
        table.add_column("Index", justify="center")
        table.add_column("Job Name", justify="left")
        table.add_column("Instance", justify="left")
        table.add_column("Last Build URL", justify="left")

        for idx, job in enumerate(jobs, start=1):  # Start index from 1
            table.add_row(
                str(idx),
                job['name'],
                job['instance'],
                job['last_build'] or "N/A"
            )

        self.console.print(table)

    def display_service_status(self, services):
        """
        Displays the health status of services in a table.
        """
        table = Table(title="Service Health Status")
        table.add_column("Service Name", justify="left")
        table.add_column("Status", justify="center")

        for service in services:
            table.add_row(service['name'], service['status'])

        self.console.print(table)
