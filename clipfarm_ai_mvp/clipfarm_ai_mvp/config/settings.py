from pathlib import Path


# ==========================
# Projeto
# ==========================

PROJECT_NAME = "ClipFinder AI V4"

VERSION = "4.0.0"


# ==========================
# Diretórios
# ==========================

ROOT = Path(__file__).resolve().parent.parent

CACHE_DIR = ROOT / "cache"
OUTPUT_DIR = ROOT / "output"
DATABASE_DIR = ROOT / "database"

CACHE_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)
DATABASE_DIR.mkdir(exist_ok=True)


# ==========================
# Base de dados
# ==========================

DATABASE_PATH = DATABASE_DIR / "clipfinder.db"


# ==========================
# Whisper
# ==========================

WHISPER_MODEL = "small"

WHISPER_DEVICE = "cpu"

WHISPER_COMPUTE = "int8"


# ==========================
# Segmentação
# ==========================

MIN_SEGMENT_DURATION = 15

MAX_SEGMENT_DURATION = 45

WINDOW_OVERLAP = 10


# ==========================
# Exportação
# ==========================

VIDEO_CODEC = "libx264"

AUDIO_CODEC = "aac"

VIDEO_FORMAT = "mp4"