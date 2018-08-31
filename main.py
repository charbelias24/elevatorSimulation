from visual import *

def main():

    is_visual = True
    sim1 = Simulation(mode = 0, visual=is_visual)
    sim2 = Simulation(mode = 1, visual=is_visual)

    visual = Visual((sim1, sim2))
    vis = Thread(target=visual.draw)

    if is_visual:
        vis.start()

    t1 = Thread(target=sim1.start_elevator)
    t2 = Thread(target=sim2.start_elevator)

    t1.start()
    sleep(0.5)
    t2.start()

    t1.join()
    t2.join()
    vis.join()


if __name__ == "__main__":
    main()
