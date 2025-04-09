import time
import test

import platform
import os
import psutil
import json

import threading

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

    def __init__(self):
        self.stop_flag = False
        self.print_lock = threading.Lock()  # 스레드 안전성(print)을 위한 Lock 객체 생성

    def print_safe(self, *args, **kwargs):
        with self.print_lock:
            print(*args, **kwargs)

    # json 형식으로 출력 + 5분마다 평균값 출력
    def print_json(self, data, avg_interval_min):
        with self.print_lock:
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
    def get_sensor_data(self, ds, interval=5, avg_interval_min=5):
        count = 0
        while not self.stop_flag:
            ds.set_env()
            MissionComputer.__env_values = ds.get_env()

            self.print_json(MissionComputer.__env_values, avg_interval_min)
            count += 1
            self.print_safe(f'count : {count}\n')

            if count % (avg_interval_min * 12) == 0:
                with self.print_lock:
                    print('======== 평균 값 출력 ========')
                    for key in MissionComputer.__history.keys():
                        avg = sum(MissionComputer.__history[key]) / len(MissionComputer.__history[key])
                        print(f'{key} : {avg:.2f} {MissionComputer.__env_values[key][2]}')
                    print()

            time.sleep(interval)

    # ============ 새롭게 추가된 메소드 ============
    # 시스템 정보 출력
    # 운영체계, 운영체계 버전, CPU 타입, CPU 코어 수, 메모리 크기(GB)
    def get_mission_computer_info(self):
        while not self.stop_flag:
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
                    print('setting.txt 파일이 존재하지 않아 모든 정보를 출력합니다.')
                    settings = list(system_info.keys())

                filtered_info = {key: system_info[key] for key in settings if key in system_info}
                with self.print_lock:
                    print('[시스템 정보 출력]')
                    print(json.dumps(filtered_info, indent=4, ensure_ascii=False))

            except Exception as e:
                self.print_safe(f'시스템 정보를 가져오는 중 오류 발생: {e}')
            time.sleep(20)

    # 시스템 부하 정보 출력
    # CPU 실시간 사용량, 메모리 실시간 사용량
    def get_mission_computer_load(self):
        while not self.stop_flag:
            try:
                cpu_load = psutil.cpu_percent(interval=1)
                memory_load = psutil.virtual_memory().percent

                load_info = {
                    'CPU 실시간 사용량': cpu_load,
                    '메모리 실시간 사용량': memory_load
                }

                with self.print_lock:
                    print('[시스템 부하 정보 출력]')
                    print(json.dumps(load_info, indent=4, ensure_ascii=False))

            except Exception as e:
                self.print_safe(f'시스템 부하 정보를 가져오는 중 오류 발생: {e}')

            time.sleep(20)

def main():
    # DummySensor 클래스의 인스턴스를 생성하고 환경값을 램덤하게 설정한 후 출력
    ds = test.DummySensor()
    # MissionComputer 클래스의 인스턴스를 생성
    runComputer = MissionComputer()

    # 멀티 스레드 실행
    t1 = threading.Thread(target=runComputer.get_sensor_data, args=(ds, 5, 5))
    t2 = threading.Thread(target=runComputer.get_mission_computer_info)
    t3 = threading.Thread(target=runComputer.get_mission_computer_load)

    t1.start()
    t2.start()
    t3.start()

    try:
        while t1.is_alive() or t2.is_alive() or t3.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        runComputer.print_safe('\nCtrl + C 감지됨. 프로그램 종료 중...')
        runComputer.stop_flag = True

    # 메인 스레드가 종료되지 않도록 대기
    t1.join()
    t2.join()
    t3.join()
    runComputer.print_safe('모든 스레드가 정상적으로 종료되었습니다.')

if __name__ == '__main__':
    main()
