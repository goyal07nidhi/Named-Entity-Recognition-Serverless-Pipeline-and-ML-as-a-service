from locust import HttpLocust, task, between, TaskSet


class UserBehaviour(TaskSet):
    @task(1)
    def docs_index(self):
        self.client.get("http://127.0.0.1:8001/")


    @task(3)
    def column_index(self):
        self.client.get("http://127.0.0.1:8001/v1/ner?url=s3%3A%2F%2Fner-api2-team6%2Finputpii%2FAGEN.txt")


    @task(4)
    def experiment_index(self):
        self.client.get("http://127.0.0.1:8001/v1/maskedandanonymized?s3_path=s3%3A%2F%2Frishvita%2Fsec-edgar%2Ftranscripts%2FAGEN.txt&Mask_Entity=NAME&deidentify_Ent=DATE")


class WebsiteUser(HttpLocust):
    task_set = UserBehaviour
    wait_time = between(5, 9)
