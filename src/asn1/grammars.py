from typing import List, Tuple

from asn1.lexers import Token, TokenType

class GrammarRoot:
    def process(self, startpos : int, tokens : List[Token]) -> Tuple[bool, int]:
        """ returns true if the tokens starting from start pos
            can be processed for this grammar; second value
            indicates the next pos after this process, if processing failed
            second value is not valid """
        raise NotImplementedError()

class GrammarChoice (GrammarRoot):
    def __init__(self, grammar_choices : List[GrammarRoot] = []) -> None:
        super().__init__()
        # list of possible subgrammars for this grammar, i.e. ORs, |
        self.grammar_choices : List[GrammarRoot] = grammar_choices
        

    def process(self, startpos : int, tokens : List[Token]) -> Tuple[bool, int]:
        """ checks if tokens match any of the choices """
        
        # checks if there is any matching sub grammars
        # if there is none, will return false
        curpos = startpos
        for grammar in self.grammar_choices:
            isok, curpos = grammar.process(curpos, tokens)
            if isok:
                # match found return
                break
        return isok, curpos

class GrammarSequence (GrammarRoot):
    def __init__(self, grammar_sequence : List[GrammarRoot] = []) -> None:
        super().__init__()
        self.grammar_sequence : List[GrammarRoot] = grammar_sequence
        self.grammarcursor : int = 0

    def process(self, startpos : int, tokens : List[Token]) -> Tuple[bool, int]:
        curpos = startpos
        for grammar in self.grammar_sequence:
            isok, curpos = grammar.process(curpos, tokens)
            if not isok:
                break
        return isok, curpos

class GrammarTerminal (GrammarRoot):
    def __init__(self, value : any) -> None:
        super().__init__()
        self.value  = value

    def process(self, startpos: int, tokens: List[Token]) -> Tuple[bool, int]:
        # if token at given possition matches grammar value return true
        # and the next index
        return (tokens[startpos].value == self.value), startpos+1

