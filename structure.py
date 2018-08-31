from random import randint, choice
from threading import Thread
from time import sleep


class Simulation:
    total_floors = 7
    total_elevators = 3
    max_people_per_step = 2
    max_people_in_hotel = 10
    max_people_generated = 20

    step = 0.1  # each elevator step is 1 second

    def __init__(self, mode):
        self.mode = mode
        self.floors = {}
        self.elevators = []
        self.nb_times_elevator_used_from_gf = 0
        self.nb_times_elevator_used_from_other = 0
        self.gf_wait_time = 0
        self.other_wait_time = 0
        # Generating the elevators
        for _ in range(Simulation.total_elevators):
            self.elevators.append(Elevator())

        # Generating the floors
        for floor_nb in list(range(-1, Simulation.total_floors))[::-1]:
            self.floors[str(floor_nb)] = Floor(floor_nb)

    def generate_people_at_gf(self):
        """ Generate the people at ground floor each with a specific direction
        """
        for _ in range(0, randint(0, Simulation.max_people_per_step)):
            direction = randint(-1, Simulation.total_floors)
            if direction >= 0:
                direction = 1
            # testing = randint(-1,Simulation.total_floors - 1)
            self.floors['0'].people.append(Person(direction=direction))

    def generate_people_at_gf_steps(self):
        """ generate people at gf every one step until the max is reached
        """
        while Person.available_count < Simulation.max_people_generated:
            self.generate_people_at_gf()
            sleep(self.step)

    def there_is_elev_on_person_floor(self, floor, person):
        best_elevator = 0
        for elevator in self.elevators:
            if len(elevator.people) < Elevator.max_nb_people and \
                            elevator.curr_floor == person.curr_floor:
                best_elevator = elevator
                break
        return best_elevator

    def there_is_elev_on_same_route_as_person(self, floor, person):
        best_elevator = 0
        min_distance = Simulation.total_floors + 1

        for elevator in self.elevators:
            if len(elevator.people) < Elevator.max_nb_people and \
                    person.on_the_elev_route(floor, elevator) and \
                            abs(elevator.curr_floor - person.curr_floor) < min_distance:
                min_distance = abs(elevator.curr_floor - person.curr_floor)
                best_elevator = elevator

        return best_elevator

    def there_is_elev_below_or_above_person(self, floor, person):
        best_elevator = 0
        min_distance = Simulation.total_floors + 1
        for elevator in self.elevators:
            if len(elevator.people) < Elevator.max_nb_people and \
                            abs(elevator.curr_floor - person.curr_floor) < min_distance and \
                    (elevator.direction == 1 and person.curr_floor >= max(elevator.curr_dest)) or \
                    (elevator.direction == -1 and person.curr_floor <= min(elevator.curr_dest)):
                ####CHECK####
                min_distance = abs(elevator.curr_floor - person.curr_floor)
                best_elevator = elevator

        return best_elevator

    def there_is_elev_none_of_above(self, floor, person):
        best_elevator = 0
        min_distance = Simulation.total_floors + 1
        for elevator in self.elevators:
            if len(elevator.people) < Elevator.max_nb_people and \
                            abs(elevator.curr_floor - person.curr_floor) < min_distance:
                # not elevator.curr_dest:
                ####CHECK####
                min_distance = abs(elevator.curr_floor - person.curr_floor)
                best_elevator = elevator

        return best_elevator

    def elevator_available(self, floor, person):
        """ returns the best elevator for each person
        """
        priority_elevators = [self.there_is_elev_on_person_floor,
                              self.there_is_elev_on_same_route_as_person,
                              self.there_is_elev_below_or_above_person,
                              self.there_is_elev_none_of_above]

        for choose_elevator in priority_elevators:
            best_elevator = choose_elevator(floor, person)
            if best_elevator:
                return best_elevator

                # add the additional elevator cases

    def people_floor_to_elev(self, floor):
        possible_people = list(filter(lambda x: x.direction != 0, floor.people))
        for i in range(len(possible_people)):
            person = possible_people[i]
            curr_elevator = self.elevator_available(floor, person)
            if curr_elevator:
                if not curr_elevator.reserve_for_person(person):
                    if person.can_enter_elevator(curr_elevator):
                        person.enter_elevator_from_floor(floor, curr_elevator)
                        if not floor.floor_nb:
                            self.nb_times_elevator_used_from_gf += 1
                        else:
                            self.nb_times_elevator_used_from_other += 1

                        # print("{} just used the elevator at floor {}".format(person.id, floor.floor_nb))
                        i -= 1
            else:
                pass
                # print("No elevator available to take you out!")
                # self.person_floor_to_elev(floor, possible_people[i])

    def people_floors_to_elev(self):
        for floor in self.floors.values():
            self.people_floor_to_elev(floor)

    def person_elev_to_floor(self, elev, person):
        elev.remove_person(person)
        self.floors[str(elev.curr_floor)].add_person(person)
        person.direction = 0
        person.in_elevator = False
        person.curr_floor = person.curr_dest
        elev.remove_curr_floor_from_dest()
        person.check_leave_hotel(self.floors[str(elev.curr_floor)])

    def people_elev_to_floor(self, elev):
        for person in list(filter(lambda x: x.curr_dest == elev.curr_floor, elev.people))[::-1]:
            self.person_elev_to_floor(elev, person)

    def people_elevs_to_floor(self):
        for elev in self.elevators:
            self.people_elev_to_floor(elev)

    def make_people_leave_floors(self):
        for floor in self.floors.values():
            floor.people_want_to_leave()

    def calculate_wait_time(self):
        for floor in self.floors.values():
            for person in list(filter(lambda x: x.direction != 0, floor.people)):
                person.increment_wait_time()
                if person.curr_floor == 0:
                    self.gf_wait_time += 1
                else:
                    self.other_wait_time += 1

    def display_results(self):
        print()
        print("-*" * 30)
        print("Total wait time at GF:", self.gf_wait_time)
        print("Total wait time at OT:", self.other_wait_time)
        print("Total steps of elevators from GF:", self.nb_times_elevator_used_from_gf)
        print("Total steps of elevators from OT:", self.nb_times_elevator_used_from_other)
        print("Average waiting time at GF:", self.gf_wait_time / self.nb_times_elevator_used_from_gf)
        print("Average waiting time at OT:", self.other_wait_time / self.nb_times_elevator_used_from_other)
        print("-*" * 30)

    def start_elevator(self):
        first_time = True
        while Person.available_count or first_time:
            # Testing

            if Person.total_count < Simulation.max_people_generated:
                self.generate_people_at_gf()

            if Person.total_count:
                first_time = False

            for elevator in self.elevators:
                elevator.set_relevant_direction()

            self.visualize()
            self.make_people_leave_floors()
            self.people_floors_to_elev()
            self.calculate_wait_time()
            self.people_elevs_to_floor()

            sleep(Simulation.step)
            self.visualize()

            elev_thread = []
            for i, elevator in enumerate(self.elevators):
                elev_thread.append(Thread(target=elevator.move_elevator))
                elev_thread[i].start()

            for i in range(Simulation.total_elevators):
                elev_thread[i].join()

            sleep(Simulation.step)
        self.display_results()


    def visualize(self):
        print("*" * 30)
        for i, elev in enumerate(self.elevators):
            print("E{} (dir{}) at floor {}:".format(i, elev.direction, elev.curr_floor), end=" ")
            for des in elev.curr_dest:
                print("D{}".format(des), end=" ")
            print(end="--")
            for per in elev.people:
                print("P{}(dir{},flr{},des{})".format(per.id,
                                                      per.direction, per.curr_floor, per.curr_dest), end=" ")
                # print("P{}".format(per.id), end = " ")
            print()
        print("-" * 30)
        for floor in self.floors.values():
            print("F{0:>2}:".format(floor.floor_nb), end=" ")
            for per in floor.people:
                print("P{}(dir{},flr{},des{})".format(per.id,
                                                      per.direction, per.curr_floor, per.curr_dest), end=" ")
                # print("P{}".format(per.id), end=" ")
            print()


class Person:
    total_count = 0
    available_count = 0

    def __init__(self, direction=0, curr_floor=0, curr_dest=0, leave_hotel=0):
        self.direction = direction
        self.curr_floor = curr_floor
        self.curr_dest = curr_dest
        self.leave_hotel = leave_hotel
        self.id = Person.total_count
        self.in_elevator = False
        self.wait_time = 0
        Person.available_count += 1
        Person.total_count += 1

    def __del__(self):
        Person.available_count -= 1

    def choose_curr_dest(self):
        """ Choose a random destination floor from the list of possible floors
        """
        possible_dest = []
        # print("ID:", self.id,"Dir:",self.direction)
        if self.direction == 1:
            possible_dest = list(range(self.curr_floor + 1, Simulation.total_floors))
        elif self.direction == -1:
            possible_dest = list(range(0, self.curr_floor)) * 3
            possible_dest.append(-1)
            possible_dest.extend([0] * 5)
            # print(possible_dest)
        self.curr_dest = choice(possible_dest)
        if not self.curr_dest:
            self.leave_hotel = 1
        return self.curr_dest

    def can_enter_elevator(self, elevator):
        """ Check if the person wants and can enter the elevator
        """
        if (self.direction != 0) and \
                (self.curr_floor == elevator.curr_floor) and \
                (len(elevator.people) < elevator.max_nb_people) and \
                ((elevator.direction == self.direction) or (elevator.direction == 0)):
            return True
        return False

    def enter_elevator_from_floor(self, floor, elevator):
        floor.remove_person(self)
        elevator.add_person(self)
        elevator.curr_dest.add(self.choose_curr_dest())
        self.in_elevator = True
        # elevator.set_relevant_direction()

    def on_the_elev_route(self, floor, elevator):
        if (elevator.direction == self.direction == 1 and \
                            elevator.curr_floor <= self.curr_floor <= max(elevator.curr_dest)) or \
                (elevator.direction == self.direction == -1 and \
                                 min(elevator.curr_dest) <= self.curr_floor <= elevator.curr_floor):
            # print("FOUND ELEVATOR THAT HAS THE SAME ROUTE AS MINE", self.id)
            return True
        else:
            return False

    def check_direction(self):
        if self.direction == 1 and self.curr_floor == Simulation.total_floors - 1:
            self.direction = -1
        elif self.direction == -1 and self.curr_floor == -1:
            self.direction = 1

    def check_leave_hotel(self, floor):
        if self.leave_hotel:
            floor.remove_person(self)
            del self

    def increment_wait_time(self):
        if self.direction and not self.in_elevator:
            self.wait_time += 1
        #print("{} is waiting at the floor {} for {}s".format(self.id, self.curr_floor, self.wait_time))


class Elevator:
    total_steps = 0
    max_nb_people = 8

    def __init__(self, direction=0, curr_floor=0):
        self.direction = direction
        self.curr_floor = curr_floor
        self.curr_dest = set()
        self.people = []

    def add_person(self, person):
        self.people.append(person)

    def remove_person(self, person):
        self.people.remove(person)

    def reserve_for_person(self, person):
        if self.curr_floor != person.curr_floor:
            self.curr_dest.add(person.curr_floor)
            return True
        return False
        # should i change the direction too?

    def set_relevant_direction(self):
        tmp_curr_dest = []

        if self.curr_floor == Simulation.total_floors - 1:
            self.direction = 0
        elif self.curr_floor == -1:
            self.direction = 0

        if self.curr_dest:
            if len(self.curr_dest) == 1 and list(self.curr_dest)[0] == self.curr_floor:
                self.direction = 0
            else:
                tmp_curr_dest.extend(self.curr_dest)
                tmp_curr_dest.sort()
                if not self.direction:
                    if tmp_curr_dest[0] > self.curr_floor:
                        self.direction = 1
                    else:
                        self.direction = -1

                elif self.direction == 1:
                    if tmp_curr_dest[-1] < self.curr_floor:
                        self.direction = -1

                else:
                    if tmp_curr_dest[0] > self.curr_floor:
                        self.direction = 1
        else:
            self.direction = 0

    def move_elevator(self):
        self.set_relevant_direction()
        if self.direction == 1:
            self.curr_floor += 1
            Elevator.total_steps += 1
        elif self.direction == -1:
            self.curr_floor -= 1
            Elevator.total_steps += 1
        self.remove_curr_floor_from_dest()

    def remove_curr_floor_from_dest(self):
        if self.curr_floor in self.curr_dest:
            self.curr_dest.remove(self.curr_floor)


class Floor:
    def __init__(self, floor_nb):
        self.floor_nb = floor_nb
        self.people = []

    def add_person(self, person):
        self.people.append(person)

    def remove_person(self, person):
        self.people.remove(person)

    def people_want_to_leave(self):
        if self.people and choice((0, 1)) and self.floor_nb:
            nb_people_leaving = randint(0, int(max(min(5, len(self.people) / 4), 1)))
            for i in range(int(nb_people_leaving)):
                # print("Changing direction of someone")
                tmp_person_choice = choice(self.people)
                if tmp_person_choice.curr_floor == -1:
                    tmp_person_choice.direction = 1
                elif tmp_person_choice.curr_floor >= Simulation.total_floors - 2:
                    tmp_person_choice.direction = -1
                else:
                    tmp_person_choice.direction = choice((-1, -1, -1, 1))
