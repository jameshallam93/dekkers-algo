import threading
import time
from random import randint
import argparse


class CriticalSection():
    def __init__(self, debug) -> None:
        self.data = []
        self.turn = 0
        self.flag = [False, False]
        self.ops = []
        self.debug = debug

    def modify_data(self, process: int) -> None:
        if self.debug:
            print(
                f'Process {process} is performing expensive calculation on data')
            time.sleep(2.5)
        else:
            time.sleep(randint(0, 10) / 1000)
        random_int = randint(0, 100)
        random_int2 = randint(0, 100)
        random_index = randint(0, len(self.data) -
                               1) if len(self.data) > 0 else 0
        self.data.append(random_int)
        self.data.append(random_int2)
        self.data.pop(random_index)
        self.ops.append({
            'process': process,
            'random_int': random_int,
            'random_int2': random_int2,
            'random_index': random_index
        })
        if self.debug:
            print(f'Process {process} modified data')
            print(
                f'Process {process} added ints: {random_int} + {random_int2}. data: {self.data}')
            print(
                f'Process {process} popped index: {random_index}. data: {self.data}')

    def enter(self, process: int) -> None:
        # set flag to indicate that process wants to enter critical section
        if self.debug:
            print(f'Process {process} wants to enter critical section')
        self.flag[process] = True
        # check if other process is in critical section, check who has the turn
        while self.flag[1 - process] and self.turn == 1 - process:
            if self.debug:
                print(
                    f'Process {process} is waiting for process {1 - process} to leave critical section')
                time.sleep(1)
            # if other process is in critical section and has turn, remove own flag and wait
            self.flag[process] = False
            pass
        if self.debug:
            print(f'Process {process} has entered critical section')
        # once other process has switched turns, set flag to indicate that process wants to enter critical section
        self.flag[process] = True
        # simulate critical section data manipulation
        self.modify_data(process)
        self.leave(process)

    def leave(self, process: int) -> None:
        # remove flag to indicate that process has left critical section
        # switch turn to other process
        self.turn = 1 - process
        self.flag[process] = False
        if self.debug:
            print(f'Process {process} has left critical section')

    def get_data(self) -> list:
        return self.data

    def get_ops(self) -> list:
        return self.ops


class Process():
    def __init__(self, process: int, cs: CriticalSection, debug: bool) -> None:
        self.process = process
        self.cs = cs
        self.debug = debug

    def run(self) -> None:
        length_of_time = randint(
            0, 10) if self.debug else randint(0, 10) / 1000
        for _ in range(100):
            time.sleep(length_of_time)
            self.cs.enter(self.process)


def interpret_ops(ops: list, cs: CriticalSection) -> None:
    expected_data = []
    for op in ops:
        print(
            f'Process {op["process"]} added {op["random_int"]} and {op["random_int2"]} and popped {op["random_index"]}')
        expected_data.append(op["random_int"])
        expected_data.append(op["random_int2"])
        expected_data.pop(op["random_index"])

    print(f'Expected data: {expected_data}')
    print(f'Actual data: {cs.get_data()}')
    print(f'Equal: {expected_data == cs.get_data()}')


def main(debug=False) -> None:
    cs = CriticalSection(debug=debug)
    p1 = Process(0, cs, debug=debug)
    p2 = Process(1, cs, debug=debug)
    t1 = threading.Thread(target=p1.run)
    t2 = threading.Thread(target=p2.run)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print(cs.get_data())
    print(cs.get_ops())
    interpret_ops(cs.get_ops(), cs)


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('--debug', action='store_true')
    args = args.parse_args()
    main(args.debug)
