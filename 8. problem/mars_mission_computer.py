import time
import test

import platform # 운영체제와 컴퓨터 시스템 정보를 가져오는 표준 라이브러리
import psutil   # pip install psutil, CPU, 메모리, 디스크 등 리소스 사용량을 확인할 수 있는 외부 라이브러리
import json

FILE_NAME = '8. problem/setting.txt'

class MissionComputer:
    __env_values = {
        'mars_base_internal_temperature': [(18, 30), 18, '도'],
        'mars_base_external_temperature': [(0, 21), 0, '도'],
        'mars_base_internal_humidity': [(50, 60), 50, '%'],
        'mars_base_external_illuminance': [(500, 715), 500, 'W/m2'],
        'mars_base_internal_co2': [(0.02, 0.1), 0.02, '%'],
        'mars_base_internal_oxygen': [(4, 7), 4, '%']
    }

    __history = {key: [] for key in __env_values.keys()}

    # json 형식으로 출력 + 5분마다 평균값 출력
    def print_json(self, data, avg_interval_min):
        print('{')
        i = 0
        for key in data.keys():
            value = data[key][1]
            MissionComputer.__history[key].append(value)
            
            # print(len(MissionComputer.__history[key]))
            if len(MissionComputer.__history[key]) > (avg_interval_min * 12):    # 5분치 데이터 저장(1분에 12개 데이터)
                MissionComputer.__history[key].pop(0)

            if i < len(data) - 1:
                print(f'\t"{key}" : {data[key][1]:.2f},')
            else:
                print(f'\t"{key}" : {data[key][1]:.2f}')

            i += 1
        print('}')

    # 환경에 대한 값 출력
    def get_sensor_data(self, ds, interval = 5, avg_interval_min = 5):
        count = 0

        print('환경 데이터 출력을 중지하려면 ctrl+c를 입력하세요.')

        try:
            while True:
                ds.set_env()
                MissionComputer.__env_values = ds.get_env()

                self.print_json(MissionComputer.__env_values, avg_interval_min)

                count += 1
                print(f'count : {count}\n')
                if count % (avg_interval_min * 12) == 0:  # 5분마다 데이터 저장
                    print('======== 5분 평균 값 ========')
                    for key in MissionComputer.__history.keys():
                        avg = sum(MissionComputer.__history[key]) / len(MissionComputer.__history[key])
                        print(f'{key} : {avg:.2f} {MissionComputer.__env_values[key][2]}')
                    print()

                time.sleep(interval)
        
        except KeyboardInterrupt:
            # 반복 중단 (Ctrl+C 입력 시 실행)
            print('System stopped....')


    # ============ 새롭게 추가된 메소드 ============
    def get_mission_computer_info(self):
        try:
            system_info = {
                '운영체계': platform.system(),
                '운영체계 버전': platform.version(),
                'CPU의 타입': platform.processor(),
                'CPU의 코어 수': psutil.cpu_count(),
                '메모리의 크기(GB)': round(psutil.virtual_memory().total / (1024 ** 3), 2)
            }

            print("[시스템 정보 출력]")
            # setting.txt 에서 출력할 항목만 불러오기
            try:
                with open(FILE_NAME, 'r', encoding='utf-8') as f:
                    settings = [line.strip() for line in f.readlines() if line.strip()]
            except FileNotFoundError:
                print('setting.txt 파일이 존재하지 않아 모든 정보를 출력합니다.')
                settings = list(system_info.keys())  # 전체 항목 출력

            # 설정된 항목만 출력
            filtered_info = {key: system_info[key] for key in settings if key in system_info}

            # json 형식으로 출력
            print(json.dumps(filtered_info, indent = 4, ensure_ascii = False))

        except Exception as e:
            print(f'시스템 정보를 가져오는 중 오류 발생: {e}')


    def get_mission_computer_load(self, interval = 1):
        try:
            cpu_load = psutil.cpu_percent(interval)         # 1초 동안 CPU 사용량 측정 (%)
            memory_load = psutil.virtual_memory().percent   # 메모리 사용량 측정 (%)

            # json 형식으로 출력
            load_info = {
                'CPU 실시간 사용량': cpu_load,
                '메모리 실시간 사용량': memory_load
            }

            print("[시스템 부하 정보 출력]")
            # setting.txt 에서 출력할 항목만 불러오기
            try:
                with open(FILE_NAME, 'r', encoding='utf-8') as f:
                    settings = [line.strip() for line in f.readlines() if line.strip()]
            except FileNotFoundError:
                print('setting.txt 파일이 존재하지 않아 모든 정보를 출력합니다.')
                settings = list(load_info.keys())  # 전체 항목 출력

            # 설정된 항목만 출력
            filtered_info = {key: load_info[key] for key in settings if key in load_info}

            # json 형식으로 출력
            print(json.dumps(filtered_info, indent = 4, ensure_ascii = False))

        except Exception as e:
            print(f'시스템 부하 정보를 가져오는 중 오류 발생: {e}')


def previous_code():
    ds = test.DummySensor()
    RunComputer = MissionComputer()
    RunComputer.get_sensor_data(ds, interval = 5, avg_interval_min = 5)

def main():
    runComputer = MissionComputer()
    runComputer.get_mission_computer_info()
    runComputer.get_mission_computer_load(interval = 1)


if __name__ == '__main__':
    main()