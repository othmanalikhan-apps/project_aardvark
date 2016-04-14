from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import QDate
from PyQt5.QtCore import QMetaObject
from PyQt5.QtCore import QRect
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QCalendarWidget
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtWidgets import QSplitter
from PyQt5.QtWidgets import QTimeEdit
from PyQt5.QtWidgets import QWidget

class Ui_Booking(object):
	def setupUi(self, Booking):
		Booking.setObjectName("Booking")
		Booking.resize(932, 576)
		sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(Booking.sizePolicy().hasHeightForWidth())
		Booking.setSizePolicy(sizePolicy)
		Booking.setStyleSheet("")
		self.lblBooking = QLabel(Booking)
		self.lblBooking.setGeometry(QRect(30, 10, 150, 70))

		font = QFont()
		font.setPointSize(24)

		self.lblBooking.setFont(font)
		self.lblBooking.setStyleSheet("")
		self.lblBooking.setFrameShape(QFrame.NoFrame)
		self.lblBooking.setFrameShadow(QFrame.Plain)
		self.lblBooking.setLineWidth(10)
		self.lblBooking.setObjectName("lblBooking")

		self.spnTable = QSpinBox(Booking)
		self.spnTable.setGeometry(QRect(672, 697, 46, 28))
		self.spnTable.setObjectName("spnTable")

		self.btnBook = QPushButton(Booking)
		self.btnBook.setEnabled(False)
		self.btnBook.setGeometry(QRect(30, 540, 181, 28))

		font = QFont()
		font.setPointSize(14)

		self.btnBook.setFont(font)
		self.btnBook.setCheckable(False)
		self.btnBook.setObjectName("btnBook")

		self.layoutWidget = QWidget(Booking)
		self.layoutWidget.setGeometry(QRect(20, 400, 361, 131))
		self.layoutWidget.setObjectName("layoutWidget")

		self.formLayout = QFormLayout(self.layoutWidget)
		self.formLayout.setContentsMargins(11, 11, 11, 11)
		self.formLayout.setSpacing(6)
		self.formLayout.setObjectName("formLayout")

		self.lblCustomer = QLabel(self.layoutWidget)

		font = QFont()
		font.setPointSize(12)

		self.lblCustomer.setFont(font)
		self.lblCustomer.setObjectName("lblCustomer")

		self.formLayout.setWidget(0, QFormLayout.LabelRole, self.lblCustomer)

		self.lnCustomer = QLineEdit(self.layoutWidget)
		self.lnCustomer.setObjectName("lnCustomer")

		self.formLayout.setWidget(0, QFormLayout.FieldRole, self.lnCustomer)

		self.lblEmail = QLabel(self.layoutWidget)

		font = QFont()
		font.setPointSize(12)

		self.lblEmail.setFont(font)
		self.lblEmail.setObjectName("lblEmail")

		self.formLayout.setWidget(1, QFormLayout.LabelRole, self.lblEmail)

		self.lnEmail = QLineEdit(self.layoutWidget)
		self.lnEmail.setObjectName("lnEmail")

		self.formLayout.setWidget(1, QFormLayout.FieldRole, self.lnEmail)

		self.lblPhone = QLabel(self.layoutWidget)

		font = QFont()
		font.setPointSize(12)

		self.lblPhone.setFont(font)
		self.lblPhone.setObjectName("lblPhone")

		self.formLayout.setWidget(2, QFormLayout.LabelRole, self.lblPhone)

		self.lnPhone = QLineEdit(self.layoutWidget)
		self.lnPhone.setObjectName("lnPhone")

		self.formLayout.setWidget(2, QFormLayout.FieldRole, self.lnPhone)

		self.widget = QWidget(Booking)
		self.widget.setGeometry(QRect(20, 81, 882, 277))
		self.widget.setObjectName("widget")

		self.gridLayout = QGridLayout(self.widget)
		self.gridLayout.setContentsMargins(11, 11, 11, 11)
		self.gridLayout.setSpacing(6)
		self.gridLayout.setObjectName("gridLayout")

		self.lblImage = QLabel(self.widget)
		sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.lblImage.sizePolicy().hasHeightForWidth())
		self.lblImage.setSizePolicy(sizePolicy)
		self.lblImage.setFrameShape(QFrame.Box)
		self.lblImage.setLineWidth(0)
		self.lblImage.setText("")
		self.lblImage.setPixmap(QPixmap("images/tables.png"))
		self.lblImage.setObjectName("lblImage")

		self.gridLayout.addWidget(self.lblImage, 0, 0, 2, 1)

		self.clnDate = QCalendarWidget(self.widget)
		self.clnDate.setGridVisible(True)

		sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.clnDate.sizePolicy().hasHeightForWidth())

		self.clnDate.setSizePolicy(sizePolicy)
		self.clnDate.setObjectName("clnDate")

		self.gridLayout.addWidget(self.clnDate, 0, 1, 1, 1)
		self.splitter = QSplitter(self.widget)
		sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
		self.splitter.setSizePolicy(sizePolicy)
		self.splitter.setOrientation(Qt.Horizontal)
		self.splitter.setObjectName("splitter")

		self.lblTime = QLabel(self.splitter)
		sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.lblTime.sizePolicy().hasHeightForWidth())
		self.lblTime.setSizePolicy(sizePolicy)

		font = QFont()
		font.setPointSize(12)

		self.lblTime.setFont(font)
		self.lblTime.setObjectName("lblTime")

		self.timeEdit = QTimeEdit(self.splitter)
		sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.timeEdit.sizePolicy().hasHeightForWidth())
		self.timeEdit.setSizePolicy(sizePolicy)
		self.timeEdit.setFrame(True)
		self.timeEdit.setMaximumDate(QDate(2000, 1, 1))
		self.timeEdit.setTimeSpec(Qt.LocalTime)
		self.timeEdit.setObjectName("timeEdit")

		self.gridLayout.addWidget(self.splitter, 1, 1, 1, 1)

		self.widget1 = QWidget(Booking)
		self.widget1.setGeometry(QRect(520, 400, 381, 160))
		self.widget1.setObjectName("widget1")

		self.gridLayout_2 = QGridLayout(self.widget1)
		self.gridLayout_2.setContentsMargins(11, 11, 11, 11)
		self.gridLayout_2.setSpacing(6)
		self.gridLayout_2.setObjectName("gridLayout_2")
		self.lblDate_2 = QLabel(self.widget1)
		sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.lblDate_2.sizePolicy().hasHeightForWidth())
		self.lblDate_2.setSizePolicy(sizePolicy)
		font = QFont()
		font.setPointSize(12)
		self.lblDate_2.setFont(font)
		self.lblDate_2.setLayoutDirection(Qt.LeftToRight)
		self.lblDate_2.setObjectName("lblDate_2")
		self.gridLayout_2.addWidget(self.lblDate_2, 0, 0, 1, 1)
		self.lblTime_2 = QLabel(self.widget1)
		sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.lblTime_2.sizePolicy().hasHeightForWidth())
		self.lblTime_2.setSizePolicy(sizePolicy)
		font = QFont()
		font.setPointSize(12)
		self.lblTime_2.setFont(font)
		self.lblTime_2.setObjectName("lblTime_2")
		self.gridLayout_2.addWidget(self.lblTime_2, 1, 0, 1, 1)
		self.lnDateDisplay = QLineEdit(self.widget1)
		self.lnDateDisplay.setEnabled(True)
		sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.lnDateDisplay.sizePolicy().hasHeightForWidth())
		self.lnDateDisplay.setSizePolicy(sizePolicy)
		self.lnDateDisplay.setFrame(True)
		self.lnDateDisplay.setReadOnly(True)
		self.lnDateDisplay.setObjectName("lnDateDisplay")
		self.gridLayout_2.addWidget(self.lnDateDisplay, 0, 1, 1, 1)
		self.lnRefNo = QLineEdit(self.widget1)
		self.lnRefNo.setEnabled(True)
		sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.lnRefNo.sizePolicy().hasHeightForWidth())
		self.lnRefNo.setSizePolicy(sizePolicy)
		self.lnRefNo.setFrame(True)
		self.lnRefNo.setReadOnly(True)
		self.lnRefNo.setObjectName("lnRefNo")
		self.gridLayout_2.addWidget(self.lnRefNo, 3, 1, 1, 1)
		self.lnTime = QLineEdit(self.widget1)
		self.lnTime.setEnabled(True)
		sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.lnTime.sizePolicy().hasHeightForWidth())
		self.lnTime.setSizePolicy(sizePolicy)
		self.lnTime.setFrame(True)
		self.lnTime.setReadOnly(True)
		self.lnTime.setObjectName("lnTime")
		self.gridLayout_2.addWidget(self.lnTime, 1, 1, 1, 1)
		self.lnTableNo = QLineEdit(self.widget1)
		self.lnTableNo.setEnabled(True)
		sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.lnTableNo.sizePolicy().hasHeightForWidth())
		self.lnTableNo.setSizePolicy(sizePolicy)
		self.lnTableNo.setFrame(True)
		# self.lnTableNo.setReadOnly(True)
		self.lnTableNo.setObjectName("lnTableNo")
		self.gridLayout_2.addWidget(self.lnTableNo, 2, 1, 1, 1)
		self.lblRef = QLabel(self.widget1)
		sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.lblRef.sizePolicy().hasHeightForWidth())
		self.lblRef.setSizePolicy(sizePolicy)
		font = QFont()
		font.setPointSize(12)
		self.lblRef.setFont(font)
		self.lblRef.setObjectName("lblRef")
		self.gridLayout_2.addWidget(self.lblRef, 3, 0, 1, 1)
		self.lblTable_2 = QLabel(self.widget1)
		sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.lblTable_2.sizePolicy().hasHeightForWidth())
		self.lblTable_2.setSizePolicy(sizePolicy)
		font = QFont()
		font.setPointSize(12)
		self.lblTable_2.setFont(font)
		self.lblTable_2.setObjectName("lblTable_2")
		self.gridLayout_2.addWidget(self.lblTable_2, 2, 0, 1, 1)
		self.lblCustomer.setBuddy(self.lnCustomer)
		self.lblEmail.setBuddy(self.lnEmail)
		self.lblPhone.setBuddy(self.lnPhone)
		self.lblTime.setBuddy(self.timeEdit)
		self.lblDate_2.setBuddy(self.lnDateDisplay)
		self.lblTime_2.setBuddy(self.lnTime)
		self.lblRef.setBuddy(self.lnRefNo)
		self.lblTable_2.setBuddy(self.lnTableNo)

		self.retranslateUi(Booking)
		QMetaObject.connectSlotsByName(Booking)

		self.makeConnecion()
		self.makeBooking()

	def retranslateUi(self, Booking):
		_translate = QCoreApplication.translate
		Booking.setWindowTitle(_translate("Booking", "Booking"))
		self.lblBooking.setText(_translate("Booking", "Booking"))
		self.btnBook.setText(_translate("Booking", "Make booking"))
		self.lblCustomer.setText(_translate("Booking", "Customer name:"))
		self.lblEmail.setText(_translate("Booking", "Email address:"))
		self.lblPhone.setText(_translate("Booking", "Phone number:"))
		self.lblTime.setText(_translate("Booking", "Time:"))
		self.timeEdit.setDisplayFormat(_translate("Booking", "hh:mm a"))
		self.lblDate_2.setText(_translate("Booking", "Date:"))
		self.lblTime_2.setText(_translate("Booking", "Time:"))
		self.lblRef.setText(_translate("Booking", "Reference number:"))
		self.lblTable_2.setText(_translate("Booking", "Table number:"))

	@pyqtSlot()
	def bookButtonEnable(self):
		items = [
			self.lnCustomer, self.lnPhone, self.lnEmail,
			self.lnTableNo, self.lnTime, self.lnDateDisplay,
			# self.lnRefNo
		]

		state = []

		for x in items:
			if len(x.text()) > 0:
				state.append(True)
			else: state.append(False)

		if list(set(state)) == [True]:
			self.btnBook.setEnabled(True)
		else:
			self.btnBook.setEnabled(False)


	@pyqtSlot()
	def changeDate(self):
		formatted_date = "%s" % self.clnDate.selectedDate().toString()
		self.lnDateDisplay.setText(formatted_date)


	# @pyqtSlot()
	def makeConnecion(self):
		self.lnCustomer.textChanged.connect(self.bookButtonEnable)
		self.lnPhone.textChanged.connect(self.bookButtonEnable)
		self.lnEmail.textChanged.connect(self.bookButtonEnable)
		self.lnTableNo.textChanged.connect(self.bookButtonEnable)

		self.timeEdit.timeChanged.connect(
			lambda: self.lnTime.setText(self.timeEdit.text()))

		self.clnDate.selectionChanged.connect(self.changeDate)

	@pyqtSlot()
	def makeBooking(self):
		# print("yes")
		pass


if __name__ == "__main__":
	import sys
	app = QApplication(sys.argv)
	Booking = QWidget()
	ui = Ui_Booking()
	ui.setupUi(Booking)
	Booking.show()
	sys.exit(app.exec_())

