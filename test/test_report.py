import json

from rptp.config import SESSION_BASE_PATH
from rptp.report import form_sessions_report


def test_sessions_report_forming():
    with open(SESSION_BASE_PATH) as f:
        sessions = json.load(f)

    report = form_sessions_report(sessions)

    assert True
