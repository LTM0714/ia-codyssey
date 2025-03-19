FILE_NAME = '3. problem/Mars_Base_Inventory_List.csv'
DNG_NAME = '3. problem/Mars_Base_Inventory_danger.csv'
BIN_NAME = '3. problem/Mars_Base_Inventory_List.bin'

# csv 파일 출력
def print_csv_file(filename):
    try:
        print('=====Mars_Base_Inventory 목록=====')

        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                print(line.strip())

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except Exception as e:
        print(f'An unexpected error occurred: {e}')


# csv 파일 읽기
def read_csv_file(filename):
    try:
        csv_list = []

        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()

            for line in lines[1:]: 
                # .strip(): 문자열 앞뒤 끝 공백 문자 제거
                # split(',', 4): 최대 4번까지 분리
                parts = line.strip().split(',', 4)
                
                if len(parts) == 5:
                    parts[4] = float(parts[4])  # 5번째 요소를 실수로 변환
                    csv_list.append(parts)
        
        # 인화성(5번째 항목)이 높은 순으로 정렬
        csv_list.sort(key = lambda item: item[4], reverse=True)

        # 인화성 지수가 0.7 이상되는 목록을 뽑아서 별도로 출력
        flame_list = [item for item in csv_list if item[4] >= 0.7]

        print('\n=====인화성 지수가 0.7 이상인 물질 목록=====')
        for inv in flame_list:
            print(inv)

        print('\n=====인화성 지수가 0.7 이상인 물질 목록 저장=====\n')
        write_csv_file(flame_list, DNG_NAME)

        # 인화성 순서로 정렬된 배열의 내용을 이진 파일형태로 저장
        print('\n=====바이너리 파일형태로 저장=====\n')
        write_bin_file(csv_list, BIN_NAME)

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except Exception as e:
        print(f'An unexpected error occurred: {e}')


# csv 파일 쓰기
def write_csv_file(lstname, filename) :
    try :
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('Substance,Weight (g/cm³),Specific Gravity,Strength,Flammability\n')
            
            for line in lstname :
                # 5번째 원소를 포함하여 원소 자료형을 문자열로 변환하여 join
                f.write(','.join(map(str, line)) + '\n')

    except FileNotFoundError:
        print(f"Ereror: The File '{filename}' was not found")
    except Exception as e:
        print(f'An unexpected error occurred: {e}')


# 이진 파일 쓰기 및 읽기
def write_bin_file(lstname, filename):
    try:
        with open(filename, 'wb') as f:  # 바이너리 모드로 파일 열기
            for item in lstname:
                # 모든 데이터를 문자열로 변환 후, 쉼표로 구분하여 한 줄로 저장
                line = ','.join(map(str, item)) + '\n'
                f.write(line.encode('utf-8'))  # UTF-8로 인코딩하여 저장

        with open(filename, 'rb') as f:
            lines = f.readlines()
            
        print('\n=====바이너리 파일 출력=====')
        for line in lines:
            print(line.decode('utf-8').strip()) # UTF-8로 디코딩 후 개행 문자 제거

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except Exception as e:
        print(f'An unexpected error occurred: {e}')


if __name__ == "__main__":
    print_csv_file(FILE_NAME)
    read_csv_file(FILE_NAME)