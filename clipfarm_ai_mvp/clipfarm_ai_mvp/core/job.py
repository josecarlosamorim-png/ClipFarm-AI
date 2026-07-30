from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ProcessingJob:

    video_path: Path

    fps: float = 0
    duration: float = 0

    width: int = 0
    height: int = 0

    audio_path: Path | None = None

    scenes: list = field(default_factory=list)

    transcript: list = field(default_factory=list)

    clips: list = field(default_factory=list)

    metadata: dict = field(default_factory=dict)
