from datetime import datetime
import socket
import json

UDP_IP = '127.0.0.1'
UDP_PORT = 5000


def run_server(ip=UDP_IP, port=UDP_PORT):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = ip, port
    sock.bind(server)
    try:
        while True:
            data, address = sock.recvfrom(1024)
            print(f'Received data: {json.loads(data)} from: {address}')
            form_data = json.loads(data)
            print(form_data, type(form_data))
            make_coment(form_data)
            print(f'Wrote: {json.loads(data)} in: data.json')
            sock.sendto(data, address)
            print(f'Send data: {json.loads(data)} to: {address}')

    except KeyboardInterrupt:
        print(f'Destroy server')
    finally:
        sock.close()


def make_coment(form_data):
    # Get the current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

    # Load existing JSON data from the file
    storage_path = 'storage/data.json'
    try:
        with open(storage_path, 'r', encoding='utf-8') as json_file:
            existing_data = json.load(json_file)
    except FileNotFoundError:
        existing_data = {}

    # Add the new entry to the existing data
    existing_data[timestamp] = {
        "username": form_data.get('username', ''),
        "message": form_data.get('message', '')
    }

    # Save the updated data as JSON
    with open(storage_path, 'w', encoding='utf-8') as json_file:
        json.dump(existing_data, json_file, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    run_server(UDP_IP, UDP_PORT)
