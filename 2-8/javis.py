# pip install SpeechRecognition PyAudio

import os
import speech_recognition as sr     # 음성 인식 라이브러리
from datetime import datetime
import pyaudio                      # 오디오 장치 정보 확인용

class JavisRecorder:
    def __init__(self):
        self.r = sr.Recognizer()            # Recognizer 객체 생성
        self.record_dir = '2-8/records'     # 녹음 파일을 저장할 디렉토리

    # 1-1. 음성 녹음
    def record_audio(self):
        while True:
            try:
                duration = float(input('\n녹음할 시간(초, 예: 5)을 입력하세요: '))
                if duration <= 0:
                    print('1초 이상의 양의 정수를 입력하세요.\n')
                    continue
                break
            except ValueError:
                print('유효한 숫자를 입력하세요.\n')

        # 마이크를 오디오 소스로 사용
        with sr.Microphone() as source:
            print('녹음 시작... Ctrl+C로 중지할 수 있습니다.')
            try:
                self.r.adjust_for_ambient_noise(source)  # 주변 소음 보정
                audio_data = self.r.record(source, duration=duration)   # duration(초)까지 녹음
                print('녹음 완료!')
            except KeyboardInterrupt:
                print('녹음이 중단되었습니다.')
                return self.record_audio()  # 재귀적으로 다시 녹음 시도

            return audio_data

    # 1-2. 오디오 데이터를 WAV 파일로 저장
    def save_audio(self, audio_data):
        # 'records' 디렉토리가 없으면 생성
        if not os.path.exists(self.record_dir):
            os.makedirs(self.record_dir)

        # 저장할 오디오 파일의 이름
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_name = f'{timestamp}.wav'
        file_path = self.record_dir + '/' + file_name

        with open(file_path, 'wb') as f:
            f.write(audio_data.get_wav_data())
        
        print(f'녹음된 오디오 파일: {file_name}')

        return file_path

    # 1-3. 음성 인식 처리
    def recognize_audio(self, audio_data):
        try:
            text = self.r.recognize_google(audio_data, language='ko-KR')
            print(f'You said: {text}')
            return text
        except sr.UnknownValueError:
            print('Sorry, could not recognize your voice')
        except sr.RequestError as e:
            print(f'Could not request results from Google Speech Recognition service: {e}')
        return None

    # 1-4. STT(Speech to Text)를 csv 파일에 저장
    def save_to_csv(self, text, file_path):
        timestamp = file_path.split('_')[1].split('.')[0]   # 'DIR/YYYYMMDD_HHMMSS.wav'에서 'HHMMSS' 부분 추출

        csv_file = file_path.replace('.wav', '.csv')
        with open(csv_file, 'w', encoding='utf-8') as f:
            if text:
                f.write(timestamp + ', ' + text)
            else:
                f.write(timestamp + ', 음성 인식 실패')


    # 2. 특정 범위 날짜의 녹음 파일 목록 출력
    def list_recordings_by_date(self, start_date_str, end_date_str):
        if not os.path.exists(self.record_dir):
            print('records 디렉토리가 존재하지 않습니다.')
            return None

        try:
            # 문자열을 날짜 객체로 변환
            start_date = datetime.strptime(start_date_str, '%Y%m%d')
            end_date = datetime.strptime(end_date_str, '%Y%m%d')

            print(f'\n{start_date_str} ~ {end_date_str} 사이의 녹음 파일:')
            found = False

            for file_name in os.listdir(self.record_dir):
                if not file_name.endswith('.wav'):
                    continue
                if '_' not in file_name:
                    continue  # 형식이 이상한 파일은 무시

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

    # 3. CSV 파일에서 키워드 검색
    def search_keyword_in_csv(self, keyword):
        print(f'\nCSV 파일에서 "{keyword}" 검색 중...')

        if not os.path.exists(self.record_dir):
            print('records 디렉토리가 존재하지 않습니다.')
            return None
        
        found = False
        for file_name in os.listdir(self.record_dir):
            # CSV 파일이 아니면 건너뜀
            if not file_name.endswith('.csv'):
                continue

            file_path = os.path.join(self.record_dir, file_name)

            try:
                with open(file_path, 'r', encoding = 'utf-8') as f:
                    for line in f:
                        if keyword.lower() in line.lower():
                            print(f'>> 파일: {file_name}\n내용: {line.strip()}')
                            found = True
            
            except Exception as e:
                print(f'파일 {file_name}을 읽는 중 오류 발생: {e}')        
        if not found:
            print(f'키워드 "{keyword}"를 포함하는 내용은 없습니다.')

    # 4. 사용 가능한 오디오 장치 정보 출력
    def device_info(self):
        print('\n사용 가능한 오디오 장치:')
        audio = pyaudio.PyAudio()
        
        for i in range(audio.get_device_count()):
            info = audio.get_device_info_by_index(i)
            # 입력(녹음) 가능한 장치만 필터링
            if info['maxInputChannels'] > 0:
                '''
                1 채널: 일반적인 모노(Mono) 마이크 (한쪽에서만 소리를 받음)
                2 채널: 스테레오(Stereo) 마이크 (왼쪽/오른쪽 두 방향에서 소리를 받음)
                4, 6, 8 채널 이상: 고급 마이크 장비, 믹서기 등에서 여러 입력을 동시에 받을 수 있음
                '''
                print(f' - [{i}] {info['name']} (채널: {info['maxInputChannels']})')

        # 기본 입력 장치 출력
        default_index = audio.get_default_input_device_info()['index']
        default_name = audio.get_default_input_device_info()['name']
        print(f'\n[기본 입력 장치] → [{default_index}] {default_name}')

        audio.terminate()   # PyAudio 객체 종료

def main():
    jvr = JavisRecorder()  # JavisRecorder 객체 생성

    while True:
        print('\n===== 음성 녹음 프로그램 =====')
        print('1. 음성 녹음 및 저장')
        print('2. 날짜 범위로 녹음 파일 목록 보기')
        print('3. 키워드로 CSV 내용 검색')
        print('4. 사용 가능한 오디오 장치 정보 보기')
        print('0. 종료')
        choice = input('선택: ')

        if choice == '1':
            audio_data = jvr.record_audio()         # 음성 녹음
            file_path = jvr.save_audio(audio_data)  # 오디오 파일로 저장
            text = jvr.recognize_audio(audio_data)  # 음성 인식
            jvr.save_to_csv(text, file_path)        # 인식된 텍스트를 CSV 파일에 저장
        elif choice == '2':
            start = input('시작 날짜 (YYYYMMDD): ')
            end = input('종료 날짜 (YYYYMMDD): ')
            jvr.list_recordings_by_date(start, end) # 날짜 범위로 녹음 파일 목록 출력
        elif choice == '3':
            keyword = input('검색할 키워드 입력: ')
            jvr.search_keyword_in_csv(keyword)      # 키워드로 CSV 파일 안의 내용용 검색
        elif choice == '4':
            jvr.device_info()                       # 사용 가능한 오디오 장치 정보 출력
        elif choice == '0':
            print('프로그램 종료.\n')
            break
        else:
            print('올바른 번호를 선택하세요.')
    

if __name__ == '__main__':
    main()