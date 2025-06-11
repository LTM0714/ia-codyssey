from mysql_helper import MySQLHelper

csv_file_path = '3-5/mars_weathers_data.csv'

def load_csv_and_insert(csv_path, db: MySQLHelper):
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        data = []
        for line in lines[1:]:      # 첫 줄은 헤더이므로 건너뜀
            line = line.strip()     # 줄바꿈 문자 제거
            weather_id, mars_date, temp, storm = line.split(',')
            data.append((mars_date, float(temp), int(storm)))

        query = '''
        INSERT INTO mars_weather (mars_date, temp, storm)
        VALUES (%s, %s, %s)
        '''
        db.execute_many_query(query, data)
        

    except Exception as e:
        print(f'CSV 처리 중 오류 발생: {e}')

    finally:
        db.close()

if __name__ == '__main__':
    db = MySQLHelper(
        host='localhost',
        user='root',
        password='root',
        database='mars_weather'
    )
    if db.connection:
        load_csv_and_insert(csv_file_path, db)
    else:
        print('데이터베이스 연결에 실패했습니다. 프로그램을 종료합니다.')

    # query = 'SELECT * FROM mars_weather'
    # result = db.fetch_query(query)
    # for row in result:
    #     print(row)
    # db.close()
