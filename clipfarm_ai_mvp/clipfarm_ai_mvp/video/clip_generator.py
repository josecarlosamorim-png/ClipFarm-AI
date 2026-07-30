from pathlib import Path
import json
import subprocess
import shutil

from core.job import ProcessingJob


class ClipGenerator:

    OUTPUT_WIDTH = 1080
    OUTPUT_HEIGHT = 1920

    VIDEO_CODEC = "libx264"
    AUDIO_CODEC = "aac"

    CRF = 18
    PRESET = "medium"

    AUDIO_BITRATE = "192k"

    FPS = 30

    def generate(self, job: ProcessingJob):

        self._check_ffmpeg()

        output_root = Path("output/clips")
        output_root.mkdir(parents=True, exist_ok=True)

        generated = []

        for index, clip in enumerate(job.best_clips, start=1):

            folder = output_root / f"clip_{index:02d}"
            folder.mkdir(parents=True, exist_ok=True)

            video_file = folder / "video.mp4"
            thumbnail_file = folder / "thumbnail.jpg"
            metadata_file = folder / "metadata.json"

            self._render_clip(
                source_video=job.video_path,
                output_video=video_file,
                start=clip["start"],
                end=clip["end"],
                subtitles=folder / "subtitles.ass"
            )

            self._create_thumbnail(
                video_file,
                thumbnail_file
            )

            metadata = {

                "title": clip.get("title", ""),

                "score": clip.get("score", 0),

                "reason": clip.get("reason", ""),

                "start": clip["start"],

                "end": clip["end"]

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

            generated.append({

                "path": video_file,

                "thumbnail": thumbnail_file,

                "metadata": metadata_file,

                "start": clip["start"],

                "end": clip["end"]

            })

        job.generated_clips = generated
    # --------------------------------------------------------
    # Renderização principal
    # --------------------------------------------------------

    def _render_clip(
        self,
        source_video,
        output_video,
        start,
        end,
        subtitles
    ):

        duration = self._clip_duration(start, end)

        vf = self._build_filter(subtitles)

        command = [

            "ffmpeg",

            "-y",

            "-ss",
            str(start),

            "-i",
            str(source_video),

            "-t",
            str(duration),

            "-vf",
            vf,

            "-r",
            str(self.FPS),

            "-c:v",
            self.VIDEO_CODEC,

            "-preset",
            self.PRESET,

            "-crf",
            str(self.CRF),

            "-pix_fmt",
            "yuv420p",

            "-c:a",
            self.AUDIO_CODEC,

            "-b:a",
            self.AUDIO_BITRATE,

            "-movflags",
            "+faststart",

            str(output_video)

        ]

        self._run_ffmpeg(command)


    # --------------------------------------------------------
    # Criar thumbnail
    # --------------------------------------------------------

    def _create_thumbnail(
        self,
        video_file,
        thumbnail_file
    ):

        command = [

            "ffmpeg",

            "-y",

            "-i",
            str(video_file),

            "-ss",
            "00:00:01",

            "-frames:v",
            "1",

            "-q:v",
            "2",

            str(thumbnail_file)

        ]

        self._run_ffmpeg(command)

    # --------------------------------------------------------
    # Verificar FFmpeg
    # --------------------------------------------------------

    def _check_ffmpeg(self):

        ffmpeg = shutil.which("ffmpeg")

        if ffmpeg is None:

            raise RuntimeError(

                "FFmpeg não encontrado. "
                "Instale o FFmpeg e adicione-o ao PATH."

            )

        return ffmpeg

    # --------------------------------------------------------
    # Garantir pasta
    # --------------------------------------------------------

    def _ensure_directory(self, path):

        path = Path(path)

        path.mkdir(
            parents=True,
            exist_ok=True
        )

        return path

    # --------------------------------------------------------
    # Duração do clip
    # --------------------------------------------------------

    def _clip_duration(
        self,
        start,
        end
    ):

        return max(
            0.1,
            end - start
        )

    # --------------------------------------------------------
    # Limpar ficheiros temporários
    # --------------------------------------------------------

    def _cleanup(self, *files):

        for file in files:

            if file is None:
                continue

            file = Path(file)

            if file.exists():

                try:
                    file.unlink()

                except Exception:
                    pass

    # --------------------------------------------------------
    # Construção dos filtros FFmpeg
    # --------------------------------------------------------

    def _build_filter(self, subtitle_file):

        filters = []

        filters.extend(
            self._video_filters()
        )

        subtitle_file = Path(subtitle_file)

        if subtitle_file.exists():

            ass_path = (
                subtitle_file
                .resolve()
                .as_posix()
                .replace("\\", "/")
                .replace(":", "\\:")
            )

            filters.append(
                f"ass='{ass_path}'"
            )

        return ",".join(filters)

    # --------------------------------------------------------
    # Filtros de vídeo
    # --------------------------------------------------------

    def _video_filters(self):

        filters = []

        # Mantém a proporção
        filters.append(

            f"scale={self.OUTPUT_WIDTH}:{self.OUTPUT_HEIGHT}:"
            "force_original_aspect_ratio=increase"

        )

        # Crop central
        filters.append(

            f"crop={self.OUTPUT_WIDTH}:{self.OUTPUT_HEIGHT}"

        )

        # Nitidez

        filters.append(

            "unsharp=5:5:1.0:5:5:0.0"

        )

        # Saturação

        filters.append(

            "eq=saturation=1.08:contrast=1.03"

        )

        return filters

    # --------------------------------------------------------
    # Zoom (preparação)
    # --------------------------------------------------------

    def _zoom_filter(self):

        return (
            "zoompan="
            "z='min(zoom+0.0008,1.10)':"
            "x='iw/2-(iw/zoom/2)':"
            "y='ih/2-(ih/zoom/2)':"
            f"d={self.FPS}"
        )

    # --------------------------------------------------------
    # Face Tracking (placeholder)
    # --------------------------------------------------------

    def _face_tracking_filter(self):

        """
        Este método ficará responsável por calcular
        automaticamente o crop usando um detector
        de rosto (MediaPipe/YOLO).

        Nesta versão devolve None.
        """

        return None

    # --------------------------------------------------------
    # Tratamento de erros FFmpeg
    # --------------------------------------------------------

    def _run_ffmpeg(self, command):

        try:

            subprocess.run(

                command,

                check=True,

                capture_output=True,

                text=True

            )

        except subprocess.CalledProcessError as exc:

            raise RuntimeError(

                "Erro ao gerar clip:\n\n"
                + exc.stderr

            ) from exc