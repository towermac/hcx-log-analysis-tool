import re

def parse_log_file(log_path, pattern, field_names):
    """
    Parse log file line by line and extract structured data using a regex pattern.

    :param log_path: Path to the log file
    :param pattern: Regex pattern for parsing each line
    :param field_names: List of field names corresponding to regex groups
    :return: List of dictionaries (parsed log entries)
    """
    regex = re.compile(pattern)
    parsed_logs = []
    with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            match = regex.match(line)
            if match:
                data = match.groups()
                entry = {field_names[i]: data[i] for i in range(len(field_names))}
                parsed_logs.append(entry)
    return parsed_logs

if __name__ == "__main__":
    # Example: Log format "2025-06-09 12:34:56 [INFO] Something happened"
    log_pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \[(\w+)\] (.*)"
    fields = ["timestamp", "level", "message"]
    log_file = "logs/app.log"
    results = parse_log_file(log_file, log_pattern, fields)
    for item in results:
        print(item)