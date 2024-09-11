import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.animation import FuncAnimation
import numpy as np
import rubiks_cube_solver as rubiks_cube_solver

def init(n):
    global global_vertices
    global animation
    global rubik
    global face_to_rotate
    global ax
    global fig
    global rotating
    global start_frame
    global curr_frame
    global solving
    global solution
    
    #initialize variables
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    rubik = rubiks_cube_solver.create_rubik(n)
    face_to_rotate = None
    start_frame = None
    curr_frame = None
    rotating =  False
    face_to_rotate = None
    global_vertices = []
    animation = FuncAnimation(fig, update, blit=False, repeat=True, interval=10, cache_frame_data=False)
    solving = False
    
    #set title of the canvas
    fig.canvas.manager.set_window_title("Rubiks Cube Solver")
    
    #connect key press events to control rubiks cube movements
    fig.canvas.mpl_connect('key_press_event', on_press)
    
    #disable some default key event handlers
    plt.rcParams["keymap.back"].remove('left')
    plt.rcParams["keymap.forward"].remove('right')
    plt.rcParams["keymap.fullscreen"].remove('f')
    plt.rcParams["keymap.home"].remove('r')
    plt.rcParams["keymap.save"].remove('s')
    plt.rcParams["keymap.zoom"].remove('o')
    
    #set vertices for each cube
    for x in range(n):
        x_list = []
        for y in range(n):
            y_list = []
            for z in range(n):
                z_list = [
                    [x + 1, y + 1, z + 1],  # Vertex 0
                    [x + 1, y + 1, z + 0],  # Vertex 1
                    [x + 1, y + 0, z + 1],  # Vertex 2
                    [x + 1, y + 0, z + 0],  # Vertex 3
                    [x + 0, y + 1, z + 1],  # Vertex 4
                    [x + 0, y + 1, z + 0],  # Vertex 5
                    [x + 0, y + 0, z + 1],  # Vertex 6
                    [x + 0, y + 0, z + 0],  # Vertex 7
                ]
                y_list.append(z_list[:])
            x_list.append(y_list[:])
        global_vertices.append(x_list[:])


def reset():
    global global_vertices
    global rubik

    global_vertices.clear()
    
    n = rubik.get_length()
    
    for x in range(n):
        x_list = []
        for y in range(n):
            y_list = []
            for z in range(n):
                z_list = [
                    [x + 1, y + 1, z + 1],  # Vertex 0
                    [x + 1, y + 1, z + 0],  # Vertex 1
                    [x + 1, y + 0, z + 1],  # Vertex 2
                    [x + 1, y + 0, z + 0],  # Vertex 3
                    [x + 0, y + 1, z + 1],  # Vertex 4
                    [x + 0, y + 1, z + 0],  # Vertex 5
                    [x + 0, y + 0, z + 1],  # Vertex 6
                    [x + 0, y + 0, z + 0],  # Vertex 7
                ]
                y_list.append(z_list[:])
            x_list.append(y_list[:])
        global_vertices.append(x_list[:])


def update(frame):
    global global_vertices
    global animation
    global rubik
    global face_to_rotate
    global ax
    global fig
    global rotating
    global start_frame
    global curr_frame
    global solving
    global solution

    curr_frame = frame
    cube = rubik.get_cube()
    face = face_to_rotate
    n = rubik.get_length()
    check_rotating()
    
    ax.clear()
    ax.text2D(-0.35, 1, "Turn RIGHT:     press <right>", transform=ax.transAxes)
    ax.text2D(-0.35, 0.95, "Turn LEFT:       press <left>", transform=ax.transAxes)
    ax.text2D(-0.35, 0.90, "Turn FRONT:    press <f>", transform=ax.transAxes)
    ax.text2D(-0.35, 0.85, "Turn BACK:      press <b>", transform=ax.transAxes)
    ax.text2D(-0.35, 0.80, "Turn UP:          press <up>", transform=ax.transAxes)
    ax.text2D(-0.35, 0.75, "Turn DOWN:    press <down>", transform=ax.transAxes)
    ax.text2D(-0.35, 0.70, "Reset:             press <r>", transform=ax.transAxes)
    ax.text2D(-0.35, 0.65, "Scramble:       press <s>", transform=ax.transAxes)
    ax.text2D(-0.35, 0.60, "Solve:             press <o>", transform=ax.transAxes)
    ax.set_axis_off()
    ax.set_xlim(-1, n+1)
    ax.set_ylim(-1, n+1)
    ax.set_zlim(-1, n+1)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    if rotating:
        ax.text2D(0.4, 0, ("Turning " + face_to_rotate), transform=ax.transAxes)

    if rubik.is_solved():
        ax.text2D(0.45, 0.05, "SOLVED", transform=ax.transAxes)

    for x in range(n):
        for y in range(n):
            for z in range(n):
                left = cube[1][n - z - 1][x]
                right = cube[3][n - z - 1][n - x - 1]
                down = cube[5][n - x - 1][y]
                up = cube[4][x][y]
                back = cube[2][n - z - 1][n - y - 1]
                front = cube[0][n - z - 1][y]

                # Define the vertices of the cube in 3D space (X, Y, Z)
                vertices = global_vertices[x][y][z]

                if rotating and to_rotate(face, (x,y,z), n):
                    axis, point = get_axis_point(face, n)
                    
                    rotated_vertices = rotate(vertices, axis, point)

                    vertices = rotated_vertices
                
                # update global_vertices with certain positions
                global_vertices[x][y][z] = vertices[:]
                
                # Define the faces of the cube by specifying which vertices to connect
                faces = [
                    [vertices[0], vertices[1], vertices[3], vertices[2]],  # Front face
                    [vertices[4], vertices[5], vertices[7], vertices[6]],  # Back face
                    [vertices[0], vertices[1], vertices[5], vertices[4]],  # Right face
                    [vertices[2], vertices[3], vertices[7], vertices[6]],  # Left face
                    [vertices[0], vertices[2], vertices[6], vertices[4]],  # Up face
                    [vertices[1], vertices[3], vertices[7], vertices[5]],  # Down face
                ]
                
                colors = [front, back, right, left, up, down]
                poly3d_collection = Poly3DCollection(faces, facecolors=colors, linewidths=1, edgecolors='black')
    
                ax.add_collection3d(poly3d_collection)
    return ax


def rotate(vertices, axis, point):
    vertices = [[x-y for x,y in zip(vertices[i], point)] for i in range(len(vertices))]
    
    # Rotate vertices by a small angle around the desired axis
    angle_deg = 10
    angle = np.radians(angle_deg)
    
     # Create a rotation matrix for the specified angle and axis
    if axis == 'x':
        rotation_matrix = np.array([[1, 0, 0],
                                     [0, np.cos(angle), -np.sin(angle)],
                                     [0, np.sin(angle), np.cos(angle)]])
    elif axis == '-x':
        rotation_matrix = np.array([[1, 0, 0],
                                     [0, np.cos(-angle), -np.sin(-angle)],
                                     [0, np.sin(-angle), np.cos(-angle)]])
    elif axis == 'y':
        rotation_matrix = np.array([[np.cos(angle), .0, np.sin(angle)],
                                     [0, 1, 0],
                                     [-np.sin(angle), 0, np.cos(angle)]])
    elif axis == '-y':
        rotation_matrix = np.array([[np.cos(-angle), .0, np.sin(-angle)],
                                     [0, 1, 0],
                                     [-np.sin(-angle), 0, np.cos(-angle)]])
    elif axis == 'z':
        rotation_matrix = np.array([[np.cos(angle), -np.sin(angle), 0],
                                     [np.sin(angle), np.cos(angle), 0],
                                     [0, 0, 1]])
    elif axis == '-z':
        rotation_matrix = np.array([[np.cos(-angle), -np.sin(-angle), 0],
                                     [np.sin(-angle), np.cos(-angle), 0],
                                     [0, 0, 1]])
    # Apply rotation to the vertices
    rotated_vertices = np.dot(vertices, rotation_matrix)
    rotated_vertices = [[x+y for x,y in zip(rotated_vertices[i], point)] for i in range(len(vertices))]
    return rotated_vertices


def get_axis_point(face, n):
    if face == "right":
        return 'y', [n/2, 0, n/2]
    elif face == "left":
        return '-y', (n/2, n, n/2)
    elif face == "front":
        return 'x', (n, n/2, n/2)
    elif face == "back":
        return '-x', (0, n/2, n/2)
    elif face == "up":
        return 'z', (n/2, n/2, n)
    elif face == "down":
        return '-z', (n/2, n/2, 0)
    elif face == "right^":
        return '-y', [n/2, 0, n/2]
    elif face == "left^":
        return 'y', (n/2, n, n/2)
    elif face == "front^":
        return '-x', (n, n/2, n/2)
    elif face == "back^":
        return 'x', (0, n/2, n/2)
    elif face == "up^":
        return '-z', (n/2, n/2, n)
    elif face == "down^":
        return 'z', (n/2, n/2, 0)


def to_rotate(face, point, n):
    if face == "right":
        return point[1] == n - 1
    elif face == "left":
        return point[1] == 0
    elif face == "front":
        return point[0] == n - 1
    elif face == "back":
        return point[0] == 0
    elif face == "up":
        return point[2] == n - 1
    elif face == "down":
        return point[2] == 0
    elif face == "right^":
        return point[1] == n - 1
    elif face == "left^":
        return point[1] == 0
    elif face == "front^":
        return point[0] == n - 1
    elif face == "back^":
        return point[0] == 0
    elif face == "up^":
        return point[2] == n - 1
    elif face == "down^":
        return point[2] == 0


def on_press(event):
    global global_vertices
    global animation
    global rubik
    global face_to_rotate
    global ax
    global fig
    global rotating
    global start_frame
    global curr_frame 
    global solving
    global solution
    
    if event.key == "right":
        if not rotating:
            start_frame = curr_frame
            face_to_rotate = "right"
    elif event.key == 'left':
        if not rotating:
            start_frame = curr_frame
            face_to_rotate = "left"
    elif event.key == "up":
        if not rotating:
            start_frame = curr_frame
            face_to_rotate = "up"  
    elif event.key == "down":
        if not rotating:
            start_frame = curr_frame
            face_to_rotate = "down"
    elif event.key == "f":
        if not rotating:
            start_frame = curr_frame
            face_to_rotate = "front"
    elif event.key == "b":
        if not rotating:
            start_frame = curr_frame
            face_to_rotate = "back"
    elif event.key == "shift+right":
        if not rotating:
            start_frame = curr_frame
            face_to_rotate = "right^"
    elif event.key == 'shift+left':
        if not rotating:
            start_frame = curr_frame
            face_to_rotate = "left^"
    elif event.key == "shift+up":
        if not rotating:
            start_frame = curr_frame
            face_to_rotate = "up^"  
    elif event.key == "shift+down":
        if not rotating:
            start_frame = curr_frame
            face_to_rotate = "down^"
    elif event.key == "F":
        if not rotating:
            start_frame = curr_frame
            face_to_rotate = "front^"
    elif event.key == "B":
        if not rotating:
            start_frame = curr_frame
            face_to_rotate = "back^" 
    elif event.key == "r":
        if not rotating:
            rubik.reset()
    elif event.key == "s":
        if not rotating:
            rubik.scramble(7)
    elif event.key == "o":
        if not rotating:
            solution = rubik.find_solution(5)
            solving = True
            face_to_rotate = next(solution, None)
            if face_to_rotate is None:
                solving = False
                start_frame = None
            else:
                start_frame = curr_frame 
 
     
def check_rotating():
    global global_vertices
    global animation
    global rubik
    global face_to_rotate
    global ax
    global fig
    global rotating
    global start_frame
    global curr_frame
    global solving
    global solution
    
    if solving:  
        if curr_frame - start_frame < 10:
            rotating = True
        else:
            rubik.perform_move(face_to_rotate)
            reset()
            face_to_rotate = next(solution, None)
            if face_to_rotate is None:
                solving = False
                rotating = False
                start_frame = None
            else:
                rotating = True
                start_frame = curr_frame
            
    elif start_frame != None and face_to_rotate != None:
        if curr_frame - start_frame < 10:
            rotating = True
        else:
            rotating = False
            start_frame = None
            rubik.perform_move(face_to_rotate)
            face_to_rotate = None
            reset()
    else:
        rotating = False
  
      
def main():
    init(3)
    plt.show()
    
if __name__ == "__main__":
    main()

