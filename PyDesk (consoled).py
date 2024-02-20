from tkinter import *
from tkinter.filedialog import askopenfilename
import os, subprocess, time, sys
from threading import Thread
from DeskDefault import *
try:
    from DeskData import *
except:
    pass

def check_pydesk(user):
    ''' Allows a User to Enter his Desk by providing Password Entry '''
    global user_now, username
    def pass_check(pwd_entry):
        ''' Checks Entered Details to let a User in '''
        global user_now, username
        if pwd_entry == globals()[user].password:
            user_now = globals()[user]
            username.set(user)
            print('ok')

    if globals()[user].password == '':
        pass_check('')
    else:            
        Label(pass_frame, text=user, bg='orange', font=("Arial",12)).grid(row=0,column=0, columnspan=3, sticky=N+S+E+W)
        Label(pass_frame, text="Enter Password: ", bg='orange', font=("Arial",12)).grid(row=1,column=0, sticky=N+S+E+W)
        pwd = Entry(pass_frame, width=40, show='*', font=("Arial",24))
        pwd.grid(row=1, column=1, sticky=N+S+E+W)
        Button(pass_frame, text='Submit', command=lambda: pass_check(pwd.get()), bg='RoyalBlue3').grid(row=1,column=2, sticky=N+S)
        
def save_to_DeskData():
    ''' Saves all information of all Users (except Guest) to DeskData file '''
    global users
    try:
        globals()[username] = user_now
    except:
        pass  
    cur_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(cur_path)
    savestr = f'from DeskDefault import *\n\nusers = {users}\n\n'
    writefile = open('DeskData.py', 'w')
    for xyz in users[1:]:
        savestr += f"\n{xyz} = User('{globals()[xyz].password}')\n"
        savestr += f"{xyz}.my_files = {globals()[xyz].my_files}\n"
        savestr += f"{xyz}.settheme('{globals()[xyz].theme}')\n"
    writefile.write(savestr)
    writefile.flush()
    writefile.close()

def create_user(x):
    ''' Creates a New User in PyDesk '''
    global usercount, uname, users, n
    add_user = Toplevel()       # Creating Toplevel for adding user
    add_user["bg"] = 'orange'
    Label(add_user, text='Enter Username', bg='orange').grid(row=0, column=0)
    uname = Entry(add_user, width=30)
    uname.grid(row=0, column=1)
    Label(add_user, text='Enter Password', bg='orange').grid(row=1, column=0)
    npwd = Entry(add_user, width=30, show='*')
    npwd.grid(row=1, column=1)
    Label(add_user, text='Verify Password', bg='orange').grid(row=2, column=0)
    vpwd = Entry(add_user, width=30, show='*')
    vpwd.grid(row=2, column=1)
    def save_user(x):
        ''' Checks for Valid User Details and Saves them to DeskData '''
        global usercount, uname, users, n
        if (uname.get()).isalnum() and uname.get() not in users and npwd.get() == vpwd.get():
            users.append(uname.get())
            n += 1
            row, column = x//8, x%8
            uname = uname.get()
            globals()[uname] = User(npwd.get())
            but = Button(frame_buttons, text=uname, bg='RoyalBlue3', image=trans,
                padx=10, pady=10, height=round(h/4), width=round(w/11), compound='center',
                command= lambda: check_pydesk(uname))
            but.grid(row=row, column=column)
            save_to_DeskData()
            add_user.destroy()
    Button(add_user, text='Save User', command=lambda:save_user(x), bg='RoyalBlue3').grid(row=3, column=1)

def update_desk():
    ''' Makes all the required changes in the current Desk'''
    apps["bg"] = user_now.appbg
    task["bg"] = user_now.appbg
    user_now.my_files.sort()
    globals()['button_info'] = user_now.my_buttons(user_now.my_files)
    for i in range(8):
        for j in range(10):
            lname = button_info[(i,j)]['fname']
            status = button_info[(i,j)]['state']
            buttons[(i,j)].config(state=status, text=lname)
    for win in pydesk.winfo_children():
        if win.winfo_class() == 'Toplevel':
            win.destroy()
    pydesk.update()
            
def open_locn(address):
    directory = os.path.realpath(os.path.dirname(address))
    os.system(f'explorer "{directory}"')
            
def run_file(address):
    directory = os.path.dirname(address)
    workfile = os.path.basename(address)
    os.chdir(directory)
    cmd = f'"{workfile}"'
    os.system(cmd)
    
def edit_idle(address):
    directory = os.path.dirname(address)
    workfile = os.path.basename(address)
    os.chdir(directory)
    cmd = f'pythonw -m idlelib "{workfile}"'
    subprocess.run(cmd)
def run_idle(address):
    directory = os.path.dirname(address)
    workfile = os.path.basename(address)
    os.chdir(directory)
    cmd = f'pythonw -m idlelib -r "{workfile}"'
    subprocess.run(cmd)

def add_modify(info, action):
    ''' Opens a Toplevel window to Add new or Modify existing file '''
    amwin = Toplevel()      # Creating ADD/MODIFY Toplevel Window
    amwin['bg'] = user_now.appbg
    amwin.geometry("500x100")
    amwin.resizable(0,0)
    amwin.attributes("-topmost",True)
    amwin.title(['Modify File' if action=='m' else 'Add File'][0])

    Label(amwin, text = 'File Name', bg = user_now.appbg, fg = user_now.textbg).grid(row=0,column=0)
    E1 = Entry(amwin, width=40)
    E1.grid(row=0, column=1)

    Label(amwin, text = 'File Location', bg = user_now.appbg, fg = user_now.textbg).grid(row=1,column=0)
    E2 = Entry(amwin, width=40)
    E2.grid(row=1, column=1)

    deskvar = IntVar(amwin, value=1)
    add_to_desk = Checkbutton(amwin, text='Add File to Desktop', variable=deskvar,
                     onvalue=1, offvalue=0, bg=user_now.appbg, fg=user_now.textbg, selectcolor=user_now.appbg)
    add_to_desk.grid(row=3, column=0)

    if action == 'm':       # Setting default inputs for MODIFY
        try:
            name = info[0]
            address = info[1]
        except:
            name = info['fname']
            address = info['address']
        E1.insert(0, name)
        E2.insert(0, address)

    def openfile():         
        '''BROWSE file through Tkinter OPEN FILE fn'''
        myfile = askopenfilename(defaultextension=".py",
                            filetypes=[("Python files", "*.py"),
                                        ("Python no-console", ".pyw")])
        E2.delete(0, len(E2.get()))
        E2.insert(0, myfile)

    def get_empty():
        ''' Returns empty cell coordinates (if any), else None '''
        for j in range(10):
            for i in range(8):
                if button_info[(i,j)]["state"] == "disabled":
                    return((i,j))
                    break
            else:
                continue
            break
        else:
            return (None)

    def save():
        ''' Checks for Valid Entries and saves to current window and DeskData '''
        if E1.get() and os.path.isfile(E2.get()) and os.path.splitext(E2.get())[1] in ['.py','.pyw']:
            #if E2.get() not in [item[1] for item in user_now.my_files]:
            if action == 'm':
                for i in range(len(user_now.my_files)):
                    if user_now.my_files[i][1] == address:
                        if address == E2.get() or (E2.get() not in [items[1] for items in user_now.my_files]):
                            if user_now.my_files[i][2] == None and deskvar.get() == 1:
                                user_now.my_files[i] = [E1.get(), E2.get(),
                                 get_empty()]
                            else:
                                user_now.my_files[i] = [E1.get(), E2.get(),
                                 [user_now.my_files[i][2] if deskvar.get()==1 else None][0]]
                        break
            elif action == 'a' and E2.get() not in [items[1] for items in user_now.my_files]:
                if deskvar.get() == 1:
                    user_now.my_files.append([E1.get(), E2.get(), get_empty()])
                else:
                    user_now.my_files.append([E1.get(), E2.get(), None])
            else:
                pass
            
            update_desk()
            save_to_DeskData()
    Button(amwin, text='Browse..', command=openfile, bg=user_now.appbg, fg=user_now.textbg).grid(row=1,column=2)
    Button(amwin, text='SAVE', command=save, bg=user_now.appbg, fg=user_now.textbg).grid(row=4, column=1)
    Button(amwin, text='Cancel', command=amwin.destroy, bg=user_now.appbg, fg=user_now.textbg).grid(row=4, column=0)

def delete_file(address):
    def delete_it():
        for i in range(len(user_now.my_files)):
            if user_now.my_files[i][1] == address:
                user_now.my_files[i][2] = None
                break
        if del1.get():
            del user_now.my_files[i]
        if del2.get():
            pass
        update_desk()
    delwin = Toplevel()
    delwin["bg"] = user_now.appbg
    delwin.title(f"Delete File- {address}")
    Label(delwin, bg=user_now.appbg, fg=user_now.textbg, text='Delete Options:').grid(row=0)
    del1 = IntVar(delwin, value=0)
    del2 = IntVar(delwin, value=0)
    Checkbutton(delwin, text='Delete Permanently from Desk', variable=del1,
                bg=user_now.appbg, fg=user_now.textbg, selectcolor=user_now.appbg).grid(row=1,column=1)
    Checkbutton(delwin, text='Delete Source File', variable=del2,
                bg=user_now.appbg, fg=user_now.textbg, selectcolor=user_now.appbg).grid(row=2,column=1)
    
    Button(delwin, bg=user_now.appbg, fg=user_now.textbg, text='Cancel', command=delwin.destroy).grid(row=3,column=0)
    Button(delwin, bg=user_now.appbg, fg=user_now.textbg, text='Delete', command=delete_it).grid(row=3,column=2)

def create_new():
    ''' Pops up a OptionMenu for creating new file '''
    new_option = Menu(pydesk, bg=user_now.appbg, fg=user_now.textbg,borderwidth=0)
    new_option.add_command(label='New IDLE script', command=Thread(target=lambda: os.system("pythonw -m idlelib untitled")).start)
    new_option.add_command(label='New IDLE shell', command=Thread(target=lambda: os.system("pythonw -m idlelib")).start)
    new_option.add_command(label='New CMD Line shell', command=Thread(target=lambda: os.system("python")).start)
    new_option.tk_popup(500, 500)

def install_mod():
    ''' Hellps user manage Python-packages on the system'''
    def install_it():
        cmd = subprocess.run(f'pip install {E1.get()}', capture_output=True, text=True)
        print(cmd.stdout)
    def uninstall_it():
        cmd = subprocess.run(f'pip uninstall {E1.get()}')
        print(cmd.stdout)
    addmod = Toplevel()
    addmod['bg'] = user_now.appbg
    
    Label(addmod, text='Type Module Name: ', bg = user_now.appbg, fg = user_now.textbg).grid(row=0, column=0)
    E1 = Entry(addmod, width=30)
    E1.grid(row=0, column=1)
    Button(addmod, text='CANCEL', bg = user_now.appbg, fg = user_now.textbg, command=addmod.destroy).grid(row=1, column=0)
    Button(addmod, text='INSTALL', bg = user_now.appbg, fg = user_now.textbg, command=install_it).grid(row=1, column=1)
    Button(addmod, text='UNINSTALL', bg = user_now.appbg, fg = user_now.textbg, command=uninstall_it).grid(row=1, column=2)

    #################
    Label(addmod, text='#Simple INSTALL/UNINSTALL works. \n MORE COMING SOON....', bg = user_now.appbg, fg = user_now.textbg).grid(row=3, column=1,columnspan=2, rowspan=2)

def my_files_tab():
    ''' Opens a MyFiles window do manage Python Files of the User '''
    my_file_win = Toplevel()    # Creating basic Window and Frame
    my_file_win['bg'] = user_now.appbg
    my_file_win.title("My Files")
    my_file_win.resizable(0,0)
    files_frame = Frame(my_file_win, bg = user_now.appbg)
    files_frame.grid(row=0, column=0, sticky=N+S+E+W)
    row = 0
    user_now.my_files.sort()

    canvas = Canvas(files_frame, bg=user_now.appbg, height=round(0.9*h), width=round(0.9*w))
    canvas.grid(row=0, column=0, sticky=N+S+W+E)

    vsb = Scrollbar(files_frame, orient="vertical", command=canvas.yview)
    vsb.grid(row=0, column=1, sticky=N+S)
    canvas.configure(yscrollcommand=vsb.set)

    frame_1 = Frame(canvas, bg=user_now.appbg)
    canvas.create_window((0, 0), window=frame_1, anchor=N+W)

    frame_2 = Frame(my_file_win, bg=user_now.appbg)
    frame_2.grid(row=1, column=0, sticky=N+S+E+W)

    label_list = []
    cur_row = IntVar(my_file_win)
    def select_row(event, row):
        cur_row.set(row)
        for i in range(len(label_list)):
            for j in range(3):
                if i == row:
                    label_list[i][j].config(bg='blue')
                else:
                    label_list[i][j].config(bg=user_now.appbg)
        Button(frame_2, text='Run',bg=user_now.appbg, fg=user_now.textbg, command=Thread(target=lambda: 
                run_file(user_now.my_files[cur_row.get()][1])).start).grid(row=0, column=1, sticky=N+S+E+W)
        Button(frame_2, text='Edit in IDLE',bg=user_now.appbg, fg=user_now.textbg, command=Thread(target=lambda: 
                edit_idle(user_now.my_files[cur_row.get()][1])).start).grid(row=0, column=2, sticky=N+S+E+W)
        Button(frame_2, text='Run in IDLE',bg=user_now.appbg, fg=user_now.textbg, command=Thread(target=lambda: 
                run_idle(user_now.my_files[cur_row.get()][1])).start).grid(row=0, column=3, sticky=N+S+E+W)
        Button(frame_2, text='Open File Location',bg=user_now.appbg, fg=user_now.textbg, command=Thread(target=lambda: 
                open_locn(user_now.my_files[cur_row.get()][1])).start).grid(row=0, column=4, sticky=N+S+E+W)
        Button(frame_2, text='Modify',bg=user_now.appbg, fg=user_now.textbg, command=Thread  (target=lambda: 
                add_modify(user_now.my_files[cur_row.get()], 'm')).start).grid(row=0, column=5, sticky=N+S+E+W)
        Button(frame_2, text='Delete',bg=user_now.appbg, fg=user_now.textbg, command=Thread(target=lambda: delete_file(user_now.my_files[cur_row.get()][1])).start).grid(row=0, column=6, sticky=N+S+E+W)
    
    os.chdir(globals()['cur_path'])
    trans = PhotoImage(file='default.png')      # Transparent pic for size in pixels

    for x in range(len(user_now.my_files)):
        l1 = Label(frame_1, text= user_now.my_files[x][0], height=round(0.05*h), width=round(0.3*w),
            image=trans, compound='center', bg=user_now.appbg, fg=user_now.textbg, borderwidth=2, relief='groove')
        l1.grid(row=x, column=0)
        l2 = Label(frame_1, text= user_now.my_files[x][1], height=round(0.05*h), width=round(0.3*w),
            image=trans, compound='center', bg=user_now.appbg, fg=user_now.textbg, borderwidth=2, relief='groove')
        l2.grid(row=x, column=1)
        l3 = Label(frame_1, text= f'{user_now.my_files[x][2]}', height=round(0.05*h), width=round(0.3*w),
            image=trans, compound='center', bg=user_now.appbg, fg=user_now.textbg, borderwidth=2, relief='groove')
        l3.grid(row=x, column=2)
        l1.bind("<Button-1>", lambda event, row=x: select_row(event, row))
        l2.bind("<Button-1>", lambda event, row=x: select_row(event, row))
        l3.bind("<Button-1>", lambda event, row=x: select_row(event, row))
        l1.bind("<Button-3>", lambda event, row=x: select_row(event, row))
        l2.bind("<Button-3>", lambda event, row=x: select_row(event, row))
        l3.bind("<Button-3>", lambda event, row=x: select_row(event, row))

        label_list.append([l1,l2,l3])
    files_frame.update_idletasks()
    Button(frame_2, text='EXIT', bg=user_now.appbg, fg=user_now.textbg, command=my_file_win.destroy).grid(row=0, column=0, sticky=N+S+E+W)

    for x in range(7):
        frame_2.columnconfigure(x, weight=1)
    my_file_win.mainloop()        

def user_settings():
    global username
    settings = Toplevel()
    settings['bg'] = user_now.appbg
    settings.title(f'User Settings- {username}')
    settings.geometry("600x400")
    settings.resizable(0,0)

    settings.rowconfigure(0, weight=1)
    settings.rowconfigure(1, weight=1)

    sett = Frame(settings, bg = user_now.appbg)
    sett.grid(row=0, column=0, sticky=N+S+E+W)
    pwd = globals()[username].password
    Label(sett, text="Username:", bg = user_now.appbg, fg = user_now.textbg, width=20).grid(row=0, column=0)
    Label(sett, text=username, bg = user_now.appbg, fg = user_now.textbg, width=20).grid(row=0, column=1)
    Label(sett, bg = user_now.appbg).grid(row=1)
    Label(sett, text='Password:', bg = user_now.appbg, fg = user_now.textbg, width=20).grid(row=2, column=0)
    Label(sett, text='*'*len(user_now.password), bg = user_now.appbg, fg = user_now.textbg, width=20).grid(row=2, column=1)
    Label(sett, bg = user_now.appbg).grid(row=3)
    Label(sett, text='Theme:', bg = user_now.appbg, fg = user_now.textbg, width=20).grid(row=4, column=0)
    Label(sett, text=user_now.theme, bg = user_now.appbg, fg = user_now.textbg, width=20).grid(row=4, column=1)
    Label(sett, bg = user_now.appbg).grid(row=5)

    def change_username():
        def new_un():
            global username, user_now
            if uname.get().isalnum() and uname.get() not in users:
                for i in range(len(users)):
                    if users[i] == username:
                        users[i] = uname.get()
                        username = uname.get()
                        globals()[uname.get()] = user_now
                        del user_now
                        user_now = globals()[uname.get()]
                        update_desk()
                        break
        change = Frame(settings, bg = user_now.appbg)
        change.grid(row=1, column=0, sticky=N+S+E+W)
        for i in range(3):
            change.rowconfigure(i, weight=1)
            change.columnconfigure(i, weight=1)
        Label(change, text='New Username:', bg = user_now.appbg, fg = user_now.textbg).grid(row=0, column=0)
        uname = Entry(change, width=40)
        uname.grid(row=0, column=2)
        Button(change, text='SAVE', command=new_un, bg=user_now.appbg, fg=user_now.textbg).grid(row=1, column=1)
        
    def change_pwd():
        def new_pwd():
            if cpwd.get() == user_now.password and npwd.get() == vpwd.get():
                user_now.password = npwd.get()
                update_desk()
        change = Frame(settings, bg = user_now.appbg)
        change.grid(row=1, column=0, sticky=N+S+E+W)
        for i in range(4):
            change.rowconfigure(i, weight=1)
            change.columnconfigure(i, weight=1)
        Label(change, text='Current Password:', bg = user_now.appbg, fg = user_now.textbg).grid(row=0, column=0)
        Label(change, text='New Password:', bg = user_now.appbg, fg = user_now.textbg).grid(row=1, column=1)
        Label(change, text='Confirm Password:', bg = user_now.appbg, fg = user_now.textbg).grid(row=2, column=1)
        cpwd = Entry(change, width=40, show='*')
        cpwd.grid(row=0, column=1)
        npwd = Entry(change, width=40, show='*')
        npwd.grid(row=1, column=2)
        vpwd = Entry(change, width=40, show='*')
        vpwd.grid(row=2, column=2)
        Button(change, text='SAVE', command=new_pwd, bg=user_now.appbg, fg=user_now.textbg).grid(row=3, column=0)

    def change_theme():
        if user_now.theme == 'light':
            user_now.settheme('dark')
        else:
            user_now.settheme('light')
        update_desk()
    def desk_reset():
        def erase_desk():
            global username, user_now
            pwd = user_now.password
            del globals()[username]
            del user_now
            globals()[username] = User(pwd)
            user_now = globals()[username]
            update_desk()

        change = Frame(settings, bg = user_now.appbg)
        change.grid(row=1, column=0, sticky=N+S+E+W)
        change.columnconfigure(0, weight=2)
        change.columnconfigure(0, weight=1)
        Label(change, text= 'This action will reset the desk\n for this user. Are you sure ??', bg=user_now.appbg, fg=user_now.textbg).grid(row=0, column=0, sticky=N+S+E+W)
        Button(change, text='Yes',bg=user_now.appbg, fg=user_now.textbg, command=erase_desk).grid(row=0, column=1, sticky=N+S+E+W)

    Button(sett, text='CHANGE', command=change_username, bg=user_now.appbg, fg=user_now.textbg).grid(row=0, column=2)
    Button(sett, text='CHANGE', command=change_pwd, bg=user_now.appbg, fg=user_now.textbg).grid(row=2, column=2)
    Button(sett, text='SWITCH THEME', command=change_theme, bg=user_now.appbg, fg=user_now.textbg).grid(row=4, column=2)
    Button(sett, text='RESET MY DESK', command=desk_reset, bg=user_now.appbg, fg=user_now.textbg).grid(row=6, column=1)


def leftclick(event):
    ''' On Double-Click recognizes the file and gives run command '''
    cordx = event.x_root
    cordy = event.y_root
    y, x = Grid.location(apps, cordx, cordy)

    try:
        pydesk.update()
        if (button_info[(x, y)]['state']) == 'active':
            Thread(target= lambda: run_file(button_info[(x,y)]['address'])).start()
    except KeyError as e:
        pass
    
def rightclick(event):
    ''' On Right-Mouse-Click recognizes the file and pops up OptionMenu
    for performing actions on the file '''
    global x, y
    cordx = event.x_root
    cordy = event.y_root
    y, x = Grid.location(apps, cordx, cordy)

    try:
        if (button_info[(x, y)]['state']) == 'active':
            name = button_info[(x, y)]['fname']
            if len(name) > 15:
                hl = f'{name[:15]}....'
            else:
                hl = name
                    # OptionMenu -- Run, Edit, Run in IDLE, Modify, Delete
            options = Menu(apps, tearoff=0, bg=user_now.appbg, fg=user_now.textbg)
            options.add_command(label=hl)
            options.add_separator()
            options.add_command(label='Run', command=Thread(target=lambda: run_file(button_info[(x,y)]['address'])).start)
            options.add_command(label='Edit in IDLE', command=Thread(target= lambda: edit_idle(button_info[(x,y)]['address'])).start)
            options.add_command(label='Run in IDLE', command=Thread(target=lambda: run_idle(button_info[(x,y)]['address'])).start)
            options.add_command(label='Modify', command=Thread(target=lambda: add_modify(button_info[(x,y)], 'm')).start)
            options.add_command(label='Delete', command=Thread(target=lambda: delete_file(button_info[(x,y)]['address'])).start)
            pydesk.update()
            options.tk_popup(cordx, cordy)
    except KeyError:
        pass



# Main Tkinter Desktop Window
pydesk = Tk()
pydesk.configure(background='orange')
pydesk.attributes('-fullscreen', True)
pydesk.title('Mini Python Desktop - PyDesk')
pydesk.update()

cur_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(cur_path)  # Opening path in cmd line
h, w = pydesk.winfo_height(), pydesk.winfo_width() # Height-Width of main window  

can_1 = Canvas(pydesk, width=w, height=h, bg="orange")
can_1.grid()
img_1 = PhotoImage(file="intro.png")
img_can = can_1.create_image(round(w/2), 0, image=img_1)
pady = 0
while pady<=round(h/2):
    can_1.move(img_can, 0, +10)
    time.sleep(0.05)
    pady += 10
    pydesk.update()
can_1.destroy()

username = StringVar(pydesk)
trans = PhotoImage(file='default.png')      # Transparent pic for size in pixels

    # Frames in login window -- Admin, other users and password entry
admin_frame = Frame(pydesk, bg='orange')
admin_frame.grid(row=0, column=0, sticky=N+S+W+E)

user_frame = Frame(pydesk, bg='orange')
user_frame.grid(row=1, column=0, sticky=N+S+W+E)
user_frame.grid_propagate(False)

pass_frame = Frame(pydesk, bg='orange')
pass_frame.grid(row=2, column=0, sticky=N+S+W+E)

                            ## USER FRAME ##
canvas = Canvas(user_frame, bg="orange", width=round(0.99*w))
canvas.grid(row=0, column=0, sticky=N+S+W+E)

vsb = Scrollbar(user_frame, orient="vertical", command=canvas.yview)
vsb.grid(row=0, column=1, sticky=N+S)
canvas.configure(yscrollcommand=vsb.set)

frame_buttons = Frame(canvas, bg="RoyalBlue3")
canvas.create_window((0, 0), window=frame_buttons, anchor=N+W)

n = 0
for user in users[2:]:
    row, column = n//8, n%8
    frame_buttons.rowconfigure(row, weight=1)
    frame_buttons.columnconfigure(column, weight=1)
    but = Button(frame_buttons, text=user, bg='RoyalBlue3', image=trans,
        padx=10, pady=10, height=round(h/4), width=round(w/11), compound='center',
        command= lambda: check_pydesk(user), font=("Arial",12))
    but.grid(row=row, column=column)
    n += 1
n -= 1
frame_buttons.update_idletasks()
user_frame.config(width=w, height=round(h/4))
canvas.config(scrollregion=canvas.bbox("all"))

                              ## ADMIN FRAME ##
adminbut = Button(admin_frame, text=users[1], image=trans, compound='center', bg='RoyalBlue3', font=("Arial",12),
                  height=round(h/4), width=round(w/3), command= lambda: check_pydesk(users[1]))
adminbut.grid(row=0, column=0, rowspan=3)

new_user = Button(admin_frame, text='Create User', image=trans, compound='center', bg='RoyalBlue3',
                  height=round(h/12), width=round(w/3), command= lambda: create_user(n+1), font=("Arial",12))
new_user.grid(row=0, column=1)

guest = Button(admin_frame, text='Guest', image=trans, compound='center', bg='RoyalBlue3', font=("Arial",12),
                  height=round(h/12), width=round(w/3), command= lambda: check_pydesk('Guest'))
guest.grid(row=1, column=1)

bye = Button(admin_frame, text='Exit', image=trans, compound='center', bg='RoyalBlue3', font=("Arial",12),
                  height=round(h/12), width=round(w/3), command= pydesk.destroy)
bye.grid(row=2, column=1)

                            ## PASS FRAME ##
pass_frame = Frame(pydesk, bg='orange')
pass_frame.grid(row=2, column=0, sticky=N+S+W+E)

pydesk.columnconfigure(0, weight=1)
user_frame.rowconfigure(0, weight=1)
for i in range(3):                          # Expanding rows and columns equally
    pydesk.rowconfigure(i, weight=1)
    admin_frame.rowconfigure(i, weight=1)
    pass_frame.columnconfigure(i, weight=1)
    pass_frame.rowconfigure(i, weight=1)
for i in range(2):
    admin_frame.columnconfigure(i, weight=1)
    user_frame.columnconfigure(i, weight=1)
    
        # Waiting for a user to join
pydesk.wait_variable(username)
username = username.get()
for child in pydesk.winfo_children():
    child.destroy()

pydesk.update()

        # BUILDING UP "USER DESK AREA"
pydesk.rowconfigure(0, weight=1)
pydesk.rowconfigure(1, weight=1)
pydesk.columnconfigure(0, weight=1)
apps = Frame(pydesk, bg=user_now.appbg)
apps.grid(row=0, sticky=N+W+S+E)

task = Frame(pydesk, bg=user_now.appbg)
task.grid(row=1, sticky=N+W+S+E)

            ## APPS FRAME ##
buttons = {}     # To store app buttons with key (row, column)
button_info = user_now.my_buttons(user_now.my_files)
trans = PhotoImage(file='default.png')

for i in range(8):
    apps.rowconfigure(i, weight=1)
    for j in range(10):
        apps.columnconfigure(j, weight=1)
        lname = button_info[(i,j)]['fname']
        status = button_info[(i,j)]['state']
        but = Button(apps, image=trans, text=lname, activebackground='RoyalBlue3',
                    height=round((9/11)*h/8), width=round((9/10)*w/10),
                    compound="center", bg='RoyalBlue3', state=status, wraplength=round((9/10)*w/10))
        but.grid(row=i, column=j)
        but.bind("<Double-Button-1>", leftclick)
        but.bind("<Button-3>", rightclick)
        buttons[(i,j)] = but

            ## TASK FRAME ##
labels = [['Exit', pydesk.destroy],['Add File',lambda: add_modify(None, 'a')],['Create New', create_new],
        ['My Files', my_files_tab],['Manage Modules', install_mod],
        ['Settings', user_settings],[''],[''],[''],['']]
for j in range(6):
    task.columnconfigure(j, weight=1)
    but = Button(task, text=labels[j][0],image=trans, bg='orange', compound='center',
                width=round(9*w/100), height=round(h/20),command=labels[j][1])
    but.grid(row=0, column=j, sticky=N)
pydesk.update()

pydesk.mainloop()
    # On Final Exit - Saving all the Changes

save_to_DeskData()