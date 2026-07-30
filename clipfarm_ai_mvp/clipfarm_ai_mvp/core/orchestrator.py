from pathlib import Path

from core.pipeline import Pipeline
from jobs.job_manager import JobManager


class Orchestrator:
    """
    Coordena todas as etapas do processamento.
    """

    def __init__(self):
        self.pipeline = Pipeline()
        self.jobs = JobManager()

    def process_video(self, video_path: str):

        video = Path(video_path)

        if not video.exists():
            raise FileNotFoundError(video)

        # Regista o job na base de dados
        job_id = self.jobs.create(video.name)

        # Executa a pipeline
        job = self.pipeline.run(video)

        # Associa o ID ao ProcessingJob
        job.job_id = job_id

        # Atualiza estado final
        self.jobs.update(
            job_id,
            job.current_stage,
            job.progress
        )

        return job