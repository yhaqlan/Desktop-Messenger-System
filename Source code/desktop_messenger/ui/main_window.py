from PySide6.QtCore import Signal
from PySide6.QtWidgets import QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QMainWindow, QPushButton, QStackedWidget, QVBoxLayout, QWidget

from .pages.chats import ChatsPage
from .pages.friends import FriendsPage
from .pages.network import NetworkPage
from .pages.notifications import NotificationsPage
from .pages.profile import ProfilePage
from .pages.settings import SettingsPage


class MainWindow(QMainWindow):
    logged_out = Signal()

    def __init__(self, repository, current_user, parent=None):
        super().__init__(parent)
        self.repository = repository
        self.current_user = current_user
        self.setWindowTitle("Desktop Messenger")
        self.resize(1180, 760)
        shell = QWidget(); row = QHBoxLayout(shell); row.setContentsMargins(0, 0, 0, 0); row.setSpacing(0)
        sidebar = QWidget(); sidebar.setObjectName("sidebar"); side = QVBoxLayout(sidebar)
        brand = QLabel("DM")
        brand.setObjectName("brandBadge")
        who = QLabel(current_user["display_name"])
        who.setObjectName("sidebarIdentity")
        self.nav = QListWidget(); self.nav.setObjectName("navigation")
        self.stack = QStackedWidget()
        pages = [
            ("Chats", ChatsPage),
            ("Friends", FriendsPage),
            ("Notifications", NotificationsPage),
            ("Network", NetworkPage),
            ("Profile", ProfilePage),
            ("Settings", SettingsPage),
        ]
        for label, page_class in pages:
            self.nav.addItem(QListWidgetItem(label))
            self.stack.addWidget(page_class(repository, current_user))
        self.nav.currentRowChanged.connect(self.stack.setCurrentIndex)
        self.nav.setCurrentRow(0)
        logout = QPushButton("Logout")
        logout.setObjectName("logoutButton")
        logout.clicked.connect(self._logout)
        side.addWidget(brand)
        side.addWidget(who)
        side.addWidget(self.nav, 1)
        side.addWidget(logout)
        row.addWidget(sidebar)
        row.addWidget(self.stack, 1)
        self.setCentralWidget(shell)

    def _logout(self):
        self.close()
        self.logged_out.emit()
