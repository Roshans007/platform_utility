import jenkins

class JenkinsClient:
    def __init__(self, jenkins_config):
        self.clients = []
        for instance in jenkins_config:
            client = jenkins.Jenkins(
                instance['url'],
                username=instance['username'],
                password=instance['api_token']
            )
            self.clients.append({'name': instance['name'], 'client': client})

    def get_failing_jobs(self):
        failing_jobs = []
        for instance in self.clients:
            client = instance['client']
            jobs = client.get_jobs()
            for job in jobs:
                if job['color'] == 'red':
                    job_info = client.get_job_info(job['name'])
                    failing_jobs.append({
                        'name': job['name'],
                        'instance': instance['name'],
                        'last_build': job_info['lastBuild']['url'] if job_info['lastBuild'] else None
                    })
        return failing_jobs

    def get_job_logs(self, instance_name, job_name):
        for instance in self.clients:
            if instance['name'] == instance_name:
                client = instance['client']
                job_info = client.get_job_info(job_name)
                if job_info['lastBuild']:
                    build_number = job_info['lastBuild']['number']
                    return client.get_build_console_output(job_name, build_number)
        return None
