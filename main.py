import datetime
from jenkins_client import JenkinsClient
from jira_client import JiraClient
from health_checker import HealthChecker
from dashboard import Dashboard
from utils.config_loader import load_config

def main():
    config = load_config('config.yaml')
    jenkins_client = JenkinsClient(config['jenkins'])
    jira_client = JiraClient(config['jira'])
    health_checker = HealthChecker(config['services'])
    dashboard = Dashboard()

    failing_jobs = jenkins_client.get_failing_jobs()
    dashboard.display_failing_jobs(failing_jobs)

    services_status = health_checker.check_services()
    dashboard.display_service_status(services_status)

    if input("Do you want to create Jira tickets for failing jobs? (yes/no): ").lower() == 'yes':
        for job in failing_jobs:
            logs = jenkins_client.get_job_logs(job['instance'], job['name'])
            timestamp = datetime.datetime.now().isoformat()
            issue = jira_client.create_issue(
                job_name=job['name'],
                logs_url=job['last_build'],
                timestamp=timestamp
            )
            print(f"Jira issue created: {issue.key}")

if __name__ == "__main__":
    main()
