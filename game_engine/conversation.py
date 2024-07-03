from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout, QDesktopWidget

def get_user_input():
    app = QApplication([])
    text_edit = QTextEdit()
    submit_button = QPushButton("Submit")
    cancel_button = QPushButton("Cancel")

    layout = QVBoxLayout()
    layout.addWidget(text_edit)

    button_layout = QHBoxLayout()
    button_layout.addWidget(submit_button)
    button_layout.addWidget(cancel_button)

    layout.addLayout(button_layout)

    dialog = QDialog()
    dialog.setWindowTitle("Input Dialog")
    dialog.setGeometry(QDesktopWidget().availableGeometry().center().x() - 200,
                        QDesktopWidget().availableGeometry().center().y() - 150, 400, 300)
    dialog.setLayout(layout)

    def submit():
        dialog.user_input = text_edit.toPlainText()
        dialog.accept()

    submit_button.clicked.connect(submit)
    cancel_button.clicked.connect(dialog.reject)

    if dialog.exec_() == QDialog.Accepted:
        return dialog.user_input
    return None

if __name__ == '__main__':
    input_value = get_user_input()
    if input_value:
        print(f"User input: {input_value}")
    else:
        print("User cancelled the input.")
