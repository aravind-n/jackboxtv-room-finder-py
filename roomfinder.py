import requests
import threading
from typing import List
from roomcodes import room_codes

class RoomFinderThread (threading.Thread):
    def __init__(self, room_codes: List[str]):
        threading.Thread.__init__(self)
        self.room_codes = room_codes

    def run(self):
        find_rooms(self.room_codes)

def find_rooms(room_codes: List[str]) -> None:
    # base endpoint
    base_url = 'https://blobcast.jackboxgames.com/room/'

    for code in room_codes:
        url = base_url + code

        resp = requests.get(url)

        # TODO log error

        if resp.status_code == 404:
            continue

        if resp.status_code == 500:
            continue

        try:
            room = resp.json()
        except:
            # TODO log the error
            continue

        if room['joinAs'] == 'audience':
            continue

        if room['requiresPassword']:
            continue

        if room['roomid'] == '':
            continue

        print('Room Code: ' + room['roomid'] + ', Game: ' + room['apptag'])

def main():
    print('Finding open rooms...')
    threads = []
    threads.append(RoomFinderThread(room_codes[:50000]))
    threads.append(RoomFinderThread(room_codes[50001:100000]))
    threads.append(RoomFinderThread(room_codes[100001:150000]))
    threads.append(RoomFinderThread(room_codes[150001:200000]))
    threads.append(RoomFinderThread(room_codes[200001:250000]))
    threads.append(RoomFinderThread(room_codes[250001:300000]))
    threads.append(RoomFinderThread(room_codes[300001:350000]))
    threads.append(RoomFinderThread(room_codes[350001:400000]))
    threads.append(RoomFinderThread(room_codes[400001:456976]))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == '__main__':
    main()