import json
import os
import webbrowser

from rptp.config import SESSION_BASE_PATH, TOKEN
from rptp.report import form_sessions_report, SESSIONS_HTML

if __name__ == '__main__':
    if os.path.exists(SESSION_BASE_PATH):
        with open(SESSION_BASE_PATH) as f:
            sessions = json.load(f)

        report = form_sessions_report(sessions)

        webbrowser.open(SESSIONS_HTML)
    else:
        print('No sessions found!')
