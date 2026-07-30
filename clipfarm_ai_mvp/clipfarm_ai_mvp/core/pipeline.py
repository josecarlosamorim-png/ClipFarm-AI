from pathlib import Path

from video.loader import VideoLoader


class Pipeline:

    def __init__(self):

        self.loader = VideoLoader()

    def run(self, video: Path):

        info = self.loader.load(video)

        print(info)

        return info
