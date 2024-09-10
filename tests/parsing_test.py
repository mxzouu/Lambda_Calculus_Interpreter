import unittest
from parsing import (buildVar, extractInputFromAbs, extractOutputFromAbs, open_parantheses_counter,
                     close_parantheses_counter,
                     balancedParantheses,
                     parantheses_couples,
                     findOpeningParanthesesIndex,
                     findClosingParanthesesIndex,
                     getTermFromParantheses,
                     getTermsFromParantheses, 
                     remove_multiple_spaces)

class TestParsing(unittest.TestCase):
    def test_balanced_parentheses(self):
        self.assertEqual(open_parantheses_counter(""), (0, []))
        self.assertEqual(open_parantheses_counter("a(b)c"), (1, [1]))
        self.assertEqual(open_parantheses_counter("a(b(c)d)e"), (2, [1, 3]))
        self.assertEqual(open_parantheses_counter("a(b(c(d)e)f)g"), (3, [1, 3, 5]))


    def test_no_parentheses(self):
        self.assertEqual(open_parantheses_counter(""), (0, []))
        self.assertEqual(open_parantheses_counter("abc"), (0, []))


class TestCloseParanthesesCounter(unittest.TestCase):
    def test_balanced_parentheses(self):
        self.assertEqual(close_parantheses_counter("()"), (1, [1]))
        self.assertEqual(close_parantheses_counter("(())"), (2, [2, 3]))
        self.assertEqual(close_parantheses_counter("(()())"), (3, [2, 4, 5]))
        self.assertEqual(close_parantheses_counter("((()))"), (3, [3, 4, 5]))

    def test_no_parentheses(self):
        self.assertEqual(close_parantheses_counter(""), (0, []))
        self.assertEqual(close_parantheses_counter("abc"), (0, []))
        self.assertEqual(close_parantheses_counter("((("), (0, []))

    def test_unbalanced_parentheses(self):
        self.assertEqual(close_parantheses_counter(")("), (1, [0]))
        self.assertEqual(close_parantheses_counter("(()"), (1, [2]))
        self.assertEqual(close_parantheses_counter("(()))"), (3, [2, 3, 4]))

    def test_balanced_parentheses(self):
        self.assertTrue(balancedParantheses("()"))
        self.assertTrue(balancedParantheses("(())"))
        self.assertTrue(balancedParantheses("(()())"))
        self.assertTrue(balancedParantheses("{[()]}"))
        self.assertTrue(balancedParantheses("a(b)c[d]e{f}"))

    def test_unbalanced_parentheses(self):
        self.assertFalse(balancedParantheses("("))
        self.assertFalse(balancedParantheses(")"))
        self.assertFalse(balancedParantheses("(()"))
        self.assertFalse(balancedParantheses("())"))
        self.assertFalse(balancedParantheses("{[}]"))
        self.assertFalse(balancedParantheses("a(b]c"))

    def test_no_parentheses(self):
        self.assertTrue(balancedParantheses(""))
        self.assertTrue(balancedParantheses("abc"))


    def test_balanced_parentheses(self):
        self.assertEqual(parantheses_couples("()"), 1)
        self.assertEqual(parantheses_couples("(())"), 2)
        self.assertEqual(parantheses_couples("(()())"), 3)
        self.assertEqual(parantheses_couples("{[()]}"), 3)
        self.assertEqual(parantheses_couples("a(b)c[d]e{f}"), 3)

    def test_unbalanced_parentheses(self):
        with self.assertRaises(AssertionError):
            parantheses_couples("(")
        with self.assertRaises(AssertionError):
            parantheses_couples(")")
        with self.assertRaises(AssertionError):
            parantheses_couples("(()")
        with self.assertRaises(AssertionError):
            parantheses_couples("())")
        with self.assertRaises(AssertionError):
            parantheses_couples("{[}]")
        with self.assertRaises(AssertionError):
            parantheses_couples("a(b]c")

    def test_no_parentheses(self):
        self.assertEqual(parantheses_couples(""), 0)
        self.assertEqual(parantheses_couples("abc"), 0)

    def test_valid_input(self):
        self.assertEqual(findOpeningParanthesesIndex("a(b)c", 3), 1)
        self.assertEqual(findOpeningParanthesesIndex("a[b]c", 3), 1)
        self.assertEqual(findOpeningParanthesesIndex("a{b}c", 3), 1)
    
    def test_invalid_closeParentheseIndex_out_of_range(self):
        with self.assertRaises(IndexError):
            findOpeningParanthesesIndex("a(b)c", 5)
        with self.assertRaises(IndexError):
            findOpeningParanthesesIndex("a(b)c", -1)
    
    def test_invalid_character_at_closeParentheseIndex(self):
        with self.assertRaises(KeyError):
            findOpeningParanthesesIndex("a(b)c", 2)
    # Todo: figure out how to make this test not crash the program
    # def test_no_matching_opening_parenthesis(self):
    #     with self.assertRaises(IndexError):
    #         findOpeningParanthesesIndex("a)b)c", 2)

    def test_valid_input(self):
        self.assertEqual(findClosingParanthesesIndex("a(b)c", 1), 3)
        self.assertEqual(findClosingParanthesesIndex("a[b]c", 1), 3)
        self.assertEqual(findClosingParanthesesIndex("a{b}c", 1), 3)
    
    def test_unbalanced_parentheses(self):
        with self.assertRaises(AssertionError):
            findClosingParanthesesIndex("a(bc", 1)
    

    # TODO:the tests below are working, figure out how to make the test exit gracefully
    # def test_unmatched_closing_parenthesis(self):
    #     with self.assertRaises(ValueError):
    #         findClosingParanthesesIndex("a)b)c", 1)
    
    # def test_mismatched_parentheses(self):
    #     with self.assertRaises(ValueError):
    #         findClosingParanthesesIndex("a(b]c", 1)
    
    # def test_no_matching_closing_parenthesis(self):
    #     with self.assertRaises(ValueError):
    #         findClosingParanthesesIndex("a(bc", 1)

    def test_getTermFromParantheses(self):
        self.assertEqual(getTermFromParantheses("(abc)", 0), "abc")
        self.assertEqual(getTermFromParantheses("a(bc)d", 1), "bc")
        self.assertEqual(getTermFromParantheses("a{bc}d", 1), "bc")  # This will fail without modifying the function to handle '{}'
        self.assertEqual(getTermFromParantheses("a[bc]d", 1), "bc")  # This will fail without modifying the function to handle '[]'
        self.assertEqual(getTermFromParantheses("a(b(c)d)e", 1), "b(c)d")

    def test_getTermsFromParantheses(self):
        self.assertEqual(getTermsFromParantheses("(abc)"), ["abc"])
        self.assertEqual(getTermsFromParantheses("a(bc)d"), ["bc"])
        self.assertEqual(getTermsFromParantheses("a{bc}d"), ["bc"])  # This will fail without modifying the function to handle '{}'
        self.assertEqual(getTermsFromParantheses("a[bc]d"), ["bc"])  # This will fail without modifying the function to handle '[]'
        self.assertEqual(getTermsFromParantheses("a(b(c)d)e"), ["b(c)d"])
        self.assertEqual(getTermsFromParantheses("a(b)c(d)e"), ["b", "d"])
        self.assertEqual(getTermsFromParantheses("a{b}c[d]e"), ["b", "d"])  # This will fail without modifying the function to handle '{}' and '[]'

    def test_getTermsFromParantheses_no_parentheses(self):
        self.assertEqual(getTermsFromParantheses("abc"), [])

    def test_getTermsFromParantheses_mixed_parentheses(self):
        self.assertEqual(getTermsFromParantheses("a(b)c{d}e[f]g"), ["b", "d", "f"])
    
    def test_remove_multiple_spaces(self):
        self.assertEqual(remove_multiple_spaces("a  b  c"), "a b c")
        self.assertEqual(remove_multiple_spaces("  a  b  c  "), "a b c")
        self.assertEqual(remove_multiple_spaces("a    b    c"), "a b c")
        self.assertEqual(remove_multiple_spaces("a b c"), "a b c")
        self.assertEqual(remove_multiple_spaces("a\tb\tc"), "a b c")
        self.assertEqual(remove_multiple_spaces("a\nb\nc"), "a b c")
        self.assertEqual(remove_multiple_spaces("a \n b \t c"), "a b c")
        self.assertEqual(remove_multiple_spaces(""), "")
        self.assertEqual(remove_multiple_spaces("   "), "")
        
    def test_extractInputFromAbs(self):
        self.assertEqual(extractInputFromAbs("λx.x"), "x")
        self.assertEqual(extractInputFromAbs("\\x.x"), "x")
        self.assertEqual(extractInputFromAbs("λxy.xy"), "xy")
        self.assertEqual(extractInputFromAbs("\\xy.xy"), "xy")
        self.assertEqual(extractInputFromAbs("λx.λy.xy"), "x")
        self.assertEqual(extractInputFromAbs("\\x.\\y.xy"), "x")

    def test_extractInputFromAbs_invalid_expression(self):
        self.assertEqual(extractInputFromAbs("x.x"), "")
        self.assertEqual(extractInputFromAbs("λ.x"), "")
        self.assertEqual(extractInputFromAbs("\\.x"), "")
        
    def test_extractOutputFromAbs(self):
        self.assertEqual(extractOutputFromAbs("λx.x"), "x")
        self.assertEqual(extractOutputFromAbs("\\x.x"), "x")
        self.assertEqual(extractOutputFromAbs("λxy.xy"), "xy")
        self.assertEqual(extractOutputFromAbs("\\xy.xy"), "xy")
        self.assertEqual(extractOutputFromAbs("λx.λy.xy"), "λy.xy")
        self.assertEqual(extractOutputFromAbs("\\x.\\y.xy"), "\\y.xy")

    def test_extractOutputFromAbs_invalid_expression(self):
        self.assertEqual(extractOutputFromAbs("x.x"), "")
        self.assertEqual(extractOutputFromAbs("λ.x"), "x")
        self.assertEqual(extractOutputFromAbs("\\.x"), "x")






if __name__ == '__main__':
    unittest.main()







# # Test case 4: No closing parentheses
# terme4 = "((())("
# expected_result4 = (0, [])
# assert close_parantheses_counter(terme4) == expected_result4