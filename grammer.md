# Mathematische operationen
## expression
- term ((PLUS|MINUS) term)*
An expression looks for a term +/- a term
## term
- factor ((MUL|DIV) factor)*
## factor
- INT|FLOAT

#       Assign
    /       /     |      \
  type identifier =  expression
                          |
                      NumberNode
                          |
                          2
(int x = 2)

# Statements
## asign
## if
## while
## try
## catch