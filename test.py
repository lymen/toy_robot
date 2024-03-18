import unittest
from io import StringIO
from unittest.mock import patch, Mock
from main import Robot, FACE, parse_command

class TestRobot(unittest.TestCase):
    def setUp(self):
        self.robot = Robot()
        print(f"\nRunning: {self._testMethodName}")

    def tearDown(self):
        print(f"Completed: {self._testMethodName}")

    def test_valid_place(self):
        test_data = [
            {'x': 0, 'y': 0, 'face': FACE['NORTH'], 'out_x': 0, 'out_y': 0, 'out_face': FACE['NORTH']},
            {'x': 1, 'y': 1, 'face': FACE['SOUTH'], 'out_x': 1, 'out_y': 1, 'out_face': FACE['SOUTH']},
            {'x': 2, 'y': 2, 'face': FACE['EAST'], 'out_x': 2, 'out_y': 2, 'out_face': FACE['EAST']},
            {'x': 3, 'y': 3, 'face': FACE['WEST'], 'out_x': 3, 'out_y': 3, 'out_face': FACE['WEST']},
        ]
        
        for data in test_data:
            self.robot.place(data['x'], data['y'], data['face'])
            self.assertEqual(self.robot.x, data['out_x'])
            self.assertEqual(self.robot.y, data['out_y'])
            self.assertEqual(self.robot.face, data['face'])

            print(f"\tscenario {data['x']},{data['y']},{data['face']} - OK")

    def test_invalid_place(self):
        test_data = [
            {'x': 0, 'y': 0, 'face': 'INVALID'},
            {'x': -1, 'y': -1, 'face': FACE['NORTH']},
            {'x': self.robot.table_size, 'y': self.robot.table_size, 'face': FACE['NORTH']},
        ]
        
        for data in test_data:
            self.robot.place(data['x'], data['y'], data['face'])
            self.assertIsNone(self.robot.x)
            self.assertIsNone(self.robot.y)
            self.assertIsNone(self.robot.face)

            print(f"\tscenario {data['x']},{data['y']},{data['face']} - OK")

    def test_move(self):
        test_data = [
            # Corner Points to test the limits
            {'x': 0, 'y': 0, 'face': FACE['SOUTH'], 'out_x': 0, 'out_y': 0},
            {'x': 0, 'y': 0, 'face': FACE['WEST'], 'out_x': 0, 'out_y': 0},
            {'x': 0, 'y': 4, 'face': FACE['NORTH'], 'out_x': 0, 'out_y': 4},
            {'x': 0, 'y': 4, 'face': FACE['WEST'], 'out_x': 0, 'out_y': 4},
            {'x': 4, 'y': 4, 'face': FACE['NORTH'], 'out_x': 4, 'out_y': 4},
            {'x': 4, 'y': 4, 'face': FACE['EAST'], 'out_x': 4, 'out_y': 4},
            {'x': 4, 'y': 0, 'face': FACE['SOUTH'], 'out_x': 4, 'out_y': 0},
            {'x': 4, 'y': 0, 'face': FACE['EAST'], 'out_x': 4, 'out_y': 0},
            # Center Points to test movements
            {'x': 2, 'y': 2, 'face': FACE['NORTH'], 'out_x': 2, 'out_y': 3},
            {'x': 2, 'y': 2, 'face': FACE['SOUTH'], 'out_x': 2, 'out_y': 1},
            {'x': 2, 'y': 2, 'face': FACE['EAST'], 'out_x': 3, 'out_y': 2},
            {'x': 2, 'y': 2, 'face': FACE['WEST'], 'out_x': 1, 'out_y': 2},
        ]
        
        for data in test_data:
            self.robot.place(data['x'], data['y'], data['face'])
            self.robot.move()
            self.assertEqual(self.robot.x, data['out_x'])
            self.assertEqual(self.robot.y, data['out_y'])

            print(f"\tscenario {data['x']},{data['y']},{data['face']} - OK")

    def test_rotate_left(self):
        test_data = [
            {'face': FACE['NORTH'], 'out_face': FACE['WEST']},
            {'face': FACE['SOUTH'], 'out_face': FACE['EAST']},
            {'face': FACE['EAST'], 'out_face': FACE['NORTH']},
            {'face': FACE['WEST'], 'out_face': FACE['SOUTH']},
        ]
        
        for data in test_data:
            self.robot.place(0, 0, data['face'])
            self.robot.left()
            self.assertEqual(self.robot.face,  data['out_face'])

            print(f"\tscenario {data['face']} - OK")

    def test_rotate_right(self):
        test_data = [
            {'face': FACE['NORTH'], 'out_face': FACE['EAST']},
            {'face': FACE['SOUTH'], 'out_face': FACE['WEST']},
            {'face': FACE['EAST'], 'out_face': FACE['SOUTH']},
            {'face': FACE['WEST'], 'out_face': FACE['NORTH']},
        ]
        
        for data in test_data:
            self.robot.place(0, 0, data['face'])
            self.robot.right()
            self.assertEqual(self.robot.face,  data['out_face'])

            print(f"\tscenario {data['face']} - OK")

    def test_report(self):
        test_data = [
            {'x': 0, 'y': 0, 'face': FACE['NORTH'], 'out_x': 0, 'out_y': 0, 'out_face': FACE['NORTH']},
            {'x': 1, 'y': 1, 'face': FACE['SOUTH'], 'out_x': 1, 'out_y': 1, 'out_face': FACE['SOUTH']},
            {'x': 2, 'y': 2, 'face': FACE['EAST'], 'out_x': 2, 'out_y': 2, 'out_face': FACE['EAST']},
            {'x': 3, 'y': 3, 'face': FACE['WEST'], 'out_x': 3, 'out_y': 3, 'out_face': FACE['WEST']},
        ]
        
        for data in test_data:
            print_output = StringIO()
            with patch('sys.stdout', new=print_output):
                self.robot.place(data['x'], data['y'], data['face'])
                self.robot.report()
                self.assertEqual(print_output.getvalue().strip(), f"{data['out_x']},{data['out_y']},{data['out_face']}")

            print(f"\tscenario {data['x']},{data['y']},{data['face']} - OK")


class TestParseCommand(unittest.TestCase):
    def setUp(self):
        print(f"\nRunning: {self._testMethodName}")

    def tearDown(self):
        print(f"Completed: {self._testMethodName}")

    def test_place_command_calls(self):
        robot = Mock()
        parse_command("PLACE 0,0,NORTH", robot)
        robot.place.assert_called_once_with(0, 0, "NORTH")

    def test_move_command_calls(self):
        robot = Mock()
        parse_command("MOVE", robot)
        robot.move.assert_called_once()

    def test_left_command_calls(self):
        robot = Mock()
        parse_command("LEFT", robot)
        robot.left.assert_called_once()

    def test_right_command_calls(self):
        robot = Mock()
        parse_command("RIGHT", robot)
        robot.right.assert_called_once()

    def test_report_command_calls(self):
        robot = Mock()
        parse_command("REPORT", robot)
        robot.report.assert_called_once()

    def test_invalid_command_does_not_call_any_method(self):
        robot = Mock()
        parse_command("INVALID", robot)
        robot.assert_not_called()

if __name__ == '__main__':
    unittest.main()