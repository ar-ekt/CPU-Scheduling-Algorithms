from typing import List
from queue import PriorityQueue
from process import Process

OUTPUT_FORMAT = (f"{'':=^45}\n{{0:^45}}\n{'':=^45}\n"
                 "    \tST  \tCT  \tRT  \tTAT \tWT\n"
                 "{1}\n"
                 f"{'':-^45}\n"
                 "AVG \t    \t    \t{2:.3f}\t{3:.3f}\t{4:.3f}\n\n"
                 "    \tTotal Time:   {5}\n"
                 "    \tIdle Time:    {6}\n"
                 "    \tUtilization:  {7}\n"
                 "    \tThroughput:   {8}")

class CPUSchedulingAlgorithms:
    def __init__(self, processes: List[Process], algorithm_name: str):
        self.algorithm_name = algorithm_name
        self.processes = processes
        self.no_processes = len(self.processes)
        self.last_time = 0

    def __str__(self):
        return OUTPUT_FORMAT.format(self.algorithm_name, "\n".join(map(str, self.processes)),
                                    self.average_response_time, self.average_turn_around_time, self.average_waiting_time,
                                    self.total_time, self.idle_time, self.utilization, self.throughput)

    def calculate(self):
        self.average_response_time = sum(p.response_time for p in self.processes) / self.no_processes
        self.average_turn_around_time = sum(p.turn_around_time for p in self.processes) / self.no_processes
        self.average_waiting_time = sum(p.waiting_time for p in self.processes) / self.no_processes

        self.total_time = self.last_time
        self.idle_time = self.total_time - sum(p.total_burst_time for p in self.processes)

        self.utilization = (self.total_time - self.idle_time) / self.total_time
        self.throughput = self.no_processes * 1000 / self.total_time