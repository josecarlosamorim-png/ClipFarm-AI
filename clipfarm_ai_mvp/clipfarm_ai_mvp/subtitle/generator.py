from pathlib import Path
import json

from core.job import ProcessingJob


class SubtitleGenerator:

    def generate(self, job: ProcessingJob):

        output_dir = Path("output/subtitles")
        output_dir.mkdir(parents=True, exist_ok=True)

        for index, clip in enumerate(job.generated_clips):

            start = clip["start"]
            end = clip["end"]

            subtitles = []

            for sentence in job.transcript:

                if sentence["end"] < start:
                    continue

                if sentence["start"] > end:
                    break

                subtitles.append({

                    "start": max(
                        sentence["start"] - start,
                        0
                    ),

                    "end": sentence["end"] - start,

                    "text": sentence["text"]

                })

            json_path = output_dir / f"clip_{index+1}.json"

            with open(
                json_path,
                "w",
                encoding="utf8"
            ) as f:

                json.dump(
                    subtitles,
                    f,
                    indent=4,
                    ensure_ascii=False
                )

            clip["subtitle_json"] = json_path
