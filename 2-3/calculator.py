import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic

form_class=uic.loadUiType("2-3/calculator.ui")[0]


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        for i in range(10):
            btn = getattr(self, f'btn_number_{i}')

            btn.clicked.connect(lambda state, button=btn: self.NumClicked(state, button))


        operators = [
            'addition', 'substraction',
            'multiplication', 'division',
            'dot', 'percent'
        ]

        # 루프 돌면서 연결
        for op in operators:
            btn = getattr(self, f'btn_{op}')
            btn.clicked.connect(lambda state, button=btn: self.StrClicked(state, button))

        # 삭제
        self.btn_delete.clicked.connect(self.delete)
        # 클리어
        self.btn_clear.clicked.connect(self.clear)
        # 계산
        self.btn_equal.clicked.connect(self.equal)


    def NumClicked(self, state, button):
        exist_line_text=self.lineEdit.text()
        now_num_text=button.text()

        if exist_line_text == "0":
            # 소수점 입력 시작을 허용하기 위해 "0."은 유지
            if now_num_text != ".":
                self.lineEdit.setText(now_num_text)
            else:
                self.lineEdit.setText(exist_line_text + now_num_text)

        else:
            self.lineEdit.setText(exist_line_text + now_num_text)

    def StrClicked(self, state, button):
        exist_line_text = self.lineEdit.text()
        now_num_text = button.text()

        self.lineEdit.setText(exist_line_text + now_num_text)

    def equal(self):
        try:
            line=self.lineEdit.text().replace(",","")
            result=eval(line)

            s1 = '{0:,}'.format(int(result))                    # 정수
            s2 = '{0:0.2f}'.format(float(result)-int(result))   # 소수
            s3=s1+s2                                            # 합
            final = s3.replace("0.", ".")                       # 소수점 앞에 0이 붙는 경우 제거
            self.lineEdit.setText(final)
        
        except ZeroDivisionError:
            self.lineEdit.setText("Error: Divide by 0")

        except SyntaxError:
            self.lineEdit.setText("Error: Invalid Syntax")

        except Exception as e:
            self.lineEdit.setText(f"Error: {e}")

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
