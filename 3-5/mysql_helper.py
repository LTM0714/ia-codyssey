# pip install mysql-connector-python

import mysql.connector
from mysql.connector import Error

class MySQLHelper:
    def __init__(self, host, user, password, database):
        try:
            self.connection = mysql.connector.connect(
                host = host,
                user = user,
                password = password,
                database = database
            )

            if self.connection.is_connected():
                db_info = self.connection.server_info
                print(f'MySQL 서버 버전: {db_info}')

                self.cursor = self.connection.cursor()

                # 연결된 DB명 확인
                self.cursor.execute('SELECT DATABASE()')
                db_name = self.cursor.fetchone()[0]
                print(f'현재 연결된 데이터베이스: {db_name}')

        except Error as e:
            print(f'MySQL 연결 중 오류 발생: {e}')
            self.connection = None
            self.cursor = None

    # 쿼리 실행 메서드
    def excute_query(self, query, values=None):
        try:
            self.cursor.excute(query, values)
            self.connection.commit()
            print('쿼리 실행 완료.')
        except Error as e:
            print(f'쿼리 실행 중 오류 발생: {e}')

    # 여러 개의 쿼리를 실행하는 메소드
    def execute_many_query(self, query, values: list):
        try:
            self.cursor.executemany(query, values)
            self.connection.commit()
            print(f'{self.cursor.rowcount}건 쿼리 실행 완료.')

        except Error as e:
            print(f'쿼리 실행 중 오류 발생: {e}')

    # 데이터 조회 메서드
    def fetch_query(self, query):
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as e:
            print(f'SELECT 쿼리 실행 중 오류 발생: {e}')

    def close(self):
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print('MySQL 연결 종료됨.')