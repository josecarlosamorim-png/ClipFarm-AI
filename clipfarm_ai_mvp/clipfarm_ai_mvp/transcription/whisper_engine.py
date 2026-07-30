from faster_whisper import WhisperModel

from core.job import ProcessingJob


class WhisperEngine:

    def __init__(self):

        self.model = WhisperModel(
            "small",
            device="cpu",
            compute_type="int8"
        )

    def transcribe(self, job: ProcessingJob):

        segments, info = self.model.transcribe(
            str(job.audio_path)
        )

        transcript = []

        for segment in segments:

            transcript.append(
                {
                    "start": segment.start,
                    "end": segment.end,
                    "text": segment.text.strip()
                }
            )

        job.transcript = transcript

        job.metadata["language"] = info.language
