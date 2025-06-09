def detect_exceptions(parsed_logs, keywords=None):
    """
    Detect exception entries in structured logs.

    :param parsed_logs: List of parsed log entries (dicts)
    :param keywords: List of exception keywords (default: common ones)
    :return: List of entries (dicts) containing exceptions
    """
    if keywords is None:
        keywords = ['error', 'exception', 'fail', 'traceback', 'critical', 'fatal']

    exception_logs = []
    for entry in parsed_logs:
        # Check all fields for exception keywords
        for value in entry.values():
            if isinstance(value, str):
                for kw in keywords:
                    if kw.lower() in value.lower():
                        exception_logs.append(entry)
                        break
    return exception_logs

if __name__ == "__main__":
    # Example structured logs
    results = [
        {"timestamp": "2025-06-09 12:00:00", "level": "INFO", "message": "Start process"},
        {"timestamp": "2025-06-09 12:01:00", "level": "ERROR", "message": "File not found error: config.ini"},
        {"timestamp": "2025-06-09 12:02:00", "level": "WARNING", "message": "Low memory"},
        {"timestamp": "2025-06-09 12:03:00", "level": "CRITICAL", "message": "Unhandled exception occurred"}
    ]
    exceptions = detect_exceptions(results)
    print("Detected exceptions:")
    for item in exceptions:
        print(item)