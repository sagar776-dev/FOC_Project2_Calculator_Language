import re

operators = ['+', '-', '++', '--', '*', '/', '^', '++', '--']
relational_operators = ['==', '<=', '>=', '!=', '<', '>']
boolean_operators = ['&&', '||', '!']
precedence = {'+': 1,
                  '-': 1,
                  '*': 2,
                  '/': 2,
                  '^': 3,
                  '--': 4,
                  '++': 4,
                  '==': 0,
                  '<=': 0,
                  '>=': 0,
                  '<': 0,
                  '>': 0,
                  '!=': 0,
                  '&&': -1,
                  '||': -1,
                  '!': -1}
variables = {}
equations = []

class Token():
    type: str
    value: str
    
    """
        >>> token('sym', '+')
        token('sym', '+')
    """
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f'token({self.type}, {self.value})'

def lexer(exp):
    """
        >>> lexer('a+b-c)
        [token(var, a), token(opr, +), token(var, b), token(opr, -), token(var, c)]
        
    """
    global variables
    global relational_operators
    global boolean_operators
    
    tokens = []
    exp = exp.replace(' ', '')
    
    i = 0
    while i < len(exp):
        if exp[i] == ' ':
            i += 1
            continue
        elif exp[i].isdigit():
            j = i
            num = ''
            while j < len(exp) and (exp[j].isdigit() or exp[j] == '.'):
                num += exp[j]
                j += 1
            i = j
            #print(num)
            tokens.append(Token('num', num))
        elif exp[i].isalpha():
            j = i
            var = ''
            while j < len(exp) and exp[j].isalpha() :
                var += exp[j]
                j += 1
            i = j
            value = 0
            if var in variables:
                value = variables[var]
            #print(var)
            tokens.append(Token('num', value))
            
        elif exp[i] == '+' and exp[i+1] == '+':
            tokens.append(Token('opr', '++'))
            i += 2
        elif exp[i] == '-' and exp[i+1] == '-':
            tokens.append(Token('opr', '--'))
            i += 2
        elif exp[i] == "(" or exp[i] == ")":
            tokens.append(Token('param', exp[i]))
            i += 1
        elif exp[i] in operators:
            if (len(tokens) == 0 or tokens[-1].type == 'opr' or tokens[-1].value == "(") and exp[i] == '-':
                j = i + 1
                if exp[j].isdigit():
                    num = ''
                    while j < len(exp) and (exp[j].isdigit() or exp[j] == '.'):
                        num += exp[j]
                        j += 1
                    i = j
                    value = 0
                    if var in variables:
                        value = variables[var]
                    #print(var)
                    tokens.append(Token('num', value * -1))
                elif exp[j].isalpha():
                    var = ''
                    while j < len(exp) and exp[j].isalpha() :
                        var += exp[j]
                        j += 1
                    i = j
                    value = 0
                    if var in variables:
                        value = variables[var]
                    #print(var)
                    tokens.append(Token('num', value * -1))
                else:
                    pass
            else:    
                tokens.append(Token('opr', exp[i]))
                i += 1
        elif (exp[i] + '' + exp[i+1]) in relational_operators: #Relational operators
            tokens.append(Token('opr', exp[i]))
            i += 2
        elif exp[i] in relational_operators: #Relational operators
            tokens.append(Token('opr', exp[i]))
            i += 1
        elif exp[i] == '&' and exp[i+1] == '&':
            tokens.append(Token('opr', '&&'))
            i += 2
        elif exp[i] == '|' and exp[i+1] == '|':
            tokens.append(Token('opr', '||'))
            i += 2
        elif exp[i] == '!':
            tokens.append(Token('opr', '!'))
            i += 1
        else:
            # print("else",exp[i])
            raise SyntaxError(f'unexpected character {exp[i]}')
    return tokens    

            
def infix_to_postfix(tokens):
    global precedence
    output = []
    operator_stack = []
    
    for token in tokens:
        type = token.type
        value = token.value
        if type == 'num':
            output.append(value)
        elif type == 'var':
            output.append(value)
        elif type == 'opr':
            while operator_stack and operator_stack[-1] != '(' and precedence[value] <= precedence[operator_stack[-1]]:
                output.append(operator_stack.pop())
            operator_stack.append(value)
        elif value == '(':
            operator_stack.append(value)
        elif value == ')':
            while operator_stack and operator_stack[-1] != '(':
                output.append(operator_stack.pop())
            operator_stack.pop()
    
    while operator_stack:
        output.append(operator_stack.pop())
    
    return output

def eval_relational_eq(num1, num2, opr):
    if opr == '==':
        return float(num1) == float(num2)
    if opr == '!=':
        return float(num1) != float(num2)
    if opr == '<':
        return float(num1) < float(num2)
    if opr == '>':
        return float(num1) > float(num2)
    if opr == '<=':
        return float(num1) <= float(num2)
    if opr == '>=':
        return float(num1) >= float(num2)
    
def eval_boolean_eq(num1, num2, opr):
    if opr == '&&':
        print(num1, num2, float(num1) and float(num2))
        res = float(num1) and float(num2)
    if opr == '||':
        res = float(num1) or float(num2)
    if opr == '!':
        res (not float(num1))
    if res == 0:
        return 0
    else:
        return 1

def evaluate_postfix(tokens):
    global relational_operators
    global boolean_operators
    stack = []
    print(tokens)
    for token in tokens:
        #print(token, stack)
        try:
            tempToken = token
            token = float(token)
        except:
             token = tempToken
        if isinstance(token, float) or isinstance(token, int):
            stack.append(float(token))
        else:
            b = stack.pop()
            if token == '++':
                stack.append(b + 1)
                continue
            elif token == '--':
                stack.append(b - 1)
                continue
            elif token == '!':
                stack.append((not float(b)))
            else:
                a = stack.pop()
                if token == '+':
                    stack.append(a + b)
                elif token == '-':
                    stack.append(a - b)
                elif token == '*':
                    stack.append(a * b)
                elif token == '/':
                    stack.append(a / b)
                elif token == '^':
                    stack.append(a ** b)
                elif token in relational_operators:
                    stack.append(int(eval_relational_eq(a, b, token)))
                elif token in boolean_operators:
                    stack.append(int(eval_boolean_eq(a, b, token)))
    
    return stack.pop()

def processExps(exps):
    global variables
    # print('exps')
    # print(exps)
    for exp in exps:
        print()
        print(exp)
        ## Handle equations by splitting LHS and RHS
        if '=' in exp:
            sides = exp.split("=")
            variable = sides[0].strip()
            eq = sides[1].strip()
            # print(variable, eq)
            if eq.isnumeric():
                variables[variable] = float(eq)
                # print("Numeric: ", eq)
            elif eq.isalpha():
                variables[variable] = variables[eq]
                # print("variable: ", eq)
            else:
                tokens = lexer(eq)
                postfix_exp = infix_to_postfix(tokens)
                print("postfix :",postfix_exp)
                res = evaluate_postfix(postfix_exp)
                # print()
                variables[variable] = res
        ## Handle print statement
        elif 'print' in exp.lower():
            print(variables)
            varList = exp.split('print')[1].split(",")
            for var in varList:
                # print('var: ', var)
                var = var.strip()
                if var in variables:
                    print(variables[var.strip()], end=":v ")
                elif var.isnumeric():
                    print(var, end = ":n ")
                else:
                    tokens = lexer(var)
                    postfix_exp = infix_to_postfix(tokens)
                    # print("postfix :",postfix_exp)
                    res = evaluate_postfix(postfix_exp)
                    print(res, end = ":r ")    
            print()
        ## Handle ++ and -- standalone
        elif exp.startswith('++') or exp.startswith('--'):
            
            variable = exp[2:]
                
            tokens = lexer(exp)
            postfix_exp = infix_to_postfix(tokens)
            print("postfix :",postfix_exp)
            res = evaluate_postfix(postfix_exp)
            # print()
            variables[variable] = res
        elif exp.endswith('++') or exp.endswith('--'):
            
            variable = exp[:-2]
                
            tokens = lexer(exp)
            postfix_exp = infix_to_postfix(tokens)
            print("postfix :",postfix_exp)
            res = evaluate_postfix(postfix_exp)
            # print()
            variables[variable] = res


exps1 = [
    "x  = 3",
    "y  = 5",
    "x = 1 + -2",
    "z  = 2 + x * y",
    "z2 = (2 + x) * y * (2<1)",
    "print x, y, z, z2"
]

exps1=[
    "x++",
    "print x",
    "print ++y + x"
]

# exps1=[
#     "x=2",
#     "y=3",
#     "z=x+-y",
#     "print z"
# ]

exps2 = [
    "pi = 3.14159",
    "r = 2",
    "area = pi * r^2",
    "print area"
]

exps3 = ["print 0 || 0"]

# print(lexer("z=x+-y"))

processExps(exps1)
# processExps(exps2)
# processExps(exps3)
        

# # print(lexer('a+b-c'))
# tokens = lexer('++2 + (3 * 5) - ++1')

# postfix_exp = infix_to_postfix(tokens)
# print(postfix_exp)
#print(evaluate_postfix([2, 3.0, 5.0, '*', '+']))
