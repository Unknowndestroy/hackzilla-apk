# gui_fixed.py

import sys
import socket
import requests
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QCursor
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QCheckBox, QLineEdit, QPushButton, QLabel, QMessageBox
)

def get_local_ip():
    """
    LAN’daki gerçek yerel IP'ni alır.
    Google DNS'e socket ile bağlanıp IP alıyoruz.
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"

LOCAL_IP = get_local_ip()
API_URL = f"http://{LOCAL_IP}:5000/set_command"

class HoverButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setStyleSheet("""
            QPushButton {
                background-color: #222;
                color: #fff;
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #444;
            }
        """)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

class HoverCheckBox(QCheckBox):
    def __init__(self, text):
        super().__init__(text)
        self.setStyleSheet("""
            QCheckBox {
                color: #fff;
                font-size: 14px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #fff;
                background-color: transparent;
                border-radius: 4px;
            }
            QCheckBox::indicator:checked {
                background-color: #e74c3c;
                border: 2px solid #e74c3c;
                border-radius: 4px;
            }
            QCheckBox:hover {
                color: #e74c3c;
            }
        """)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

class ControlPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📡 Kontrol Paneli - Hackzilla")
        self.setFixedSize(400, 300)
        self.setStyleSheet("background-color: #111;")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Başlık ve IP gösterimi
        title = QLabel(f"Hack By Unknown Destroyer\n[IP: {LOCAL_IP}]")
        title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #e74c3c;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # 1. Checkbox: Kilitle
        self.cb_lock = HoverCheckBox("Kilitle")
        self.cb_lock.stateChanged.connect(self.send_command)
        layout.addWidget(self.cb_lock)

        # 2. Checkbox + Textbox: Özel Mesaj
        msg_layout = QHBoxLayout()
        self.cb_msg = HoverCheckBox("Özel Mesaj")
        # Buraya state yerine toggled bağladık:
        self.cb_msg.toggled.connect(self.on_msg_checkbox_toggled)
        msg_layout.addWidget(self.cb_msg)

        self.txt_msg = QLineEdit()
        self.txt_msg.setPlaceholderText("Mesajını buraya yaz...")
        self.txt_msg.setEnabled(False)  # Başta kapalı
        self.txt_msg.setStyleSheet("""
            QLineEdit {
                background-color: #222;
                color: #fff;
                border: 2px solid #444;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
            QLineEdit:hover {
                border-color: #e74c3c;
            }
        """)
        self.txt_msg.returnPressed.connect(self.send_command)
        msg_layout.addWidget(self.txt_msg)
        layout.addLayout(msg_layout)

        # 3. Bildirim Gönder: Textbox + Buton
        notify_layout = QHBoxLayout()
        self.txt_notify = QLineEdit()
        self.txt_notify.setPlaceholderText("Bildirim metni...")
        self.txt_notify.setStyleSheet("""
            QLineEdit {
                background-color: #222;
                color: #fff;
                border: 2px solid #444;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
            QLineEdit:hover {
                border-color: #f1c40f;
            }
        """)
        notify_layout.addWidget(self.txt_notify)

        self.btn_notify = HoverButton("▶️ Gönder Bildirim")
        self.btn_notify.clicked.connect(self.on_notify_clicked)
        notify_layout.addWidget(self.btn_notify)
        layout.addLayout(notify_layout)

        # Durum etiketi
        self.lbl_status = QLabel("")
        self.lbl_status.setFont(QFont("Segoe UI", 10))
        self.lbl_status.setStyleSheet("color: #bbb;")
        self.lbl_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.lbl_status)

        self.setLayout(layout)

    def on_msg_checkbox_toggled(self, checked: bool):
        """
        checked True ise textbox'u aktif et, değilse pasif yap.
        Ayrıca, checkbox ve kilit durumu varsa hemen commit et.
        """
        self.txt_msg.setEnabled(checked)
        if not checked:
            self.txt_msg.clear()
        # Eğer şu an kilit checkbox'ı işaretliyse, komutu güncelle
        if self.cb_lock.isChecked():
            self.send_command()

    def on_notify_clicked(self):
        metin = self.txt_notify.text().strip()
        if not metin:
            QMessageBox.warning(self, "Uyarı", "Önce bildirim metnini gir lan!")
            return
        QMessageBox.information(self, "Gönderildi", f"Bildirim gönderildi: {metin}")
        self.txt_notify.clear()

    def send_command(self):
        """
        GUI'den ne durumda olduğumuzu al, API'ye POST yap.
        Kilit durumu ve mesaj (eğer checkbox işaretliyse) gönder.
        """
        komut = {
            "lock_screen": self.cb_lock.isChecked(),
            "message": self.txt_msg.text().strip() if self.cb_msg.isChecked() else ""
        }
        try:
            resp = requests.post(API_URL, json=komut, timeout=3)
            if resp.status_code == 200:
                self.lbl_status.setText("Komut gönderildi 🥷")
                self.lbl_status.setStyleSheet("color: #2ecc71;")
            else:
                self.lbl_status.setText("API hatası... 🤡")
                self.lbl_status.setStyleSheet("color: #e74c3c;")
        except Exception:
            self.lbl_status.setText("Bağlantı yok, API’yi ayarla! 💀")
            self.lbl_status.setStyleSheet("color: #e74c3c;")

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QWidget {
            font-family: 'Segoe UI';
        }
    """)
    panel = ControlPanel()
    panel.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
