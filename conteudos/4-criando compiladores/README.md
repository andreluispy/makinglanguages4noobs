# Criando um compilador
 Já criamos um interpretador e vamos finalmente criar um compilador, lembra que no final da parte dos interpretadores eu disse para salvar o código? O código é quase o mesmo, pois só muda na parte `# Exec functions` que se tornará a área `# Code generate` onde geraremos o código C.

 Agora vamos começar com o código fazendo algumas modificações:
 ```py
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

class interpreter:
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

def main():
    Interpreter = interpreter()
    while True:
        line = input(">> ")             # get input
        Interpreter.main(line)          # call interpreter

main()
 ```

 Note que é o mesmo código, mas em `__init__` criamos uma variável do tipo lista(array) chamada `ccode`, agora temos a parte do token que é igual à última parte e por isso teremos menos trabalho, agora vamos iniciar a parte da geração do código, mas primeiro você deve saber algumas coisas, primeiro que vamos gerar o código em C e depois chamar o compilador para gerar o executável com o comando `gcc scriptc.c -o scriptc` e também que vamos usar a biblioteca `<stdio.h>` de C para poder usar funções como `printf()` e, finalmente, vamos começar a gerar o código do print:

 ```py
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

    # write code
    for line in Compiler.ccode: # para cada linha em self.ccode, não estamos dentro da classe compiler então invez de self usamos a variavel que contem a classe compiler no caso é a variavel Compiler
        script.write(line + "\n") # escreva a linha com \n(pular para proxima linha)

    script.write('return 0;\n') # escrever return 0
    script.write('}') # fechar metodo main
    script.close()
    
    system("gcc scriptc.c -o scriptc") # gerar execultavel
    system("rm scriptc.c") # deletar codigo C

main()
 ```

 Observe que a parte `main()` mudou porque agora lemos um arquivo chamado `script.test` que é o script que irá armazenar o código escrito em nossa linguagem e observe que se você quiser pode colocar qualquer nome que desejar ou até mesmo implementar o leitura dos argumentos da linha de comando para que possamos digitar: `python compiler.py scriptdaminhalang.myextension`. Além disso, também incluímos a lib os que nos permite executar comandos no terminal, e também observamos que C tem um código padrão que é:

 ```c
#include <stdio.h>

int main(){
    return 0;
}
 ```

 Este código já foi escrito por nosso compilador, mas separado da parte que escreve o código de self.ccode. Para testar, se executarmos o script python, na pasta onde está teremos um executável chamado scriptc, lembrando que você deve ter gcc para usar o comando de compilação `gcc scriptc.c -o scriptc`, se quiser pode também use outro compilador de C como clang ou mingw. E agora implementar o comando add:

 ```py
        # Code generate
        _function = self.tokens[0].value # a variavel _function recebe o valor do primeiro token na lista de tokens que como vimos é a nossa função
        
        if _function == 'print': # se a função for "print"
            if self.tokens[1].type == STRING: # verificar se o token é string
                self.ccode.append(f'printf("{self.tokens[1].value}\\n");') # adicionar a função printf com a string para o codigo(self.ccode), note que passamos a string do codigo usando aspas simples('') porque senão as aspas duplas do comando printf iam entrar em conflito
        elif _function == "add":
            self.ccode.append(f'printf("%i\\n", {self.tokens[1].value}+{self.tokens[2].value});')
 ```
 Aqui implementei o comando add em lá na classe `compiler` em code generate e agora implementar a criação de variaveis e o print para variaveis:

 ```py
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
 ```

 Agora, se digitarmos isso no script:

 ```
string name = "andre";
print name;
 ```

 E se executarmos o `scriptc`, obteremos o seguinte resultado: `andre`. Finalmente fizemos a mesma coisa que o interpretador, mas no compilador e o mais interessante sobre o compilador é que temos um executável que podemos distribuir para qualquer pessoa! Mas você notou que nosso compilador gera código C e chama o compilador C, você sabe como funciona o compilador C? Simples, o compilador C gera o código mas em Assembly, a linguagem mais próxima do código de máquina(binário) e chama o compilador Assembly. E o compilador assembly pega o código assembly e o transforma em código de máquina (binário) e, finalmente, o executável é gerado. Finalmente fizemos um interpretador e um compilador e eu poderia parar por aí porque você provavelmente entendeu a lógica de ambos, mas ainda vamos brincar e crie um interpretador em C e também ver sobre compilador para assembly, não vamos construir um compilador assembly, mas sim comparando um compilador assembly que fiz com um compilador C.

 [retornar](../../README.md)
