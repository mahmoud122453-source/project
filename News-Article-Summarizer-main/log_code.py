import logging
import os


class Logger:
    """File logger used by the Streamlit app and the summarizer.

    Writes to log_files/<name>.log. The line format matches the existing
    project logs: ``2026-02-27 17:18:37,745 - INFO - message``.
    """

    @staticmethod
    def get_logs(name):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        if not logger.handlers:
            os.makedirs("log_files", exist_ok=True)
            log_path = os.path.join("log_files", f"{name}.log")
            handler = logging.FileHandler(log_path, encoding="utf-8")
            handler.setLevel(logging.DEBUG)
            handler.setFormatter(
                logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            )
            logger.addHandler(handler)

        return logger
