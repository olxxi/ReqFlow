HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reflow Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f9f9f9; }}
        h1 {{ text-align: center; color: #333; }}
        .log {{ border: 1px solid #ccc; margin-bottom: 20px; padding: 10px; border-radius: 5px; background-color: #fff; }}
        .log-header {{ cursor: pointer; padding: 5px; background-color: #f7f7f7; border-bottom: 1px solid #ccc; }}
        .log-body {{ display: none; padding: 10px; }}
        .log-header:hover {{ background-color: #eaeaea; }}
        .status-success {{ color: green; }}
        .status-failure {{ color: red; }}
        .status-warning {{ color: orange; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 8px 12px; border: 1px solid #ccc; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    <h1>{report_name} - {date}</h1>
    {log_entries}
    <script>
        function toggleLog(header) {{
            const body = header.nextElementSibling;
            body.style.display = body.style.display === 'block' ? 'none' : 'block';
        }}
    </script>
</body>
</html>
"""
