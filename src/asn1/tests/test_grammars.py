import unittest
from asn1.grammars import  *

# TODO test case for GrammarChoice

class GrammarTerminalTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.grammar = GrammarTerminal("Test")

    def test_correct_token(self):
        input =  [Token("Test", TokenType.IDENTIFIER)]
        self.assertEqual(self.grammar.process(0, input), (True,1))

    def test_wrong_token(self):    
        input =  [Token("wrong", TokenType.IDENTIFIER)]
        self.assertEqual(self.grammar.process(0, input), (False,1))

class GrammarSequenceTestCase (unittest.TestCase):
    def setUp(self) -> None:
        grammar_sequence = [
            GrammarTerminal("Hello"),
            GrammarTerminal("there"),
            GrammarTerminal("my"),
            GrammarTerminal("name")
        ]
        self.grammar = GrammarSequence(grammar_sequence)
    
    def test_correct(self):
        input = [
            Token("Hello"),
            Token("there"),
            Token("my"),
            Token("name")
        ]
        assert(self.grammar.process(0,input), (True, 4))


if __name__ == '__main__':
    unittest.main()