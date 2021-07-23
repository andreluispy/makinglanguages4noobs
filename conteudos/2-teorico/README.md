# 1 - Não Pule a Teoria
 As pessoas costumam pular a parte teórica porque acham que é chato, mas é muito importante conhecer a teoria, caso contrário você não pode implementar a prática, mas vou tentar fazer essa parte de teoria a mais curta possível

# 2 - Como uma linguagem funciona?
 Basicamente, a linguagem pode ser representada por:

 `input > linguagem > output`

 Talvez isso não diga muito para você, mas por exemplo a representação de um hello world seria:

 `print("hello world") > python > hello world`

 Acho que agora deu para entender melhor o que quis dizer, mas a linguagem não é tão simples e é isso que veremos a seguir

# 3 - Formas de Execultar o codigo
 O código pode ser executado de duas maneiras: interpretação e compilação

 - Interpretação: Analisa o código-fonte e executa
 - Compilação: Analisa o código-fonte e gera o código executável

 Existem também 2 "variantes" da compilação:
 
 - bytecode: é assim que funciona o python e o java, é uma compilação mas diferente da convencional onde gera código executável pelo sistema operacional, aqui no bytecode o código gerado não é executado pelo seu sistema operacional mas sim por uma "máquina virtual" da linguagem, o que a faz funcionar na maioria dos sistemas evitando bugs
 - Transpilação: é o mesmo processo da compilação, mas compila para uma linguagem de alto nível(tendo em vista que compilação gera um código numa linguagem de baixo nível), por exemplo, se você tem um hello world em python e deseja transformá-lo em C sem reescrever o hello world em C então você usa a transpilação(isso existe em python e é chamado de Cython, aqui fica uma dica para quem quiser tornar os códigos Python mais rápidos)

# 4 - Analise lexica, sintatica e semantica
 O compilador ou interpretador passa por 3 análises importantes:

 - Lexica: A função do analisador ou scanner léxico é ler o código-fonte, caractere por caractere, separando-os em tokens. Também é responsabilidade desta fase eliminar elementos "decorativos" do programa, como espaços em branco, marcas de formatação de texto e comentários.
 - Sintaxe: A análise Sintatica é o processo responsável por verificar se os símbolos contidos no programa fonte formam um programa válido ou não.
 - Semântica: O papel do analisador semântico é fornecer métodos pelos quais as estruturas construídas pelo analisador possam ser avaliadas ou executadas. Um exemplo de tarefa do próprio analisador semântico é verificar os tipos de variáveis ​​nas expressões.

 O compilador também passa por outras fases que nem sempre são feitas pela maioria das linguagens, mas destaco:
 - Geração de código intermediário: ainda não é o código objeto(assembly ou C), mas sim um código que é fácil de manipular pelo gerador de código objeto
 - otimização: otimiza o código
 - Geração de código-objeto: aqui o código intermediário finalmente se torna código objeto e o compilador da linguagem que está sendo usada como código-objeto é chamado

[retornar](../../README.md)
