from tkinter import *
import pymysql
from tkinter import ttk, filedialog
import pandas as pd
import numpy as np
import re
root = Tk()



my_frame = Frame(root)
my_frame.pack(pady=20)

# treeview scrollbar
ver_scroll = Scrollbar(my_frame)
ver_scroll.pack(side=RIGHT, fill=Y)
tree_scroll = Scrollbar(my_frame, orient='horizontal')
tree_scroll.pack(side=BOTTOM, fill=X)

# create tree view
my_tree = ttk.Treeview(my_frame, yscrollcommand=ver_scroll.set, xscrollcommand=tree_scroll.set)

ver_scroll.config(command=my_tree.yview)
tree_scroll.config(command=my_tree.xview)

def file_open():
    global df
    filename = filedialog.askopenfilename(
        initialdir="C:\\Users\\92350\\OneDrive\\ucd\\prac\\sample report",
        title = "Open a File",
        filetypes=(("xlsx files","*.xlsx"),("All Files","*.*"))
    )
    if filename:
        try:
            filename = r"{}".format(filename)
            df = pd.read_csv(filename, sep="\t")
            tmp_filename = filename.split('/')[-1]
            tmp_filename = tmp_filename.split('-ctDNA')[0]
            df['filename'] = tmp_filename # add filename to df
        except ValueError:
            my_label.config(text="File Couldn't be Opened")
        except FileNotFoundError:
            my_label.config(text="File Couldn't be Found")
    # clear old tree view
    clear_tree()

    # set up new tree view
    my_tree["column"] = list(df.columns)
    my_tree["show"] = "headings"
    # loop through column list for headers
    for column in my_tree["column"]:
        my_tree.heading(column, text=column)
    # put data in tree view
    df_rows = df.to_numpy().tolist()
    for row in df_rows:
        my_tree.insert("", "end", values=row)

    df = df.replace({np.nan: None}) # replace nan for sql insertion
    print(df)
    my_tree.pack()

def clear_tree():
    my_tree.delete(*my_tree.get_children()) # go through entire tree and delete

# add a menu
my_menu = Menu(root)
root.config(menu=my_menu)

# add menu dropdown
file_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Spreadsheet", menu=file_menu)
file_menu.add_command(label="Open",command=file_open)

my_label = Label(root, text="")
my_label.pack(pady=20)

def upload():
    conn = pymysql.connect(
        host="localhost",
        port=int(3306),
        user="root",
        passwd="102030",
        db="gui"
    )
    print(conn)
    cursor = conn.cursor()

    values = list(map(tuple, df.values))
    cursor.executemany('''INSERT INTO orig_sample(
                Chromosome,
                Position,
                ID,
                Impact,
                Sequence,
                AA,
                Gene,
                Alle_freq,
                file_name
                ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ''', values)
    conn.commit()


# upload button
myButton = Button(root, text='Upload', command=upload)
myButton.pack()



root.mainloop()