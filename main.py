from structure import *
from threading import Thread
from visual import *

def main():
    sim1 = Simulation(mode = 0, visual=True)
    sim2 = Simulation(mode = 1, visual=True)

    #gen = Thread(target=generate_people, args=[(sim1, sim2), ])
    visual = Visual((sim1, sim2))

    v = Thread(target=visual.draw)
    t1 = Thread(target=sim1.start_elevator)
    t2 = Thread(target=sim2.start_elevator)

    #gen.start()
    #sleep(0.01)
    v.start()

    t1.start()
    sleep(0.5)
    t2.start()
    sleep(0.5)

    #gen.join()
    t1.join()
    t2.join()
    while True:
        sleep(0.5)


if __name__ == "__main__":
    main()
