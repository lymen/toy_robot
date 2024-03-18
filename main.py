FACE = {
    'NORTH': 'NORTH',
    'SOUTH': 'SOUTH',
    'EAST': 'EAST',
    'WEST': 'WEST',
}

ROTATE_LEFT = {
    FACE['NORTH']: FACE['WEST'],
    FACE['SOUTH']: FACE['EAST'],
    FACE['EAST']: FACE['NORTH'],
    FACE['WEST']: FACE['SOUTH'],
}

ROTATE_RIGHT = {
    FACE['NORTH']: FACE['EAST'],
    FACE['SOUTH']: FACE['WEST'],
    FACE['EAST']: FACE['SOUTH'],
    FACE['WEST']: FACE['NORTH'],
}


class Robot:
    def __init__(self):
        self.x = None
        self.y = None
        self.face = None
        self.table_size = 5

    def place(self, x, y, face):
        if self.is_valid_position(x, y) and face in FACE.values():
            self.x = x
            self.y = y
            self.face = face

    def move(self):
        if self.is_on_table():
            new_x, new_y = self._calculate_new_position()
            if self.is_valid_position(new_x, new_y):
                self.x, self.y = new_x, new_y

    def left(self):
        if self.is_on_table():
            self.face = ROTATE_LEFT[self.face]

    def right(self):
        if self.is_on_table():
            self.face = ROTATE_RIGHT[self.face]

    def report(self):
        if self.is_on_table():
            print(f'{self.x},{self.y},{self.face}')

    def is_valid_position(self, x, y):
        return 0 <= x < self.table_size and 0 <= y < self.table_size

    def is_on_table(self):
        return self.x is not None and self.y is not None and self.face is not None

    def _calculate_new_position(self):
        if self.face == 'NORTH':
            return self.x, self.y + 1
        elif self.face == 'SOUTH':
            return self.x, self.y - 1
        elif self.face == 'EAST':
            return self.x + 1, self.y
        elif self.face == 'WEST':
            return self.x - 1, self.y


def parse_command(command_str, robot):
    command = command_str.upper().strip().split()
    if not command:
        return None

    command_name = command[0]
    if command_name == 'PLACE':
        try:
            if len(command) == 2:
                x, y, face = command[1].split(',')
                robot.place(int(x), int(y), face)
        except Exception as e:
            print('Invalid command. Valid commands are PLACE x,y,face, MOVE, LEFT, RIGHT, REPORT.')
    elif command_name == 'MOVE':
        robot.move()
    elif command_name == 'LEFT':
        robot.left()
    elif command_name == 'RIGHT':
        robot.right()
    elif command_name == 'REPORT':
        robot.report()
    else:
        print('Invalid command. Valid commands are PLACE x,y,face, MOVE, LEFT, RIGHT, REPORT.')

    return None


if __name__=='__main__':
    robot = Robot()

    while True:
        input_command = input('Enter command: ')
        parse_command(input_command, robot)
