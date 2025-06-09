# Log Analysis Tool

This tool integrates **log extraction, parsing, exception detection, HTML report generation, and a graphical interface** for local batch log analysis. It supports common log formats and archives, highlights exceptions, and produces structured HTML reports.

---

## Project Structure

```
log_extractor.py           # Log extraction module
log_parser.py              # Log parsing module
exception_detector.py      # Exception detection module
html_reporter.py           # HTML report generation module
log_gui.py                 # GUI main program
log_report_template.html   # Optional: Custom HTML template
README.md                  # Usage instructions
```

---

## 1. Environment Preparation

1. **Install Python 3 (recommended 3.7 or above)**
2. **This tool only depends on Python standard libraries.**
   - If you want to use custom HTML templates (like `log_report_template.html`), you may integrate a template engine like `jinja2` as needed.

---

## 2. Quick Start with GUI

1. **Put all modules in the same directory.**
2. **Run the main program:**
    ```bash
    python log_gui.py
    ```
3. **Usage steps:**
   - Click "Browse" to select a log archive (`.zip`, `.tar.gz`, `.tgz` supported).
   - Click "Extract and Analyze" to automatically extract, parse, and detect exceptions.
   - View logs and highlighted exceptions in the interface. Double-click any row to see details.

---

## 3. Command-Line/Script Mode for HTML Reports

1. **Extract log files:**
    ```python
    from log_extractor import extract_log
    files = extract_log('your_log.zip')
    ```

2. **Parse log files:**
    ```python
    from log_parser import parse_log_file
    log_pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \[(\w+)\] (.*)"
    fields = ["timestamp", "level", "message"]
    parsed_logs = parse_log_file(files[0], log_pattern, fields)
    ```

3. **Detect exception logs:**
    ```python
    from exception_detector import detect_exceptions
    exceptions = detect_exceptions(parsed_logs)
    ```

4. **Generate HTML report:**
    ```python
    from html_reporter import generate_html_report
    html_path = generate_html_report(parsed_logs, exceptions, output_path="log_report.html")
    print(f"Report generated: {html_path}")
    ```

---

## 4. Customization & Extension

- **Log format adaptation**  
  Adjust the regex and fields in `log_parser.py` to support your log format.
- **Custom exception keywords**  
  Set your own keyword list in `exception_detector.py`.
- **HTML style customization**  
  Edit `log_report_template.html` or the style section of `html_reporter.py`.
- **Batch/multi-file processing**  
  Extend the main program or modules to loop over all files as needed.
- **Web version, multi-language, localization, etc.**  
  You can extend this project for your business needs.

---

## 5. FAQ

- **No log file found**  
  Make sure the archive contains a `.log` or `.txt` file.
- **Encoding/character display issues**  
  Ensure log files are UTF-8 encoded, or adjust the encoding argument in the code.
- **Archive format not supported**  
  Add more archive format support in `log_extractor.py` if needed.

---

## 6. Contact

For issues, suggestions, or custom requirements, please open an issue or contact the author.
