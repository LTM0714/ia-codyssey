import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic

form_class=uic.loadUiType("2-3/calculator.ui")[0]


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.btn_number_1.clicked.connect(lambda state, button=self.btn_number_1: self.NumClicked(state, button))
        self.btn_number_2.clicked.connect(lambda state, button=self.btn_number_2: self.NumClicked(state, button))
        self.btn_number_3.clicked.connect(lambda state, button=self.btn_number_3: self.NumClicked(state, button))
        self.btn_number_4.clicked.connect(lambda state, button=self.btn_number_4: self.NumClicked(state, button))
        self.btn_number_5.clicked.connect(lambda state, button=self.btn_number_5: self.NumClicked(state, button))
        self.btn_number_6.clicked.connect(lambda state, button=self.btn_number_6: self.NumClicked(state, button))
        self.btn_number_7.clicked.connect(lambda state, button=self.btn_number_7: self.NumClicked(state, button))
        self.btn_number_8.clicked.connect(lambda state, button=self.btn_number_8: self.NumClicked(state, button))
        self.btn_number_9.clicked.connect(lambda state, button=self.btn_number_9: self.NumClicked(state, button))
        self.btn_number_0.clicked.connect(lambda state, button=self.btn_number_0: self.NumClicked(state, button))
        self.btn_number_00.clicked.connect(lambda state, button=self.btn_number_00: self.NumClicked(state, button))

        self.btn_addition.clicked.connect(lambda state, button=self.btn_addition: self.StrClicked(state, button))
        self.btn_substraction.clicked.connect(lambda state, button=self.btn_substraction: self.StrClicked(state, button))
        self.btn_multiplication.clicked.connect(lambda state, button=self.btn_multiplication: self.StrClicked(state, button))
        self.btn_division.clicked.connect(lambda state, button=self.btn_division: self.StrClicked(state, button))
        self.btn_dot.clicked.connect(lambda state, button=self.btn_dot: self.StrClicked(state, button))

        self.btn_memory_1.clicked.connect(self.memory)
        self.btn_memory_2.clicked.connect(self.memory2)

        self.btn_lBracket.clicked.connect(lambda state, button=self.btn_lBracket: self.StrClicked(state, button))
        self.btn_rBracket.clicked.connect(lambda state, button=self.btn_rBracket: self.StrClicked(state, button))
        self.btn_AS.clicked.connect(lambda state, button=self.btn_AS: self.StrClicked(state, button))
        #self.btn_route.clicked.connect(self.routeClicked())
        self.btn_percent.clicked.connect(lambda state, button=self.btn_percent: self.StrClicked(state, button))

        self.btn_delete.clicked.connect(self.delete)
        self.btn_clear.clicked.connect(self.clear)

        self.btn_equal.clicked.connect(self.equal)

    def NumClicked(self, state, button):
        exist_line_text=self.lineEdit.text()
        now_num_text=button.text()

        self.lineEdit.setText(exist_line_text + now_num_text)

    def StrClicked(self, state, button):
        exist_line_text = self.lineEdit.text()
        now_num_text = button.text()

        self.lineEdit.setText(exist_line_text + now_num_text)

    def equal(self):
        line=self.lineEdit.text().replace(",","")
        result=eval(line)

        s1 = '{0:,}'.format(int(result))                    #정수
        s2 = '{0:0.2f}'.format(float(result)-int(result))   #소수
        s3=s1+s2                                            #합
        final = s3.replace("0.", ".")
        self.lineEdit.setText(final)

    def memory(self):
        result=self.lineEdit.text()
        self.le_saveResult.setText(result)

    def memory2(self):
        result=self.le_saveResult.text()
        self.lineEdit.setText(self.lineEdit.text()+result)

    def clear(self):
        self.lineEdit.clear()

    def delete(self):
        d=self.lineEdit.text()
        d=d[:-1]
        self.lineEdit.setText(d)


if __name__=='__main__':
    app=QApplication(sys.argv)
    myWindow=WindowClass()
    myWindow.show()
    app.exec_()
