from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
import sqlite3

class DB:
    def __init__(self, db):
        #Init the databse class
        self.db = db

        #Connecting to the database
        self.conn = sqlite3.connect(db)

        #Cursor
        self.cur = self.conn.cursor()

        #Create the table if it does not exist
        self.cur.execute('CREATE TABLE IF NOT EXISTS contacts(id INTEGER PRIMARY KEY, name text, number text, email text, relation text)')

        #Commit the command to execute
        self.conn.commit()

    def fetch_all(self):
        #Fetch the data from the database
        self.cur.execute('SELECT * FROM contacts')
        return self.cur.fetchall()

    def add(self,name,number,email,relation):
        #Insert the element into the table
        self.cur.execute('INSERT INTO contacts VALUES(NULL, ?, ?, ?, ?)',(name,number,email,relation))
        self.conn.commit()

    def delete(self,id):
        #Delete the entry from the sql database
        self.cur.execute('DELETE FROM contacts WHERE id = ?', (id,))
        self.conn.commit()

    def update(self,id,name,number,email,relation):
        #Updates the database
        self.cur.execute('UPDATE contacts SET name = ?, number = ?, email = ?, relation = ? WHERE id = ?', (name,number,email,relation,id))
        self.conn.commit()
        
    def __del__(self):
        #Destructor
        self.conn.close()

class Application(Frame):
    '''Main class for the application Frame'''
    def __init__(self, db, master = None):
        '''Initialise the current class'''
        self.master = master
        self.db = db
        self.id_lookup = {}

        #Calling the super class to initialise the frame inside of the master
        super().__init__(master)

        #Create the applications inside of the window
        self.load_widgets()

        #Load key bindings
        self.load_binds()

        #Create a variable to select an item
        self.selected = None

        #Pack the frame into the master
        self.pack()

        #Populate the list
        self.populate_list()

    def load_binds(self):
        #Load the key bindings for the main gui
        self.master.bind('<Delete>',self.remove)
        self.master.bind('<Return>', self.add)
        self.master.bind('<Up>',self.f_prev)
        self.master.bind('<Down>',self.f_next)

        #Binding the scrollbar to the textbox
        self.databox.bind('<<ListboxSelect>>',self.select_item)

    def f_prev(self,_event):
        #Shift the cursor in the listbox to the previous one
        self.databox.tk_focusPrev

    def f_next(self,_event):
        #Shift the cursor in the list box to the next one
        self.databox.tk_focusNext

    def load_widgets(self):
        '''Main method to load that widgets which will be used within the GUI'''
        #Creating a label for the title
        self.title = Label(self,text = 'Address Book')

        #Adding all of the string variables
        self.name = StringVar()
        self.number = StringVar()
        self.email = StringVar()
        self.relation = StringVar()

        #Adding all of the Entries
        self.name_entry = Entry(self, textvariable = self.name)
        self.number_entry = Entry(self, textvariable = self.number)
        self.email_entry = Entry(self, textvariable = self.email)
        self.relation_entry = Entry(self, textvariable = self.relation)

        #Adding the labels for the items
        self.name_label = Label(self,text = 'Name')
        self.number_label = Label(self,text = 'Number')
        self.email_label = Label(self,text = 'Email')
        self.relation_label = Label(self,text = 'Relation')

        #Adding the buttons for the widget
        self.add_btn = Button(self, text = 'Add', command = self.add)
        self.update_btn = Button(self, text = 'Update', command = self.update)
        self.instructions_btn = Button(self, text = 'Instructions', command = self.instructions)
        self.remove_btn = Button(self, text = 'Remove', command = self.remove)

        #Creating a new frame to store the databox as well as the scrollbar
        self.dataframe = Frame(self,border=  0)

        #Adding a textbox to show the addresses of the people in the database
        self.databox = Listbox(self.dataframe,height = 8, width = 80, border = 0)

        #Adding a scrollbar for the textbox
        self.databox_scrollbar = Scrollbar(self.dataframe)

        #Binding the scroll to the databox
        self.databox.configure(yscrollcommand = self.databox_scrollbar.set,scrollregion = self.databox.bbox('active'))
        self.databox_scrollbar.configure(command = self.databox.yview)

        #Packing the databox and the scroll bar into secondary frame
        self.databox.pack(side = LEFT)
        self.databox_scrollbar.pack(side = RIGHT, fill = Y)

        #Packing the main label
        self.title.grid(row = 0, column = 1, columnspan = 5, padx = 10 ,pady = 10)

        #Packing name related widgets
        self.name_label.grid(row = 1, column = 1 ,padx = 10,pady = 5)
        self.name_entry.grid(row = 1, column = 2)

        #Packing number related widgets
        self.number_label.grid(row = 1, column = 4)
        self.number_entry.grid(row = 1,column = 5, padx = 10)

        #Packing email related widgets
        self.email_label.grid(row = 2, column = 1, padx = 10)
        self.email_entry.grid(row = 2, column = 2)

        #Packing the relation related widgets
        self.relation_label.grid(row = 2, column = 4)
        self.relation_entry.grid(row = 2, column = 5, padx = 10)

        #Packing the buttons
        self.add_btn.grid(row = 4, column =  1)
        self.remove_btn.grid(row = 4, column = 2)
        self.update_btn.grid(row = 4, column = 4)
        self.instructions_btn.grid(row=4, column = 5)

        #Packing the databox related widgets
        self.dataframe.grid(row = 6, column = 1, columnspan = 6, padx = 10, pady = 10)

    def clear_inputs(self):
        self.name_entry.delete(0,END)
        self.number_entry.delete(0,END)
        self.relation_entry.delete(0,END)
        self.email_entry.delete(0,END)

    def select_item(self,_event = None):
        '''Selects an the item that the user has pressed'''
        #Unpack the item that the user has selected
        selected = self.databox.curselection()

        #Check if there is anything selected
        if(len(selected) > 0 and selected[0] != 0):
            #Set the id of the current item to the selected item
            self.selected = selected[0]

            #Clear the entrybox
            self.clear_inputs()

            #Make the data for the selected item onto the list
            id,name,number,email,relation = map(lambda x: x.strip(),self.databox.get(self.selected).split())
            self.name_entry.insert(0,name)
            self.number_entry.insert(0,number)
            self.email_entry.insert(0,email)
            self.relation_entry.insert(0,relation)
        else:
            self.selected = None

    def populate_list(self) -> None:
        '''Populate the databox with values which are previously stored'''

        self.id_lookup = {}
        #Clear the listbox of current items
        self.databox.delete(0,END)
        self.databox.insert(END, f"{'Index':^15} {'Name':^20} {'Number':^20} {'Email':^20} {'Relation':^20}")

        #Iterate through the items and add them to the parts box
        for item in self.db.fetch_all():
            #Align the values
            self.id_lookup[self.databox.size()] = item[0]
            self.databox.insert(END, f"{self.databox.size():<{20-len(str(self.databox.size()))}} {item[1]:^{24-len(str(item[1]))}} {item[2]:^{26-len(str(item[2]))}} {item[3]:^{28-len(str(item[3]))}} {item[4]:^{25-len(str(item[4]))}}")

    def instructions(self) -> None:
        messagebox.showinfo('Instructions', '''How to use\nFill up all of the information and use the buttons to add, remove, or update contacts''')

    def get_all(self):
        '''Get all of the information within the entry'''
        return (self.name.get(), self.number.get(), self.email.get(), self.relation.get())

    def add(self, _event = None) -> None:
        '''Add the items into the database'''

        #If the entries are empty
        if("" in self.get_all()):
            messagebox.showerror('Please fill in the entres','Please fill up the entries before adding')
            return

        #If the number is invalids
        elif(not self.number.get().isdigit()):
            messagebox.showerror('Invalid input','The number that you have entered is invalid')
            return
            
        name,number,email,relation = self.get_all()
        self.db.add(name,number,email,relation)
        self.populate_list()
        self.databox.selection_set(END)
        self.databox.see(END)
        self.select_item()
        self.clear_inputs()

    def remove(self,_event = None) -> None:
        '''Remove the selected item'''
        #Check if there is an item that is selected
        if(self.selected != None):
            #If there is something that is selected remove it
            id = self.id_lookup[self.selected]
            self.db.delete(id)
            ind = self.selected
            
            self.populate_list()
            if(ind < self.databox.size()):
                self.databox.selection_set(ind)
                self.databox.see(ind)
                self.select_item()
            else:
                self.databox.selection_set(END)
                self.databox.see(END)
                self.select_item()
        else:
            messagebox.showerror('Selection Error','Please select an entry from the address book \nto remove')
    
    def update(self) -> None:
        '''Update an item on the list'''
        if(self.selected):
            #If there is something selected
            id = self.id_lookup[self.selected]
            name,number,email,relation = self.get_all()
            self.db.update(id,name,number,email,relation)
            self.populate_list()
            self.databox.selection_set(self.selected)
            self.databox.see(self.selected)
            self.select_item()
        else:
            #If there is nothing selected
            messagebox.showerror('Selection Error', 'Please select an entry from the address book \nto update')
    

def main():
    """Main function to be run when the file is executed as the main file"""
    db = DB('contacts.db')
    root = Tk()
    root.title("Address Book")
    root.geometry('700x500')
    app = Application(db,root)
    root.mainloop()


#Check if the file is executed as the main file
if(__name__ == '__main__'):
    main()