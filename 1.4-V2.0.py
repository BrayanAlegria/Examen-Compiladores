import tkinter as tk
from tkinter import ttk
import ply.lex as lex

def analizar(event=None):
    datos = entry1.get()
    ci = ingreso(datos)
    
    resultado_texto.config(state=tk.NORMAL)
    for estado in ci:
        resultado_texto.insert(tk.END, estado + '\n')
    
    resultado_texto.config(state=tk.DISABLED)

def eliminar():
    resultado_texto.config(state=tk.NORMAL)
    resultado_texto.delete('1.0', tk.END)
    resultado_texto.config(state=tk.DISABLED)

tokens = ['ID','LPAREN', 'RPAREN', 'PUBLIC', 'STATIC', 'VOID', 'MAIN', 'LBRACE', 'RBRACE', 'INT', 'EQUALS', 'SEMICOLON', 'FLOAT', 'AREA', 'BASE', 'ALTURA', 'DIV', 'MULT','NU', 'DIGIT']
linea = 1

palabras_reservadas = {
    '(': 'LPAREN',
    ')': 'RPAREN',
    'public': 'PUBLIC',
    'static': 'STATIC',
    'void': 'VOID',
    'main': 'MAIN',
    '{': 'LBRACE',
    '}': 'RBRACE',
    'int': 'INT',
    '=': 'EQUALS',
    ';': 'SEMICOLON',
    'n': 'ID',
    'area':'AREA',
    'base': 'BASE',
    'altura':'ALTURA',
}

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = palabras_reservadas.get(t.value, 'ID')
    return t

#regex tokens
t_INT = r'int'
t_EQUALS = r'='
t_SEMICOLON = r';'
t_FLOAT = r'\d+\d+'
t_DIV =  r'\/'
t_MULT = r'\*'
t_DIGIT = r'\d'
t_NU = r'\d+'

t_LPAREN = r'\('
t_RPAREN = r'\)'

t_LBRACE = r'\{'
t_RBRACE = r'\}'

#ignore espacios en blanco
def t_WHITESPACE(t):
    r'[\t]+'
    pass
t_ignore = ' \t'

def t_error(t):
    print(f"Carácter ilegal: '{t.value[0]}' en la línea {t.lineno}")
    t.lexer.skip(1)

def error(datos):
    return [f'no definido: {datos}']

def ingreso(datos):
    global linea
    if len(datos) < 1:
        return ['Cadena inválida: La cadena está vacía.']

    token = lex.lex()
    token.input(datos)
    lexer = []
    es_valido = True

    for toke in token:
        if toke.type == 'ID':
            es_valido = es_valido and (toke.value in palabras_reservadas or toke.value.isdigit())
            categoria = 'Identificador'
        elif toke.type == 'PUBLIC' or toke.type == 'PUBLIC':
            categoria = 'Reservado'
        elif toke.type == 'LPAREN' or toke.type == 'LPAREN':
            categoria = 'Símbolo'
        elif toke.type == 'RPAREN' or toke.type == 'RPAREN':
            categoria = 'Símbolo'
        elif toke.type == 'LBRACE' or toke.type == 'LBRACE':
            categoria = 'Delimitador'
        elif toke.type == 'BASE':
            categoria = 'Reservada'
        elif toke.type == 'NU':
            categoria = 'NUMERO'
        elif toke.type == 'MULT':
            categoria = 'Operador'  
        elif toke.type == 'DIV':
            categoria = 'Operador'  
        elif toke.type == 'AREA':
            categoria = 'Reservada'  
        elif toke.type == 'ALTURA':
            categoria = 'Reservada'
        elif toke.type == 'RBRACE' or toke.type == 'RBRACE':
            categoria = 'Delimitador'
        elif toke.type == 'FLOAT':
            categoria = 'Número'
        else:
            es_valido = es_valido and toke.type in palabras_reservadas.values()
            if toke.type == 'STATIC':
                categoria = 'Reservado'
            elif toke.type == 'VOID':
                categoria = 'Reservado'   
            elif toke.type == 'MAIN':
                categoria = 'Identificador'
            elif toke.type == 'INT':
                categoria = 'Reservado'
            elif toke.type == 'EQUALS':
                categoria = 'Operador'
            elif toke.type == 'SEMICOLON':
                categoria = 'Delimitador'
            else:
                categoria = 'No clasificado'

        estado = '->Linea: {:4} Valor {:10} Categoría {:10}'.format(
            str(toke.lineno), str(toke.value), categoria)
        lexer.append(estado)

    return lexer

# Interfaz gráfica
ventana = tk.Tk()
ventana.title("Analizador léxico")
ventana.geometry("1000x800")

frame = ttk.Frame(ventana, padding=(30, 30, 30, 30))
frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

marca_agua = ttk.Label(frame, text="Brayan DSM | 6°M", font=("Times", 12), foreground="blue")
marca_agua.place(relx=1, rely=0, anchor=tk.NE)

entry1 = ttk.Entry(frame, width=60)
entry1.grid(column=0, row=0, padx=10, pady=10)

resultado_texto = tk.Text(frame, height=15, width=100, state=tk.DISABLED)
resultado_texto.grid(column=0, row=1, padx=10, pady=10)

boton_analizar = ttk.Button(frame, text="Analizar", command=analizar)
boton_analizar.grid(column=0, row=2, pady=20, sticky=tk.N+tk.S+tk.W+tk.E)

boton_limpiar = ttk.Button(frame, text="Limpiar", command=eliminar)
boton_limpiar.grid(column=0, row=3, pady=20, sticky=tk.N+tk.S+tk.W+tk.E)

# Enter para analizar
entry1.bind("<Return>", analizar)

ventana.mainloop()
