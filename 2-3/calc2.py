import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic

form_class=uic.loadUiType("2-3/calculator.ui")[0]


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        number_buttons = [
            self.btn_number_1, self.btn_number_2, self.btn_number_3,
            self.btn_number_4, self.btn_number_5, self.btn_number_6,
            self.btn_number_7, self.btn_number_8, self.btn_number_9, self.btn_number_0
        ]

        for btn in number_buttons:
            # btn.clicked.connect(): 버튼을 클릭했을 때 어떤 함수를 실행할지 정해주는 코드
            # lambda는 함수를 만들겠다는 뜻(이름이 없는 익명 함수)
            # state는 PyQt의 clicked 시그널이 bool 하나를 넘기기 때문에 필요함
            # button=btn: lambda 함수가 만들어질 그 순간의 btn을 기억하라는 뜻
            # 만일 lambda state: self.NumClicked(state, btn)로 작성하면, 모든 lambda가 마지막 버튼만 기억(btn=btn_number_0)하게 됨
            # def func(매개변수1, 매개변수2=기본값): return 표현식
            btn.clicked.connect(lambda state, button=btn: self.NumClicked(state, button))

        # 연산자 버튼들을 딕셔너리에 저장
        operator_buttons = {
            'btn_addition': self.btn_addition,
            'btn_substraction': self.btn_substraction,
            'btn_multiplication': self.btn_multiplication,
            'btn_division': self.btn_division,
            'btn_dot': self.btn_dot
        }

        # 루프 돌면서 연결
        for name, btn in operator_buttons.items():
            btn.clicked.connect(lambda state, button=btn: self.StrClicked(state, button))


        #self.btn_memory_1.clicked.connect(self.memory)
        #self.btn_memory_2.clicked.connect(self.memory2)

        #self.btn_lBracket.clicked.connect(lambda state, button=self.btn_lBracket: self.StrClicked(state, button))
        #self.btn_rBracket.clicked.connect(lambda state, button=self.btn_rBracket: self.StrClicked(state, button))
        #self.btn_AS.clicked.connect(lambda state, button=self.btn_AS: self.StrClicked(state, button))
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
