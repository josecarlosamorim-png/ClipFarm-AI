from faster_whisper import WhisperModel

from core.job import ProcessingJob


class WhisperEngine:
    """
    Responsável pela transcrição do áudio.

    Gera uma lista de segmentos contendo:
        - start
        - end
        - duration
        - text
        - words (quando disponíveis)

    Estes segmentos serão usados posteriormente pelo
    SegmentExtractor para criar candidatos a clips.
    """

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

            best_of=5,

            temperature=0.0,

            vad_filter=True,

            vad_parameters={
                "min_silence_duration_ms": 500,
                "speech_pad_ms": 200
            },

            word_timestamps=True,

            condition_on_previous_text=False
        )

        transcript = []

        for segment in segments:

            words = []

            if getattr(segment, "words", None):

                for word in segment.words:

                    words.append({

                        "start": word.start,

                        "end": word.end,

                        "word": word.word.strip(),

                        "probability": getattr(
                            word,
                            "probability",
                            1.0
                        )

                    })

            transcript.append({

                "start": segment.start,

                "end": segment.end,

                "duration": segment.end - segment.start,

                "text": segment.text.strip(),

                "words": words

            })

        job.transcript = transcript

        job.metadata["language"] = info.language

        job.metadata["language_probability"] = getattr(
            info,
            "language_probability",
            1.0
        )

        job.metadata["transcript_segments"] = len(transcript)