from tkinter import ttk
from tkinter import *

import sqlite3

class vendrs:
    # connection dir property
    db_name = 'database.db'

    def __init__(self, window):
        # Initializations 
        self.wind = window
        self.wind.title('Madetex')

        # Creating a Frame Container 
        frame = LabelFrame(self.wind, text = 'Cadastrar novos vendedores')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)

        # Name Input
        Label(frame, text = 'Name: ').grid(row = 1, column = 0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row = 1, column = 1)

        # senha Input
        Label(frame, text = 'senha: ').grid(row = 2, column = 0)
        self.senha = Entry(frame, show='*')
        self.senha.grid(row = 2, column = 1)

        # Button Add vendrs
        ttk.Button(frame, text = 'Salvar', command = self.add_vendrs).grid(row = 3, columnspan = 2, sticky = W + E)

        # Output Messages 
        self.message = Label(text = '', fg = 'red')
        self.message.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)

        # Table
        self.tree = ttk.Treeview(height = 10, columns = 2)
        self.tree.grid(row = 4, column = 0, columnspan = 2)
        self.tree.heading('#0', text = 'Name', anchor = CENTER)
        self.tree.heading('#1', text = 'senha', anchor = CENTER)

        # Buttons
        ttk.Button(text = 'DELETAR', command = self.delete_vendrs).grid(row = 5, column = 0, sticky = W + E)
        ttk.Button(text = 'EDITAR', command = self.edit_vendrs).grid(row = 5, column = 1, sticky = W + E)

        # Filling the Rows
        self.get_vendrs()

    # Function to Execute Database Querys
    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    # Get vendrs from Database
    def get_vendrs(self):
        # cleaning Table 
        Registro = self.tree.get_children()
        for element in Registro:
            self.tree.delete(element)
        # getting data
        query = 'SELECT * FROM vendrs ORDER BY name DESC'
        db_rows = self.run_query(query)
        # filling data
        for row in db_rows:
            self.tree.insert('', 0, text = row[1], values = row[2])

    # User Input Validation
    def validation(self):
        return len(self.name.get()) != 0 and len(self.senha.get()) != 0

    def add_vendrs(self):
        if self.validation():
            query = 'INSERT INTO vendrs VALUES(NULL, ?, ?)'
            parameters =  (self.name.get(), self.senha.get())
            self.run_query(query, parameters)
            self.message['text'] = 'Vendedor {} adicionado'.format(self.name.get())
            self.name.delete(0, END)
            self.senha.delete(0, END)
        else:
            self.message['text'] = 'Nome e senha são obrigatórios'
        self.get_vendrs()

    def delete_vendrs(self):
        self.message['text'] = ''
        try:
           self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Selecione um Registro para DELETAR'
            return
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM vendrs WHERE name = ?'
        self.run_query(query, (name, ))
        self.message['text'] = 'Registro {} excluso'.format(name)
        self.get_vendrs()

    def edit_vendrs(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Selecione um Registro para EDITAR'
            return
        name = self.tree.item(self.tree.selection())['text']
        old_senha = self.tree.item(self.tree.selection())['values'][0]
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Editar registro'
        #Name
        Label(self.edit_wind, text = 'Nome:').grid(row = 0, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = name), state = 'readonly').grid(row = 0, column = 2)
        # novo Nome
        Label(self.edit_wind, text = 'Nova senha:').grid(row = 1, column = 1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row = 1, column = 2)

        # Old senha
        Label(self.edit_wind, text = 'Senha:').grid(row = 2, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_senha), state = 'readonly').grid(row = 2, column = 2)
        # Nova senha
        Label(self.edit_wind, text = 'Novo Nome:').grid(row = 3, column = 1)
        new_senha= Entry(self.edit_wind)
        new_senha.grid(row = 3, column = 2)

        Button(self.edit_wind, text = 'Update', command = lambda: self.edit_Registros(new_name.get(), name, new_senha.get(), old_senha)).grid(row = 4, column = 2, sticky = W)
        self.edit_wind.mainloop()

    def edit_Registros(self, new_name, name, new_senha, old_senha):
        query = 'UPDATE vendrs SET name = ?, senha = ? WHERE name = ? AND senha = ?'
        parameters = (new_name, new_senha,name, old_senha)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'Registro {} alterado!'.format(name)
        self.get_vendrs()

if __name__ == '__main__':
    window = Tk()
    application = vendrs(window)
    window.mainloop()
