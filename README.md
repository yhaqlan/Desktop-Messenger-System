# Desktop Messenger

A team course project exploring desktop messaging, local storage, and network communication.

## Team

Created collaboratively by [yhaqlan](https://github.com/yhaqlan) and [Ali](https://github.com/Ali20280).

## Project overview

The primary application is a Python desktop messenger using PySide6 and SQLite. The source includes account and chat data models, synchronization logic, LAN and relay transport examples, and authenticated message encryption. A source-only Flutter companion prototype is included under Android - IOS.

## Run the desktop source

1. Install Python 3.11 or later.
2. Open a terminal in Source code.
3. Install dependencies with python -m pip install -r requirements.txt.
4. Start the app with python run_desktop_messenger.py.

See Source code/README.md for the source package details and additional commands.

## Repository contents

- Source code/ — primary Python application and core tests.
- Android - IOS/ — experimental Flutter companion source.
- Database/, DFD Diagrams/, UML Diagrams/, and UI_UX/ — schema and design artifacts.
- DOCUMENTATION/ and Project Management/ — project report and plan.
- Published/ — Windows build configuration and validation checklist.

## Scope and validation

The included package identifies itself as an academic reconstruction based on reference materials; see RECONSTRUCTION_NOTICE.md. The Windows executable and local SQLite database are not included. The notice and validation documents describe which platform and multi-device scenarios still need testing. The Flutter companion is source-only and does not claim feature parity with the desktop app.

This repository does not include a license. Contact the team before reusing the project.
