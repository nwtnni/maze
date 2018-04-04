from os import remove
from sys import argv
from time import sleep
from maze import Point
import imageio
import binary
import dfs
import hunt
import kruskal
import random_walk
import sidewinder
import wilson
import plot


def usage():
    usage = "Usage: python main.py <ALGORITHM> <WIDTH> <HEIGHT> <OUTPUT>\n"
    usage += "where <ALGORITHM> is exactly one of:\n"
    usage += "  -b : Binary\n"
    usage += "  -d : Depth-first search\n"
    usage += "  -h : Hunt and kill\n"
    usage += "  -k : Kruskal's minimum spanning tree algorithm\n"
    usage += "  -r : Random walk\n"
    usage += "  -s : Sidewinder (variant of binary)\n"
    usage += "  -w : Wilson's algorithm\n"
    usage += "where <WIDTH> is the width of the generated maze\n"
    usage += "where <HEIGHT> is the height of the generated maze\n"
    usage += "where <OUTPUT> is exactly one of:\n"
    usage += "  --print\n"
    usage += "    - Print final maze to stdout\n"
    usage += "  --step <SEC>\n"
    usage += "    - Print each step to stdout with <SEC> delay\n"
    usage += "  --outline <PATH>\n"
    usage += "    - Save maze outline to <PATH>.png\n"
    usage += "  --solution <PATH> <X1> <Y1> <X2> <Y2>\n"
    usage += "    - Save maze solution from (X1, Y1) to (X2, Y2) in <PATH>.png\n"
    usage += "    - Requires 0 <= X1, X2 < WIDTH, 0 <= Y1, Y2 < HEIGHT\n"
    usage += "  --heatmap <PATH> <X> <Y>\n"
    usage += "    - Save maze heatmap with center (X, Y) to <PATH>.png\n"
    usage += "    - Requires 0 <= X < WIDTH, 0 <= Y < HEIGHT\n"
    usage += "  --paired <PATH> <X1> <Y1> <X2> <Y2>\n"
    usage += "    - Save maze outline + solution to <PATH>.png, <PATH>_sol.png\n"
    usage += "    - Requires 0 <= X1, X2 < WIDTH, 0 <= Y1, Y2 < HEIGHT\n"
    usage += "  --gif <PATH> <FPS>\n"
    usage += "    - Save maze animation to <PATH>.gif with <FPS>\n"
    print(usage)


def last(frames): return [f for f in frames][-1]


def pos_int(i):
    if int(i) > 0:
        return int(i)
    else:
        raise ValueError


def pos_float(f):
    if float(f) > 0:
        return float(f)
    else:
        raise ValueError


def parse_algorithm():
    alg = argv[1]
    if alg == "-b":
        return binary.generate
    elif alg == "-d":
        return dfs.generate
    elif alg == "-h":
        return hunt.generate
    elif alg == "-k":
        return kruskal.generate
    elif alg == "-r":
        return random_walk.generate
    elif alg == "-s":
        return sidewinder.generate
    elif alg == "-w":
        return wilson.generate
    else:
        return None


def parse_dimensions():
    try:
        return pos_int(argv[2]), pos_int(argv[3])
    except ValueError:
        return None


def parse_output(frames, w, h):
    out = argv[4]

    if out == "--print":
        handle_print(frames)

    elif out == "--step":
        try:
            delay = pos_float(argv[5])
        except ValueError:
            print("Error: <SEC> must be positive float")
            return
        handle_step(frames, delay)

    elif out == "--outline":
        path = argv[5]
        handle_outline(frames, path)

    elif out == "--solution" or out == "--paired" or out == "--heatmap":
        try:
            s = Point(int(argv[6]), int(argv[7]))
            if out == "--heatmap":
                f = Point(0, 0)
            else:
                f = Point(int(argv[8]), int(argv[9]))
        except ValueError:
            print("Error: coordinates must be integers")
            return

        def lesser(s, f): return s.x < 0 or s.y < 0 or f.x < 0 or f.y < 0

        def greater(s, f): return s.x >= w or f.x >= w or s.y >= h or f.y >= h

        if lesser(s, f) or greater(s, f):
            print("Error: coordinates out of bounds")
            return

        path = argv[5]
        if out == "--solution":
            handle_solution(frames, path, s, f)
        elif out == "--paired":
            handle_paired(frames, path, s, f)
        else:
            handle_heat(frames, path, s)

    elif out == "--gif":
        path = argv[5]
        try:
            fps = pos_float(argv[6])
        except ValueError:
            print("Error: <FPS> must be positive float")
        handle_gif(frames, path, fps)

    else:
        print("Error: unknown <OUTPUT> flag")
        return


def handle_print(frames):
    print(last(frames))


def handle_step(frames, delay):
    for frame in frames:
        print(frame)
        sleep(delay)


def handle_outline(frames, path):
    maze = last(frames)
    plot.save_outline(maze, path + ".png")


def handle_solution(frames, path, s, f):
    maze = last(frames)
    plot.save_sol(maze, s, f, path + ".png")


def handle_heat(frames, path, s):
    maze = last(frames)
    plot.save_heat(maze, s, path + ".png")


def handle_paired(frames, path, s, f):
    maze = last(frames)
    plot.save_outline(maze, path + ".png")
    plot.save_sol(maze, s, f, path + "_sol.png")


def handle_gif(frames, path, fps):
    temp = ".temp_maze.png"
    with imageio.get_writer(path + ".gif", mode='I', fps=fps) as writer:
        for frame in frames:
            plot.save_outline(frame, temp)
            image = imageio.imread(temp)
            writer.append_data(image)
    remove(temp)


def main():
    if len(argv) < 5:
        usage()
        return

    generate = parse_algorithm()

    if generate is None:
        print("Error: unknown <ALGORITHM> flag")
        return

    dim = parse_dimensions()

    if dim is None:
        print("Error: <WIDTH> and <HEIGHT> must be positive integers")
        return

    w, h = dim
    parse_output(generate(w, h), w, h)


if __name__ == "__main__":
    main()
