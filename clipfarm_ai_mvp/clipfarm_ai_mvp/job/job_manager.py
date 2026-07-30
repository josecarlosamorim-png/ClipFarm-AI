from database.database import Database


class JobManager:

    def __init__(self):
        self.db = Database()

    # --------------------------------------------------
    # Criação
    # --------------------------------------------------

    def create(self, video_name):
        return self.db.create_job(video_name)

    # --------------------------------------------------
    # Atualização de progresso
    # --------------------------------------------------

    def update(self, job_id, stage, progress):

        self.db.update_progress(
            job_id,
            stage,
            progress
        )

    # --------------------------------------------------
    # Job concluído
    # --------------------------------------------------

    def finish(self, job_id):

        self.db.update_progress(
            job_id,
            "Completed",
            100
        )

    # --------------------------------------------------
    # Job com erro
    # --------------------------------------------------

    def fail(self, job_id, message="Error"):

        self.db.update_progress(
            job_id,
            message,
            -1
        )

    # --------------------------------------------------
    # Consultas
    # --------------------------------------------------

    def get(self, job_id):
        return self.db.get_job(job_id)

    def list(self):
        return self.db.list_jobs()