from utils.html_report import generate_html_report

def test_generate_html():
    result = {
        "passed": 5,
        "failed": 1,
        "total": 6
    }
    path = generate_html_report(result)
    assert "report.html" in path
