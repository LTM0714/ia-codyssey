import time
import test
# import msvcrt

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

    def get_sensor_data(self, interval = 5):
        ds = test.DummySensor()
        count = 0

        print('환경 데이터 출력을 중지하려면 ctrl+c를 입력하세요.')

        try:
            while True:
                # # Windows 환경에서 비동기적으로 키 입력 감지
                # if msvcrt.kbhit():  # 키가 눌렸는지 확인(입력 대기 없이 체크 가능)
                #     key = msvcrt.getch().decode('utf-8')  # 입력된 키를 가져옴, 바이트 형식으로 반환된 값을 문자열로 변환
                #     if key.lower() == 'q':
                #         print("System stopped…")
                #         break  # 루프 종료

                ds.set_env()
                MissionComputer.__env_values = ds.get_env()

                for key in MissionComputer.__env_values.keys():
                    value = MissionComputer.__env_values[key][1]
                    MissionComputer.__history[key].append(value)

                    # print(len(MissionComputer.__history[key]))
                    if len(MissionComputer.__history[key]) > 60:    # 5분치 데이터 저장(1분에 12개 데이터)
                        MissionComputer.__history[key].pop(0)
                    print(f'{key} : {MissionComputer.__env_values[key][1]:.2f} {MissionComputer.__env_values[key][2]}')

                count += 1
                print(f'count : {count}\n')
                if count % 60 == 0:  # 5분마다 데이터 저장
                    print('======== 5분 평균 값 ========')
                    for key in MissionComputer.__history.keys():
                        avg = sum(MissionComputer.__history[key]) / len(MissionComputer.__history[key])
                        print(f'{key} : {avg:.2f} {MissionComputer.__env_values[key][2]}')
                    print()

                time.sleep(interval)
        
        except KeyboardInterrupt:
            # 반복 중단 (Ctrl+C 입력 시 실행)
            print('System stopped....')

def main():
    RunComputer = MissionComputer()

    RunComputer.get_sensor_data()


if __name__ == "__main__":
    main()