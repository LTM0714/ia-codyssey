import random

class DummySensor:
    # 환경 변수 범위 설정 (class 변수)
    __env_values = {
        'mars_base_internal_temperature': [(18, 30), 18, '도'],
        'mars_base_external_temperature': [(0, 21), 0, '도'],
        'mars_base_internal_humidity': [(50, 60), 50, '%'],
        'mars_base_external_illuminance': [(500, 715), 500, 'W/m2'],
        'mars_base_internal_co2': [(0.02, 0.1), 0.02, '%'],
        'mars_base_internal_oxygen': [(4, 7), 4, '%']
    }

    def set_env(self):
        for key in DummySensor.__env_values :
            DummySensor.__env_values[key][1] = random.uniform(*DummySensor.__env_values[key][0])
        
    def get_env(self):        

        return DummySensor.__env_values
    
def main():
    # DummySensor 클래스의 인스턴스를 생성하고 환경값을 설정한 후 출력
    ds = DummySensor()
    # print(ds.get_env())
    ds.set_env()
    get = ds.get_env()
    for key in get.keys():
        print(f'{key} : {get[key][1]:.2f} {get[key][2]}')
    
if __name__ == '__main__':
    main()