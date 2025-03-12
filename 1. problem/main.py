# main.py
# mission_computer_main.log 파일을 열고 전체 내용을 화면에 출력

def read_log_file():
    try:
        with open("1. problem/mission_computer_main.log", 'r', encoding='utf-8') as f:
            content = f.readlines()
            for line in content:
                print(line.strip()) # strip() 메서드: 문자열의 앞뒤 공백 또는 특정 문자를 제거하는 기능
            return content

    except FileNotFoundError:
        print("Error: The file 'mission_computer_main.log' was not found.")
    except Exception as e:
        print("Error: 예기치 않은 오류 발생", e)

def main():
    log_data = read_log_file()
    
if __name__ == "__main__":
    main()