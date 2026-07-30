from database.database import Database


class JobManager:

    def __init__(self):

        self.db = Database()

    def create(self, video_name):

        return self.db.create_job(video_name)

    def update(

        self,

        job_id,

        stage,

        progress

    ):

        self.db.update_progress(

            job_id,

            stage,

            progress

        )