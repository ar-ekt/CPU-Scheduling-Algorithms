from typing import List
from functools import cmp_to_key
from cpu_scheduling_algorithms import CPUSchedulingAlgorithms
from process import Process


class SJF(CPUSchedulingAlgorithms):
    def __init__(self, processes: List[Process], depend_total_burst_time: int):
        super().__init__(processes, "SJF")

        self.depend_total_burst_time = depend_total_burst_time
        self.ready_queue = self.processes[:]

    def process(self, process: Process):
        burst_start_time = max(process.ready_time, self.last_time)
        burst_end_time = burst_start_time + process.burst_times[process.level]

        if process.start_time is None:
            process.start_time = burst_start_time

        if process.level != process.last_level:
            process.ready_time = burst_end_time + process.io_times[process.level]
            process.level += 1
            self.ready_queue.append(process)
        else:
            process.complete_time = burst_end_time
            process.calculate()

        self.last_time = burst_end_time

    def schedule(self):
        while self.ready_queue:
            next_process: Process = self.get_next_process()
            self.process(next_process)

        self.calculate()

    def compare(self, process1: Process, process2: Process, ready_mode: bool):
        cmp_tuple1 = (ready_mode and process1.ready_time,
                      sum(process1.burst_times[process1.level:]) + sum(process1.io_times[process1.level:]) if self.depend_total_burst_time else process1.burst_times[process1.level],
                      process1.process_id)

        cmp_tuple2 = (ready_mode and process2.ready_time,
                      sum(process2.burst_times[process2.level:]) + sum(process2.io_times[process2.level:]) if self.depend_total_burst_time else process2.burst_times[process2.level],
                      process2.process_id)

        return -1 if cmp_tuple1 < cmp_tuple2 else 1 if cmp_tuple1 > cmp_tuple2 else 0

    def get_next_process(self) -> Process:
        ready_processes_ontime = [p for p in self.ready_queue if p.ready_time <= self.last_time]

        if len(ready_processes_ontime) == 0:
            next_process = sorted(self.ready_queue, key=cmp_to_key(lambda p1, p2: self.compare(p1, p2, True)))[0]
        else:
            next_process = sorted(ready_processes_ontime, key=cmp_to_key(lambda p1, p2: self.compare(p1, p2, False)))[0]

        self.ready_queue.remove(next_process)
        return next_process