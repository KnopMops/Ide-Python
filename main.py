import codecs
from tkinter import *
from tkinter.filedialog import *
import tkinter.scrolledtext
import tkinter.messagebox as msg
import platform
import sys
import os
import subprocess

icondir = f'{sys.base_prefix}/lib/idlelib/Icons'
compiler = Tk()
name = 'KnoCharm'
compiler.title(f'untitled - {name}')
file_path = ''
iconfile = os.path.join(icondir, "idle.ico")
compiler.wm_iconbitmap(default=iconfile)

def set_file_path(path):
    global file_path
    file_path = path

def open_file():
    path = askopenfile(filetypes=[('Python files', '*.py')])
    try:
        with open(path, "r") as file:
            code = file.read()
            editor.delete('1.0', END)
            editor.insert('1.0', code)
    except:
        pass

def save_as():
    if file_path == '':
        path = asksaveasfile(filetypes=[('Python files', '*.py')])
    else:
        path = file_path
    with open("path", "w", encoding='utf-8') as file:
        code = editor.get('1.0', END)
        file.write(code)
        set_file_path(path)
        compiler.title(f'{path} - {name}')

def run():
    if file_path == '':
        msg.showerror('Error, file not save', 'Пожалуйста сохраните свой код')
    else:
        command = f'python {file_path}'
        save_as()
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        code_output.config(state='normal')
        code_output.insert('1.0', output)
        code_output.insert('1.0', error)
        code_output.insert('1.0', f'==== {file_path} ====\n')
        code_output.config(state='disabled')

def update_label():
    row, col = editor.index('insert').split('.')
    label.config(text=f'Python {platform.python_version()} Line {row}, Column {col}')
    compiler.after(100, update_label)

editor = tkinter.scrolledtext.ScrolledText(undo=True)
editor.pack()

menu_bar = Menu(compiler)

file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label='Open', command=open_file)
file_menu.add_command(label='Save', command=save_as)
file_menu.add_command(label='Save as', command=save_as)
file_menu.add_command(label='Exit', command=quit)
menu_bar.add_cascade(label='file', menu=file_menu)

run_bar = Menu(menu_bar, tearoff=0)
run_bar.add_command(label='Run', command=run)
menu_bar.add_cascade(label='Run', menu=run_bar)

compiler.config(menu=menu_bar)

code_output = tkinter.scrolledtext.ScrolledText(height=10, state='disabled')
code_output.pack()

label = Label(compiler, anchor='e')
label.pack(fill='x')

update_label()
compiler.mainloop()