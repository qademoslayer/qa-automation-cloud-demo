import datetime

def generate_html_report(test_results: dict, output_path="report.html"):
    html_content = f"""
    <html>
        <head>
            <title>Test Summary Report</title>
        </head>
        <body>
            <h1>Automation Test Summary</h1>
            <p>Date: {datetime.datetime.now()}</p>
            <hr>
            <h2>Summary:</h2>
            <ul>
                <li>Passed: {test_results.get('passed')}</li>
                <li>Failed: {test_results.get('failed')}</li>
                <li>Total: {test_results.get('total')}</li>
            </ul>
        </body>
    </html>
    """
    with open(output_path, "w") as f:
        f.write(html_content)

    return output_path
