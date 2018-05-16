import mdl
from display import *
from matrix import *
from draw import *

def run(filename):
    """
    This function runs an mdl script
    """
    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [0,
              255,
              255]]
    areflect = [0.1,
                0.1,
                0.1]
    dreflect = [0.5,
                0.5,
                0.5]
    sreflect = [0.5,
                0.5,
                0.5]

    color = [0, 0, 0]
    tmp = new_matrix()
    ident( tmp )

    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    tmp = []
    step_3d = 20

    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return

    for command in commands:
        line = command[0]
        args = command[1:]

        if line == 'sphere' and len(args) == 4:
            add_sphere(tmp,
                       args[0], args[1], args[2],
                       args[3], step_3d)
            matrix_mult( stack[-1], tmp )
            draw_polygons(tmp, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
            tmp = []

        elif line == 'torus' and len(args) == 5:
            add_torus(tmp,
                      args[0], args[1], args[2],
                      args[3], args[4], step_3d)
            matrix_mult( stack[-1], tmp )
            draw_polygons(tmp, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
            tmp = []

        elif line == 'box' and len(args) == 6:
            add_box(tmp,
                    args[0], args[1], args[2],
                    args[3], args[4], args[5])
            matrix_mult( stack[-1], tmp )
            draw_polygons(tmp, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
            tmp = []

        elif line == 'line' and len(args) == 6:
            add_edge( tmp,
                      args[0], args[1], args[2],
                      args[3], args[4], args[5] )
            matrix_mult( stack[-1], tmp )
            draw_lines(tmp, screen, zbuffer, color)
            tmp = []

        elif line == 'scale':
            t = make_scale(args[0], args[1], args[2])
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t]

        elif line == 'move':
            t = make_translate(args[0], args[1], args[2])
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t]

        elif line == 'rotate':
            theta = args[1] * (math.pi / 180)
            if args[0] == 'x':
                t = make_rotX(theta)
            elif args[0] == 'y':
                t = make_rotY(theta)
            else:
                t = make_rotZ(theta)
            matrix_mult( stack[-1], t )
            stack[-1] = [ x[:] for x in t]

        elif line == 'push':
            stack.append( [x[:] for x in stack[-1]] )

        elif line == 'pop':
            stack.pop()

        elif line == 'display':
            display(screen)

        elif line == 'save':
            save_extension(screen, args[0]+args[1])

        else:
            pass
