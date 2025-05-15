import zipfile
import string
import multiprocessing
import time
from datetime import datetime
import io

# 압축 파일과 결과 저장 파일명
ZIP_FILE = 'emergency_storage_key.zip'
OUTPUT_FILE = 'password.txt'

# 암호는 소문자+숫자로 된 6자리
CHARSET = string.ascii_lowercase + string.digits
PASSWORD_LENGTH = 6

# 전체 조합 수
# CHARSET의 길이와 PASSWORD_LENGTH를 곱하여 전체 조합 수 계산
TOTAL_COMBINATIONS = len(CHARSET) ** PASSWORD_LENGTH

# multiprocessing.cpu_count()를 사용하여 시스템의 CPU 코어 수를 확인
PROCESS_COUNT = multiprocessing.cpu_count()

# 각 프로세스가 시도할 범위의 크기
LOG_INTERVAL = 100000

# 시작 시간과 전체 시도 횟수를 저장할 공유 변수
start_time = time.time()
attempt_counter = multiprocessing.Value('i', 0)

# found = Value('b', False) # 비번 찾았는지 여부를 공유하는 변수


# 주어진 인덱스를 CHARSET 기준의 패스워드 문자열로 변환하는 함수
def index_to_password(index):
    base = len(CHARSET)
    chars = []

    for _ in range(PASSWORD_LENGTH):
        # (index = a // b, rem = a % b)
        index, rem = divmod(index, base)
        # index가 0이면 divmod(0, 36) = (0, 0) -> CHARSET[0] = 'a' -> 'aaaaaa'
        # index가 1이면 divmod(1, 36) = (0, 1) -> CHARSET[1] = 'b' -> 'baaaaa'
        chars.append(CHARSET[rem])

    # chars 리스트를 역순으로 변환하여 패스워드 생성
    # 예를 들어, chars = ['b', 'a', 'a', 'a', 'a'] -> 'aaaaab'
    return ''.join(reversed(chars))


# 하나의 프로세스가 주어진 범위 내의 모든 인덱스에 대해 패스워드를 생성하고 해제를 시도하는 함수
def try_password_range(start, end):
    try:
        # zip 파일을 메모리로 로딩
        with open(ZIP_FILE, 'rb') as f:
            zip_data = io.BytesIO(f.read())

        # zip 파일 열기
        zf = zipfile.ZipFile(zip_data, 'r')

        fname = zf.namelist()[0] # zip 파일 첫번째 파일 이름
        
        # 주어진 범위 내의 모든 인덱스에 대해 패스워드를 생성
        # 0 -> 'aaaaaa', 1 -> 'aaaaab', ..., 999999 -> 'zzzzzz'
        for idx in range(start, end):
            password = index_to_password(idx)

            # 잠금 안하면 동시 접근 시 충돌 발생, 암호 시도 횟수 카운트
            with attempt_counter.get_lock():
                attempt_counter.value += 1
                count = attempt_counter.value

            try:
                with zf.open(fname, 'r', pwd=password.encode()) as file:
                    file.read(1) # 파일이 정상인지 최소 1바이트 읽기

                    duration = time.time() - start_time
                    print('\n[+] 암호 해제 성공!')
                    print(f'[+] 암호: {password}')
                    print(f'[+] 시작 시간: {datetime.fromtimestamp(start_time).strftime("%Y-%m-%d %H:%M:%S")}')
                    print(f'[+] 시도 횟수: {count}')
                    print(f'[+] 소요 시간: {duration:.2f}초')

                    with open(OUTPUT_FILE, 'w') as f:
                        f.write(password)

                    return password

            except Exception:
                if count % LOG_INTERVAL == 0:
                    print(f'[시도 {count}회] 경과 시간: {time.time() - start_time:.2f}초')

    except Exception as e:
        print(f'[!] 오류 발생 (범위 {start}~{end}): {e}')


# 멀티코어를 활용하여 Brute Force 방식으로 병렬 처리하는 함수
def unlock_zip():
    print(f'multiprocessing 해킹 시작 (사용 코어 수: {PROCESS_COUNT})')
    print(f'시작 시간: {datetime.fromtimestamp(start_time).strftime("%Y-%m-%d %H:%M:%S")}')

    # 각 프로세스에 할당할 범위를 계산
    chunk_size = TOTAL_COMBINATIONS // PROCESS_COUNT
    ranges = []

    # 각 프로세스에 할당할 범위를 계산하여 ranges 리스트에 추가
    for i in range(PROCESS_COUNT):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i < PROCESS_COUNT - 1 else TOTAL_COMBINATIONS
        ranges.append((start, end))

    # 프로세스를 자동으로 관리해주는 병렬 처리 도구
    with multiprocessing.Pool(PROCESS_COUNT) as pool:
        pool.starmap(try_password_range, ranges)


if __name__ == '__main__':
    unlock_zip()
