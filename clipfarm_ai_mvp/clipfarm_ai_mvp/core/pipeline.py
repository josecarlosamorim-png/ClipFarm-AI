from pathlib import Path

from video.loader import VideoLoader
from video.scene_detector import SceneDetector
from audio.extractor import AudioExtractor


class Pipeline:

    def __init__(self):

        self.loader = VideoLoader()

        self.detector = SceneDetector()

        self.audio = AudioExtractor()

    def run(self, video: Path):

        info = self.loader.load(video)

        scenes = self.detector.detect(video)

        audio = self.audio.extract(video)

        info["audio"] = str(audio)

        info["scene_changes"] = len(scenes)

        info["scenes"] = scenes[:20]

        return info
