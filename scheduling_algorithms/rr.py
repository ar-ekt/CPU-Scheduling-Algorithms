from typing import List
from queue import PriorityQueue
from cpu_scheduling_algorithms import CPUSchedulingAlgorithms
from process import Process


class RR(CPUSchedulingAlgorithms):
    def __init__(self, processes: List[Process], time_quantum: int, fill: bool = True):
        super().__init__(processes, "RR")

        self.time_quantum = time_quantum
        self.ready_queue = PriorityQueue()
        if fill:
            for p in self.processes:
                self.ready_queue.put(p)

    def process(self, process: Process):
        burst_start_time = max(process.ready_time, self.last_time)
        burst_time = min(process.burst_times[process.level], self.time_quantum)
        burst_end_time = burst_start_time + burst_time
        process.burst_times[process.level] -= burst_time

        if process.start_time is None:
            process.start_time = burst_start_time

        if process.burst_times[process.level] != 0:
            process.ready_time = burst_end_time
            self.ready_queue.put(process)
        elif process.level != process.last_level:
            process.ready_time = burst_end_time + process.io_times[process.level]
            process.level += 1
            self.ready_queue.put(process)
        else:
            process.complete_time = burst_end_time
            process.calculate()

        self.last_time = burst_end_time

    def schedule(self):
        while not self.ready_queue.empty():
            next_process: Process = self.ready_queue.get()
            self.process(next_process)

        self.calculate()