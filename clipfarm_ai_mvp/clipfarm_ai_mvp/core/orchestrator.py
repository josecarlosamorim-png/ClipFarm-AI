from pathlib import Path

from core.pipeline import Pipeline


class Orchestrator:
    """
    Coordena todas as etapas do processamento.
    """

    def __init__(self):
        self.pipeline = Pipeline()

    def process_video(self, video_path: str):

        video = Path(video_path)

        if not video.exists():
            raise FileNotFoundError(video)

        return self.pipeline.run(video)
