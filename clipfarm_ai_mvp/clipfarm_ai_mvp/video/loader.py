from pathlib import Path

import cv2


class VideoLoader:

    def load(self, video_path: Path):

        capture = cv2.VideoCapture(str(video_path))

        if not capture.isOpened():
            raise RuntimeError("Não foi possível abrir o vídeo.")

        fps = capture.get(cv2.CAP_PROP_FPS)

        frames = capture.get(cv2.CAP_PROP_FRAME_COUNT)

        width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))

        height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

        duration = frames / fps if fps else 0

        capture.release()

        return {
            "path": str(video_path),
            "fps": round(fps, 2),
            "frames": int(frames),
            "duration": round(duration, 2),
            "width": width,
            "height": height,
        }
