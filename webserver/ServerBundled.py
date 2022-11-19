import json
import math
import socket
import sys
from datetime import datetime

import mysql.connector

# 服务端固定每页50条数据
PAGE_SIZE = 50


# DBmsConnect
class DBmsConnect:

    def __init__(self):
        self.dbms = mysql.connector.connect(
            host='1.12.59.12',
            user='xws',
            password='Yanzi@520',
            database='game_zone'
        )


def calculate_data_pages_and_total():
    # query data from game_links table
    cursor.execute('SELECT game_id, game_name FROM game_links')
    data = cursor.fetchall()
    return {'total': len(data), 'pages': math.ceil(len(data) / PAGE_SIZE)}


def make_data(current):
    records = []

    # query data from game_links table
    offset = current * PAGE_SIZE - PAGE_SIZE
    sql = f'SELECT game_id, game_name FROM game_links LIMIT {PAGE_SIZE} OFFSET {offset}'
    cursor.execute(sql)
    data = cursor.fetchall()

    # query detail based on game_id
    for row in data:
        val = row['game_id']
        sql_detail = f"SELECT game_id, \
        game_cn_name, \
        game_original_name, \
        game_total_story_time, \
        game_release_date_and_platform, \
        game_type, \
        game_is_cn_supported, \
        game_producer, \
        game_desc, \
        game_player_tags FROM game_details WHERE game_id = '{val}'"
        cursor.execute(sql_detail)
        row_detail = cursor.fetchone()
        row['detail'] = row_detail
        records.append(row)

    return records


def run_server():
    # Define socket host and port
    SERVER_HOST = '0.0.0.0'
    SERVER_PORT = 5555

    # Create socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(10)
    print('Server running...')
    print(f'Listening on port {SERVER_PORT}')

    while True:
        # Wait for client connections
        try:
            client_connection, client_address = server_socket.accept()
        except Exception as e:
            print(e)
            sys.exit()
        print('========================start=================')
        print(f'{datetime.now()}\n')
        print(f'Request coming from {client_address[0]}:{client_address[1]}')
        print()
        # Get the client request
        request = ''
        try:

            request = client_connection.recv(1024).decode()
            print('====Request info====')
            print(request)
        except Exception as e:
            print('====error info======')
            print(e)
            pass

        print('=======================end=================\n\n')
        # query method
        method = ''
        # query path
        path = ''
        # query param
        query_params = {'current': 1}
        try:
            # query method
            method = request.split('\r\n')[0].split()[0]
            # query full path
            path = request.split('\r\n')[0].split()[1]
            # query info
            query_info = path.split('?')[1]
            query_current_str = query_info.split('&')[0]
            query_params = {'current': int(query_current_str.split('=')[1])}
        except Exception as e:
            print(e)
            pass
        # response header
        header = ''
        # response body
        body = ''
        # final response
        response = ''
        # only support get method now
        if method == 'GET':
            if path.startswith('/api/list'):
                header = 'Content-Type:text/json'
                # 请求页数超过最大页数
                if query_params['current'] > data_info['pages']:
                    response = f'HTTP/1.1 403 Forbidden\n\nForbidden'
                    client_connection.sendall(response.encode())
                    client_connection.close()
                    continue
                records = {
                    'code': 0,
                    'status': 'ok',
                    'data': {
                        'current': query_params['current'],
                        'page_size': PAGE_SIZE,
                        'pages': data_info['pages'],
                        'total': data_info['total'],
                        'records': make_data(query_params['current'])
                    }
                }
                body = json.dumps(records, ensure_ascii=False)
            response = f'HTTP/1.1 200 OK\n{header}\n\n{body}'
        else:
            response = f'HTTP/1.1 405 Method Not Allowed\n\n'

        # Send HTTP response
        try:
            client_connection.sendall(response.encode())
        except Exception as e:
            print('====error info======')
            print(e)
            pass
        client_connection.close()

    # Close socket
    server_socket.close()


if __name__ == '__main__':
    # 连接数据库
    dbms = DBmsConnect().dbms
    cursor = dbms.cursor(dictionary=True)
    # 获取列表总数信息
    data_info = calculate_data_pages_and_total()
    run_server()
