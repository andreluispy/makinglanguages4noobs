#! /bin/python3

# language types
STRING = "STRING"
INT = "INT"
IDENTIFY = "IDENTIFY"
NULL = "NULL"

def error(line, error):
    print(f"Error in line {line}: {error}")

class token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class compiler:
    def __init__(self):
        self.ccode = []
        self.vars = {} # a nossa "hash table"
        self.actual_line = 0

    def main(self, line):
        # recriando variaveis usadas de linha em linha!
        self.i = 0  # indice atual da linha
        self.c = '' # char(letra) atual da linha
        self.line = line # guardando a string da linha numa variavel de classe
        self.actual_token = token(NULL, '') # variavel actual_token será o token atual
        self.tokens = [] # uma lista para guardar os tokens
        self.in_string = False # bool controler to strings

        self.actual_line += 1

        while True:
            self.c = self.line[self.i] # definir a letra atual para o indice atual da linha

            if self.c == ';':
                break
            elif self.c.isdigit() and self.actual_token.type == INT or self.c.isdigit() and self.actual_token.type == NULL: # se a char atual é um numero e estamos em um numero INT ou começando um token
                self.actual_token.type = INT # tipo de actual token é INT
                self.actual_token.value = self.actual_token.value + self.c # adicionar a char atual para a string do valor atual do token

                if self.line[self.i+1].isdigit(): # se o proximo char for um numero então continue
                    pass
                else: # se o proximo char não for um numero então guarde o token atual e limpe o valor de atual_token
                    self.tokens.append(self.actual_token)
                    self.actual_token = token(NULL, '')
            elif self.c == '"': # se char atual seja "
                if self.in_string: # se já estiver numa string(aspa de fechamento da string) então in_string = false, adiciona o actual token para tokens e actual_token é limpo
                    self.in_string = False
                    self.tokens.append(self.actual_token)
                    self.actual_token = token(NULL, '')
                else: # senão(aspa de inicio da string) então in_string = True, tipo do token atual é string
                    self.actual_token.type = STRING
                    self.in_string = True
            elif self.c.isalnum(): # se o caractere é alfa numerico(do alfabeto or numero)
                if self.in_string: # se estamos numa string
                    self.actual_token.value = self.actual_token.value + self.c
                else: # senão for string então é função!
                    self.actual_token.type = IDENTIFY
                    self.actual_token.value = self.actual_token.value + self.c
                    
                    if self.line[self.i + 1] in [" ", ';']: # se o proximo caractere é um espaço então acabou a função
                        self.tokens.append(self.actual_token)
                        self.actual_token = token(NULL, '')

            elif self.c == ' ' and self.in_string: # se o caractere é um espaço e estamos em uma string
                self.actual_token.value = self.actual_token.value + self.c

            self.i += 1 # ir para proximo indice

        # Code generate
        _function = self.tokens[0].value # a variavel _function recebe o valor do primeiro token na lista de tokens que como vimos é a nossa função
        
        if _function == 'print': # se a função for "print"
            if self.tokens[1].type == STRING: # verificar se o token é string
                self.ccode.append(f'printf("{self.tokens[1].value}\\n");') # adicionar a função printf com a string para o codigo(self.ccode), note que passamos a string do codigo usando aspas simples('') porque senão as aspas duplas do comando printf iam entrar em conflito
            else: # senão for string
                var = self.vars[self.tokens[1].value]
                if var.type == STRING:
                    tipo = 's'
                elif var.type == INT:
                    tipo = 'i'
                
                self.ccode.append(f'printf("%{tipo}\\n", {self.tokens[1].value});') # mostre o valor da variavel
        elif _function in ['int', 'string']: # comparar se a função é um tipo de dados(ou seja declaração de variavel: int idade = 18;)            
            # errors
            _error = False
            if _function == "string":
                if self.tokens[2].type != STRING:
                    error(self.actual_line, "Esperado tipo STRING")
                    _error = True
            elif _function == "int":
                if self.tokens[2].type != INT:
                    error(self.actual_line, "Esperado tipo INT")
                    _error = True

            if _error == False:
                self.vars[self.tokens[1].value] = self.tokens[2] # guardar tipo de variavel em self.vars para usar no print

                if self.tokens[0].value == 'string':
                    self.ccode.append(f'char {self.tokens[1].value}[] = "{self.tokens[2].value}";') # codigo C para variaveis strings
                elif self.tokens[0].value == 'int':
                    self.ccode.append(f'int {self.tokens[1].value} = {self.tokens[2].value};') # codigo C para variaveis int
        elif _function == "add":
            self.ccode.append(f'printf("%i\\n", {self.tokens[1].value}+{self.tokens[2].value});')

def main():
    from os import system # usar função system para execultar comandos no console

    Compiler = compiler()
    code = open('script.test', 'r') # abrir arquivo de script que vai ser chamado de script.test
    for _line in code:
        Compiler.main(_line.replace('\n', ''))
    
    # Write Code
    script = open("scriptc.c", "w") # abrir arquivo scriptc.c(onde o codigo ficará guardado)
    script.write('#include <stdio.h>\n') # incluir lib stdio
    script.write('int main(){\n') # escrever função main

    # write code in self.ccode
    for line in Compiler.ccode: # para cada linha em self.ccode
        script.write(line + "\n") # escreva a linha com \n(pular para proxima linha)

    script.write('return 0;\n') # escrever return 0
    script.write('}') # fechar metodo main
    script.close()
    
    system("gcc scriptc.c -o scriptc") # gerar execultavel
    system("rm scriptc.c") # deletar codigo C

main()
