from typing import List, Tuple
from queue import PriorityQueue
from cpu_scheduling_algorithms import CPUSchedulingAlgorithms
from process import Process


class MLFQ(CPUSchedulingAlgorithms):
    def __init__(self, processes: List[Process], time_quantum1: int, time_quantum2: int):
        super().__init__(processes, "MLFQ")

        self.time_quantums = [time_quantum1, time_quantum2]
        self.ready_queues = [PriorityQueue(), PriorityQueue(), PriorityQueue()]
        for p in self.processes:
            self.ready_queues[0].put(p)

    def process(self, process: Process, queue_index: int):
        if queue_index in (0, 1):
            burst_start_time = max(process.ready_time, self.last_time)
            burst_time = min(process.burst_times[process.level], self.time_quantums[queue_index])
            burst_end_time = burst_start_time + burst_time
            process.burst_times[process.level] -= burst_time

            if process.start_time is None:
                process.start_time = burst_start_time

            if process.burst_times[process.level] != 0:
                process.ready_time = burst_end_time
                self.ready_queues[queue_index + 1].put(process)
            elif process.level != process.last_level:
                process.ready_time = burst_end_time + process.io_times[process.level]
                process.level += 1
                self.ready_queues[queue_index].put(process)
            else:
                process.complete_time = burst_end_time
                process.calculate()

            self.last_time = burst_end_time

        else:
            burst_start_time = max(process.ready_time, self.last_time)
            burst_end_time = burst_start_time + process.burst_times[process.level]

            if process.start_time is None:
                process.start_time = burst_start_time

            if process.level != process.last_level:
                process.ready_time = burst_end_time + process.io_times[process.level]
                process.level += 1
                self.ready_queues[queue_index].put(process)
            else:
                process.complete_time = burst_end_time
                process.calculate()

            self.last_time = burst_end_time

    def schedule(self):
        while not all(q.empty() for q in self.ready_queues):
            next_process, queue_index = self.get_next_process()
            self.process(next_process, queue_index)

        self.calculate()

    def get_next_process(self) -> Tuple[Process, int]:
        for queue_index in range(3):
            if not self.ready_queues[queue_index].empty():
                next_process: Process = self.ready_queues[queue_index].get()
                if next_process.ready_time <= self.last_time:
                    return next_process, queue_index
                else:
                    for check_queue_index in range(queue_index + 1, 3):
                        if not self.ready_queues[check_queue_index].empty():
                            check_next_process: Process = self.ready_queues[check_queue_index].get()
                            if check_next_process.ready_time <= next_process.ready_time:
                                self.ready_queues[queue_index].put(next_process)
                                return check_next_process, check_queue_index
                            else:
                                self.ready_queues[check_queue_index].put(check_next_process)
                    return next_process, queue_index