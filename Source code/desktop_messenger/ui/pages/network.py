from PySide6.QtWidgets import QFormLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSpinBox, QVBoxLayout, QWidget

from ..widgets import PageHeader, StatusPill


class NetworkPage(QWidget):
    def __init__(self, repository, current_user, parent=None):
        super().__init__(parent)
        self.repository = repository
        self.current_user = current_user
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        top = QHBoxLayout()
        top.addWidget(PageHeader("Network", "Offline, LAN/Hotspot, and demonstration relay modes"), 1)
        top.addWidget(StatusPill("Offline", online=False))
        layout.addLayout(top)

        lan = QGroupBox("LAN / Hotspot - port 8765")
        lan_form = QFormLayout(lan)
        host_ip = QLineEdit("192.168.1.10")
        lan_port = QSpinBox(); lan_port.setRange(1, 65535); lan_port.setValue(8765)
        lan_buttons = QHBoxLayout()
        lan_buttons.addWidget(QPushButton("Host Chat Server"))
        lan_buttons.addWidget(QPushButton("Join Local Server"))
        lan_form.addRow("Server IPv4", host_ip)
        lan_form.addRow("Port", lan_port)
        lan_form.addRow(lan_buttons)
        layout.addWidget(lan)

        relay = QGroupBox("Internet Relay - port 9876")
        relay_form = QFormLayout(relay)
        address = QLineEdit("127.0.0.1")
        address.setToolTip("127.0.0.1 is this computer, not a public relay")
        relay_port = QSpinBox(); relay_port.setRange(1, 65535); relay_port.setValue(9876)
        password = QLineEdit(); password.setEchoMode(QLineEdit.Password)
        relay_buttons = QHBoxLayout()
        relay_buttons.addWidget(QPushButton("Register / Connect"))
        relay_buttons.addWidget(QPushButton("Disconnect / Offline"))
        relay_form.addRow("Server address", address)
        relay_form.addRow("Port", relay_port)
        relay_form.addRow("Password", password)
        relay_form.addRow(relay_buttons)
        layout.addWidget(relay)
        notice = QLabel("The reconstructed networking services are executable from the included command-line launchers. This page preserves the intended control surface; platform integration should be validated on Windows.")
        notice.setObjectName("infoCallout")
        notice.setWordWrap(True)
        layout.addWidget(notice)
        layout.addStretch()
