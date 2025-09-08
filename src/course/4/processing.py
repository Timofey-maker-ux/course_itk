import json
import math
import multiprocessing
import random
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


def generate_data(n):
    return [random.randint(1, 1000) for _ in range(n)]


def process_number(n):
    return math.factorial(n)


def run_single(data):
    start = time.time()
    [process_number(n) for n in data]
    return time.time() - start


def run_threadpool(data):
    start = time.time()
    with ThreadPoolExecutor() as executor:
        list(executor.map(process_number, data))
    return time.time() - start


def run_processpool(data):
    start = time.time()
    with ProcessPoolExecutor() as executor:
        list(executor.map(process_number, data))
    return time.time() - start


def worker(input_queue, output_queue):
    while True:
        n = input_queue.get()
        if n is None:
            break
        process_number(n)
        output_queue.put(1)


def run_multiprocessing_process(data):
    start = time.time()
    cpu_count = multiprocessing.cpu_count()
    input_queue = multiprocessing.Queue()
    output_queue = multiprocessing.Queue()

    processes = [
        multiprocessing.Process(target=worker, args=(input_queue, output_queue))
        for _ in range(cpu_count)
    ]
    for p in processes:
        p.start()

    for n in data:
        input_queue.put(n)
    for _ in processes:
        input_queue.put(None)

    for _ in data:
        output_queue.get()

    for p in processes:
        p.join()

    return time.time() - start


def main():
    N = 100000
    data = generate_data(N)

    times = dict()
    times["single"] = run_single(data)
    times["threadpool"] = run_threadpool(data)
    times["processpool"] = run_processpool(data)
    times["multiprocessing_process"] = run_multiprocessing_process(data)

    print("Время выполнения (сек):")
    for k, v in times.items():
        print(f"{k}: {v:.3f}")

    with open("timings.json", "w", encoding="utf-8") as f:
        json.dump(times, f, indent=2)


if __name__ == "__main__":
    main()
