# ICFP Programming Contest 2024 

We competed in the 24h lightning division, June 28—29, 2024.

### Team ΔΛΔ members

* [Peter Hanukaev](https://peterhanukaev.com/)
* Mark Holcomb
* [Neea Rusch](https://nkrusch.github.io/)
* Vignesh Sivakumar
* Jason Weeks

### Recap

Our choice programming language was Python.
We also had a Discord integration that posted our scores to out team server (in `.github`).

#### Challenge: hello

First we wrote a few different translators for the ICFP language.
But the translators are simple, and do not include evaluation of ICFP.
However, they were sufficient to complete the _hello_ challenge, and get us enrolled in _lambdaman_ and _spaceship_ courses.
During the hello challenge, we also discovered and solved the backdoor command to enroll in _3d_ course.

Our ICFP translators are in `index.py` and `parser.py`.
We also had a utility to ease communication with the server in `senq-req.py`
The initial messages we exchanged are in `messages/`.
Instruction for the various courses are in the repository root.

#### Challenge: lambdaman

We tried a few different approaches to solve the lambdaman puzzles.
One attempt is in `lambdaman_solver.py` and another strategy is in `simple_lm.py`.

The second is vary naive, and finds non-optimal solutions, but it does find solutions for all mazes.
It works by putting the pills in order, using a simple distance measure. 
Then, for the ordered sequence of pills, it finds the shortest path between each pair of pills. 

We were unable to solve problems #6, #9 and #21 since we did not complete evaluation for ICFP.
We could solve problem #10, because it was possible to construct the maze by reading the clues contained in the server response.

#### Challenge: spaceship

We first solved a few of the simple problems by hand (#1 and #3).
We tried to come up with a general solution, but this did not work out.

In the end we had a simple solution `space.py`, with heavy restriction, that works for some problems.
It puts the coordinates in order, so that the distance between coordinates is minimal. 
Then, it calculates at each step, which phone dial button will move the spaceship to the next position.
The built-in restriction is that the step take exactly one timestep,
meaning the solver fails on every problem, where progress cannot be made on each step

#### Challenge: 3d

We started work on this problem but were unable to complete any solutions.
The stater solution is in `3d_prog.py` and an example input in `3d_input.txt`.

#### Challenge: efficiency

We never discovered how to enroll in this course 🙁.
