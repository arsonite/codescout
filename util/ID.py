import multiprocessing
import pyperclip
import threading
import time

from collections import Counter
from datetime import datetime
from uuid import uuid4


class IDThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self)

        self.id = kwargs.get('id')
        self.number = kwargs.get('number')
        self.uuids = []

    def run(self):
        print(f'Generating {self.number} IDs ...')
        for i in range(0, self.number):
            uuid = ID.generate()
            self.uuids.append(uuid)
        print(f'Created {self.number} IDs in thread {self.id}.')


class ID():
    @staticmethod
    def exists():
        return False

    @staticmethod
    def generate(printID=False):
        """
        Generates a 60-bit pseudo-random UUID with a custom algorithm that also takes the current timestamp into account,
        without exposing the MAC-address of the PC that the UUID is generated on (unlike the official UUID1 specification).
        Sucessfully tested collisions with 100.000.000 single threaded generated IDs in non-interrupted sequence and
        10.000.000 multi threaded generated IDs.

        Args:
            printID (bool, optional): Print the generated ID to the console. Defaults to False.
            copyToClipboard (bool, optional): Copy the generated ID to your systems clipboard. Defaults to False.

        Returns:
            String: The generated UUID
        """
        t = datetime.now()  # Grabbing current datetime
        datestamp = f'{t.day}{t.month}{t.year}'  # Reformat the date
        # Reformat the time, I seperated date and time to keep the date as a consistent part of the ID
        timestamp = f'{t.microsecond}{t.second}{t.minute}{t.hour}'
        # Converting date and time to integer and those integer into hex
        firstID = hex(int(timestamp))[2:] + hex(int(datestamp))[2:] + datestamp
        # Generating a pseudo-random second ID via UUID4 specification, to ensure further collision-safety
        secondID = (str(uuid4()) + str(uuid4())).replace('-', '')
        # Concatenating both IDs and trimming the final ID down to 60 bytes for DB and HTTP compatibility
        uuid = (firstID + secondID)[:60]
        if printID:
            print(f'Generated ID: {uuid}')
        return uuid

    @staticmethod
    def testCollision(number, multithreaded=False):
        uuids = []
        if multithreaded:
            threadCount = multiprocessing.cpu_count()
            print(f'Utilizing {threadCount} threads.')
            individualNumber = int(number / threadCount)
            threadPool = []
            for i in range(0, threadCount):
                threadPool.append(IDThread(id=i, number=individualNumber))

            for thread in threadPool:
                print(f'Starting thread {thread.id} ...')
                thread.start()

            for thread in threadPool:
                print(f'Joining thread {thread.id} ...')
                thread.join()

            print('All threads joined.')
            uuids = []
            print(f'Joining {individualNumber * threadCount} IDs ...')
            for thread in threadPool:
                uuids += thread.uuids
            print(f'Joined {individualNumber * threadCount} IDs.')

            print(f'Commencing collision checking.\n')
            duplicates = [item for item,
                          count in Counter(uuids).items() if count > 1]
            if len(duplicates) > 0:
                print('Found duplicates:\n')
                print(duplicates)
            else:
                print('No duplicates found.')

        else:
            print(f'Generating {number} IDs ...')
            for i in range(0, number):
                uuid = ID.generate()
                uuids.append(uuid)
            print(f'Created {number} IDs. Commencing collision checking.\n')
            duplicates = [item for item,
                          count in Counter(uuids).items() if count > 1]
            if len(duplicates) > 0:
                print('Found duplicates:\n')
                print(duplicates)
            else:
                print('No duplicates found.')


if __name__ == '__main__':
    # from TurtleHare import TurtleHare
    # TurtleHare.static.measure(ID.testCollision, 100_000_000, True)
    
    ID.generate(True, True)
