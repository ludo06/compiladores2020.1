# ------------------------------------------------------------
# Processing a log file
# ------------------------------------------------------------
import ply.lex as lex

# List of token names.   This is always required
tokens = [
    'TIMESTAMP',
    'PROC',
    'MESSAGE'
]

def t_TIMESTAMP(t):
    # Regular expression for TIMESTAMP
    r'\d{2}:\d{2}:\d{2}.\d{6}\s-\d{4}'
    t.type = 'TIMESTAMP'
    return t

def t_PROC(t):
    # Regular expression for PROC
    r'\t[a-zA-Z]+\t'
    t.value = t.value[1:len(t.value) - 1]
    return t

def t_MESSAGE(t):
    # Regular expression for MESSAGE
    r'.+\n*'
    t.value = t.value[:len(t.value) - 1]
    return t

# Error handling rule
def t_error(t):
    r'.+\n*'
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


class LogProcLexer:
    data = None
    lexer = None
    def __init__(self):
        fh = open("log", 'r')
        self.data = fh.read()
        fh.close()
        self.lexer = lex.lex()
        self.lexer.input(self.data)

    def collect_messages(self):
        tokenExpecteds = []

        while True:
                token = self.lexer.token()

                if token == None:
                    break

                if token.value == 'kernel' and token.type == 'PROC':
                    tokenExpecteds.append(self.lexer.token())

        return tokenExpecteds


if __name__ == '__main__':
    print(LogProcLexer().collect_messages())

