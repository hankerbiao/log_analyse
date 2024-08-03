import re
from config import setting
import io
import logging

SAVE_PATH = setting.log_save_path
RE_COMPILE = re.compile(setting.re_compile)
DECODE = setting.log_open_coding


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


def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
