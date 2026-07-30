from core.job import ProcessingJob
import cv2


class VideoLoader:

    def load(self, job: ProcessingJob):

        capture = cv2.VideoCapture(str(job.video_path))

        if not capture.isOpened():
            raise RuntimeError("Não foi possível abrir o vídeo.")

        job.fps = capture.get(cv2.CAP_PROP_FPS)

        job.total_frames = int(
            capture.get(cv2.CAP_PROP_FRAME_COUNT)
        )

        job.width = int(
            capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        )

        job.height = int(
            capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        )

        if job.fps > 0:
            job.duration = (
                job.total_frames / job.fps
            )

        capture.release()
