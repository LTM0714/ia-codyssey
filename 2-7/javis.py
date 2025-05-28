import os
import speech_recognition as sr     # 음성 인식 라이브러리
from datetime import datetime


# Recognizer 객체 생성
r = sr.Recognizer()

RECORD_DIR = '2-7/records'


# 음성 녹음
def record_audio():
    # 마이크를 오디오 소스로 사용
    with sr.Microphone() as source:
        print('\n음성 녹음을 시작하려면 Enter 키를 누르세요.')
        input()        
        print('녹음 시작...')
        r.adjust_for_ambient_noise(source)  # 주변 소음 보정
        audio_data = r.listen(source, timeout=5, phrase_time_limit=10)  # 5초 동안 음성 입력 대기, 최대 10초까지 녹음
        print('녹음 완료!')

        return audio_data

# 오디오 데이터를 WAV 파일로 저장
def save_audio(audio_data):
    # 'records' 디렉토리가 없으면 생성
    if not os.path.exists(RECORD_DIR):
        os.makedirs(RECORD_DIR)

    # 저장할 오디오 파일의 이름
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    file_name = f'{timestamp}.wav'
    file_path = RECORD_DIR + '/' + file_name

    with open(file_path, 'wb') as f:
        f.write(audio_data.get_wav_data())
    
    print(f'녹음된 오디오 파일: {file_name}')

    return file_path

# 음성 인식 처리
def recognize_audio(audio_data):
    try:
        text = r.recognize_google(audio_data, language='ko-KR')
        print(f'You said: {text}')
    except sr.UnknownValueError:
        print('Sorry, could not recognize your voice')
    except sr.RequestError as e:
        print(f'Could not request results from Google Speech Recognition service: {e}')

# 특정 범위 날짜의 녹음 파일 목록 출력
def list_recordings_by_date(start_date_str, end_date_str):
    if not os.path.exists(RECORD_DIR):
        print('records 디렉토리가 존재하지 않습니다.')
        return None

    try:
        # 문자열을 날짜 객체로 변환
        start_date = datetime.strptime(start_date_str, '%Y%m%d')
        end_date = datetime.strptime(end_date_str, '%Y%m%d')

        print(f'\n{start_date_str} ~ {end_date_str} 사이의 녹음 파일:')
        found = False

        for file_name in os.listdir(RECORD_DIR):
            if not file_name.endswitch('.wav'):
                continue
            if '_' not in file_name:
                continue    # 형식이 이상한 파일은 무시
                
            date_str = file_name.split('_')[0]  # 'YYYYMMDD_HHMMSS.wav' → 'YYYYMMDD'
            
            try:
                file_date = datetime.strptime(date_str, '%Y%m%d')
                if start_date <= file_date <= end_date:
                    print(' -', file_name)
                    found = True
            except ValueError:
                continue  # 날짜 형식이 아닌 파일은 건너뜀

        if not found:
            print('해당 날짜 범위에 녹음 파일이 없습니다.')
    except ValueError:
        print('날짜 형식이 올바르지 않습니다. (예: 20010714)')


def main():
    while True:
        print('\n===== 음성 녹음 프로그램 =====')
        print('1. 음성 녹음 및 저장')
        print('2. 날짜 범위로 녹음 파일 목록 보기')
        print('3. 종료')
        choice = input('선택: ')

        if choice == '1':
            audio_data = record_audio()     # 음성 녹음
            save_audio(audio_data)          # 오디오 파일로 저장
            recognize_audio(audio_data)     # 음성 인식
        elif choice == '2':
            start = input('시작 날짜 (YYYYMMDD): ')
            end = input('종료 날짜 (YYYYMMDD): ')
            list_recordings_by_date(start, end)
        elif choice == '3':
            print('프로그램 종료.\n')
            break
        else:
            print('올바른 번호를 선택하세요.')
    

if __name__ == '__main__':
    main()
