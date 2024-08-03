from config import setting
from src.log_processor import clean_logs
from src.utils import setup_logging

if __name__ == '__main__':
    setup_logging()
    clean_logs(setting.log_save_path)
