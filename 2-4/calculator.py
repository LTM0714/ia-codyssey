import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic

form_class=uic.loadUiType('2-4/calculator.ui')[0]

class Calculator:
    def __init__(self):
        self.reset()


    # 숫자 입력 시 문자열로 이어 붙임
    def append_number(self, num):
        self.current += num

    # 사칙연산
    def add(self):
        self.operator = '+'
        return self.operator
    
    def subtract(self):
        self.operator = '-'
        return self.operator
    
    def multiply(self):
        self.operator = '*'
        return self.operator
    
    def divide(self):
        self.operator = '/'
        return self.operator

    # 초기화
    def reset(self):
        self.current = ''
        self.operator = ''

    # 음수 양수
    def negative_positive(self):
        if self.current:
            if self.current.startswith('-'):
                self.current = self.current[1:]
            else:
                self.current = '-' + self.current

    # 퍼센트
    def percent(self):
        if self.current:
            self.current = str(float(self.current) / 100)

    # 소수점
    def append_dot(self):
        if "." not in self.current:
            if self.current == '':
                self.current = '0.'
            else:
                self.current += '.'

    # eval 함수로 계산
    def equal(self):
        try:
            expression = self.current
            result = eval(expression)
            return str(result)
        
        except ZeroDivisionError:
            return 'Error: Divide by 0'
        except SyntaxError:
            return 'Error: Syntax Error'
        except Exception as e:
            return f'Error: {e}'


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.calculator = Calculator()

        # 숫자 버튼 연결
        for i in range(10):
            btn = getattr(self, f'btn_number_{i}')
            btn.clicked.connect(lambda state, button=btn: self.num_clicked(button))

        # 연산자 버튼 연결
        self.btn_addition.clicked.connect(self.addition)
        self.btn_substraction.clicked.connect(self.substraction)
        self.btn_multiplication.clicked.connect(self.multiplication)
        self.btn_division.clicked.connect(self.division)

        self.btn_clear.clicked.connect(self.clear)
        self.btn_np.clicked.connect(self.np)
        self.btn_percent.clicked.connect(self.percent)
        self.btn_dot.clicked.connect(self.dot)
        
        self.btn_equal.clicked.connect(self.equal)


    # 현재 계산기 상태를 UI(lineEdit)에 반영
    def update_display(self):
        self.lineEdit.setText(self.calculator.current)

    # 숫자 버튼 클릭 시 호출되는 메서드
    def num_clicked(self, button):
        num = button.text()
        self.calculator.append_number(num)
        self.update_display()

    # 연산자 버튼(사칙연산) 클릭 시 호출되는 메서드
    def addition(self):
        self.calculator.current += self.calculator.add()
        self.update_display()

    def substraction(self):
        self.calculator.current += self.calculator.subtract()
        self.update_display()

    def multiplication(self):
        self.calculator.current += self.calculator.multiply()
        self.update_display()

    def division(self):
        self.calculator.current += self.calculator.divide()
        self.update_display()

    # 초기화 버튼 클릭 시 호출되는 메서드
    def clear(self):
        self.calculator.reset()
        self.update_display()

    # 음수 양수 버튼 클릭 시 호출되는 메서드
    def np(self):
        self.calculator.negative_positive()
        self.update_display()

    # 퍼센트 버튼 클릭 시 호출되는 메서드
    def percent(self):
        self.calculator.percent()
        self.update_display()

    # 소수점 버튼 클릭 시 호출되는 메서드
    def dot(self):
        self.calculator.append_dot()
        self.update_display()

    # 계산 버튼 클릭 시 호출되는 메서드
    def equal(self):
        result = self.calculator.equal()
        self.calculator.current = result
        self.update_display()


if __name__=='__main__':
    app=QApplication(sys.argv)
    myWindow=WindowClass()
    myWindow.show()
    app.exec_()