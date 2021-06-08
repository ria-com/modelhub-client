# import python modules
import os
import sys
import unittest

# add package root
sys.path.append(os.getcwd())


class TestExample(unittest.TestCase):
    def test_example(self) -> None:
        self.assertEqual(1, 1)


if __name__ == '__main__':
    unittest.main()
