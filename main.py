from pandas import read_csv
from copy import deepcopy
from typing import List
from process import Process
from fcfs import FCFS
from rr import RR
from sjf import SJF
from mlfq import MLFQ


def process_generator(csv_file_name: str) -> List[Process]:
    processes = []
    rows = read_csv(csv_file_name).to_dict(orient="records")
    for row in rows:
        process = Process(row["process_id"],
                          row["arrival_time"],
                          [row["cpu_time1"], row["cpu_time2"]],
                          [row["io_time"]])
        processes.append(process)
    return processes


if __name__ == "__main__":
    processes = process_generator("process_inputs.csv")

    fcfs_scheduler = FCFS(deepcopy(processes))
    fcfs_scheduler.schedule()
    print(fcfs_scheduler, end="\n\n\n")

    rr_scheduler = RR(deepcopy(processes), 5)
    rr_scheduler.schedule()
    print(rr_scheduler, end="\n\n\n")

    sjf_scheduler = SJF(deepcopy(processes), False)
    sjf_scheduler.schedule()
    print(sjf_scheduler, end="\n\n\n")

    mlfq_scheduler = MLFQ(deepcopy(processes), 8, 16)
    mlfq_scheduler.schedule()
    print(mlfq_scheduler)