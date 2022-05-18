import time

next_depth = 'a'
next_plate = '1'

is_current = True


def update_plate():
    global next_plate
    if next_plate == '1':
        next_plate = '2'
    elif next_plate == '2':
        next_plate = '1'


def update_depth():
    global next_depth
    if next_depth == 'a':
        next_depth = 'b'
    elif next_depth == 'b':
        next_depth = 'c'
    elif next_depth == 'c':
        next_depth = 'a'

if __name__ == '__main__':

    for i in range(3):
        print(f"next_depth: {next_depth} y next_plate: {next_plate}")
        time.sleep(1)
        update_depth()
        update_plate()
