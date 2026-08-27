from locust import HttpUser, task
class SmokeUser(HttpUser):
    @task
    def health(self): self.client.get('/api/v1/health')
