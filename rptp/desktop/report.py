import json
import os
import webbrowser

from rptp.config import SESSION_BASE_PATH, SESSIONS_HTML
from rptp.report import form_sessions_report


def start_generate_report():
    if os.path.exists(SESSION_BASE_PATH):
        print('Loading sessions...')
        with open(SESSION_BASE_PATH) as f:
            sessions = json.load(f)

        print('Generating report...')
        report = form_sessions_report(sessions)

        print('Report created, opening browser...')
        webbrowser.open(SESSIONS_HTML)
    else:
        print('No sessions found!')
