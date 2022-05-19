################################################
##################  Front End   ################
################################################
from sqlite3 import *
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.ttk import *
from backEnd import *

root = Tk()
root.geometry("1500x600+10+10")
root.resizable(False, False)
root.configure(bg="#e6e6e6")
root.title("Safran Seat USA - DV Engineering")
root.iconbitmap("Safran.ico")

# Dictionary is not ordered, so we need to make it an ordered one.
version = [
    "beta 1.01", "\nThe CRUD keys are active.\nThe part titles : in progress.\nAdding material curves : in progress, needs plot package.\nVersion feature : in progress, needs OrderedDict package.\nOutputs/Errors /Warnings :  planned for future.\nFileter feature : planned for future.",
    "beta 1.02", "\nManaging part title in progress.\nRemoved the property explanation from titles.\nAdding material curves : in progress, needs plot package.\nVersion feature : in progress, needs OrderedDict package.\nOutputs/Errors /Warnings :  planned for future.\nFilter feature : planned for future.",
    "beta 1.03", "\nUpdated to work on part titles only.\nRemoved the property explanation from titles.\npart_db version in progress.\nAdding material curves : in progress, needs plot package.\nVersion feature : in progress, needs OrderedDict package.\nOutputs/Errors /Warnings :  planned for future.\nFilter feature : planned for future.",
    "beta 1.04", "\nAdded database-resources.\nRemoved the property explanation from titles.\nVersion feature is complete.\nAdding material curves : in progress, needs plot package.\nOutputs/Errors /Warnings :  planned for future.\nFilter feature : planned for future.",
    "beta 1.05", "\nAdded Seat query section.\nAdded database-resources.\nRemoved the property explanation from titles.\nVersion feature is complete.\nAdding material curves : in progress, needs plot package.\nOutputs/Errors /Warnings :  planned for future.\nFilter feature : planned for future.\nMake executable version with limited functionality.",
    "beta 1.06", "\nAdded number of materials used\nAdded Seat query section.\nAdded database-resources.\nRemoved the property explanation from titles.\nVersion feature is complete.\nAdding material curves : in progress, needs plot package.\nOutputs/Errors /Warnings :  planned for future.\nFilter feature : planned for future.\nMake executable version with limited functionality.",
    "beta 1.07", "\nFunction processing is started\nAdded number of materials used\nAdded Seat query section.\nAdded database-resources.\nRemoved the property explanation from titles.\nVersion feature is complete.\nOutputs/Errors /Warnings :  planned for future.\nFilter feature : planned for future.\nMake executable version with limited functionality.",
    "beta 1.08", "\nAdding function ID in progress\nFunction processing is started\nAdded number of materials used\nAdded Seat query section.\nAdded database-resources.\nRemoved the property explanation from titles.\nVersion feature is complete.\nOutputs/Errors /Warnings :  planned for future.\nFilter feature : planned for future.\nMake executable version with limited functionality.",
    "beta 1.09", "\nViquar proposal to reduce the title of the part to first \nPlanned for Outputs/Errors/Warnings\nPlanned for Filters."
]

app_version = version[-2]
version_description = version[-1]


def plotCurve(event):
    selected = dbTree.focus()
    # returns the values associated with ID
    values = dbTree.item(selected, 'values')
    plt.close()
    key = values[6]
    curve = ""
    x = []
    y = []

    curve = function[key]

    for i in range(len(curve)):
        if i % 2 == 0:
            x.append(curve[i])
        else:
            y.append(curve[i])

    print(f"{key}")
    print(f"{x}")
    print(f"{y}")

    plt.gcf().canvas.set_window_title('Curve Plot')
    # canvas.set_window_title('Test')
    # pylab.gfc().canvas.manager.set_window_title('Title Test')
    plt.xlabel("True Strain in/in")
    plt.ylabel("True Stress psi")
    plt.title(f"Function {values[6]}")
    plt.plot(x, y, color='lightblue',
             linestyle='solid', marker='o',
             markerfacecolor='blue', markersize=5)
    plt.show()


########################################
################ dbLoad ################
########################################
def dbLoad(dbTree):

    partAlias = []
    partTitle = []
    partMatID = []

    matID = []
    law = []
    matTitle = []
    functionID = []

    connection = sqlite3.connect('part_1p01.db')
    cursor = connection.cursor()

    cursor.execute('SELECT rowid, partAlias, partTitle, partMatID FROM part')
    all_in_part = cursor.fetchall()

    # Considering the first column in sqlite3 is index
    for i in all_in_part:
        partAlias.append(i[0])
        partTitle.append(i[1])
        partMatID.append(i[2])

    cursor.execute(
        'SELECT rowid, matID, law, matTitle, functionID FROM Mat_PLAS_TAB')
    all_in_mat = cursor.fetchall()

    for j in all_in_mat:
        matID.append(j[1])
        law.append(j[2])
        matTitle.append(j[3])
        functionID.append(j[4])

    count = 1
    result = cursor.execute(''' 
        SELECT part.partAlias, part.partTitle, Mat_PLAS_TAB.matTitle, part.partMatID, Mat_PLAS_TAB.law, Mat_PLAS_TAB.functionID
        FROM part
        INNER JOIN Mat_PLAS_TAB ON part.partMatID = Mat_PLAS_TAB.matID
        INNER JOIN MAT_function ON Mat_PLAS_TAB.functionID = MAT_function.functionID
    ''')

    for row in result:

        if count % 2 == 0:
            dbTree.insert(parent='', index='end', iid=count, text="", values=(
                count, row[0], row[1], row[2], row[3], row[4], row[5]), tags=('oddrow', ))
        else:
            dbTree.insert(parent='', index='end', iid=count, text="", values=(
                count, row[0], row[1], row[2], row[3], row[4], row[5]), tags=('evenrow', ))
        count += 1
# end means the row will be added to the bottom of database
    # dbTree.bind("<<TreeviewSelect>>", plot_by_double)
    dbTree.bind('<Double-1>', plotCurve)


def help():
    version_label.config(
        text=version[-1] + "\n\nThis is a Beta version app and for testing only.\nPlease contact Shreyas Krishna\nor Fardin Shokoohi to get help or share issues.")


seatFile = "Seat"
seatPartLength = "0"
seatMaterialLength = "0"
seatVoidLength = "0"
seatJointLength = "0"

matFile = "MAT_DB_LSDYNA_TO_RADIOSS_FORMAT_v008.inc"
SMFile = "SM-S01_v03-Database.inc"


def seatQuery():

    global seatFile
    global seatPartLength
    global seatMaterialLength
    global seatVoidLength
    global seatJointLength

    inFile = open_file()
    n = 0
    VOID = 100  # assuming void material id = 100

    part_list = []
    material_list = []
    void_list = []
    joint_list = []

    with open(inFile, "r") as seatFile:
        for line in seatFile:
            line = line.strip("\n")
            if line[0:6] == "/PART/":
                n = 1
                continue

            if n == 1:
                partTitle = line
                part_list.append(partTitle)
                n = 2
                continue

            if n == 2:
                n = 0
                partMaterial = line.split()[1]
                material_list.append(partMaterial)
                if int(partMaterial) == 100:
                    void_list.append(partMaterial)
                if int(partMaterial) == 0:
                    joint_list.append(partMaterial)

    materialSet = set(material_list)

    seatFile = inFile.split("/")[-1]
    seatFile = seatFile[:-9]
    seatPartLength = len(part_list)
    seatMaterialLength = len(materialSet)
    seatVoidLength = len(void_list)
    seatJointLength = len(joint_list)

    print("Seat breakdown : {}".format(seatFile))
    print("@100 Number of parts in seat = {}".format(seatPartLength))
    print("@100 Number of joints in seat = {}".format(seatJointLength))
    print("@100 Number of different materials used in seat = {}".format(seatMaterialLength))
    print("@100 Number of parts with void material id 100 = {}".format(seatVoidLength))
    print("@100 seat_report : complete")

    seatFrame.config(text=seatFile)
    seat_part_label.config(
        text="\nNumber of parts = {:>4}".format(seatPartLength))

    seat_joint_label.config(
        text="Number of joints = {:>4}".format(seatJointLength))
    seat_void_label.config(
        text="Number of parts with void material = {:>4}".format(seatVoidLength))
    seat_material_label.config(
        text="Number of different materials used = {:>4}".format(seatMaterialLength))


# =====================================Add Filter =================================================
def filterTitle(*args):
    title_updated.set(title_var.get())
    x = title_updated.get()
    # Treeview.get_children() returns a list of items in Treeview.
    for child in dbTree.get_children():
        dbTree.delete(child)

    dbQuery(dbTree, oddTag, evenTag, x)


# =====================================Material Description Column=============================
dbManager = DatabaseManager()
dbManager.dbExistence()

partLength, SMLength, SMfunctionLength, matLength, matFunctionLength = databaseLengthQuery()
if SMLength == 0 or SMLength == None:
    writeDatabase = True
    Law70_parse(matFile)
    Law70_parse(SMFile)
    PLAS_TAB_parse(matFile)
    PLAS_TAB_parse(SMFile)
    PLAS_JOHNS_parse(matFile)
    PLAS_JOHNS_parse(SMFile)
    VOID_parse(matFile)
    VOID_parse(SMFile)
    FABRI_parse(matFile)
    FABRI_parse(SMFile)
    HONEYCOMB_parse(matFile)
    HONEYCOMB_parse(SMFile)

    function = matFunctionParse(writeDatabase)
    SMfunction = SMfunctionParse(writeDatabase)
    function |= SMfunction

    partLength, SMLength, SMfunctionLength, matLength, matFunctionLength = databaseLengthQuery()

else:
    writeDatabase = False
    function = matFunctionParse(writeDatabase)
    function1 = SMfunctionParse(writeDatabase)
    function |= function1

column = ["ID", "Part Alias", "Part Title",
          "Mat Title", "Mat ID", "Mat Law", "Function ID"]
alias_var = StringVar()
title_var = StringVar()
title_updated = StringVar()

# =====================================STYLE=======================================================
style = ttk.Style()
style.theme_use("default")

style.configure("Treeview",
                background="#e6e6e6",
                foreground="BLACK",
                rowheight=25,
                fieldbackground="e6e6e6"
                )
style.map("Treeview",
          background=[('selected', '#007f99')])

# =====================================CRUD functions======================================================


def update():

    partAlias = []
    partTitle = []
    partMatID = []
    des = ""
    global num
    num = int(partLength) + 1

    connection = sqlite3.connect('part_1p01.db')
    cursor = connection.cursor()

    cursor.execute("SELECT partAlias, partTitle, partMatID FROM part")
    rows = cursor.fetchall()

    for row in rows:
        partAlias.append(row[0])
        partTitle.append(row[1])
        partMatID.append(row[2])

    # print(f"@ 293 partMatID = {partMatID}")
    selected = dbTree.focus()                   # focus returns the selected record ID
    # returns the values associated with ID
    values = dbTree.item(selected, 'values')
    # print(f"values[0] = {values[0]}")
    # print(f"values[1] = {values[1]}")
    # print(f"values[2] = {values[2]}")
    # print(f"values[3] = {values[3]}")

    rowID = values[0]
    ali = alias_entry.get()
    tit = title_entry.get()
    mat = int(materialID_entry.get())
    print(f"@307 mat = {mat}, type = {type(mat)}")
    print(f"@ 308 partMatID = {partMatID}, type(partMatID) = {type(partMatID)}")
    print("\n\n")

    if mat in partMatID:
        materialID_index = partMatID.index(mat)
        des = partTitle[materialID_index]
        cursor.execute(
            "UPDATE part SET partAlias = ?, partTitle = ?, partMatID = ? WHERE oid = ?", (ali, tit, des, rowID))
        print(f"@313 Database is updated for : {mat, tit}")
    else:
        messagebox.showerror('error', 'Wrong Material ID, No Change')
        ali = values[1]
        tit = values[2]
        des = values[3]
        mat = values[4]
        # law = values[5]

    connection.commit()
    connection.close()

    # save new data
    # dbTree.item(selected, text="", values=(rowID, ali, tit, des, mat))

    # Clear entry boxes
    alias_entry.delete(0, END)
    title_entry.delete(0, END)
    materialID_entry.delete(0, END)



def select():
    # Clear entry boxes
    alias_entry.delete(0, END)
    title_entry.delete(0, END)
    materialID_entry.delete(0, END)

    selected = dbTree.focus()                   # focus returns the selected record ID
    # returns the values associated with ID
    values = dbTree.item(selected, 'values')

    alias_entry.insert(0, values[1])            # values[1] = title_entry
    title_entry.insert(0, values[2])            # values[1] = title_entry
    materialID_entry.insert(0, values[4])       # values[2] = materialID_entry


def add():

    partAlias = []
    partTitle = []
    partMatID = []
    des = ""
    global num

    num = int(partLength) + 1
    ali = alias_entry.get()
    tit = title_entry.get()
    mat = int(materialID_entry.get())

    connection = sqlite3.connect('part_1p01.db')
    cursor = connection.cursor()
    cursor.execute("SELECT partAlias, partTitle, partMatID FROM part")
    rows = cursor.fetchall()

    for row in rows:
        partAlias.append(row[0])
        partTitle.append(row[1])
        partMatID.append(row[2])

    if mat in partMatID:
        materialID_index = partMatID.index(mat)
        des = partTitle[materialID_index]

        cursor.execute("INSERT INTO part VALUES (:partAlias, :partTitle, :partMaterial)",
            {
                'partAlias': ali,
                'partTitle': tit,
                'partMaterial': mat,
            })
    else:
        messagebox.showerror('error', 'Wrong Material Number')

    connection.commit()
    connection.close()

    dbTree.insert(parent="", index="end", iid=num,
                  values=(num, ali, tit, des, mat))
    num += 1

    # Clear entry boxes
    alias_entry.delete(0, END)
    title_entry.delete(0, END)
    materialID_entry.delete(0, END)

    print("@385 Database is updated for : {}".format(tit))
    return


# in progress
def delete():

    selected = dbTree.focus()                   # focus returns the selected record ID

    # returns the values associated with ID
    values = dbTree.item(selected, 'values')
    print("@395 Deleted from Detabase: {}{}{}{}".format(
        values[0], values[1], values[2], values[3]))
    # values[0] is record ID/rowid

    connection = sqlite3.connect("part_1p01.db")
    cursor = connection.cursor()

    # in sqlite3 the row id is presented by oid
    cursor.execute("DELETE FROM part WHERE oid = {}".format(values[0]))
    connection.commit()
    connection.close()

    dbTree.delete(selected)
    print("@410 Database is updated for : {}".format(values[0]))

    # Clear entry boxes
    alias_entry.delete(0, END)
    title_entry.delete(0, END)
    materialID_entry.delete(0, END)

# =====================================Mouse EVENTS======================================================


def query_enter(event):
    query_button.config()
    status_label.config(
        text="Returns number of parts, assigned materials and joints in seat.")


def query_leave(event):
    query_button.config()
    status_label.config(text="")


def accuracy_enter(event):
    accuracy_button.config()
    status_label.config(
        text="Check the accuracy of a seat by comparison between the materials assigned to seat with those available in database.")


def accuracy_leave(event):
    accuracy_button.config()
    status_label.config(text="")


def reinstate_enter(event):
    reinstate_button.config()
    status_label.config(text="Assigns materials to a seat.")


def reinstate_leave(event):
    reinstate_button.config()
    status_label.config(text="")


def database_enter(event):
    database_button.config()
    status_label.config(
        text="Adds new records to database from a reliable seat model.")


def database_leave(event):
    database_button.config()
    status_label.config(text="")


def help_enter(event):
    help_button.config()
    status_label.config(
        text="This is a beta version app and for testing only.   /   Please share any comment or bug you found with Shreyas or Fardin for correction.")


def help_leave(event):
    help_button.config()
    status_label.config(text="")


def resources_enter(event):
    help_button.config()
    status_label.config(
        text="The seat used to create database listed will be listed.")


def resources_leave(event):
    help_button.config()
    status_label.config(text="")


def exit_enter(event):
    exit_button.config()
    status_label.config(text="Exits the app.")


def exit_leave(event):
    exit_button.config()
    status_label.config(text="")


def select_enter(event):
    select_button.config()
    status_label.config(text="Selects the record(s) in tree.")


def select_leave(event):
    select_button.config()
    status_label.config(text="")


def add_enter(event):
    add_button.config()
    status_label.config(text="Add new record to database.")


def add_leave(event):
    add_button.config()
    status_label.config(text="")


def update_enter(event):
    update_button.config()
    status_label.config(text="Updates the selected record.")


def update_leave(event):
    update_button.config()
    status_label.config(text="")


def delete_enter(event):
    delete_button.config()
    status_label.config(text="Deletes the selected record.")


def delete_leave(event):
    delete_button.config()
    status_label.config(text="")


# =====================================FRAMES======================================================
BigFrame = Frame(root)
BigFrame.pack(padx=4)

statusFrame = Frame(root, height=20)
statusFrame.pack(padx=4, side=BOTTOM, fill=X)

CommandFrame = Frame(BigFrame, width=150)
CommandFrame.pack(side=LEFT, padx=4)

mainFrame = LabelFrame(BigFrame, width=1000, text="Database")
mainFrame.pack(side=LEFT, padx=4, pady=4, fill=X, expand=True)

recordLabelFrame = LabelFrame(mainFrame, text="Record")
recordLabelFrame.pack(pady=8)

recordFrame = Frame(recordLabelFrame)
recordFrame.pack()

crudFrame = Frame(recordLabelFrame)
crudFrame.pack(pady=8)

filterFrame = LabelFrame(mainFrame, text="Filter")
filterFrame.pack(pady=4)

treeFrame = LabelFrame(mainFrame)
treeFrame.pack(padx=4, pady=4)

ControlFrame = LabelFrame(BigFrame, text="Control")
ControlFrame.pack(padx=4, pady=4, fill=BOTH, expand=True)

helpFrame = LabelFrame(ControlFrame, text=" MatCompass version " + app_version)
helpFrame.pack(pady=4, fill=BOTH, expand=True)

databaseFrame = LabelFrame(ControlFrame, text="Database")
databaseFrame.pack(pady=8, fill=BOTH, expand=True)

seatFrame = LabelFrame(ControlFrame, text=seatFile)
seatFrame.pack(pady=4, fill=BOTH, expand=True)

# ========================================command WIDGETS===================================================
# The command lambda does not take any arguments at all.
# A lambda can refer to variables outside it; this is called a closure.
# We call lambda function and it execute the query.
# We can pass parameters to query function now; something that was not possible without lambda function
# report_button = Button(CommandFrame, text='Seat Query', command=lambda: get(query()))
# The function after command will be called immediately after creation of the widget. We don't want that:
# We the function to be called when it is selected.
# Using lambda function in Menu for Tkinter GUI
query_button = Button(CommandFrame, width=15, text='Query',
                      command=lambda: seatQuery())
query_button.pack(pady=1)
query_button.bind("<Enter>", query_enter)
query_button.bind("<Leave>", query_leave)


accuracy_button = Button(CommandFrame, width=15,
                         text='Accuracy', command=lambda: seatAccuracy())
accuracy_button.pack(pady=1)
accuracy_button.bind("<Enter>", accuracy_enter)
accuracy_button.bind("<Leave>", accuracy_leave)

reinstate_button = Button(CommandFrame, width=15,
                          text='Reinstate', command=lambda: reinstate())
reinstate_button.pack(pady=1)
reinstate_button.bind("<Enter>", reinstate_enter)
reinstate_button.bind("<Leave>", reinstate_leave)

database_button = Button(CommandFrame, width=15,
                         text='Database', command=lambda: database())
database_button.pack(pady=1)
database_button.bind("<Enter>", database_enter)
database_button.bind("<Leave>", database_leave)

help_button = Button(CommandFrame, width=15,
                     text='Help', command=lambda: help())
help_button.pack(pady=1)
help_button.bind("<Enter>", help_enter)
help_button.bind("<Leave>", help_leave)

resources_button = Button(CommandFrame, width=15,
                          text='Resources', command=lambda: resources())
resources_button.pack(pady=1)
resources_button.bind("<Enter>", resources_enter)
resources_button.bind("<Leave>", resources_leave)

exit_button = Button(CommandFrame, width=15, text='Exit', command=root.destroy)
exit_button.pack(pady=1)
exit_button.bind("<Enter>", exit_enter)
exit_button.bind("<Leave>", exit_leave)

# ========================================help WIDGETS===================================================
status_label = Label(statusFrame, anchor=W, relief=SUNKEN)
status_label.pack(side=BOTTOM, fill=X, ipady=2)

# ========================================crud WIDGETS===================================================
alias_label = Label(recordFrame, text="Part Alias")
alias_label.grid(row=0, column=0)
alias_entry = Entry(recordFrame, width=30)
alias_entry.grid(row=1, column=0)

title_label = Label(recordFrame, text="Part Title")
title_label.grid(row=0, column=1)
title_entry = Entry(recordFrame, width=30)
title_entry.grid(row=1, column=1)

materialID_label = Label(recordFrame, text="Material ID")
materialID_label.grid(row=0, column=2)
materialID_entry = Entry(recordFrame, width=30)
materialID_entry.grid(row=1, column=2)


add_button = Button(crudFrame,  width=10, text='Add', command=lambda: add())
add_button.grid(row=1, column=0, padx=2, sticky=E)
add_button.bind("<Enter>", add_enter)
add_button.bind("<Leave>", add_leave)

delete_button = Button(crudFrame,  width=10,
                       text='Delete', command=lambda: delete())
delete_button.grid(row=1, column=1, padx=2, sticky=E)
delete_button.bind("<Enter>", delete_enter)
delete_button.bind("<Leave>", delete_leave)

select_button = Button(crudFrame,  width=10,
                       text='Select', command=lambda: select())
select_button.grid(row=1, column=2, padx=2, sticky=E)
select_button.bind("<Enter>", select_enter)
select_button.bind("<Leave>", select_leave)

update_button = Button(crudFrame,  width=10,
                       text='Update', command=lambda: update())
update_button.grid(row=1, column=3, padx=2, sticky=E)
update_button.bind("<Enter>", update_enter)
update_button.bind("<Leave>", update_leave)


# ========================================dbTree===================================================
# A new try for Treeview based on Tree.py John Elder
# Treeview scrollbar
# It is easier to attach the Treeview to a frame because we want to put a scrollbar on there
# tkk.tree.focus returns the selected item row in the Treeview. If nothing is selected then it returns an empty string (“”).
# ttk.tree.item() takes tkk.tree.focus as an argument followed by ‘value‘. This will return all the values in the selected item. These values are returned in a tuple.

scroll = Scrollbar(treeFrame)
scroll.pack(side=RIGHT, fill=Y)

dbTree = ttk.Treeview(treeFrame, yscrollcommand=scroll.set,
                      selectmode="extended", show="headings")
dbTree.pack()

scroll.config(command=dbTree.yview)

if int(partLength) > 0:
    oddTag = dbTree.tag_configure("oddrow", background="white")
    evenTag = dbTree.tag_configure("evenrow", background="lightblue")
    dbLoad(dbTree)

# Format columns
dbTree['columns'] = column
dbTree.column("ID", width=70, minwidth=40, anchor=CENTER)
dbTree.column("Part Alias", width=150, minwidth=20, anchor=W)
dbTree.column("Part Title", width=120, minwidth=80, anchor=W)
dbTree.column("Mat Title", width=380, minwidth=200, anchor=W)
dbTree.column("Mat ID", width=90, minwidth=50, anchor=CENTER)
dbTree.column("Mat Law", width=100, minwidth=60, anchor=W)
dbTree.column("Function ID", width=70, minwidth=40, anchor=W)

# add Headings
dbTree.heading("ID", text="ID", anchor=CENTER)
dbTree.heading("Part Alias", text="Part Alias", anchor=CENTER)
dbTree.heading("Part Title", text="Part Title", anchor=CENTER)
dbTree.heading("Mat Title", text="Mat Title", anchor=CENTER)
dbTree.heading("Mat ID", text="Mat ID", anchor=CENTER)
dbTree.heading("Mat Law", text="Mat Law", anchor=CENTER)
dbTree.heading("Function ID", text="Function ID", anchor=CENTER)
dbTree.pack()


partLength_label = Label(
    treeFrame, text="Number of parts in DataBase = {:>5}".format(partLength), anchor=W)
partLength_label.pack()

# ====================================Control WIDGETS===================================================
dbManager = DatabaseManager()

version_label = Label(helpFrame, text="{}".format(version_description))
version_label.pack(anchor=W)

global seat_part_label
global seat_material_label
global seat_void_label
global seat_joint_label

seat_part_label = Label(
    seatFrame, text="\nNumber of parts = {:>4}".format(seatPartLength))
seat_part_label.pack(anchor=NW)
seat_void_label = Label(
    seatFrame, text="Number of voids = {:>4}".format(seatVoidLength))
seat_void_label.pack(anchor=NW)
seat_joint_label = Label(
    seatFrame, text="Number of joints = {:>4}".format(seatJointLength))
seat_joint_label.pack(anchor=NW)
seat_material_label = Label(
    seatFrame, text="Number of different materials used = {:>4}".format(seatMaterialLength))
seat_material_label.pack(anchor=NW)

SMFile_label = Label(databaseFrame, text="\nDatabase 1 = {}".format(SMFile))
SMFile_label.pack(anchor=NW)
SM_Length_label = Label(
    databaseFrame, text="Number of materials = {:>4}".format(SMLength))
SM_Length_label.pack(anchor=NW)
# function_Length_label = Label(
#     databaseFrame, text="Number of material laws = {:>4}".format(SMlawLength))
# function_Length_label.pack(anchor=NW)
function_Length_label = Label(
    databaseFrame, text="Number of functions = {:>4}".format(SMfunctionLength))
function_Length_label.pack(anchor=NW)

matFile_label = Label(databaseFrame, text="\nDatabase 2 = {}".format(matFile))
matFile_label.pack(anchor=NW)
material_Length_label = Label(
    databaseFrame, text="Number of materials = {:>4}".format(matLength))
material_Length_label.pack(anchor=NW)
# material_Length_label = Label(
#     databaseFrame, text="Number of material laws = {:>4}".format(matLawLength))
# material_Length_label.pack(anchor=NW)
function_Length_label = Label(
    databaseFrame, text="Number of functions = {:>4}".format(matFunctionLength))
function_Length_label.pack(anchor=NW)


# ====================================Filter WIDGETS===================================================
alias_filter_label = Label(filterFrame, text="Part Alias")
alias_filter_label.grid(row=0, column=0)
alias_filter_entry = Entry(filterFrame, width=30, textvariable=alias_var)
alias_filter_entry.grid(row=1, column=0, pady=4, sticky=W)

title_filter_label = Label(filterFrame, text="Part Title")
title_filter_label.grid(row=0, column=1)
title_filter_entry = Entry(filterFrame, width=30, textvariable=title_var)
title_filter_entry.grid(row=1, column=1, pady=4, sticky=W)

material_filter_label = Label(filterFrame, text="Material ID")
material_filter_label.grid(row=0, column=2)
material_filter_entry = Entry(filterFrame, width=14)
material_filter_entry.grid(row=1, column=2, padx=2, pady=4, sticky=W)

# title_var.trace("w", filterTitle)  # w=write : every time the title_var is changed the function filterTitle will be triggerred
# x = title_filter_entry.get()

root.mainloop()
