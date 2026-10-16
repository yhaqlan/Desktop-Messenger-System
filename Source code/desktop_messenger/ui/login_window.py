from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFormLayout, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QPushButton, QTabWidget, QVBoxLayout, QWidget


class LoginWindow(QWidget):
    authenticated = Signal(object)

    def __init__(self, repository, parent=None):
        super().__init__(parent)
        self.repository = repository
        self.setWindowTitle("Desktop Messenger")
        self.resize(540, 560)
        shell = QVBoxLayout(self)
        title = QLabel("Desktop Messenger")
        title.setObjectName("brandTitle")
        subtitle = QLabel("Offline • LAN • Relay • Encrypted")
        subtitle.setObjectName("brandSubtitle")
        shell.addWidget(title)
        shell.addWidget(subtitle)
        tabs = QTabWidget()
        tabs.addTab(self._login_tab(), "Sign in")
        tabs.addTab(self._register_tab(), "Create account")
        shell.addWidget(tabs, 1)

    def _login_tab(self):
        page = QWidget(); form = QFormLayout(page)
        self.login_username = QLineEdit(); self.login_username.setPlaceholderText("username")
        self.login_password = QLineEdit(); self.login_password.setEchoMode(QLineEdit.Password)
        button = QPushButton("Sign in")
        button.clicked.connect(self._sign_in)
        form.addRow("Username", self.login_username)
        form.addRow("Password", self.login_password)
        form.addRow(button)
        return page

    def _register_tab(self):
        page = QWidget(); form = QFormLayout(page)
        self.register_username = QLineEdit()
        self.register_display = QLineEdit()
        self.register_email = QLineEdit()
        self.register_password = QLineEdit(); self.register_password.setEchoMode(QLineEdit.Password)
        button = QPushButton("Create local account")
        button.clicked.connect(self._register)
        form.addRow("Username", self.register_username)
        form.addRow("Display name", self.register_display)
        form.addRow("Email (optional)", self.register_email)
        form.addRow("Password", self.register_password)
        form.addRow(button)
        return page

    def _sign_in(self):
        user = self.repository.authenticate(self.login_username.text(), self.login_password.text())
        if user is None:
            QMessageBox.warning(self, "Sign in failed", "Invalid username or password.")
            return
        self.authenticated.emit(user)

    def _register(self):
        try:
            user = self.repository.create_user(
                self.register_username.text(),
                self.register_display.text(),
                self.register_password.text(),
                self.register_email.text() or None,
            )
        except Exception as exc:
            QMessageBox.warning(self, "Registration failed", str(exc))
            return
        QMessageBox.information(self, "Account created", "The account was created in the local SQLite database.")
        self.authenticated.emit(user)
