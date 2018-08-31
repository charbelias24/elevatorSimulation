# ElevatorSimulation
## Description
### Short description
The aim of the competition is to create a virtual game that simulates a real life problem and
enhance your skills in Python programming and data analysis. The competition is all digital
(without physical making).
#### What do you win?
The winner of the competition wins a course on Python in Germany with Python expert Bernd
Klein. The course will take place in a German city (Munich, Berlin, Frankfurt, …) or at the
beautiful Lake Constance area, close to Switzerland.
### Full description
The task is about elevators and the simulation of their usage. Elevators seem to be a modern
invention, but at a closer look you will find out that they are older than 2000 years. It goes back
to the Roman architect Vitruvius, who claims that it has already been invented by Archimedes.
Anyway, elevators became a necessity with the birth of skyscapers.
The idea for this task was born in a hotel in Berlin. Elevators - as most most people know them -
only move, if buttons are pushed. If you board an elevator and push the button for the fourth
floor, it will go to this floor. It will wait now on the fourth level until either somebody boards the
cabin or somebody puts a button on another level to call an elevator. The three elevators in this
hotel work differently. First of all, they are waiting most of the time at ground floor. After taking
one or more people to the desired destination, an elevator will immediately return to the
groundfloor, maybe taking in passengers on intermediate floors on their way down.
This way a new guest arriving at the hotel will nearly always find at least one of the three
elevators ready to board. This means nearly no waiting time at ground-floor, but on the other
hand, you will have to wait on all other floors with almost absolute certainty.

The task consists in simulating the movements of the elevators. We will count the number of
levels the elevators go up and down. If a person uses an elevator from the ground-floor to the
third floor, the elevator moves three levels. If it moves back to ground-floor, the total number will
be six levels.
We can write a program, simulating people randomly coming into our hotel and move to a
random floor. They will remain for a random time on this floor - most probably in their room,
before they go down again or maybe into the basement. In the beginning our hotel is completely
empty, after this we have to keep track of the people on the different floors. We also have to
simulate the effect if people go down from 5th floor and pick up people on other levels.
We compare both kinds of elevator behaviours, i.e. the “normal” behaviour and the “return to
basement” one.
