"""
Courtesy of Stackoverflow:

http://stackoverflow.com/questions/19966056/
pyqt5-how-can-i-connect-a-qpushbutton-to-a-slot
"""
from client.Client import ClientLogic

from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QTextEdit
)


class Window(QWidget):

    def __init__(self):

        super(Window, self).__init__()
        self.setWindowTitle("Sloppy GUI")
        self.setMinimumSize(320, 300)

        self.button = QPushButton("Search", self)
        self.button.clicked.connect(self.handleSearchButton)
        self.textArea = QTextEdit(self)

        self.label = QLabel(self)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.textArea)
        layout.addWidget(self.button)


    def handleSearchButton(self):
        """
        """
        name = self.textArea.toPlainText()

        client = ClientLogic()
        bookingRef = client.fetchBookingRef(name)

        self.label.setText(bookingRef)



def main():
    """
    Runs the GUI.
    """
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    import sys
    main()