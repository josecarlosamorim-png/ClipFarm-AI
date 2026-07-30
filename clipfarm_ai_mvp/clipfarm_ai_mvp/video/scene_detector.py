import cv2

from core.job import ProcessingJob


class SceneDetector:

    def detect(self, job: ProcessingJob):

        capture = cv2.VideoCapture(str(job.video_path))

        if not capture.isOpened():
            raise RuntimeError("Erro ao abrir vídeo.")

        previous = None
        scenes = []
        frame_number = 0

        threshold = 35

        while True:

            ok, frame = capture.read()

            if not ok:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            if previous is not None:

                diff = cv2.absdiff(previous, gray)

                score = diff.mean()

                if score > threshold:

                    scenes.append(frame_number)

            previous = gray

            frame_number += 1

        fps = capture.get(cv2.CAP_PROP_FPS)

        capture.release()

        job.scenes = [
            round(frame / fps, 2)
            for frame in scenes
        ]
