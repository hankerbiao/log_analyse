import re
from config import setting
import io
import logging
from typing import Dict, List
import pandas as pd

SAVE_PATH = setting.log_save_path
RE_COMPILE = re.compile(setting.re_compile)
DECODE = setting.log_open_coding
import traceback


def parse_log_entry(log_line: str) -> tuple:
    parts = log_line.strip().split('|')
    return tuple(parts) if len(parts) == 4 else None


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


def calculate_time_differences(times: List[float]) -> Dict[str, float]:
    return {
        "total_time": times[7] - times[0],
        "T4_T1": times[3] - times[0],
        "T4_T3": times[3] - times[2],
        "T4_T2": times[3] - times[1],
        "T3_T2": times[2] - times[1],
        "T3_T1": times[2] - times[0],
        "T2_T1": times[1] - times[0],
        "T8_T5": times[7] - times[4],
        "T8_T6": times[7] - times[5],
        "T8_T7": times[7] - times[6],
        "T7_T6": times[6] - times[5],
        "T7_T5": times[6] - times[4],
        "T6_T5": times[5] - times[4],
        "T5_T4": times[4] - times[3]
    }


def save_to_csv(data: Dict[str, Dict[str, str]], output_file: str):
    logging.info(f"Start saving data to CSV: {output_file}")
    try:
        df = pd.DataFrame.from_dict(data, orient='index')
        df.reset_index(inplace=True)
        df.columns = ['unique_id'] + [f'T{i}' for i in range(1, 9)]
        df.to_csv(output_file, index=False)
        logging.info(f"Data saved to {output_file}")
    except Exception as e:
        logging.error(f"Error saving data to CSV: {e}")
        print(traceback.format_exc())


def save_analysis_results(results: List[List], output_file: str):
    try:
        df = pd.DataFrame(results,
                          columns=['Metric', 'Mean', 'Max', 'Min', 'Top 90', 'Top 95', 'Top 99', 'Valid Data Count'])
        df.to_excel(output_file, index=False)
        logging.info(f"Analysis results saved to {output_file}")
    except Exception as e:
        logging.error(f"Error saving analysis results: {e}")
        traceback.print_exc()
