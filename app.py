import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
import requests

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PCR Trader Pro")

        layout = QVBoxLayout()
        self.label = QLabel("Loading...")

        layout.addWidget(self.label)
        self.setLayout(layout)

        self.update()

    def update(self):
        url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"
        headers = {"User-Agent": "Mozilla/5.0"}

        session = requests.Session()
        session.get("https://www.nseindia.com", headers=headers)
        data = session.get(url, headers=headers).json()

        records = data["records"]["data"]

        ce = sum(r.get("CE", {}).get("openInterest", 0) for r in records if "CE" in r)
        pe = sum(r.get("PE", {}).get("openInterest", 0) for r in records if "PE" in r)

        pcr = round(pe / ce if ce else 0, 2)

        self.label.setText(f"NIFTY PCR: {pcr}")


app = QApplication(sys.argv)
window = App()
window.show()
sys.exit(app.exec_())
