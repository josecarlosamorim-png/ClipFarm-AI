from pathlib import Path

from moviepy import VideoFileClip


class AudioExtractor:

    def extract(self, job):

        output_folder = Path("cache")

        output_folder.mkdir(exist_ok=True)

        audio_path = output_folder / "audio.wav"

        video = VideoFileClip(str(job.video_path))

        video.audio.write_audiofile(
            str(audio_path),
            logger=None
        )

        video.close()

        job.audio_path = audio_path
