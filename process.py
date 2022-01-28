from typing import List


class Process:
    def __init__(self, process_id: int, arrival_time: int, burst_times: List[int], io_times: List[int]):
        self.process_id = process_id
        self.arrival_time = arrival_time
        self.burst_times = burst_times
        self.io_times = io_times
        self.no_bursts = len(self.burst_times)
        self.total_burst_time = sum(self.burst_times)

        self.level = 0
        self.last_level = self.no_bursts - 1
        self.ready_time = self.arrival_time

        self.start_time = None
        self.complete_time = None

    def __str__(self: "Process"):
        return f"P{self.process_id:<3}\t{self.start_time:<4}\t{self.complete_time:<4}\t{self.response_time:<4}\t{self.turn_around_time:<4}\t{self.waiting_time:<4}"

    def __lt__(self, other: "Process"):
        return (self.ready_time, self.process_id) < (other.ready_time, other.process_id)

    def __eq__(self, other):
        return self.process_id == other.process_id

    def calculate(self):
        self.response_time = self.start_time - self.arrival_time
        self.turn_around_time = self.complete_time - self.arrival_time
        self.waiting_time = self.turn_around_time - (self.total_burst_time + sum(self.io_times))