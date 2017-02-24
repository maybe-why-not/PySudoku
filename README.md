# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: Two boxes located within a unit and that contain identical two-digit values are known as naked twins. Since these boxes can only contain one of those two values, all other boxes in the same unit cannot contain any of these values. Thus, we can eliminate those two digits from all other boxes of the unit.

Oversimplifying a little, the algorithm would work as follows: you would first get all boxes that have two-digit values, and then you would get the ones that are on the same unit. Once you have these, you circle through them and eliminate the digits from these boxes.

Constraint propagation with naked twins would work in a similar way as other solution techniques, such as elimination and only choice. In my case I applied the naked twins technique after elimination and only choice, so it is called iteratively by the search function.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: The diagonal sudoku problem uses constraint propagation on the same manner as the regular sudoku solver. The difference lies in that both diagonals represent additional units (besides columns, rows, and 3x3 squares). When we solve the sudoku, the constraint of having only one instance of each 1-9 digit per unit is applied to these diagonal units as well.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.