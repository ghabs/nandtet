import unittest
from parser import Parser,Command

class ParserTests(unittest.TestCase):
    def setUp(self):
        self.parser = Parser("test/testAdd.txt")
    
    def testAdd(self):
        parsed = self.parser.parse()
        self.assertEqual(parsed[0], Command("1"))

if __name__ == "__main__":
    unittest.main()
