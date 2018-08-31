from structure import *
from threading import Thread
from visual import *

def main():
    is_visual = False
    sim1 = Simulation(mode = 0, visual=is_visual)
    sim2 = Simulation(mode = 1, visual=is_visual)

    t1 = Thread(target=sim1.start_elevator)
    t2 = Thread(target=sim2.start_elevator)

    if is_visual:
        visual = Visual((sim1, sim2))
        vis = Thread(target=visual.draw)
        vis.start()

    t1.start()
    t2.start()
    #sleep(0.5)

    #gen.join()
    t1.join()
    t2.join()


if __name__ == "__main__":
    main()
