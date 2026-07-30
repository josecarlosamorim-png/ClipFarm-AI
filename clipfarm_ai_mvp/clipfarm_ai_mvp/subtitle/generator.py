from pathlib import Path
import json

from core.job import ProcessingJob


class SubtitleGenerator:

    MIN_WORDS = 2
    MAX_WORDS = 4
    MAX_DURATION = 2.5

    def generate(self, job: ProcessingJob):

        output_dir = Path("output/subtitles")
        output_dir.mkdir(parents=True, exist_ok=True)

        for clip in job.generated_clips:

            clip_start = clip["start"]
            clip_end = clip["end"]

            subtitles = self._build_subtitles(
                job.transcript,
                clip_start,
                clip_end
            )

            folder = clip["path"].parent

            json_file = folder / "subtitles.json"
            srt_file = folder / "subtitles.srt"
            ass_file = folder / "subtitles.ass"

            self._save_json(subtitles, json_file)
            self._save_srt(subtitles, srt_file)
            self._save_ass(subtitles, ass_file)

            clip["subtitle_json"] = json_file
            clip["subtitle_srt"] = srt_file
            clip["subtitle_ass"] = ass_file

    # --------------------------------------------------------
    # Construção das legendas
    # --------------------------------------------------------

    def _build_subtitles(
        self,
        transcript,
        clip_start,
        clip_end
    ):

        subtitles = []
        words = []

        for sentence in transcript:

            if sentence["end"] < clip_start:
                continue

            if sentence["start"] > clip_end:
                break

            # fallback se não houver word timestamps

            if not sentence.get("words"):

                subtitles.append({

                    "start": max(
                        0.0,
                        sentence["start"] - clip_start
                    ),

                    "end": min(
                        clip_end - clip_start,
                        sentence["end"] - clip_start
                    ),

                    "text": sentence["text"].strip()

                })

                continue

            # processamento palavra a palavra

            for word in sentence["words"]:

                if word["end"] < clip_start:
                    continue

                if word["start"] > clip_end:
                    continue

                start = max(
                    0.0,
                    word["start"] - clip_start
                )

                end = min(
                    clip_end - clip_start,
                    word["end"] - clip_start
                )

                if end <= start:
                    continue

                words.append({

                    "text": word["word"],

                    "start": start,

                    "end": end

                })

        if not words:
            return subtitles

        return self._group_words(words)

    # --------------------------------------------------------
    # Agrupamento inteligente
    # --------------------------------------------------------

    def _group_words(self, words):

        subtitles = []

        current = []

        group_start = None

        for word in words:

            if group_start is None:
                group_start = word["start"]

            current.append(word)

            duration = word["end"] - group_start

            should_finish = False

            if len(current) >= self.MAX_WORDS:
                should_finish = True

            if duration >= self.MAX_DURATION:
                should_finish = True

            if word["text"].endswith((".", "!", "?")):
                should_finish = True

            if word["text"].endswith(",") and len(current) >= self.MIN_WORDS:
     
                should_finish = True

            if should_finish:

                subtitles.append({

                    "start": current[0]["start"],

                    "end": current[-1]["end"],

                    "text": " ".join(
                        w["text"]
                        for w in current
                    )

                })

                current = []
                group_start = None

        if current:

            subtitles.append({

                "start": current[0]["start"],

                "end": current[-1]["end"],

                "text": " ".join(
                    w["text"]
                    for w in current
                )

            })

        return subtitles

    # --------------------------------------------------------
    # Guardar JSON
    # --------------------------------------------------------

    def _save_json(self, subtitles, path):

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

    # --------------------------------------------------------
    # Guardar SRT
    # --------------------------------------------------------

    def _save_srt(self, subtitles, path):

        with open(
            path,
            "w",
            encoding="utf8"
        ) as f:

            for index, sub in enumerate(subtitles, start=1):

                text = self._wrap_text(
                    sub["text"],
                    max_chars=42
                ).replace("\\N", "\n")

                f.write(f"{index}\n")

                f.write(
                    f"{self._format_srt(sub['start'])} --> "
                    f"{self._format_srt(sub['end'])}\n"
                )

                f.write(text)

                f.write("\n\n")

    # --------------------------------------------------------
    # Guardar ASS
    # --------------------------------------------------------

    def _save_ass(self, subtitles, path):

        with open(
            path,
            "w",
            encoding="utf8"
        ) as f:

            # --------------------------
            # Script
            # --------------------------

            f.write("[Script Info]\n")
            f.write("Title: ClipFinder AI\n")
            f.write("ScriptType: v4.00+\n")
            f.write("PlayResX:1080\n")
            f.write("PlayResY:1920\n")
            f.write("WrapStyle:0\n")
            f.write("ScaledBorderAndShadow:yes\n")
            f.write("\n")

            # --------------------------
            # Estilos
            # --------------------------

            f.write("[V4+ Styles]\n")

            f.write(
                "Format: "
                "Name,Fontname,Fontsize,"
                "PrimaryColour,SecondaryColour,"
                "OutlineColour,BackColour,"
                "Bold,Italic,Underline,StrikeOut,"
                "ScaleX,ScaleY,Spacing,Angle,"
                "BorderStyle,Outline,Shadow,"
                "Alignment,MarginL,MarginR,MarginV,Encoding\n"
            )

            f.write(
                "Style: "
                "Default,"
                "Arial,"
                "68,"
                "&H00FFFFFF,"
                "&H0000FFFF,"
                "&H00000000,"
                "&H64000000,"
                "-1,"
                "0,"
                "0,"
                "0,"
                "100,"
                "100,"
                "0,"
                "0,"
                "1,"
                "3,"
                "1,"
                "2,"
                "60,"
                "60,"
                "220,"
                "1\n"
            )

            f.write("\n")

            # --------------------------
            # Eventos
            # --------------------------

            f.write("[Events]\n")

            f.write(
                "Format: "
                "Layer,Start,End,Style,Name,"
                "MarginL,MarginR,MarginV,"
                "Effect,Text\n"
            )

            for sub in subtitles:

                text = self._wrap_text(
                    sub["text"]
                )

                text = (
                    text
                    .replace("{", "")
                    .replace("}", "")
                )

                f.write(

                    "Dialogue: 0,"

                    f"{self._format_ass(sub['start'])},"

                    f"{self._format_ass(sub['end'])},"

                    "Default,,0,0,0,,"

                    f"{text}\n"

                )

    # --------------------------------------------------------
    # Quebra automática de linhas
    # --------------------------------------------------------

    def _wrap_text(
        self,
        text: str,
        max_chars: int = 28
    ) -> str:

        if not text:
            return ""

        words = text.split()

        if len(words) <= 2:
            return text

        lines = []
        current = []

        for word in words:

            candidate = " ".join(current + [word])

            if len(candidate) <= max_chars:

                current.append(word)

            else:

                if current:
                    lines.append(" ".join(current))

                current = [word]

        if current:
            lines.append(" ".join(current))

        return "\\N".join(lines)

    # --------------------------------------------------------
    # Formato SRT
    # --------------------------------------------------------

    def _format_srt(
        self,
        seconds: float
    ) -> str:

        seconds = max(0.0, seconds)

        hours = int(seconds // 3600)

        minutes = int((seconds % 3600) // 60)

        secs = int(seconds % 60)

        milliseconds = int(
            round(
                (seconds - int(seconds)) * 1000
            )
        )

        if milliseconds >= 1000:

            milliseconds = 0
            secs += 1

        if secs >= 60:

            secs = 0
            minutes += 1

        if minutes >= 60:

            minutes = 0
            hours += 1

        return (
            f"{hours:02}:"
            f"{minutes:02}:"
            f"{secs:02},"
            f"{milliseconds:03}"
        )

    # --------------------------------------------------------
    # Formato ASS
    # --------------------------------------------------------

    def _format_ass(
        self,
        seconds: float
    ) -> str:

        seconds = max(0.0, seconds)

        hours = int(seconds // 3600)

        minutes = int((seconds % 3600) // 60)

        secs = int(seconds % 60)

        centiseconds = int(
            round(
                (seconds - int(seconds)) * 100
            )
        )

        if centiseconds >= 100:

            centiseconds = 0
            secs += 1

        if secs >= 60:

            secs = 0
            minutes += 1

        if minutes >= 60:

            minutes = 0
            hours += 1

        return (
            f"{hours}:"
            f"{minutes:02}:"
            f"{secs:02}."
            f"{centiseconds:02}"
        )

    # --------------------------------------------------------
    # Karaoke (preparação futura)
    # --------------------------------------------------------

    def _karaoke_text(self, subtitle):

        """
        Futuramente este método irá gerar
        tags ASS \\k para highlight palavra
        a palavra.

        Nesta versão devolve apenas o texto.
        """

        return subtitle["text"]