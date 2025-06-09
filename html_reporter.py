import datetime

def generate_html_report(parsed_logs, exception_logs, output_path="log_report.html"):
    """
    Generate an HTML report for log analysis.

    :param parsed_logs: List of structured logs (dicts)
    :param exception_logs: List of exception logs (dicts)
    :param output_path: Output HTML file path
    :return: Output HTML file path
    """
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total = len(parsed_logs)
    exc_count = len(exception_logs)
    exc_set = set(id(x) for x in exception_logs)

    html = [
        "<!DOCTYPE html>",
        "<html lang='en'>",
        "<head>",
        "<meta charset='utf-8'/>",
        "<title>Log Analysis Report</title>",
        "<style>",
        "body { font-family: Arial, sans-serif; margin: 40px; }",
        "h1 { color: #20264b; }",
        "table { border-collapse: collapse; width: 100%; }",
        "th, td { border: 1px solid #eee; padding: 8px; text-align: left; }",
        "th { background: #f2f2f2; }",
        ".exception { background: #ffeaea; color: #c00; }",
        ".summary { margin: 1em 0; }",
        "</style>",
        "</head>",
        "<body>",
        f"<h1>Log Analysis Report</h1>",
        f"<div class='summary'>Generated: {now_str}<br/>Total logs: {total}, Exceptions: <span style='color:#c00'>{exc_count}</span></div>",
        "<table>",
        "<tr><th>#</th><th>Timestamp</th><th>Level</th><th>Message</th></tr>"
    ]

    for idx, log in enumerate(parsed_logs):
        row_cls = "exception" if id(log) in exc_set else ""
        html.append(
            f"<tr class='{row_cls}'><td>{idx+1}</td><td>{log.get('timestamp','')}</td><td>{log.get('level','')}</td><td>{log.get('message','')}</td></tr>"
        )

    html.extend([
        "</table>",
        "<h2>Exception Logs</h2>",
        "<ul>"
    ])

    for ex in exception_logs:
        html.append(
            f"<li><b>{ex.get('timestamp','')}</b> [{ex.get('level','')}] {ex.get('message','')}</li>"
        )
    html.extend([
        "</ul>",
        "</body>",
        "</html>"
    ])

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(html))
    return output_path

if __name__ == "__main__":
    # Example usage
    results = [
        {"timestamp": "2025-06-09 12:00:00", "level": "INFO", "message": "Start process"},
        {"timestamp": "2025-06-09 12:01:00", "level": "ERROR", "message": "File not found error: config.ini"},
        {"timestamp": "2025-06-09 12:02:00", "level": "WARNING", "message": "Low memory"},
        {"timestamp": "2025-06-09 12:03:00", "level": "CRITICAL", "message": "Unhandled exception occurred"}
    ]
    exceptions = [
        {"timestamp": "2025-06-09 12:01:00", "level": "ERROR", "message": "File not found error: config.ini"},
        {"timestamp": "2025-06-09 12:03:00", "level": "CRITICAL", "message": "Unhandled exception occurred"}
    ]
    path = generate_html_report(results, exceptions)
    print(f"HTML report generated: {path}")