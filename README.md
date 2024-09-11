# Rubiks-GUI-and-Solver-using-IDDFS
This is a Python-based Rubik’s Cube solver that includes both a graphical user interface (GUI) and a solving algorithm based on the Iterative Deepening Depth-First Search (IDDFS) algorithm. It currently supports Rubik's cubes of different sizes, with the default set to a 3x3 cube.

# Features

IDDFS Solver: The solver uses the IDDFS algorithm to solve the cube.
Multiple Cube Sizes: Supports different cube sizes (e.g., 3x3, 4x4, etc.), with the default set to 3x3.
Scramble Depth: The current version supports scrambles up to depth 6. A new version with deeper scrambling support is in development.

# Installation
## Clone the Repository
You can download the program by cloning the repository. Run the following command:

bash
Copy code
git clone <repository-url>
Replace <repository-url> with the actual URL of your repository.

Manual Download
Alternatively, you can manually download the two required files:

rubiks_cube_gui.py
rubiks_cube_solver.py
Ensure both files are in the same directory.

How to Run the Program

Download both rubiks_cube_gui.py and rubiks_cube_solver.py and place them in the same folder.
Make sure you have Python installed (preferably version 3.x).
Navigate to the folder where both files are located.
Run the GUI script by executing the following command in your terminal:
bash
Copy code
python rubiks_cube_gui.py
This will launch the graphical interface where you can interact with the cube and test the solver.

Usage

Cube Sizes: By default, the program solves a 3x3 Rubik’s cube, but you can choose other sizes like 4x4, etc.
Solver Limitations: At the moment, the program can handle scrambles up to a depth of 6. This means it can solve scrambles with a maximum of 6 moves. A future update will increase this depth.
Requirements

Python 3.x
tkinter (for GUI)
Make sure to have all dependencies installed by running:

bash
Copy code
pip install -r requirements.txt
Upcoming Features

Extended Scramble Depth: The next version will support scrambles of greater depths.
Improved Performance: Optimization updates for larger cube sizes and scramble complexities.
