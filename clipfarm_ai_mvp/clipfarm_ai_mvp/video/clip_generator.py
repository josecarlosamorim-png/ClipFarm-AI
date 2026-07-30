from pathlib import Path
import json
import re

import ffmpeg

from core.job import ProcessingJob


class ClipGenerator:

    MAX_CLIPS = 10

    def __init__(self):

        self.output_dir = Path("output/clips")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate(self, job: ProcessingJob):

        job.generated_clips = []

        source = str(job.video_path)

        for index, clip in enumerate(job.best_clips[: self.MAX_CLIPS], start=1):

            safe_title = self._safe_filename(
                clip.get("title", f"clip_{index}")
            )

            clip_folder = self.output_dir / f"{index:02d}_{safe_title}"
            clip_folder.mkdir(parents=True, exist_ok=True)

            video_file = clip_folder / "video.mp4"
            thumb_file = clip_folder / "thumbnail.jpg"
            metadata_file = clip_folder / "metadata.json"

            duration = clip["end"] - clip["start"]

            try:

                (
                    ffmpeg
                    .input(source, ss=clip["start"], t=duration)
                    .output(
                        str(video_file),
                        vcodec="libx264",
                        acodec="aac",
                        preset="fast",
                        movflags="+faststart"
                    )
                    .overwrite_output()
                    .run(quiet=True)
                )

                (
                    ffmpeg
                    .input(str(video_file), ss=min(1, duration/2))
                    .output(
                        str(thumb_file),
                        vframes=1
                    )
                    .overwrite_output()
                    .run(quiet=True)
                )

                metadata = {

                    "title": clip.get("title"),

                    "category": clip.get("category"),

                    "score": clip.get("score"),

                    "heuristic_score": clip.get("heuristic_score"),

                    "llm_score": clip.get("llm_score"),

                    "confidence": clip.get("confidence"),

                    "start": clip["start"],

                    "end": clip["end"],

                    "duration": duration

                }

                with open(
                    metadata_file,
                    "w",
                    encoding="utf8"
                ) as f:

                    json.dump(
                        metadata,
                        f,
                        indent=4,
                        ensure_ascii=False
                    )

                job.generated_clips.append({

                    "title": metadata["title"],

                    "category": metadata["category"],

                    "score": metadata["score"],

                    "confidence": metadata["confidence"],

                    "duration": duration,

                    "start": clip["start"],

                    "end": clip["end"],

                    "path": video_file,

                    "thumbnail": thumb_file,

                    "metadata": metadata_file

                })

            except ffmpeg.Error as e:

                print(e)

    def _safe_filename(self, text):

        text = text.lower()

        text = re.sub(r"[^\w\s-]", "", text)

        text = re.sub(r"\s+", "_", text)

        return text[:40]