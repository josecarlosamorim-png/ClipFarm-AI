from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ProcessingJob:

    # Entrada
    video_path: Path

    # Metadados do vídeo
    fps: float = 0.0
    duration: float = 0.0
    width: int = 0
    height: int = 0
    total_frames: int = 0

    # Áudio
    audio_path: Path | None = None

    # Processamento
    scenes: list = field(default_factory=list)
    transcript: list = field(default_factory=list)
    candidates: list = field(default_factory=list)
    clips: list = field(default_factory=list)

    # Informação extra
    metadata: dict = field(default_factory=dict)
