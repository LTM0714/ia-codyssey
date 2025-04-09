import time
import test

import platform
import os
import psutil
import json

import multiprocessing

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
        for i, key in enumerate(data.keys()):
            value = data[key][1]
            MissionComputer.__history[key].append(value)

            if len(MissionComputer.__history[key]) > (avg_interval_min * 12):
                MissionComputer.__history[key].pop(0)

            comma = ',' if i < len(data) - 1 else ''
            print(f'\t"{key}" : {value:.2f}{comma}')
        print('}')

    # 환경에 대한 값 출력, 5초마다 데이터 수집, 5분마다 평균값 출력
    def get_sensor_data(self, interval=5, avg_interval_min=5):
        ds = test.DummySensor()
        count = 0
        while True:
            ds.set_env()
            MissionComputer.__env_values = ds.get_env()
            
            print("[센서 데이터 출력]")
            self.print_json(MissionComputer.__env_values, avg_interval_min)
            count += 1
            print(f'count : {count}\n')

            if count % (avg_interval_min * 12) == 0:
                print('======== 평균 값 출력 ========')
                for key in MissionComputer.__history.keys():
                    avg = sum(MissionComputer.__history[key]) / len(MissionComputer.__history[key])
                    print(f'{key} : {avg:.2f} {MissionComputer.__env_values[key][2]}')
                print()

            time.sleep(interval)

    # 시스템 정보 출력
    # 운영체계, 운영체계 버전, CPU 타입, CPU 코어 수, 메모리 크기(GB)
    def get_mission_computer_info(self):
        while True:
            try:
                system_info = {
                    '운영체계': platform.system(),
                    '운영체계 버전': platform.version(),
                    'CPU의 타입': platform.processor(),
                    'CPU의 코어 수': os.cpu_count(),
                    '메모리의 크기(GB)': round(psutil.virtual_memory().total / (1024 ** 3), 2)
                }

                try:
                    with open(FILE_NAME, 'r', encoding='utf-8') as f:
                        settings = [line.strip() for line in f.readlines() if line.strip()]
                except FileNotFoundError:
                    print('setting.txt 파일이 없어 전체 정보를 출력합니다.')
                    settings = list(system_info.keys())

                filtered_info = {key: system_info[key] for key in settings if key in system_info}
                print("[시스템 정보 출력]")
                print(json.dumps(filtered_info, indent=4, ensure_ascii=False))
            
            except Exception as e:
                print(f'시스템 정보를 가져오는 중 오류 발생: {e}')
            time.sleep(20)

    # 시스템 부하 정보 출력
    # CPU 실시간 사용량, 메모리 실시간 사용량
    def get_mission_computer_load(self):
        while True:
            try:
                cpu_load = psutil.cpu_percent(interval=1)         # 1초 동안 CPU 사용량 측정 (%)
                memory_load = psutil.virtual_memory().percent   # 메모리 사용량 측정 (%)

                load_info = {
                    'CPU 실시간 사용량': cpu_load,
                    '메모리 실시간 사용량': memory_load
                }

                print("[시스템 부하 정보 출력]")
                print(json.dumps(load_info, indent = 4, ensure_ascii = False))
                
            except Exception as e:
                print(f'시스템 부하 정보를 가져오는 중 오류 발생: {e}')
            
            time.sleep(20)

def main():
    runComputer1 = MissionComputer()
    runComputer2 = MissionComputer()
    runComputer3 = MissionComputer()

    p1 = multiprocessing.Process(target=runComputer1.get_sensor_data)
    p2 = multiprocessing.Process(target=runComputer2.get_mission_computer_info)
    p3 = multiprocessing.Process(target=runComputer3.get_mission_computer_load)

    p1.start()
    p2.start()
    p3.start()

    try:
        print("프로세스 실행 중... Ctrl + C를 누르면 종료됩니다.")
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nCtrl + C 감지됨. 프로세스 종료 중...")
        p1.terminate()
        p2.terminate()
        p3.terminate()

        p1.join()
        p2.join()
        p3.join()
        print("모든 프로세스가 종료되었습니다.")

if __name__ == '__main__':
    main()
