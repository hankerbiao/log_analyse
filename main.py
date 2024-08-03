from config import setting
from src.log_analysis import process_logs, analyze_throughput
from src.log_processor import clean_logs
from src.utils import setup_logging

if __name__ == '__main__':
    setup_logging()
    # 1. 清理日志文件
    clean_logs(setting.log_save_path)
    # 2. 计算日志
    result = analyze_throughput(process_logs(setting.clean_log_save_path))
    for i in result:
        print(i)
