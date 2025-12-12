import sqlite3 #used for creating database,inserting records
import csv #used for exporting records into .csv file
import tkinter as tk #used for gui
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt #used for plotting graphs

DB_NAME= "students.db" #name of the sqlite database file that will be created

def init_db(): #defines a function that initializes the database
    conn=sqlite3.connect(DB_NAME) #creates an object that connets the DB_NAME with sql database
    cur=conn.cursor() #creates an object that executes the sql queries 
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS students
        (roll_no interger primary key,
        name text not null,
        class text,
        marks_sub1 integer default 0,
        marks_sub2 integer default 0,
        marks_sub3 integer default 0,
        marks_sub4 integer default 0,
        marks_sub5 integer default 0,
        marks_sub6 integer default 0,
        total integer,
        percentage real,
        grades text)"""
    )
    conn.commit() #used to commit the changes permanently made above in the database
    conn.close() #closes the database connection to free resources

def insert_student(data): #initializes a function to insert data in the database
    conn= sqlite3.connect(DB_NAME) 
    cur=conn.cursor()
    cur.execute("""
    insert into students(roll_no,name,class,marks_sub1,marks_sub2,marks_sub3,marks_sub4,marks_sub5,marks_sub6,total,percentage,grades)
    values(?,?,?,?,?,?,?,?,?,?,?,?)
    """,data)
    conn.commit()
    conn.close()

def update_student_db(data): #a function to upadate records of a specific roll no.
    conn=sqlite3.connect(DB_NAME)
    cur=conn.cursor()
    cur.execute("""
    UPDATE students
    SET name=?, class=?, marks_sub1=?, marks_sub2=?, marks_sub3=?, marks_sub4=?, marks_sub5=?, marks_sub6=?, total=?, percentage=?, grades=?
    WHERE roll_no=?
    """, data)
    conn.commit()
    conn.close()

def delete_student_db(roll_no): #function to delete record for a particular roll no.
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE roll_no=?", (roll_no,))
    conn.commit()
    conn.close()

def fetch_student(roll_no): #function to extract data stored for a particular roll no.
    conn= sqlite3.connect(DB_NAME)
    cur=conn.cursor()
    cur.execute("select * from students where roll_no=?",(roll_no,))
    row=cur.fetchone()
    conn.close()
    return row

def fetch_all_students():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM students ORDER BY roll_no")
    rows = cur.fetchall()
    conn.close()
    return rows

def calculate_result(marks):
    total=sum(marks)
    #assuming each subject is out of 100=> max total=600
    percentage=(total/600)*100
    #grade logic 
    if percentage>=90:
        grade="A+"
    elif percentage>=80:
        grade="A"
    elif percentage>=70:
        grade="B+"
    elif percentage>=60:
        grade="B"
    elif percentage>=50:
        grade="C"
    else:
        grade="F"
    return total, round(percentage,2),grade

#GUI Application

class StudentRMSapp:
    def __init__(self,root):
        self.root=root
        root.title("Student Result Mangement System")
        root.geometry("950x600")
        root.resizable(False,False)
        #Variable
        self.var_roll=tk.StringVar()
        self.var_name=tk.StringVar()
        self.var_class=tk.StringVar()
        self.var_m1=tk.StringVar()
        self.var_m2=tk.StringVar()
        self.var_m3=tk.StringVar()
        self.var_m4=tk.StringVar()
        self.var_m5=tk.StringVar()
        self.var_m6=tk.StringVar()

        #Top Frame
        form_frame= ttk.LabelFrame(root,text="Student Details")
        form_frame.place(x=10,y=10,width=430,height=330)
        
        #Row 1
        ttk.Label(form_frame,text="Roll No:").grid(row=0,column=0,padx=6,pady=6,sticky="W")
        ttk.Entry(form_frame,textvariable=self.var_roll).grid(row=0,column=1,padx=6,pady=6)

        ttk.Label(form_frame, text="Name:").grid(row=0,column=2,padx=6,pady=6,sticky="W")
        ttk.Entry(form_frame, textvariable=self.var_name,width=25).grid(row=0,column=3,padx=6,pady=6)

        # Row 2
        ttk.Label(form_frame, text="Class:").grid(row=1, column=0, padx=6, pady=6, sticky="w")
        ttk.Entry(form_frame, textvariable=self.var_class).grid(row=1, column=1, padx=6, pady=6)

        # Marks
        ttk.Label(form_frame, text="Marks Sub 1:").grid(row=2, column=0, padx=6, pady=6, sticky="w")
        ttk.Entry(form_frame, textvariable=self.var_m1).grid(row=2, column=1, padx=6, pady=6)

        ttk.Label(form_frame, text="Marks Sub 2:").grid(row=2, column=2, padx=6, pady=6, sticky="w")
        ttk.Entry(form_frame, textvariable=self.var_m2).grid(row=2, column=3, padx=6, pady=6)

        ttk.Label(form_frame, text="Marks Sub 3:").grid(row=3, column=0, padx=6, pady=6, sticky="w")
        ttk.Entry(form_frame, textvariable=self.var_m3).grid(row=3, column=1, padx=6, pady=6)

        ttk.Label(form_frame, text="Marks Sub 4:").grid(row=3, column=2, padx=6, pady=6, sticky="w")
        ttk.Entry(form_frame, textvariable=self.var_m4).grid(row=3, column=3, padx=6, pady=6)

        ttk.Label(form_frame, text="Marks Sub 5:").grid(row=4, column=0, padx=6, pady=6, sticky="w")
        ttk.Entry(form_frame, textvariable=self.var_m5).grid(row=4, column=1, padx=6, pady=6)

        ttk.Label(form_frame, text="Marks Sub 6:").grid(row=4, column=2, padx=6, pady=6, sticky="w")
        ttk.Entry(form_frame, textvariable=self.var_m6).grid(row=4, column=3, padx=6, pady=6)
        
        # Creating buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=5, column=0, columnspan=4, pady=10)

        # First row
        ttk.Button(btn_frame, text="Add Student", width=15, command=self.add_student).grid(row=0, column=0, padx=4, pady=2)
        ttk.Button(btn_frame, text="Update Student", width=15, command=self.update_student).grid(row=0, column=1, padx=4, pady=2)
        ttk.Button(btn_frame, text="Delete Student", width=15, command=self.delete_student).grid(row=0, column=2, padx=4, pady=2)

        # Second row
        ttk.Button(btn_frame, text="Search", width=15, command=self.search_student).grid(row=1, column=0, padx=4, pady=2)
        ttk.Button(btn_frame, text="Clear Fields", width=15, command=self.clear_fields).grid(row=1, column=1, padx=4, pady=2)

        #Right frame having controls
        control_frame=ttk.Labelframe(root,text="Actions")
        control_frame.place(x=450,y=10,width=480,height=150)

        ttk.Button(control_frame, text="View All Students", command=self.view_all).pack(side="left", padx=10, pady=20) #.pack saves the button in a partcular direction without defining that direction
        ttk.Button(control_frame, text="Export to CSV", command=self.export_csv).pack(side="left", padx=10)
        ttk.Button(control_frame, text="Plot Grade Distribution", command=self.plot_grades).pack(side="left", padx=10)
        ttk.Button(control_frame, text="Exit", command=root.quit).pack(side="left", padx=10)

        #Table Frame
        table_frame=ttk.Frame(root)
        table_frame.place(x=10,y=350,width=920,height=230)

        columns=("roll_no","name","class","m1","m2","m3","m4","m5","m6","total","percentage","grade")
        self.tree=ttk.Treeview(table_frame,columns=columns,show="headings",height=9)
        for col in columns:
            self.tree.heading(col,text=col.title().replace("_"," "))
            # width adjustments
            if col == "name":
                w = 160
            elif col == "total":
                w = 60
            elif col == "percentage":
                w = 80
            else:
                w = 70
            self.tree.column(col, width=w, anchor="center")
        self.tree.pack(side="left", fill="both", expand=True)
            
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")

        #loading existing records
        self.view_all()

        # bind double-click to load values into fields
        self.tree.bind("<Double-1>", self.on_treeview_double_click) 

    #GUI helper methods
    def clear_fields(self):
        self.var_roll.set("")
        self.var_name.set("")
        self.var_class.set("")
        self.var_m1.set("")
        self.var_m2.set("")
        self.var_m3.set("")
        self.var_m4.set("")
        self.var_m5.set("")
        self.var_m6.set("")

    def validate_marks(self,*marks_str):
        """
        Validate that marks are integers between 0 to 100
        returns list of ints or raises value error
        """
        marks=[]
        for s in marks_str:
            s=s.strip()
            if s=="":
                val=0
            else:
                try:
                    val=int(s)
                except ValueError:
                    raise ValueError("Marks must be integers")
                if not(0<=val<=100):
                    raise ValueError("Marks should be between 0 to 100")
                
            marks.append(val)
        return marks
    
    #CRUD operations

    def add_student(self):
        roll=self.var_roll.get().strip()
        name=self.var_name.get().strip()
        cls=self.var_class.get().strip()
        if roll==""or name=="":
            messagebox.showerror("Input Error","Roll number and name are required.")
            return
        try:
            roll_no=int(roll)
        except ValueError:
            messagebox.showerror("Input Error","Roll number must be an integer.")
            return
        
        try:
            marks= self.validate_marks(self.var_m1.get(),self.var_m2.get(),self.var_m3.get(),self.var_m4.get(),self.var_m5.get(),self.var_m6.get())
        except ValueError as e:
            messagebox.showerror("Marks Error",str(e))
            return
        total,percentage,grade=calculate_result(marks)

        #check if roll number already exists
        if fetch_student(roll_no):
            messagebox.showerror("Duplicate",f"Student with roll no {roll_no} already exists.")
            return
        data=(roll_no,name,cls,marks[0],marks[1],marks[2],marks[3],marks[4],marks[5],total,percentage,grade)
        try:
            insert_student(data)
            messagebox.showinfo("Success", "Student added successfully.")
            self.view_all()
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("DB Error", str(e))

    def update_student(self):
        roll=self.var_roll.get().strip()
        if roll=="":
            messagebox.showerror("Input Error","Please enter a roll number to update")
            return
        try:
            roll_no=int(roll)
        except ValueError:
            messagebox.showerror("Input Error","Roll number muust be an integer")
            return
        if not fetch_student(roll_no):
            messagebox.showerror("Not Found",f"No student found with roll number {roll_no}.")
            return
        
        name=self.var_name.get().strip()
        cls=self.var_class.get().strip()
        if name=="":
            messagebox.showerror("Input Error","Name is required")
            return
        try:
            marks=self.validate_marks(self.var_m1.get(),self.var_m2.get(),self.var_m3.get(),self.var_m4.get(),self.var_m5.get(),self.var_m6.get(),)
        except ValueError as e:
            messagebox.showerror("Marks Error", str(e))
            return
        
        total, percentage, grade = calculate_result(marks)
        data = (name, cls, marks[0], marks[1], marks[2], marks[3], marks[4], marks[5], total, percentage, grade, roll_no)
        try:
            update_student_db(data)
            messagebox.showinfo("Success", "Student updated successfully.")
            self.view_all()
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("DB Error", str(e))

    def delete_student(self):
        roll=self.var_roll.get().strip()
        if roll=="":
            messagebox.showerror("Input Error","Please enter a roll number to delete")
            return
        try:
            roll_no=int(roll)
        except ValueError:
            messagebox.showerror("Input Error","Roll number must be an integer")
            return
        if not fetch_student(roll_no):
            messagebox.showerror("Not Found",f"No student found with roll number {roll_no}.")
            return
        
        confirm=messagebox.askyesno("Confirm Delete",f"Are you sure you want to delete student with roll no {roll_no}?")
        if not confirm:
            return
        
        try:
            delete_student_db(roll_no)
            messagebox.showinfo("Success","Student deleted successfully.")
            self.view_all()
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("DB Error", str(e))

    def search_student(self):
        roll=self.var_roll.get().strip()
        if roll=="":
            messagebox.showerror("Input Error","Please enter a valid roll number to search")
            return
        try:
            roll_no = int(roll)
        except ValueError:
            messagebox.showerror("Input Error", "Roll number must be integer.")
            return
        
        row=fetch_student(roll_no)
        if not row:
            messagebox.showinfo("Not Found",f"No student found with roll number {roll_no}.")
            return
        # row format: (roll_no, name, class, m1, m2, m3, m4, m5, total, percentage, grade)
        self.var_name.set(row[1])
        self.var_class.set(row[2])
        self.var_m1.set(str(row[3]))
        self.var_m2.set(str(row[4]))
        self.var_m3.set(str(row[5]))
        self.var_m4.set(str(row[6]))
        self.var_m5.set(str(row[7]))
        self.var_m6.set(str(row[8]))

        # highlight record in treeview
        self.view_all()
        for item in self.tree.get_children():
            vals = self.tree.item(item, "values")
            if int(vals[0]) == roll_no:
                self.tree.selection_set(item)
                self.tree.focus(item)
                self.tree.see(item)
                break

    def view_all(self):
        #clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        rows=fetch_all_students()
        for r in rows:
            self.tree.insert("","end",values=r)

    def on_treeview_double_click(self, event):
        item = self.tree.focus()
        if not item:
            return
        vals = self.tree.item(item, "values")
        # fill the form with selected record
        self.var_roll.set(vals[0])
        self.var_name.set(vals[1])
        self.var_class.set(vals[2])
        self.var_m1.set(vals[3])
        self.var_m2.set(vals[4])
        self.var_m3.set(vals[5])
        self.var_m4.set(vals[6])
        self.var_m5.set(vals[7])
        self.var_m6.set(vals[8])
    
    #Extra features
    def export_csv(self):
        rows=fetch_all_students()
        if not rows:
            messagebox.showinfo("No Data","No records to export.")
            return
        #asking a user where to save the data
        file_path=filedialog.asksaveasfilename(defaultextension=".csv",
                                               filetype=[("csv files","*.csv"),("All files","*.*")],
                                               title="Save as")
        if not file_path:
            return
        try:
            with open(file_path,mode="w",newline="",encoding="utf-8")as f:
                writer=csv.writer(f)
                header = ["Roll No", "Name", "Class", "Marks1", "Marks2", "Marks3", "Marks4", "Marks5","Marks6", "Total", "Percentage", "Grade"]
                writer.writerow(header)
                for r in rows:
                    writer.writerow(r)
            messagebox.showinfo("Exported", f"Records exported to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def plot_grades(self):
       rows = fetch_all_students()
       if not rows:
        messagebox.showinfo("No Data", "No students to plot.")
        return

       # Extract names and percentages
       names = [r[1] for r in rows]         # name is column index 1
       percentages = [r[10] for r in rows]  # percentage is column index 10

       plt.figure(figsize=(10, 5))
       plt.bar(names, percentages)

       plt.title("Student Percentage Chart")
       plt.xlabel("Student Name")
       plt.ylabel("Percentage (%)")

       plt.xticks(rotation=45, ha='right')  # rotate names for visibility
       plt.tight_layout()
       plt.show()


def main():
    init_db()
    root = tk.Tk()
    app = StudentRMSapp(root)
    root.mainloop()


if __name__ == "__main__":
    main()    
        



    