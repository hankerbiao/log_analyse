import os
import logging
import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed
import io
import re
from settings import Settings

# 初始化设置
settings = Settings()
RE_COMPILE = re.compile(settings.re_compile)
SAVE_PATH = settings.log_save_path
DECODE = settings.log_open_coding
CHUNK_SIZE = 100 * 1024 * 1024  # 100MB chunks

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def clean_logs(logs_save_path):
    """清理日志文件的优化版本，使用多进程处理文件并捕获异常。"""
    file_paths = [
        os.path.join(logs_save_path, file_name)
        for file_name in os.listdir(logs_save_path)
        if file_name.endswith('.log') and "uperformance" in file_name
    ]

    max_workers = min(os.cpu_count() or 1, 8)

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_file, file_path): file_path for file_path in file_paths}

        for future in as_completed(futures):
            file_path = futures[future]
            try:
                future.result()
                logging.info(f"Successfully processed file: {file_path}")
            except Exception as exc:
                logging.error(f"Error processing file {file_path}: {exc}")


def process_chunk(chunk):
    """处理文件的一个块。"""
    buffer = io.StringIO()
    for line in chunk.splitlines():
        try:
            decoded_line = line.decode(DECODE, errors='ignore').strip()
            res = RE_COMPILE.findall(decoded_line)
            if res and len(res[0]) == 4:
                node, function_code, unique_id, cur_time = res[0]
                write_line = f'{node}|{function_code}|{unique_id}|{cur_time}\n'
                buffer.write(write_line)
        except Exception as e:
            logging.error(f"Error processing line: {e}")
    return buffer.getvalue()


def process_file(file_path):
    """处理单个文件。"""
    try:
        if os.path.getsize(file_path) == 0:
            logging.info(f"Empty file, skipping: {file_path}")
            return

        output_file = os.path.join(SAVE_PATH, f"clean_log_{os.path.basename(file_path)}")
        logging.info(f"Start cleaning file: {file_path}")

        with open(file_path, 'rb') as f, open(output_file, 'w', encoding='utf-8') as out_f:
            while True:
                chunk = f.read(CHUNK_SIZE)
                if not chunk:
                    break
                processed_chunk = process_chunk(chunk)
                out_f.write(processed_chunk)

        logging.info(f"Finished cleaning: {file_path}")
    except Exception as e:
        logging.error(f"Error processing file {file_path}: {e}")
        traceback.print_exc()
        raise


if __name__ == '__main__':
    clean_logs(SAVE_PATH)