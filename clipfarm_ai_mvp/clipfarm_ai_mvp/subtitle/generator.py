from pathlib import Path
import json

from core.job import ProcessingJob


class SubtitleGenerator:

    def generate(self, job: ProcessingJob):

        output_dir = Path("output/subtitles")
        output_dir.mkdir(parents=True, exist_ok=True)

        for index, clip in enumerate(job.generated_clips, start=1):

            start_time = clip["start"]
            end_time = clip["end"]

            subtitles = []

            for sentence in job.transcript:

                if sentence["end"] < start_time:
                    continue

                if sentence["start"] > end_time:
                    break

                subtitles.append({

                    "start": max(
                        sentence["start"] - start_time,
                        0
                    ),

                    "end": min(
                        sentence["end"] - start_time,
                        end_time - start_time
                    ),

                    "text": sentence["text"].strip()

                })

            folder = clip["path"].parent

            json_file = folder / "subtitles.json"
            srt_file = folder / "subtitles.srt"
            ass_file = folder / "subtitles.ass"

            self._save_json(
                subtitles,
                json_file
            )

            self._save_srt(
                subtitles,
                srt_file
            )

            self._save_ass(
                subtitles,
                ass_file
            )

            clip["subtitle_json"] = json_file
            clip["subtitle_srt"] = srt_file
            clip["subtitle_ass"] = ass_file

    # ------------------------------------------------

    def _save_json(
        self,
        subtitles,
        path
    ):

        with open(
            path,
            "w",
            encoding="utf8"
        ) as f:

            json.dump(

                subtitles,

                f,

                indent=4,

                ensure_ascii=False

            )

    # ------------------------------------------------

    def _save_srt(
        self,
        subtitles,
        path
    ):

        with open(
            path,
            "w",
            encoding="utf8"
        ) as f:

            for i, sub in enumerate(subtitles, start=1):

                f.write(f"{i}\n")

                f.write(

                    f"{self._format_srt(sub['start'])} --> {self._format_srt(sub['end'])}\n"

                )

                f.write(sub["text"] + "\n\n")

    # ------------------------------------------------

    def _save_ass(
        self,
        subtitles,
        path
    ):

        with open(
            path,
            "w",
            encoding="utf8"
        ) as f:

            f.write("[Script Info]\n")
            f.write("ScriptType: v4.00+\n")
            f.write("\n")

            f.write("[V4+ Styles]\n")

            f.write(
                "Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,"
                "OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,"
                "ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,"
                "Alignment,MarginL,MarginR,MarginV,Encoding\n"
            )

            f.write(
                "Style: Default,Arial,18,&H00FFFFFF,&H0000FFFF,"
                "&H00000000,&H64000000,-1,0,0,0,100,100,0,0,"
                "1,2,0,2,10,10,10,1\n"
            )

            f.write("\n")

            f.write("[Events]\n")

            f.write(
                "Format: Layer,Start,End,Style,Name,"
                "MarginL,MarginR,MarginV,Effect,Text\n"
            )

            for sub in subtitles:

                f.write(

                    "Dialogue: 0,"

                    f"{self._format_ass(sub['start'])},"

                    f"{self._format_ass(sub['end'])},"

                    "Default,,0,0,0,,"

                    f"{sub['text']}\n"

                )

    # ------------------------------------------------

    def _format_srt(
        self,
        seconds
    ):

        h = int(seconds // 3600)

        m = int((seconds % 3600) // 60)

        s = int(seconds % 60)

        ms = int((seconds - int(seconds)) * 1000)

        return f"{h:02}:{m:02}:{s:02},{ms:03}"

    # ------------------------------------------------

    def _format_ass(
        self,
        seconds
    ):

        h = int(seconds // 3600)

        m = int((seconds % 3600) // 60)

        s = int(seconds % 60)

        cs = int((seconds - int(seconds)) * 100)

        return f"{h}:{m:02}:{s:02}.{cs:02}"