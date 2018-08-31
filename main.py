from test_structure import *
from threading import Thread
from time import sleep

def main():
    simulation = Simulation(1)
    Thread(target=simulation.start_elevator).start()



if __name__ == "__main__":
    main()