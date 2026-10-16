from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from ..widgets import PageHeader


class ProfilePage(QWidget):
    def __init__(self, repository, current_user, parent=None):
        super().__init__(parent)
        self.repository = repository
        self.current_user = current_user
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.addWidget(PageHeader('Profile', 'Local account identity'))
        empty = QLabel('Update your display name and optional profile image.')
        empty.setObjectName("emptyState")
        empty.setAlignment(Qt.AlignCenter)
        empty.setWordWrap(True)
        layout.addWidget(empty, 1)
