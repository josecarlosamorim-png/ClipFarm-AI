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

            str(job.audio_path),

            beam_size=5,

            vad_filter=True,

            word_timestamps=True,

            condition_on_previous_text=False

        )

        transcript = []

        for segment in segments:

            words = []

            if segment.words:

                for w in segment.words:

                    words.append({

                        "word": w.word.strip(),

                        "start": float(w.start),

                        "end": float(w.end)

                    })

            transcript.append({

                "start": float(segment.start),

                "end": float(segment.end),

                "duration": float(segment.end-segment.start),

                "text": segment.text.strip(),

                "words": words

            })

        job.transcript = transcript

        job.metadata["language"] = info.language

        job.metadata["language_probability"] = info.language_probability