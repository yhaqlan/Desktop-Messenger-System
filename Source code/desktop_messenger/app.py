from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from .config import AppConfig
from .database import MessengerRepository
from .ui.login_window import LoginWindow
from .ui.main_window import MainWindow


class DesktopMessengerApplication:
    def __init__(self):
        self.qt = QApplication(sys.argv)
        qss = Path(__file__).parent / "ui" / "assets" / "dark.qss"
        self.qt.setStyleSheet(qss.read_text(encoding="utf-8"))
        config = AppConfig.load(Path("config.json"))
        self.repository = MessengerRepository(config.database_path)
        self.login = LoginWindow(self.repository)
        self.main: MainWindow | None = None
        self.login.authenticated.connect(self._open_main)

    def _open_main(self, user):
        self.login.hide()
        self.main = MainWindow(self.repository, user)
        self.main.logged_out.connect(self._return_to_login)
        self.main.show()

    def _return_to_login(self):
        self.main = None
        self.login.show()

    def run(self) -> int:
        self.login.show()
        return self.qt.exec()


def main() -> int:
    return DesktopMessengerApplication().run()
