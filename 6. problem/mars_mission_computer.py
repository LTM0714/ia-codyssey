import random

class DummySensor:
    def __init__(self):
        # 환경 변수와 범위를 딕셔너리로 정의
        self.env_ranges = {
            'mars_base_internal_temperature': (18, 30),
            'mars_base_external_temperature': (0, 21),
            'mars_base_internal_humidity': (50, 60),
            'mars_base_external_illuminance': (500, 715),
            'mars_base_internal_co2': (0.02, 0.1),
            'mars_base_internal_oxygen': (4, 7)
        }
        # 각 키에 대한 초기값을 0.0으로 설정
        self.env_values = {key: 0.0 for key in self.env_ranges}

    def set_env(self):
        # 각 환경 변수에 대해 범위에 맞는 랜덤 값을 설정
        for key, (low, high) in self.env_ranges.items():
            self.env_values[key] = round(random.uniform(low, high), 2)
        
    def get_env(self):        
        # 랜덤 날짜 및 시간 생성
        random_month = random.randint(1, 12)
        # 홀수달(1, 3, 5, 7, 9, 11)은 31일까지, 짝수달(4, 6, 8, 10, 12)은 30일까지, 2월은 28일까지
        if random_month == 2:
            random_day = random.randint(1, 28)
        elif random_month % 2 == 1:
            random_day = random.randint(1, 31)
        else:
            random_day = random.randint(1, 30)

        random_hour = random.randint(0, 23)
        random_minute = random.randint(0, 59)
        random_second = random.randint(0, 59)
        timestamp = f"2025-{random_month:02d}-{random_day:02d} {random_hour:02d}:{random_minute:02d}:{random_second:02d}"
        
        log_entry = f'{timestamp}, '
        log_entry += ', '.join([f'{key}: {value}' for key, value in self.env_values.items()])
        
        # 로그 파일에 기록
        with open('6. problem/tmp.log', 'a') as log_file:
            log_file.write(log_entry + '\n')

        return self.env_values
    
if __name__ == '__main__':
    # DummySensor 클래스의 인스턴스를 생성하고 환경값을 설정한 후 출력
    ds = DummySensor()
    # print(ds.get_env())
    ds.set_env()
    print(ds.get_env())