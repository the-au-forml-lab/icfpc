from parsec import generate, regex, string, many, ParseError
import string as pystring
from index import decode_str

# Helper functions
def to_int(chars):
    base = 94
    result = 0
    for char in chars:
        result = result * base + (ord(char) - 33)
    return result

# Parsers
whitespace = regex(r'\s*')

@generate
def boolean():
    result = yield string('T') | string('F')
    return 'bool', result == 'T'

@generate
def integer():
    yield string('I')
    digits = yield regex(r'[!-~]+')
    return 'int', to_int(digits)

@generate
def string_literal():
    yield string('S')
    content = yield regex(r'[!-~]+')
    return 'string', decode_str(content)

@generate
def unary_op():
    yield string('U')
    op = yield regex(r'[-!#$]')
    arg = yield icfp_expr
    return 'unary', op, arg

@generate
def binary_op():
    yield string('B')
    op = yield regex(r'[+\-*/%<>=&.TD$|]')
    left = yield icfp_expr
    right = yield icfp_expr
    return 'binary', op, left, right

@generate
def if_statement():
    yield string('?')
    cond = yield icfp_expr
    true_branch = yield icfp_expr
    false_branch = yield icfp_expr
    return 'if', cond, true_branch, false_branch

@generate
def lambda_abstraction():
    yield string('L')
    var_num = yield regex(r'[!-~"#$]*')
    body = yield icfp_expr
    return 'lambda', to_int(var_num), body

@generate
def variable():
    yield string('v')
    var_num = yield regex(r'[!-~#$"]+')
    return 'var', to_int(var_num)

# Main ICFP parser
@generate
def icfp_expr():
    yield whitespace
    result = yield (
        lambda_abstraction |
        variable |
        integer |
        string_literal |
        boolean |
        unary_op |
        binary_op |
        if_statement
    )
    yield whitespace
    return result

icfp_program = many(icfp_expr)

# Function to parse ICFP code
def parse_icfp(code):
    try:
        return icfp_program.parse(code)
    except ParseError as e:
        print(f"Parse error at position {e.loc}:")
        print(f"Expected: {e.expected}")
        print(f"Got: {code[e.loc:e.loc+10]}")
        return None

# Function to test the specification example

# Updated test function
def test_specification_example():
    example = "B$ L# B$ L\" B+ v\" v\" B* I$ I# v8"
    expected_structure = ('binary', '$',
        ('lambda', 2,
            ('binary', '$',
                ('lambda', 1,
                    ('binary', '+',
                        ('var', 1),
                        ('var', 1)
                    )
                ),
                ('binary', '*',
                    ('int', 3),
                    ('int', 2)
                )
            )
        ),
        ('var', 23)
    )

    result = parse_icfp(example)

    if result[0] == expected_structure:
        print("Specification example parsed correctly!")
    else:
        print("Specification example parsing failed.")
        print("Expected:", expected_structure)
        print("Got:", result[0])
        # Print detailed comparison
        compare_structures(expected_structure, result[0])

def compare_structures(expected, actual, path=""):
    if isinstance(expected, tuple) and isinstance(actual, tuple):
        if len(expected) != len(actual):
            print(f"Mismatch in tuple length at {path}")
            return
        for i, (e, a) in enumerate(zip(expected, actual)):
            compare_structures(e, a, f"{path}[{i}]")
    elif expected != actual:
        print(f"Mismatch at {path}: Expected {expected}, got {actual}")

# Test the parser
if __name__ == "__main__":
    test_cases = [
        """T F""",
        """I/6""",
        """SB%,,/}Q/2,$_""",
        """U- I$""",
        """B+ I# I$""",
        """? B> I# I$ S9%3 S./""",
        """B$ B$ L# L$ v# B. SB%,,/ S}Q/2,$_ IK""",
        """B$ B$ L# B$ L# B$ v# B$ v# v# L# B$ v# B$ v# v# L# L# ? B= v# I! I# B$ L$ B+ B$ v# v$ B$ v# v$ B- v# I# I%""",
        """? B= B$ B$ B$ B$ L$ L$ L$ L# v$ I" I# I$ I% I$ ? B= B$ L$ v$ I+ I+ ? B= BD I$ S4%34 S4 ? B= BT I$ S4%34 S4%3 ? B= B. S4% S34 S4%34 ? U! B& T F ? B& T T ? U! B| F F ? B| F T ? B< U- I$ U- I# ? B> I$ I# ? B= U- I" B% U- I$ I# ? B= I" B% I( I$ ? B= U- I" B/ U- I$ I# ? B= I# B/ I( I$ ? B= I' B* I# I$ ? B= I$ B+ I" I# ? B= U$ I4%34 S4%34 ? B= U# S4%34 I4%34 ? U! F ? B= U- I$ B- I# I& ? B= I$ B- I& I# ? B= S4%34 S4%34 ? B= F F ? B= I$ I$ ? T B. B. SM%,&k#(%#+}IEj}3%.$}z3/,6%},!.'5!'%y4%34} U$ B+ I# B* I$> I1~s:U@ Sz}4/}#,!)-}0/).43}&/2})4 S)&})3}./4}#/22%#4 S").!29}q})3}./4}#/22%#4 S").!29}q})3}./4}#/22%#4 S").!29}q})3}./4}#/22%#4 S").!29}k})3}./4}#/22%#4 S5.!29}k})3}./4}#/22%#4 S5.!29}_})3}./4}#/22%#4 S5.!29}a})3}./4}#/22%#4 S5.!29}b})3}./4}#/22%#4 S").!29}i})3}./4}#/22%#4 S").!29}h})3}./4}#/22%#4 S").!29}m})3}./4}#/22%#4 S").!29}m})3}./4}#/22%#4 S").!29}c})3}./4}#/22%#4 S").!29}c})3}./4}#/22%#4 S").!29}r})3}./4}#/22%#4 S").!29}p})3}./4}#/22%#4 S").!29}{})3}./4}#/22%#4 S").!29}{})3}./4}#/22%#4 S").!29}d})3}./4}#/22%#4 S").!29}d})3}./4}#/22%#4 S").!29}l})3}./4}#/22%#4 S").!29}N})3}./4}#/22%#4 S").!29}>})3}./4}#/22%#4 S!00,)#!4)/.})3}./4}#/22%#4 S!00,)#!4)/.})3}./4}#/22%#4""",
        """U$ B+ I# B* I$> I1~s:U@""",
        """B. SF B$ B$ L" B$ L" B$ L# B$ v" B$ v# v# L# B$ v" B$ v# v# L$ L# ? B= v# I" v" B. v" B$ v$ B- v# I" Sl I#,""",
        """B$ L+ B. B. SF B$ B$ v+ Sl IR B$ B$ v+ B. S~ B$ B$ v+ Sl IS IR L" B$ L" B$ L# B$ v" B$ v# v# L# B$ v" B$ v# v# L$ L# ? B= v# I" v" B. v" B$ v$ B- v# I\""""
    ]

    for i, case in enumerate(test_cases, 1):
        print(f"Test case {i}:")
        print(f"Input: {case}")
        result = parse_icfp(case)
        print(f"Parsed: {result}")
        print()

    # Run the specification example test
    test_specification_example()
