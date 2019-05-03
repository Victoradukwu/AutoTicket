from locust import HttpLocust, TaskSet, task


class UserBehavior(TaskSet):
    def __init__(self, parent):
        super(UserBehavior, self).__init__(parent)

    @task
    def create(self):
        self.client.get("/flights/")


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 1000
    max_wait = 1500
