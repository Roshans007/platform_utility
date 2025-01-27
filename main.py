import datetime
from jenkins_client import JenkinsClient
from jira_client import JiraClient
from health_checker import HealthChecker
from dashboard import Dashboard
from utils.config_loader import load_config

def select_jobs(failing_jobs):
    """
    Allows the user to select specific jobs for which tickets should be created.
    Returns a list of selected jobs.
    """
    print("\nSelect the jobs for which you want to create Jira tickets:")
    for idx, job in enumerate(failing_jobs, start=1):  # Start index from 1
        print(f"[{idx}] {job['name']} (Instance: {job['instance']})")

    selected_indices = input("\nEnter the indices of jobs (comma-separated): ")
    selected_indices = [int(idx.strip()) for idx in selected_indices.split(",") if idx.strip().isdigit()]
    return [failing_jobs[idx - 1] for idx in selected_indices if 1 <= idx <= len(failing_jobs)]  # Adjust index

def main():
    config = load_config('config.yaml')
    jenkins_client = JenkinsClient(config['jenkins'])
    jira_client = JiraClient(config['jira'])
    health_checker = HealthChecker(config['services'])
    dashboard = Dashboard()

    # Step 1: Fetch failing jobs and display them
    failing_jobs = jenkins_client.get_failing_jobs()
    dashboard.display_failing_jobs(failing_jobs)

    # Step 2: Allow the user to select jobs for ticket creation
    selected_jobs = select_jobs(failing_jobs)

    # Step 3: Create Jira tickets for the selected jobs
    if selected_jobs:
        for job in selected_jobs:
            logs = jenkins_client.get_job_logs(job['instance'], job['name'])
            timestamp = datetime.datetime.now().isoformat()
            issue = jira_client.create_issue(
                job_name=job['name'],
                logs_url=job['last_build'],
                timestamp=timestamp
            )
            print(f"Jira issue created: {issue.key}")
    else:
        print("No jobs selected for ticket creation.")

    # Step 4: Check and display service health
    services_status = health_checker.check_services()
    dashboard.display_service_status(services_status)

if __name__ == "__main__":
    main()
