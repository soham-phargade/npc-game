from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout, QDesktopWidget

class TextInputDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Input Dialog")
        self.setGeometry(100, 100, 400, 300)
        self.center()

        self.layout = QVBoxLayout()

        self.text_edit = QTextEdit(self)
        self.layout.addWidget(self.text_edit)

        self.button_layout = QHBoxLayout()

        self.submit_button = QPushButton("Submit", self)
        self.submit_button.clicked.connect(self.submit)
        self.button_layout.addWidget(self.submit_button)

        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.reject)
        self.button_layout.addWidget(self.cancel_button)

        self.layout.addLayout(self.button_layout)

        self.setLayout(self.layout)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def submit(self):
        self.user_input = self.text_edit.toPlainText()
        self.accept()

def get_user_input():
    app = QApplication([])
    dialog = TextInputDialog()
    if dialog.exec_() == QDialog.Accepted:
        return dialog.user_input
    return None

if __name__ == '__main__':
    input_value = get_user_input()
    if input_value:
        print(f"User input: {input_value}")
    else:
        print("User cancelled the input.")
