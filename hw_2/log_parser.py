"""
Module to parse all .log files in directory or one file by selected path
"""

import os
import json
from collections import Counter


def analyze_log(log_file):
    """function to parse .log file"""

    requests_count = 0
    http_methods_counter = Counter()
    ip_counter = Counter()
    top_requests_by_duration = []

    with open(log_file, "r", encoding='utf-8') as file:
        for line in file:
            requests_count += 1
            items = line.split()
            ip = items[0]
            date = "[" + items[3][1:] + " " + items[4][:-1] + "]"
            url_row = items[10]
            url = url_row.replace('"', '')
            http_method = items[5][1:]
            http_methods_counter[http_method] += 1
            ip_counter[ip] += 1
            duration = int(items[-1])

            if len(top_requests_by_duration) < 3:
                top_requests_by_duration.append({
                    "ip": ip,
                    "date": date,
                    "method": http_method,
                    "url": url,
                    "duration": duration
                })
            else:
                top_requests_by_duration.sort(
                    key=lambda x: x['duration'], reverse=True)
                if duration > top_requests_by_duration[2]['duration']:
                    top_requests_by_duration.pop()
                    top_requests_by_duration.append({
                        "ip": ip,
                        "date": date,
                        "method": http_method,
                        "url": url,
                        "duration": duration
                    })
    top_ip_by_requests = dict(ip_counter.most_common(3))
    total_stat = dict(http_methods_counter)

    return {
        "top_ips": top_ip_by_requests,
        "top_longest": top_requests_by_duration,
        "total_stat": total_stat,
        "total_requests": requests_count,
    }


def main(path_to_logs):
    """main function to read files"""

    if os.path.exists(path_to_logs) and os.path.isdir(path_to_logs):
        # is it directory?
        logs = [f"{path_to_logs}/{f}" for f in os.listdir(path_to_logs) if
                f.endswith(".log")]
    elif os.path.exists(path_to_logs) and not os.path.isdir(path_to_logs):
        # or file
        logs = [path_to_logs]
    else:
        # if path is wrong
        raise FileNotFoundError(f"Directory '{path_to_logs}' not found.")

    for log_file in logs:
        log_statistic = analyze_log(log_file)
        output_file = log_file.replace(".log", ".json")

        with open(output_file, "w", encoding='utf-8') as json_file:
            json.dump(log_statistic, json_file, indent=4)
            print(f"Statistics for {log_file}:")
            print(json.dumps(log_statistic, indent=4), '\n')


if __name__ == "__main__":
    path_to_logs = input("Please, input destination to directory or file: ")
    main(path_to_logs)
