from structure import *
from threading import Thread


def main():
    sim1 = Simulation(mode = 0, visual=False)
    sim2 = Simulation(mode = 1, visual=False)
    t1 = Thread(target=sim1.start_elevator)
    t2 = Thread(target=sim2.start_elevator)

    t1.start()
    sleep(0.5)
    t2.start()
    sleep(0.5)

    t1.join()
    t2.join()


if __name__ == "__main__":
    main()
