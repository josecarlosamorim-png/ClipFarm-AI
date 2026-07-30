from pathlib import Path


class Pipeline:

    def run(self, video: Path):

        print(f"Video recebido: {video.name}")

        return {
            "status": "ok",
            "video": video.name
        }
