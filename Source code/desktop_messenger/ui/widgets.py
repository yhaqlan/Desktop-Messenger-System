from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout


class PageHeader(QFrame):
    def __init__(self, title: str, subtitle: str = "", parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        label = QLabel(title)
        label.setObjectName("pageTitle")
        layout.addWidget(label)
        if subtitle:
            note = QLabel(subtitle)
            note.setObjectName("pageSubtitle")
            note.setWordWrap(True)
            layout.addWidget(note)


class StatusPill(QFrame):
    def __init__(self, label: str, online: bool = False, parent=None):
        super().__init__(parent)
        self.setObjectName("statusPillOnline" if online else "statusPillOffline")
        row = QHBoxLayout(self)
        row.setContentsMargins(10, 4, 10, 4)
        text = QLabel(label)
        text.setAlignment(Qt.AlignCenter)
        row.addWidget(text)
