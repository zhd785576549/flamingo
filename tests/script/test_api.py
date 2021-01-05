from locust import HttpUser, TaskSet, task


class QuickstartUser(TaskSet):
    @task(1)
    def test_url(self):
        self.client.get("/test/params/1111/")


class WebSitUser(HttpUser):
    tasks = [QuickstartUser]

    min_wait = 3000  # 单位为毫秒
    max_wait = 6000  # 单位为毫秒
