
from tkinter import *
from functools import partial
import numpy
from tkinter import ttk
import pandas as pd

user_pass = {"Cjackson": "Password", "Ecasey": "Password", "Jrobinson": "Password", "Nmattern": "Password",
             "Lmaher": "Pass"}
user_list = []
pass_list = []
def login_info(username, password):
    print("Username:", username.get())
    print("Password:", password.get())
    user_list.append(username.get())
    user_list.append(password.get())

    if (username.get() in user_pass.keys()) and (password.get() in user_pass.values()):
        import tkinter as tk

        tkWindow.destroy()
        root = tk.Tk()
        root.title('Sprout')
        root.geometry('350x300')
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)

        class buttons:

            def __init__(self,master):
                frame = Frame(master)
                frame.pack()
                #buttons
                self.allButton = Button(frame, text="All Data", command=self.databutt)
                self.allButton.grid(column=0, row=0, sticky=tk.W, ipadx=30, ipady=30, padx=10, pady=10)

                self.filterButton = Button(frame, text="Filter", command=self.filtbutt)
                self.filterButton.grid(column=1, row=0, sticky=tk.W, ipadx=30, ipady=30, padx=10, pady=10)

                self.graphButton = Button(frame, text="Graphs", command=self.graphbutt)
                self.graphButton.grid(column=0, row=1, sticky=tk.E, ipadx=30, ipady=30, padx=10, pady=10)

                self.modButton = Button(frame, text="Modify Users", command=self.modbutt)
                self.modButton.grid(column=1, row=1, sticky=tk.E, ipadx=30, ipady=30, padx=10, pady=10)

            #button functions (windows)
            def databutt(self):
                newwindow = Toplevel(root)
                newwindow.geometry("400x300")
                Label(newwindow, text="data goes here").pack()

            #Cooper
            def filtbutt(self):
                import tkinter
                #reset StringVars of widgets
                def reset_vars():
                    model_var.set('Model Type')
                    price_range_var.set('Price Range')
                    interior_var.set('Colors-Interior')
                    exterior_var.set('Colors-Exterior')
                    condition_var.set('Car Condition')
                    location_entry.delete(0,END)
                    location_entry.insert(0,'Location')

                #filters dataframe by price range
                def price_sort(df_filtered, min_max):
                    if (min_max != 'Any' and min_max != 'Price Range'):
                        range = str(min_max).split('-')
                        min = int(range[0].strip().replace('k','000'))
                        max = int(range[1].strip().replace('k','000'))
                        df_filtered = df_filtered[df_filtered['price'].between(min, max, inclusive='both')]

                    return df_filtered

                #filters dataframe by model type
                def model_sort(df_filtered, type):
                    if (type != 'Any' and type != 'Model Type'):
                        df_filtered = df_filtered[df_filtered['model_name'].str.contains(type, case=False)]

                    return df_filtered


                #filters dataframe by interior colors
                def i_col_sort(df_filtered, i_col):
                    if (i_col != 'Colors-Interior' and i_col != 'Any'):
                        df_filtered = df_filtered[df_filtered['interior_color'].str.contains(i_col,case=False)]

                    return df_filtered
                    
                #filters dataframe by exterior colors
                def e_col_sort(df_filtered, e_col):
                    if (e_col != 'Colors-Exterior' and e_col != 'Any'):
                        df_filtered = df_filtered[df_filtered['exterior_color'].str.contains(e_col,case=False)]
                    
                    return df_filtered
                    
                #filters dataframe by location
                def loc_sort(df_filtered, loc):
                    if (loc != 'Location' and loc != ''):
                        #add code for inputted text of non locations
                        df_filtered = df_filtered[df_filtered['location_id'].str.contains(loc, case=False)]
                
                    return df_filtered

                #filters dataframe by condition
                def con_sort(df_filtered, con):
                    if (con != 'Car Condition' and con != 'Any'):
                        df_filtered = df_filtered[df_filtered['condition'].str.contains(con, case=False)]
                
                    return df_filtered

                #command for apply button. Displays new dataframe with filters from widgets
                def apply_filters(df, type, e_col, i_col, range, con, loc):
                    #deletes existing tree/spreadsheet
                    my_tree.delete(*my_tree.get_children())
                    df = model_sort(df, type)
                    df = e_col_sort(df, e_col)
                    df = i_col_sort(df, i_col)
                    df = price_sort(df, range)
                    df = con_sort(df, con)
                    df = loc_sort(df, loc)
                    #creating new treeview of filtered dataframe
                    my_tree['column'] = list(df.columns)
                    my_tree['show'] = 'headings'
                    for column in my_tree['column']:
                        my_tree.heading(column, text=column)
                    df_rows = df.to_numpy().tolist()
                    for row in df_rows:
                        my_tree.insert('', 'end', values=row)
                    #resets the display on the filter widgets
                    reset_vars()

                window = Toplevel(root)
                window.title('Filter')
                window.geometry('750x500')
                my_frame = tkinter.Frame(window)
                my_frame.pack(pady=20,fill = tkinter.BOTH, expand = True)

                #reads in excel-database file
                df = pd.read_csv('./db.csv')
                global df_filtered
                df_filtered = df
                #database innately does not show all columns if larger than certain point
                #this negates that
                pd.set_option("display.max_rows", 2000)
                pd.set_option('display.max_columns', 1000)
                pd.set_option('display.width', 1000)

                #scrollbars for tree
                my_scrollbar = ttk.Scrollbar(my_frame, orient = 'vertical')
                my_scrollbar.pack(side='right', fill='y')
                my_xscrollbar = ttk.Scrollbar(my_frame, orient='horizontal')
                my_xscrollbar.pack(side='bottom',fill='x')
                global my_tree
                my_tree = tkinter.ttk.Treeview(my_frame, yscrollcommand=my_scrollbar.set,xscrollcommand=my_xscrollbar.set)
                my_scrollbar.config(command=my_tree.yview)
                my_xscrollbar.config(command=my_tree.xview)

                #creates initial tree with 'all data'
                my_tree['column'] = list(df.columns)
                my_tree['show'] = 'headings'
                for column in my_tree['column']:
                    my_tree.heading(column, text=column)


                df_rows = df.to_numpy().tolist()
                for row in df_rows:
                    my_tree.insert('', 'end', values=row)

                #Filters code
                #Price filter
                price_range_var = tkinter.StringVar(window)
                price_range_var.set('Price Range')
                price_range = [
                    '0 - 25k',
                    '25k - 50k',
                    '50k - 75k',
                    '75k - 100k',
                    '100k - 125k',
                    '125k - 150k',
                    '150k - 175k',
                    '175k - 200k',
                    'Any'
                ]
                price_range_tab = OptionMenu(window, price_range_var, *price_range)


                #location filter-entry
                location_entry = Entry(window, width=15)
                location_entry.insert(0,'Location')

                #model filter
                models = [
                    'SEDAN',
                    'CABRIOLET',
                    'COUPE',
                    'WAGON',
                    'SUV',
                    'AMG',
                    'MAYBACH',
                    'ROADSTER',
                    'Any'
                ]
                model_var = tkinter.StringVar(window)
                model_var.set('Model Type')
                model_tab = OptionMenu(window, model_var, *models)

                #style - color filters
                interior_var = tkinter.StringVar(window)
                exterior_var = tkinter.StringVar(window)
                interior_var.set('Colors-Interior')
                exterior_var.set('Colors-Exterior')
                interior_colors = [
                    'Red',
                    'Black',
                    'Beige',
                    'Any'
                ]
                exterior_colors = [
                    'Polar_White',
                    'Night_Black',
                    'Denim_Blue',
                    'Red_Metallic',
                    'Any'
                ]
                interior_style = OptionMenu(window, interior_var, *interior_colors)
                exterior_style = OptionMenu(window, exterior_var, *exterior_colors)

                #condition filters
                condition = [
                    'New',
                    'Used',
                    'Any'
                ]
                condition_var = tkinter.StringVar(window)
                condition_var.set('Car Condition')
                condition_tab = OptionMenu(window, condition_var, *condition)

                #apply filter button
                apply = Button(window, text='Apply Filters',
                                command= lambda: 
                                apply_filters(
                                df,
                                model_var.get(), exterior_var.get(),
                                interior_var.get(), price_range_var.get(), 
                                condition_var.get(), location_entry.get()
                                ))

                #pushing widgets to window
                filler_label = Label(window,text='---------')
                filler2_label= Label(window,text='---------')
                filler3_label= Label(window,text='---------')
                filler4_label= Label(window,text='---------')
                filler5_label= Label(window,text='---------')
                filler6_label= Label(window,text='---------')
                model_tab.pack(side=LEFT, anchor=tkinter.S)
                filler3_label.pack(side=LEFT, anchor=tkinter.S)
                exterior_style.pack(side=LEFT,anchor=tkinter.S)
                filler2_label.pack(side=LEFT, anchor=tkinter.S)
                interior_style.pack(side=LEFT, anchor=tkinter.S)
                filler_label.pack(side=LEFT, anchor=tkinter.S)
                price_range_tab.pack(side=LEFT, anchor=tkinter.S)
                filler4_label.pack(side=LEFT, anchor=tkinter.S)
                condition_tab.pack(side=LEFT, anchor=tkinter.S)
                filler5_label.pack(side=LEFT, anchor=tkinter.S)
                location_entry.pack(side=LEFT, anchor=tkinter.S)
                filler6_label.pack(side=LEFT, anchor=tkinter.S)
                apply.pack(side=LEFT,anchor=tkinter.S)
                my_tree.pack(fill=tkinter.BOTH, expand=True)

                window.mainloop()
                
                
            #Jaelin
            def graphbutt(self):
                #newwindow = Toplevel(root)
                #newwindow.geometry("400x300")
                #Label(newwindow, text="Graphs go here").pack()
                import matplotlib.pyplot as plt 
                import numpy as np
                x = np.arange(1, 25)

                labels = 'a class sedan', 'c class cabriolet', 'c class coupe', 'c class sedan', 'cla coupe', 'cls coupe', 'e class cabriolet', 'e class coupe', 'e class sedan', 'e class wagon', 'eqb suv', 'eqs sedan', 'eqs suv', 'g class suv', 'gla suv', 'glb suv', 'glc coupe', 'glc suv', 'gle coupe', 'gle suv', 'gls suv', 'mercedes amg gt', 'mercedes amg gt 4 door coupe', 'mercedes maybach s class', 's class sedan', 'sl roadster'
                sizes = [48, 72, 72, 48, 96, 24, 72, 72, 96, 24, 48, 72, 72, 48, 96, 72, 24, 96, 48, 144, 72, 120, 48, 48, 48, 48]
                colors = ['dimgrey', 'darkgrey', 'papayawhip', 'aquamarine', 'ivory', 'khaki', 'gray', 'thistle', 'lightcyan', 'cadetblue', 'lightblue','powderblue', 'lavenderblush', 'royalblue', 'lavender', 'lightsteelblue', 'skyblue', 'teal', 'paleturquoise', 'mistyrose', 'palegoldenrod', 'hotpink', 'darkslategray', 'honeydew', 'darkcyan', 'seashell']

                fig, plot1 = plt.subplots()
                plot1.axis('equal')
                plot1.set_title('Number of Models Per Class')
                plot1.pie(sizes, labels=labels, colors=colors)
                

                fig, plot2 = plt.subplots()

                xdata=['Sedan', 'Cabriolet', 'Coupe', 'Wagon', 'SUV', 'GT', '4DGT', 'Roadster']
                ydata= [73980, 69557, 67721, 68400, 66680, 159440, 97550, 157750]

                plot2.set_title('Price Per [car] model')
                plot2.bar(xdata,ydata)

                labels2 = 'Plant', 'Store'
                sizes2 = [307, 1349]
                colors2 = ['powderblue', 'slategray']

                fig, plot3 = plt.subplots()

                plot3.axis('equal')
                plot3.set_title('Store v Plant (location)')
                plot3.pie(sizes2, labels=labels2, colors=colors2)

                plt.show()


            def modbutt(self):
                import tkinter as tk

                new = tk.Tk()
                new.title('User Modification')
                new.geometry('350x300')

                class smolbuttons:
                    def __init__(self, master):
                        frame = Frame(master)
                        frame.pack()

                        self.passButton = Button(frame, text="Change Password", command=self.passbutt)
                        self.passButton.pack()

                        self.userButton = Button(frame, text="Add new User", command=self.userbutt)
                        self.userButton.pack()

                    def passbutt(self):
                        import tkinter as tk
                        from functools import partial
                        from tkinter import ttk


                        neww = Tk()
                        neww.title('Change Password')
                        neww.geometry('350x300')

                        def apply(text, textt):
                            print("Username:", text.get())
                            print("Password:", textt.get())

                        userlabel = Label(neww, text="Username").pack()
                        text = tk.StringVar()
                        userentry = ttk.Entry(neww, textvariable=text).pack()

                        passlabel = Label(neww,text="New Password").pack()
                        textt = tk.StringVar()
                        passentry = ttk.Entry(neww,textvariable=textt).pack()

                        apply = partial(apply, text, textt)

                        applyButton = ttk.Button(neww, text="Apply", command=apply).pack()




                    def userbutt(self):
                        import tkinter as tk
                        from functools import partial
                        from tkinter import ttk

                        newww = Tk()
                        newww.title('Change Password')
                        newww.geometry('350x300')

                        def appply(text, textt):
                            print("Username:", ttext.get())
                            print("Password:", ttextt.get())

                        userlabel = Label(newww, text="New Username").pack()
                        ttext = tk.StringVar()
                        userentry = ttk.Entry(newww, textvariable=ttext).pack()

                        passlabel = Label(newww, text="New Password").pack()
                        ttextt = tk.StringVar()
                        passentry = ttk.Entry(newww, textvariable=ttextt).pack()

                        appply = partial(appply, ttext, ttextt)

                        applyButton = ttk.Button(newww, text="Apply", command=appply).pack()

                z = smolbuttons(new)
                new.mainloop()

        b = buttons(root)
        root.mainloop()
    else:
        incorrectLabel = Label(tkWindow, text="Incorrect Username or Password").grid(row=8, column=1)


tkWindow = Tk()
tkWindow.geometry('400x300')
tkWindow.title('Sprout User Login')

usernameLabel = Label(tkWindow, text="Username").grid(row=0, column=0)
username = StringVar()
usernameEntry = Entry(tkWindow, textvariable=username).grid(row=0, column=1)

passwordLabel = Label(tkWindow, text="Password").grid(row=1, column=0)
password = StringVar()
passwordEntry = Entry(tkWindow, textvariable=password, show='*').grid(row=1, column=1)

login_info = partial(login_info, username, password)

loginButton = Button(tkWindow, text="Login", command=login_info).grid(row=4, column=0)

incorrectLabel = Label(tkWindow, text="").grid(row=8, column=1)

tkWindow.mainloop()