from pathlib import Path

import ffmpeg

from core.job import ProcessingJob


class ClipGenerator:

    def __init__(self):

        self.output_dir = Path("output/clips")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate(self, job: ProcessingJob):

        job.generated_clips = []

        source = str(job.video_path)

        for index, clip in enumerate(job.best_clips[:5], start=1):

            output = self.output_dir / f"clip_{index}.mp4"

            try:

                (
                    ffmpeg
                    .input(
                        source,
                        ss=clip["start"],
                        to=clip["end"]
                    )
                    .output(
                        str(output),
                        codec="copy"
                    )
                    .overwrite_output()
                    .run(quiet=True)
                )

                job.generated_clips.append({

                    "path": output,

                    "score": clip["score"],

                    "title": clip["title"],

                    "duration": clip["end"] - clip["start"],

                    "start": clip["start"],

                    "end": clip["end"]

                })

            except ffmpeg.Error:

                continue
