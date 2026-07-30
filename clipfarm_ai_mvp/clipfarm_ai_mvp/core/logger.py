import logging
from pathlib import Path

LOG_FOLDER = Path("logs")
LOG_FOLDER.mkdir(exist_ok=True)

LOG_FILE = LOG_FOLDER / "clipfinder.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(
            LOG_FILE,
            encoding="utf8"
        ),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("ClipFinder")


# =====================================================
# Funções utilitárias
# =====================================================

def log_step(step: str):
    logger.info("=" * 60)
    logger.info(step)


def log_info(message: str):
    logger.info(message)


def log_warning(message: str):
    logger.warning(message)


def log_error(message: str):
    logger.error(message)


def log_exception(exc: Exception):
    logger.exception(exc)


def log_job(job):

    logger.info("")

    logger.info("========== JOB ==========")

    logger.info("Status: %s", job.status)

    logger.info("Progress: %d%%", job.progress)

    logger.info("Stage: %s", job.current_stage)

    logger.info("Elapsed: %.2fs", job.elapsed_time)

    logger.info("Scenes: %d", len(job.scenes))

    logger.info("Transcript: %d", len(job.transcript))

    logger.info("Segments: %d", len(job.segments))

    logger.info("Best Clips: %d", len(job.best_clips))

    logger.info("Generated Clips: %d", len(job.generated_clips))

    if job.errors:

        logger.error("Errors:")

        for error in job.errors:
            logger.error(error)

    logger.info("=========================")