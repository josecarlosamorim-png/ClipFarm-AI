from pathlib import Path

from core.pipeline import Pipeline
from core.job import ProcessingJob

from jobs.job_manager import JobManager


class Orchestrator:
    """
    Coordena todas as etapas do processamento.
    """

    def __init__(self):

        self.pipeline = Pipeline()
        self.jobs = JobManager()

    def process_video(
        self,
        video_path: str,
        campaign=None,
    ):

        video = Path(video_path)

        if not video.exists():
            raise FileNotFoundError(video)

        # ---------------------------------------
        # Cria o ProcessingJob
        # ---------------------------------------

        job = ProcessingJob(

            video_path=video,

            campaign=campaign,

        )

        # ---------------------------------------
        # Regista o Job
        # ---------------------------------------

        job.job_id = self.jobs.create(
            video.name
        )

        # ---------------------------------------
        # Executa a pipeline
        # ---------------------------------------

        job = self.pipeline.run(job)

        # ---------------------------------------
        # Atualiza progresso
        # ---------------------------------------

        self.jobs.update(

            job.job_id,

            job.current_stage,

            job.progress,

        )

        return job