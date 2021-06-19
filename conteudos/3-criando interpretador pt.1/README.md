# Finalmente mão na massa
 Finalmente, vamos ao que interessa e implementar um interpretador python.

 Uma coisa importante é sobre o método que usaremos para ler as "palavras", ele pode não ser o mais simples em comparação com a manipulação de string padrão do python e os métodos regex, mas esses métodos causam uma lentidão em nosso programa e isso faz parte da otimização, que eu disse na introdução.

 Então, vamos ver algumas fases que faremos no interpretador:
 - Criar classe de token
 - Leia a entrada, passe a entrada para o intérprete
 - O intérprete gera tokens (Análise Lexica)
 - O intérprete executa tokens
 - comando de impressão
 - variáveis

# Syntax
 Outra coisa que tenho a dizer é que toda linguagem tem uma sintaxe definida, então para sua linguagem você deve criar uma sintaxe, nossa sintaxe será uma sintaxe criada por mim chamada sintaxe regius que é uma mistura de python e c ++:
 - Olá, mundo: `print" Olá, mundo ";`
 - variáveis: `int age = 10;`
 - Mostrar variáveis: `idade de impressão;`

# Base
 Vamos fazer a função principal e criar os tipos de token do nosso idioma
 
```py
# language types
STRING = "STRING"
INT = "INT"
IDENTIFY = "IDENTIFY"
NULL = "NULL"

def main():
    Interpreter = interpreter()
    while True:
        line = input(">> ")             # get input
        Interpreter.main(line)          # call interpreter

main()
```

 **LEMBRANDO QUE AS CLASSES DE TOKEN E INTERPRETADOR DEVEM ESTAR ENTRE A FUNÇÃO MAIN E OS TIPOS**, exemplo:
 
 ```py
# language types
STRING = "STRING"
INT = "INT"
IDENTIFY = "IDENTIFY"
NULL = "NULL"

class token:
    ...

class interpreter:
    ...

def main():
    Interpreter = interpreter()
    while True:
        line = input(">> ")             # get input
        Interpreter.main(line)          # call interpreter

main()
```

 Então, agora vamos fazer uma classe de token e definir o tipo e o valor do token como um argumento:

```py
class token:
    def __init__(self, type, value):
        self.type = type
        self.value = value
```

 E criamos uma classe para o nosso interpretador definindo a linha como um argumento na função main do interpretador:
 
 ```py
class interpreter:
    def __init__(self):
        pass
    def main(line):
        pass
 ```

 Agora vamos fazer o processo de interpretação que é explicado nos comentários:

 ```py
class interpreter:
    def __init__(self):
        self.vars = {} # a nossa "hash table"

    def main(self, line):
        # recriando variaveis usadas de linha em linha!
        self.i = 0  # indice atual da linha
        self.c = '' # char(letra) atual da linha
        self.line = line # guardando a string da linha numa variavel de classe
        self.actual_token = token(NULL, '') # variavel actual_token será o token atual
        self.tokens = [] # uma lista para guardar os tokens
        self.in_string = False # bool controler to strings

        while True:
            self.c = self.line[self.i] # definir a letra atual para o indice atual da linha
            print(self.c)

            if self.c == ';':
                break

            self.i += 1 # ir para proximo indice
 ```

 Desta forma, nosso interpretador pode ler uma linha e mostrar cada dígito dela no console até atingir `;` e parar a análise lexica

 Agora vamos gerar tokens de análise lexica, além de registrar os tokens no console e desativar o log de caracteres:

 ```py
class interpreter:
    def __init__(self):
        self.vars = {} # a nossa "hash table"

    def main(self, line):
        # recriando variaveis usadas de linha em linha!
        self.i = 0  # indice atual da linha
        self.c = '' # char(letra) atual da linha
        self.line = line # guardando a string da linha numa variavel de classe
        self.actual_token = token(NULL, '') # variavel actual_token será o token atual
        self.tokens = [] # uma lista para guardar os tokens
        self.in_string = False # bool controler to strings

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
            
            self.i += 1 # ir para proximo indice
        
        for __token__ in self.tokens:
            print(__token__.type, __token__.value)
 ```

 Este interpretador por enquanto apenas registra tokens de números, mas para teste se você executar e digitar: `123;`. Você receberá esta saída: `INT 123`

 Agora temos que implementar uma leitura de string usando aspas duplas controladas por um booleano do compilador:

 ```py
class interpreter:
    def __init__(self):
        self.vars = {} # a nossa "hash table"

    def main(self, line):
        # recriando variaveis usadas de linha em linha!
        self.i = 0  # indice atual da linha
        self.c = '' # char(letra) atual da linha
        self.line = line # guardando a string da linha numa variavel de classe
        self.actual_token = token(NULL, '') # variavel actual_token será o token atual
        self.tokens = [] # uma lista para guardar os tokens
        self.in_string = False # bool controler to strings

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

            elif self.c == ' ' and self.in_string: # se o caractere é um espaço e estamos em uma string
                self.actual_token.value = self.actual_token.value + self.c

            self.i += 1 # ir para proximo indice
        
        for __token__ in self.tokens:
            print(__token__.type, __token__.value)

 ```

 Agora, se executarmos e digitarmos `123 "hello world" 456;` a saída esperada é:
 ```
INT 123
STRING hello world
INT 456
 ```

 E se o caractere é uma letra, mas nós não estamos em uma string, então ele só pode ser do tipo IDENTIFY, que é o tipo que vamos usar para palavras reservadas da linguagem como funções, tipos (quando criamos uma variável e temos que digitar o tipo primeiro) e etc... Vamos implementar isso agora, fazendo algumas pequenas modificações na parte `self.c.isalnum()`:

```py
class interpreter:
    def __init__(self):
        self.vars = {} # a nossa "hash table"

    def main(self, line):
        # recriando variaveis usadas de linha em linha!
        self.i = 0  # indice atual da linha
        self.c = '' # char(letra) atual da linha
        self.line = line # guardando a string da linha numa variavel de classe
        self.actual_token = token(NULL, '') # variavel actual_token será o token atual
        self.tokens = [] # uma lista para guardar os tokens
        self.in_string = False # bool controler to strings

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
        
        for __token__ in self.tokens:
            print(__token__.type, __token__.value)

```

 Agora que sabemos quando um token é uma função, podemos finalmente executar o código e criar um hello world em nossa linguagem. Como sabemos que na sintaxe de nossa linguagem, o primeiro token é sempre a função e os demais são os argumentos, podemos usar isso para que possamos tornar nosso trabalho mais fácil:

```py
class interpreter:
    def __init__(self):
        self.vars = {} # a nossa "hash table"

    def main(self, line):
        # recriando variaveis usadas de linha em linha!
        self.i = 0  # indice atual da linha
        self.c = '' # char(letra) atual da linha
        self.line = line # guardando a string da linha numa variavel de classe
        self.actual_token = token(NULL, '') # variavel actual_token será o token atual
        self.tokens = [] # uma lista para guardar os tokens
        self.in_string = False # bool controler to strings

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
        
        for __token__ in self.tokens:
            print(__token__.type, __token__.value)

        # Exec functions
        _function = self.tokens[0].value # a variavel _function recebe o valor do primeiro token na lista de tokens que como vimos é a nossa função
        
        if _function == 'print': # se a função for "print"
            if self.tokens[1].type == STRING: # verificar se o token é string
                print(self.tokens[1].value) # print(mostre na tela) o valor do segundo token da lista(a string do print)
```
 Se digitarmos `print "hello world";` então poderemos ver:
 
 ```
hello world
 ```

 E assim terminamos de criar nosso primeiro interpretador que mostra apenas hello world na tela, mas é um bom começo, depois de entender como a geração de token funciona, podemos implementar qualquer função na parte `# exec functions` apenas adicionando mais 1 elif.
 
 E agora deixo como uma "tarefa" você adicionar uma nova função no interpretador chamada `add` onde você passa dois números e ele retorna a soma desses 2 números. Se você não conseguiu implementar isso, então vou mostrar a você, simplesmente você deve na parte `# Exec functions` adicionar um elif (else if) para a função `add` e adicionar o valor do token 2 (índice 1) com o token 3 (índice 2), mas ambos devem ser convertidos para int usando a função `int()` do python, veja abaixo:

```py
        # Exec functions
        _function = self.tokens[0].value # a variavel _function recebe o valor do primeiro token na lista de tokens que como vimos é a nossa função

        if _function == 'add': # se a função for "add"
            value = int(self.tokens[1].value) + int(self.tokens[2].value) # somar o valor do segundo token da lista com o valor do 3 token da lista convertidos para int
            print(value) # mostrar soma
```

 Se você digitar `add 1 2;` a saída esperada é: `3`

 E agora vamos implementar variáveis! Basicamente, precisamos entender como ocorre a alocação de uma variável no ram, baseado na seguinte variável `nome = "Andre"` ela tem seu valor ocupando um espaço na memória, e este espaço tem um endereço(parte da memória onde ele está), para obter um valor na memória, não estamos procurando um espaço com um identificador "nome", mas um espaço que tenha o mesmo endereço daquele onde armazenamos a variável. Algo importante é que para cada linguagem e cada objetivo temos uma implementação diferente, na linguagem brasileira **3bc** existem apenas endereços de memória e não o nome da variável e por isso o criador implementou o sistema de árvore binária, em uma linguagem como a nossa onde temos um nome da variável, uma das melhores maneiras seria implementar uma **tabela hash** que basicamente funciona como um json:
 
 ```json
{
"nome" : "Andre"
}
 ```

 E em python temos um tipo padrão que já faz isso para nós, o **dicionário (dict)**, o dicionário python é basicamente uma tabela hash mas com várias abstrações (simplificações), o ideal seria criar a nossa própria tabela de hash, mas daria muito trabalho e não vamos fazer.

 Basicamente, temos um dicionário chamado vars em `__init__` e armazenamos as variáveis nele, observe que apenas adicionamos uma variável em ` __init__` e dois novos elif's na parte `# Exec functions` e na parte da função de print

```py
# Isso na função __init__:
        self.vars = {}

# Isso na função main:

        # Exec functions
        _function = self.tokens[0].value # a variavel _function recebe o valor do primeiro token na lista de tokens que como vimos é a nossa função
        
        if _function == 'print': # se a função for "print"
            if self.tokens[1].type == STRING: # verificar se o token é string
                print(self.tokens[1].value) # print(mostre na tela) o valor do segundo token da lista(a string do print)
            else: # senão for string
                print(self.vars[self.tokens[1].value].value) # mostre o valor da variavel
        elif _function in ['int', 'string']: # comparar se a função é um tipo de dados(ou seja declaração de variavel: int idade = 18;)
            self.vars[self.tokens[1].value] = self.tokens[2]
```

 Se digitarmos `string name = "andre";` e depois digitar `print name;` a saída esperada é: `andre`

 E assim implementamos nosso sistema de variáveis! E também uma modificação da parte de print para mostrar variáveis. Agora lembra da função add? Vamos modificá-la para que possamos adicionar variáveis INT:

```py
        elif _function == 'add': # se a função for "add"
            if self.tokens[1].type == IDENTIFY: # se o primeiro numero for uma variavel(IDENTIFY)
                self.tokens[1].type = INT # tipo recebe INT
                self.tokens[1].value = self.vars[self.tokens[1].value].value # valor recebe o valor da variavel

            if self.tokens[2].type == IDENTIFY: # se o segundo numero for uma variavel(IDENTIFY)
                self.tokens[2].type = INT # tipo recebe INT
                self.tokens[2].value = self.vars[self.tokens[2].value].value # valor recebe o valor da variavel

            value = int(self.tokens[1].value) + int(self.tokens[2].value) # somar o valor do segundo token da lista com o valor do 3 token da lista convertidos para int
            print(value) # mostrar soma
```

 Se digitarmos `int n1 = 20;` e `int n2 = 30;` e, em seguida, `add n1 n2;` a saída esperada é: `50`

 E essa parte é uma parte interessante, já temos um interpretador muito interessante e sei que você pode implementar o que quiser sem minha ajuda! Outra coisa é que não fizemos a parte dos erros, se por exemplo você cria uma variável STRING e passa um número INT que o interpretador aceita. Então, vamos à parte dos erros! Antes da classe do interpretador, vamos criar uma função de erro:

 ```py
def error(error):
    print(f"Error: {error}")
 ```

 E vamos implementar essa função na parte de criação de variáveis:
 
 ```py
# Em main:

        # Exec functions

        elif _function in ['int', 'string']: # comparar se a função é um tipo de dados(ou seja declaração de variavel: int idade = 18;)
            _error = False
            
            if _function == "string":
                if self.tokens[1].type != STRING:
                    error("Esperado tipo STRING")
                else:
                    pass
            elif _function == "int":
                if self.tokens[1].type != INT:
                    error("Esperado tipo INT")
                else:
                    pass

            if _error == False:
                self.vars[self.tokens[1].value] = self.tokens[2]
 ```

 Se digitarmos `int n1 = "hello";` a saída esperada é: `Erro: tipo INT esperado`

 Agora fizemos uma parte importante que são os erros, mas não mostramos a linha em que o erro acontece, então vamos adicionar estes códigos no início das funções:

 ```py
def error(line, error):
    print(f"Error in line {line}: {error}")

class interpreter:
    def __init__(self):
        self.actual_line = 0
    def main(self, line):
        self.actual_line += 1

        # Exec functions
        elif _function in ['int', 'string']: # comparar se a função é um tipo de dados(ou seja declaração de variavel: int idade = 18;)
            _error = False
            
            if _function == "string":
                if self.tokens[1].type != STRING:
                    error(self.actual_line, "Esperado tipo STRING")
                else:
                    pass
            elif _function == "int":
                if self.tokens[1].type != INT:
                    error(self.actual_line, "Esperado tipo INT")
                else:
                    pass

            if _error == False:
                self.vars[self.tokens[1].value] = self.tokens[2]
 ```

 E se digitarmos `int n1 = "hello";` a saída esperada é `Erro na linha 1: Tipo INT esperado`.
 
 E se digitarmos novamente `string name = 10;` a saída esperada é `Erro na linha 2: Tipo STRING esperado`.
 
 E finalmente implementamos o sistema de contagem de linha! E agora, finalmente criamos um interpretador em um nível decente, então terminamos nosso interpretador e podemos ir em frente e salvar este código porque vamos usar uma grande parte dele na construção de compiladores.

 [retornar](../../README.md)