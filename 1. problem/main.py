LOG_NAME = '1. problem/mission_computer_main.log'
ISSUE_NAME = '1. problem/issue.log'

log = []
def read_log_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            while True :
                line = f.readline()    # 한 줄씩 읽기
                if not line :
                    break
                log.append(line.strip().split(','))   # log에 저장, strip()으로 앞뒤 공백 제거, split(',')으로 쉼표로 구분

        # log file 출력
        for item in log:
            print(item)
        
        # log file 역순 출력
        sorted_log = sorted(log, key=lambda x : x[0], reverse=True) # key=lambda x : x[0]으로 날짜순 정렬
        for item in sorted_log:
            print(item)

        # 문제가 된 log만 출력(2023-08-27 11:35:00 이후 로그)
        issue_log = [item for item in log if item[0] >= '2023-08-27 11:35:00']
        for item in issue_log:
            print(item)

        # 문제가 된 log(2023-08-27 11:35:00 이후 로그)만 issue_log파일로 저장
        with open(ISSUE_NAME, 'w', encoding='utf-8') as f :
            for item in issue_log:
                f.write(','.join(map(str, item)) + '\n')    

    except FileNotFoundError:
        print("Error: The file 'mission_computer_main.log' was not found.")
    except Exception as e:
        print('Error: 예기치 않은 오류 발생', e)
    
if __name__ == "__main__":
    read_log_file(LOG_NAME)