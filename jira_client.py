from jira import JIRA

class JiraClient:
    def __init__(self, jira_config):
        self.client = JIRA(
            server=jira_config['url'],
            basic_auth=(jira_config['username'], jira_config['api_token'])
        )
        self.project_key = jira_config['project_key']
        self.template = jira_config['issue_template']

    def create_issue(self, job_name, logs_url, timestamp, log_path=None):
        summary = self.template['summary_pattern'].format(job_name=job_name)
        description = self.template['description_template'].format(
            job_name=job_name, timestamp=timestamp, logs_url=logs_url
        )
        issue = self.client.create_issue(fields={
            'project': {'key': self.project_key},
            'summary': summary,
            'description': description,
            'issuetype': {'name': 'Bug'},
            'labels': ['jenkins_failure']
        })
        if log_path:
            self.client.add_attachment(issue=issue.key, attachment=log_path)
        return issue
