import cv2


class SceneDetector:

    def detect(self, video_path):

        capture = cv2.VideoCapture(str(video_path))

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

        return [

            round(frame / fps, 2)

            for frame in scenes

        ]
