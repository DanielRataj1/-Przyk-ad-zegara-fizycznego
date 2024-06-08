import time
import random
import threading
import sys

class Process:
    def __init__(self, id):
        self.id = id
        self.clock = 0
        self.lock = threading.Lock()

    def increment_clock(self):
        with self.lock:
            increment = random.randint(1, 5)
            self.clock += increment
            print(f"Proces {self.id}: Zegar został zinkrementowany o {increment}. Aktualny czas: {self.clock}")

    def send_message(self, other):
        with self.lock:
            timestamp = self.clock
        print(f"Proces {self.id}: Wysłano wiadomość z czasem {timestamp} do procesu {other.id}")
        other.receive_message(timestamp)

    def receive_message(self, timestamp):
        with self.lock:
            self.clock = max(self.clock, timestamp)
        print(f"Proces {self.id}: Otrzymano wiadomość z czasem {timestamp}. Aktualny czas: {self.clock}")

def run_process(process, stop_event):
    while not stop_event.is_set():
        time.sleep(random.uniform(0.5, 2))
        process.increment_clock()

def simulate_communication(processes, stop_event):
    while not stop_event.is_set():
        sender, receiver = random.sample(processes, 2)
        sender.send_message(receiver)
        time.sleep(random.uniform(1, 3))

def terminate_program(stop_event):
    print("Koniec działania programu.")
    stop_event.set()
    sys.exit()

if __name__ == "__main__":
    num_processes = 3
    processes = [Process(i) for i in range(num_processes)]

    stop_event = threading.Event()

    # Uruchomienie wątków dla procesów
    threads = []
    for process in processes:
        t = threading.Thread(target=run_process, args=(process, stop_event))
        t.start()
        threads.append(t)

    # Symulowanie komunikacji między procesami
    communication_thread = threading.Thread(target=simulate_communication, args=(processes, stop_event))
    communication_thread.start()

    # Timer, który zakończy działanie programu po minucie
    timer = threading.Timer(60, terminate_program, args=(stop_event,))
    timer.start()

    for t in threads:
        t.join()
    communication_thread.join()
