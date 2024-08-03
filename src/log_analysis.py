from collections import defaultdict
from typing import Dict, List
import logging
import os
import numpy as np

from src.utils import parse_log_entry, calculate_time_differences, save_to_csv, save_analysis_results
output = 'output'
os.makedirs(output, exist_ok=True)


def process_logs(logs_path: str) -> Dict[str, Dict[str, str]]:
    data = defaultdict(dict)
    for filename in os.listdir(logs_path):
        file_path = os.path.join(logs_path, filename)
        logging.info(f"Start calculating file: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                entry = parse_log_entry(line)
                if entry:
                    node, function_code, unique_id, timestamp = entry
                    data[unique_id][node] = timestamp
    return data


def analyze_throughput(data: Dict[str, Dict[str, str]], *, to_csv=False, to_excel=True) -> List[List]:
    if to_csv:
        logging.info(f"Start saving data to CSV: {to_csv}")
        save_to_csv(data, os.path.join(output,'results.csv'))
    error_nums = 0
    time_diff_lists = defaultdict(list)
    for value in data.values():
        if len(value) != 8:
            continue
        try:
            times = [float(value.get(f'T{i}', 0)) for i in range(1, 9)]
        except ValueError:
            error_nums += 1
            continue
        calculated = calculate_time_differences(times)
        if calculated["total_time"] <= 0:
            continue
        for k, v in calculated.items():
            time_diff_lists[k].append(v)

    results = []
    for metric, values in time_diff_lists.items():
        values.sort()
        n = len(values)
        results.append([
            metric,
            f"{np.mean(values) / 1000:.2f}",
            f"{values[-1] / 1000:.2f}",
            f"{values[0] / 1000:.2f}",
            f"{values[int(n * 0.90)] / 1000:.2f}",
            f"{values[int(n * 0.95)] / 1000:.2f}",
            f"{values[int(n * 0.99)] / 1000:.2f}",
            n
        ])
    print("error line num:", error_nums)
    if to_excel:
        logging.info("Start saving data to Excel")
        save_analysis_results(results, os.path.join(output,'results.xlsx'))
    return results
