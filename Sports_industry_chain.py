from tkinter import *
from tkinter import ttk 
from pandastable import Table, TableModel
import sqlite3
import pandas as pd
db_name = 'Sports_industry_chain.db'

class Sports_industry_chain():
    
    def __init__(self, master):
        self.master = master
        self.master.title ('Sports_industry_chain')
        f1=Frame(master)
        f1.grid(row = 0, column = 0, sticky = W+E+N+S)
        #建置sol輸入介面
        f1_1=Frame(f1, bg="light yellow")
        f1_1.grid(row = 0, column = 0, rowspan = 4, columnspan = 3, sticky = W+E+N+S)
        Label (f1_1,text = 'SQL', bg="light cyan").grid (row = 0, column = 0,columnspan = 2,rowspan=2)
        self.name = Text(f1_1, height=10, width=60)
        self.name.grid(row = 3, column = 1,columnspan = 2,padx=10)
        ttk.Button (f1_1,text ='Command', command = self.adding).grid (row = 0 , column = 2,rowspan=2)
        
        #建置結果輸出介面
        f2=Frame(master, bg="light yellow")
        f2.grid(row = 4, column = 0,sticky = W+E+N+S)
        
        Label ( f2,text = 'Result',bg = "light cyan").grid (row = 0, column = 3, columnspan=1)
        self.tree = ttk.Treeview (f2)
        self.tree.grid (row = 1, column = 0,columnspan=4, sticky="nsew")
        
        
        self.message = Label(f2,text = '', fg = 'blue',bg="alice blue")
        self.message.grid(row = 0, column = 0,columnspan=2)
        f2.grid_columnconfigure(3, weight=1)
        f2.grid_rowconfigure(1, weight=1)
        
        #設置選擇表格下拉選單
        f1_2=Frame(f1,bg="alice blue")
        f1_2.grid(row = 0, column = 4, rowspan = 4, sticky = W+E+N+S)
        f1_2_f1 = LabelFrame(f1_2,text = 'Table Selection', fg='magenta', bg="light yellow")
        f1_2_f1.grid (row = 0, column = 0,padx=10,pady=10,sticky=W)
        self.table=StringVar()
        self.tabchosen=ttk.Combobox(f1_2_f1,width=12,textvariable=self.table,state='readonly')
        self.tabchosen['values']=("TEAMs","PLAYERs","FANs","GAMEs","PLAY","SPONSOR","AGENTs","BELONG_TO")
        self.tabchosen.grid(row=0,column=0)
        ttk.Button (f1_2_f1,text ='PRESS here!!!', command = self.table_window).grid (row = 1 , column = 0)
        
        #聚合及巢狀函數選單
        f1_2_f2 = LabelFrame(f1_2,text = 'Button_Query',fg='magenta',bg="light yellow")
        f1_2_f2.grid (row = 4, column = 0,padx=10,pady=10,sticky=W)       
        self.value=StringVar()
        self.valchosen=ttk.Combobox(f1_2_f2,width=12,textvariable=self.value,state='readonly')
        self.valchosen['values']=("COUNT","HAVING_COUNT","MAX_MIN_AVG","SUM","IN","NOT IN","NOT_EXISTS","EXISTS")
        self.valchosen.grid(row=3,column=0)
        ttk.Button (f1_2_f2,text ='PRESS here!!!', command = self.function).grid (row = 5 , column = 0)
        
        #建立Quit button
        ttk.Button (f2,text ='Quit', command = self.finish).grid (row = 5 , column = 0)
        


    #開啟要執行的表格
    def table_window(self):
        table=self.tabchosen.get()
        tablewindow=Toplevel(self.master)
        if table=="TEAMs":
            myGUI=TEAMs(tablewindow)
        if table=="PLAYERs":
            myGUI=PLAYERs(tablewindow)
        if table=="FANs":
            myGUI=FANs(tablewindow)
        if table=="GAMEs":
            myGUI=GAMEs(tablewindow)
        if table=="PLAY":
            myGUI=PLAY(tablewindow)
        if table=="SPONSOR":
            myGUI=SPONSOR(tablewindow)
        if table=="AGENTs":
            myGUI=AGENTs(tablewindow)
        if table=="BELONG_TO":
            myGUI=BELONG_TO(tablewindow)

        
    #察看結果        
    def viewing_records (self,query) :

        records = self.tree.get_children()
        for element in records :
            self.tree.delete (element)
        db_rows=self.run_query(query)
        conn = sqlite3.connect(db_name)
        df = pd.read_sql_query(query, conn)
        t_title=list(df.columns.values)

        self.tree["show"]="headings" 
        self.tree["columns"]=t_title
        

        for col in t_title:
            self.tree.heading(col,text=col)
        for row in db_rows :
            self.tree.insert ('', 'end',values=row)
        
        return

    #執行SQL             
    def run_query (self, query) :
        with sqlite3.connect (db_name) as conn :
            cursor = conn.cursor()
            query_result = conn.execute (query)
            conn.commit()
        return query_result
                
    def adding (self) :
        query = self.name.get("1.0",END)
        self.run_query (query)
        self.message['text'] = ''
        self.name.delete("1.0",END)
        self.viewing_records(query)
    # 定義Complex queries
    def function(self):
        value=self.valchosen.get()
        if value=="NOT IN":
            query="SELECT * FROM TEAMs WHERE TName NOT IN (SELECT TName FROM PLAY)"
            self.run_query(query)
            self.message['text'] = '沒有打比賽的所有球隊'
        if value=="IN":
            query="SELECT * FROM TEAMs WHERE TName IN (SELECT TName FROM PLAY)"
            self.run_query(query)
            self.message['text'] = '有打比賽的所有球隊'
        if value=="COUNT":
            query="SELECT F.FNo, FName, count(*) AS '# of Games' FROM GAMEs as G,FANs as F WHERE G.FNo = F.FNo GROUP BY F.FNo"
            self.run_query(query)
            self.message['text'] = '每個球迷進場的比賽數'
        if value=="HAVING_COUNT":
            query="SELECT F.FNo,FName,count(*) AS '# of Games' FROM GAMEs as G,FANs as F WHERE G.FNo=F.FNo GROUP BY F.FNo having count(*)>=3"
            self.message['text'] = '進場超過3場的球迷'
        if value=="MAX_MIN_AVG":
            query="select T.TName, T.Record, MAX(Attendance) as MAX_Game_Attendance, MIN(Attendance) as MIN_Game_Attendance, AVG(Attendance) as AVG_Order_Amount FROM TEAMs AS T, PLAY AS P,GAMEs AS G WHERE T.TName=P.TName and P.GNO=G.GNo GROUP BY T.TName"
            self.message['text'] = '球隊所參與的比賽中單場最高、最低進場及總平均進場人數'
        if value=="EXISTS":
            query="SELECT A.ANo, A.AName, A.Age, A.Phone_Number FROM AGENTs as A WHERE EXISTS (SELECT * FROM SPONSOR as S where A.ANo=S.ANo) GROUP BY A.ANo"
            self.message['text'] = '取得有贊助比賽的經紀人'
        if value=="NOT_EXISTS":
            query="SELECT A.ANo, A.AName, A.Age, A.Phone_Number FROM AGENTs as A WHERE NOT EXISTS (SELECT * FROM SPONSOR as S WHERE A.ANo=S.ANo)"
            self.message['text'] = '取得沒有贊助比賽的經紀人'
        if value=="SUM":
            query="SELECT G.Location, sum(G.Attendance) as Total_Attendance FROM GAMEs as G GROUP BY G.Location"
            self.message['text'] = '所有球場的總入場人數'
    
        self.viewing_records(query)

    def finish(self):
        self.master.destroy()    

# 對於每個table建立功能
class TEAMs:
    def __init__(self, master):
        self.master = master
        self.master.geometry("1100x400")
        self.master.title ('TEAMs')
       
        self.frame = LabelFrame (self.master, text = 'Add new record',fg="blue")
        self.frame.grid (row =0 , column = 1)      
        
        self.lable1=Label (self.frame,text = 'TName').grid (row = 0, column = 1)
        self.TName = Entry (self.frame)
        self.TName.grid(row = 1, column = 1)
        self.lable2=Label (self.frame,text = 'Record').grid (row = 0, column = 2)
        self.Record = Entry (self.frame)
        self.Record.grid(row = 1, column = 2)
        self.lable3=Label (self.frame,text = 'Championship').grid (row = 0, column = 3)
        self.Championship = Entry (self.frame)
        self.Championship.grid(row = 1, column = 3)
        self.lable4=Label (self.frame,text = 'Division').grid (row = 0, column = 4)
        self.Division = Entry (self.frame)
        self.Division.grid(row = 1, column = 4)
        
        self.tree = ttk.Treeview (self.master)
        self.tree.grid (row = 4, column = 1,columnspan=6)
        
        ttk.Button (self.frame,text ='Add',command=self.adding).grid (row = 0 , column = 5)
        ttk.Button (self.frame,text ='Quit',command=self.finish).grid (row = 1 , column = 5)
        ttk.Button (self.master,text ='Delect',command=self.delecting).grid (row = 5 , column = 3)
        ttk.Button (self.master,text ='Edit',command=self.editing).grid (row = 5 , column = 1)
        
        Label (self.master,text = 'Result').grid (row = 3, column = 1)        
        self.viewing_records()

    def adding (self) :
        query = 'INSERT INTO TEAMs VALUES ( ?, ?, ?, ?)'
        parameters = (self.TName.get(), self.Record.get(), self.Championship.get(), self.Division.get())
        self.run_query (query, parameters)
        self.TName.delete(0,END)
        self.Record.delete(0,END)
        self.Championship.delete(0,END)
        self.Division.delete(0,END)
        self.viewing_records()

    def run_query (self, query, parameters = () ) :
        with sqlite3.connect (db_name) as conn :
            cursor = conn.cursor()
            query_result = conn.execute (query,parameters)
            conn.commit()
        return query_result
    
    def viewing_records (self) :
        
        records = self.tree.get_children()
        for element in records :
            self.tree.delete (element)

        query="select* from TEAMs"
        db_rows=self.run_query(query)
        conn = sqlite3.connect(db_name)
        df = pd.read_sql_query(query, conn)
        t_title=list(df.columns.values)

        self.tree["show"]="headings" 
        self.tree["columns"]=t_title

        for col in t_title:
            self.tree.heading(col,text=col)
        for row in db_rows :
            self.tree.insert ('', 'end',values=row)

        return

    def delecting (self) :
        TName = self.tree.item (self.tree.selection())['values'][0]
        query = 'DELETE FROM TEAMs WHERE TName = ?'
        self.run_query (query, (TName,))
        self.viewing_records()
        
    def editing (self):
        old_value=[]
        for i in range(4):
            old_value.append(self.tree.item(self.tree.selection())['values'][i])
                
        self.edit_wind = Toplevel ()
        self.edit_wind.title('Editing')

        Label (self.edit_wind, text = 'Old').grid (row = 0, column = 1)
        Label (self.edit_wind, text = 'New').grid (row = 1,column = 1)
        for i in range(4):
            Entry (self.edit_wind , textvariable = StringVar(self.edit_wind, value = old_value[i]), state = 'readonly').grid(row = 0, column = 2+i)
        
        #KEY值不變
        Entry (self.edit_wind , textvariable = StringVar(self.edit_wind, value = self.tree.item(self.tree.selection())['values'][0]), state = 'readonly').grid(row = 1, column = 2)
        
        new_value=[]
        for i in range(3):
            new_value.append(Entry (self.edit_wind))
            new_value[i].grid (row = 1, column =3+i)
            
        Button (self.edit_wind, text = 'Save changes', command = lambda: self.edit_records(
                new_value[0].get(),new_value[1].get(),new_value[2].get(),old_value[1],old_value[2],old_value[3])).grid (row = 2, column = 2, sticky = W)
        
        self.edit_wind.mainloop()

    def edit_records (self,new_value0,new_value1,new_value2,old_value1,old_value2,old_value3):
        query = 'UPDATE TEAMs SET Record = ?,Championship=?,Division=? WHERE Record = ? AND Championship=? AND Division=? '
        parameters = (new_value0,new_value1,new_value2,old_value1,old_value2,old_value3)
        self.run_query (query, parameters)
        self.edit_wind.destroy()
        self.viewing_records()
        
    def finish(self):
        self.master.destroy()
        
        
class PLAYERs:
    def __init__(self, master):
        self.master = master
        self.master.geometry("700x400")
        self.master.title ('PLAYERs')
       
        self.frame = LabelFrame (self.master, text = 'Add new record',fg="blue")
        self.frame.grid (row =0 , column = 1)      
        
        self.lable1=Label (self.frame,text = 'PNo').grid (row = 0, column = 1)
        self.PNo = Entry (self.frame)
        self.PNo.grid(row = 1, column = 1)
        self.lable2=Label (self.frame,text = 'PName').grid (row = 0, column = 2)
        self.PName = Entry (self.frame)
        self.PName.grid(row = 1, column = 2)
        self.lable3=Label (self.frame,text = 'Position').grid (row = 0, column = 3)
        self.Position = Entry (self.frame)
        self.Position.grid(row = 1, column = 3)
        self.lable4=Label (self.frame,text = 'Salary').grid (row = 0, column = 4)
        self.Salary = Entry (self.frame)
        self.Salary.grid(row = 1, column = 4)
        
        self.tree = ttk.Treeview (self.master)
        self.tree.grid (row = 4, column = 1,columnspan=6)
        
        ttk.Button (self.frame,text ='Add',command=self.adding).grid (row = 0 , column = 5)
        ttk.Button (self.frame,text ='Quit',command=self.finish).grid (row = 1 , column = 5)
        ttk.Button (self.master,text ='Delect',command=self.delecting).grid (row = 5 , column = 3)
        ttk.Button (self.master,text ='Edit',command=self.editing).grid (row = 5 , column = 1)
        
        Label (self.master,text = 'Result').grid (row = 3, column = 1)
        
        self.viewing_records()

#        self.name = Entry ()
    def adding (self) :
        query = 'INSERT INTO PLAYERs VALUES ( ?, ?, ?, ?)'
        parameters = (self.PNo.get(), self.PName.get(), self.Position.get(), self.Salary.get())
        self.run_query (query, parameters)
        self.PNo.delete(0,END)
        self.PName.delete(0,END)
        self.Position.delete(0,END)
        self.Salary.delete(0,END)
        
        self.viewing_records()

    def run_query (self, query, parameters = () ) :
        with sqlite3.connect (db_name) as conn :
            cursor = conn.cursor()
            query_result = conn.execute (query,parameters)
            conn.commit()
        return query_result
    
    def viewing_records (self) :
        
        records = self.tree.get_children()
        for element in records :
            self.tree.delete (element)

        query="select* from PLAYERs"
        db_rows=self.run_query(query)
        conn = sqlite3.connect(db_name)
        df = pd.read_sql_query(query, conn)
        t_title=list(df.columns.values)

        self.tree["show"]="headings" 
        self.tree["columns"]=t_title
#        self.tree = ttk.Treeview (self.master,columns=t_title,show="headings")
#        self.tree.grid (row = 4, column = 1,columnspan=6)

        for col in t_title:
            self.tree.heading(col,text=col)
        for row in db_rows :
            self.tree.insert ('', 'end',values=row)

        return

    def delecting (self) :
        PNo = self.tree.item (self.tree.selection())['values'][0]
        query = 'DELETE FROM PLAYERs WHERE PNo = ?'
        self.run_query (query, (PNo,))
        self.viewing_records()
        
    def editing (self):
        #取得要編輯那一列的值
        old_value=[]
        for i in range(2):
            old_value.append(self.tree.item(self.tree.selection())['values'][i])
                
        self.edit_wind = Toplevel ()
        self.edit_wind.title('Editing')

        Label (self.edit_wind, text = 'Old').grid (row = 0, column = 1)
        Label (self.edit_wind, text = 'New').grid (row = 1,column = 1)
        for i in range(2):
            Entry (self.edit_wind , textvariable = StringVar(self.edit_wind, value = old_value[i]), state = 'readonly').grid(row = 0, column = 2+i)
        
        #KEY值不變
        Entry (self.edit_wind , textvariable = StringVar(self.edit_wind, value = self.tree.item(self.tree.selection())['values'][0]), state = 'readonly').grid(row = 1, column = 2)
        
        new_value=[]
        for i in range(1):
            new_value.append(Entry (self.edit_wind))
            new_value[i].grid (row = 1, column =3+i)
            
        Button (self.edit_wind, text = 'Save changes', command = lambda: self.edit_records(
                new_value[0].get(),new_value[1].get(),new_value[2].get(),old_value[1],old_value[2],old_value[3])).grid (row = 2, column = 2, sticky = W)
        
        self.edit_wind.mainloop()

    def edit_records (self,new_value0,new_value1,new_value2,old_value1,old_value2,old_value3):
        query = 'UPDATE PLAYERs SET PName = ?,Position=?,Salary=? WHERE PName = ? AND Position=? AND Salary=?'
        parameters = (new_value0,new_value1,new_value2,old_value1,old_value2,old_value3)
        self.run_query (query, parameters)
        self.edit_wind.destroy()
#        self.message['text'] = 'Record () changed.'.format (name)
        self.viewing_records()
        
    def finish(self):
        self.master.destroy()

class FANs:
    def __init__(self, master):
        self.master = master
        self.master.geometry("900x400")
        self.master.title ('FANs')
       
        self.frame = LabelFrame (self.master, text = 'Add new record',fg="blue")
        self.frame.grid (row =0 , column = 1)      
        
        self.lable1=Label (self.frame,text = 'FNo').grid (row = 0, column = 1)
        self.FNo = Entry (self.frame)
        self.FNo.grid(row = 1, column = 1)
        self.lable2=Label (self.frame,text = 'FName').grid (row = 0, column = 2)
        self.FName = Entry (self.frame)
        self.FName.grid(row = 1, column = 2)
        self.lable3=Label (self.frame,text = 'Supporting_Team').grid (row = 0, column = 3)
        self.Supporting_Team = Entry (self.frame)
        self.Supporting_Team.grid(row = 1, column = 3)
        self.lable4=Label (self.frame,text = 'Age').grid (row = 0, column = 4)
        self.Age = Entry (self.frame)
        self.Age.grid(row = 1, column = 4)
        
        self.tree = ttk.Treeview (self.master)
        self.tree.grid (row = 4, column = 1,columnspan=6)
        
        ttk.Button (self.frame,text ='Add',command=self.adding).grid (row = 0 , column = 5)
        ttk.Button (self.frame,text ='Quit',command=self.finish).grid (row = 1 , column = 5)
        ttk.Button (self.master,text ='Delect',command=self.delecting).grid (row = 5 , column = 3)
        ttk.Button (self.master,text ='Edit',command=self.editing).grid (row = 5 , column = 1)
        
        Label (self.master,text = 'Result').grid (row = 3, column = 1)        
        self.viewing_records()

    def adding (self) :
        query = 'INSERT INTO FANs VALUES ( ?, ?, ?, ?)'
        parameters = (self.FNo.get(), self.FName.get(), self.Supporting_Team.get(), self.Age.get())
        self.run_query (query, parameters)
        self.FNo.delete(0,END)
        self.FName.delete(0,END)
        self.Supporting_Team.delete(0,END)
        self.Age.delete(0,END)
        self.viewing_records()

    def run_query (self, query, parameters = () ) :
        with sqlite3.connect (db_name) as conn :
            cursor = conn.cursor()
            query_result = conn.execute (query,parameters)
            conn.commit()
        return query_result
    
    def viewing_records (self) :
        
        records = self.tree.get_children()
        for element in records :
            self.tree.delete (element)

        query="select* from FANs"
        db_rows=self.run_query(query)
        conn = sqlite3.connect(db_name)
        df = pd.read_sql_query(query, conn)
        t_title=list(df.columns.values)

        self.tree["show"]="headings" 
        self.tree["columns"]=t_title

        for col in t_title:
            self.tree.heading(col,text=col)
        for row in db_rows :
            self.tree.insert ('', 'end',values=row)

        return

    def delecting (self) :
        FNo = self.tree.item (self.tree.selection())['values'][0]
        query = 'DELETE FROM FANs WHERE FNo = ?'
        self.run_query (query, (FNo,))
        self.viewing_records()
        
    def editing (self):
        old_value=[]
        for i in range(4):
            old_value.append(self.tree.item(self.tree.selection())['values'][i])
                
        self.edit_wind = Toplevel ()
        self.edit_wind.title('Editing')

        Label (self.edit_wind, text = 'Old').grid (row = 0, column = 1)
        Label (self.edit_wind, text = 'New').grid (row = 1,column = 1)
        for i in range(4):
            Entry (self.edit_wind , textvariable = StringVar(self.edit_wind, value = old_value[i]), state = 'readonly').grid(row = 0, column = 2+i)
        
        #KEY值不變
        Entry (self.edit_wind , textvariable = StringVar(self.edit_wind, value = self.tree.item(self.tree.selection())['values'][0]), state = 'readonly').grid(row = 1, column = 2)
        
        new_value=[]
        for i in range(3):
            new_value.append(Entry (self.edit_wind))
            new_value[i].grid (row = 1, column =3+i)
            
        Button (self.edit_wind, text = 'Save changes', command = lambda: self.edit_records(
                new_value[0].get(),new_value[1].get(),new_value[2].get(),old_value[1],old_value[2],old_value[3])).grid (row = 2, column = 2, sticky = W)
        
        self.edit_wind.mainloop()

    def edit_records (self,new_value0,new_value1,new_value2,old_value1,old_value2,old_value3):
        query = 'UPDATE FANs SET FName = ?,Supporting_Team=?,Age=? WHERE FName = ? AND Supporting_Team=? AND Age=?'
        parameters = (new_value0,new_value1,new_value2,old_value1,old_value2,old_value3)
        self.run_query (query, parameters)
        self.edit_wind.destroy()
        self.viewing_records()
        
    def finish(self):
        self.master.destroy()

class GAMEs:
    def __init__(self, master):
        self.master = master
        self.master.geometry("1200x400")
        self.master.title ('GAMEs')
       
        self.frame = LabelFrame (self.master, text = 'Add new record',fg="blue")
        self.frame.grid (row =0 , column = 1)      
        
        self.lable1=Label (self.frame,text = 'GNo').grid (row = 0, column = 1)
        self.GNo = Entry (self.frame)
        self.GNo.grid(row = 1, column = 1)
        self.lable2=Label (self.frame,text = 'Game_Time').grid (row = 0, column = 2)
        self.Game_Time = Entry (self.frame)
        self.Game_Time.grid(row = 1, column = 2)
        self.lable3=Label (self.frame,text = 'Location').grid (row = 0, column = 3)
        self.Location = Entry (self.frame)
        self.Location.grid(row = 1, column = 3)
        self.lable4=Label (self.frame,text = 'Attendance').grid (row = 0, column = 4)
        self.Attendance = Entry (self.frame)
        self.Attendance.grid(row = 1, column = 4)
        self.lable4=Label (self.frame,text = 'FNo').grid (row = 0, column = 5)
        self.FNo = Entry (self.frame)
        self.FNo.grid(row = 1, column = 5)



        self.tree = ttk.Treeview (self.master)
        self.tree.grid (row = 4, column = 1,columnspan=6)
        
        ttk.Button (self.frame,text ='Add',command=self.adding).grid (row = 0 , column = 6)
        ttk.Button (self.frame,text ='Quit',command=self.finish).grid (row = 1 , column = 6)
        ttk.Button (self.master,text ='Delect',command=self.delecting).grid (row = 5 , column = 3)
        ttk.Button (self.master,text ='Edit',command=self.editing).grid (row = 5 , column = 1)
        
        Label (self.master,text = 'Result').grid (row = 3, column = 1)        
        self.viewing_records()

    def adding (self) :
        query = 'INSERT INTO GAMEs VALUES ( ?, ?, ?, ?, ?)'
        parameters = (self.GNo.get(), self.Game_Time.get(), self.Location.get(), self.Attendance.get(), self.FNo.get())
        self.run_query (query, parameters)
        self.GNo.delete(0,END)
        self.Game_Time.delete(0,END)
        self.Location.delete(0,END)
        self.Attendance.delete(0,END)
        self.FNo.delete(0,END)
        self.viewing_records()

    def run_query (self, query, parameters = () ) :
        with sqlite3.connect (db_name) as conn :
            cursor = conn.cursor()
            query_result = conn.execute (query,parameters)
            conn.commit()
        return query_result
    
    def viewing_records (self) :
        
        records = self.tree.get_children()
        for element in records :
            self.tree.delete (element)

        query="select* from GAMEs"
        db_rows=self.run_query(query)
        conn = sqlite3.connect(db_name)
        df = pd.read_sql_query(query, conn)
        t_title=list(df.columns.values)

        self.tree["show"]="headings" 
        self.tree["columns"]=t_title

        for col in t_title:
            self.tree.heading(col,text=col)
        for row in db_rows :
            self.tree.insert ('', 'end',values=row)

        return

    def delecting (self) :
        GNo = self.tree.item (self.tree.selection())['values'][0]
        query = 'DELETE FROM GAMEs WHERE GNo = ?'
        self.run_query (query, (GNo,))
        self.viewing_records()
        
    def editing (self):
        old_value=[]
        for i in range(5):
            old_value.append(self.tree.item(self.tree.selection())['values'][i])
                
        self.edit_wind = Toplevel ()
        self.edit_wind.title('Editing')

        Label (self.edit_wind, text = 'Old').grid (row = 0, column = 1)
        Label (self.edit_wind, text = 'New').grid (row = 1,column = 1)
        for i in range(5):
            Entry (self.edit_wind , textvariable = StringVar(self.edit_wind, value = old_value[i]), state = 'readonly').grid(row = 0, column = 2+i)
        
        #KEY值不變
        Entry (self.edit_wind , textvariable = StringVar(self.edit_wind, value = self.tree.item(self.tree.selection())['values'][0]), state = 'readonly').grid(row = 1, column = 2)
        
        new_value=[]
        for i in range(4):
            new_value.append(Entry (self.edit_wind))
            new_value[i].grid (row = 1, column =3+i)
            
        Button (self.edit_wind, text = 'Save changes', command = lambda: self.edit_records(
                new_value[0].get(),new_value[1].get(),new_value[2].get(),new_value[3].get(),old_value[1],old_value[2],old_value[3],old_value[4])).grid (row = 2, column = 2, sticky = W)
        
        self.edit_wind.mainloop()

    def edit_records (self,new_value0,new_value1,new_value2,new_value3,old_value1,old_value2,old_value3,old_value4):
        query = 'UPDATE GAMEs SET Game_Time = ?,Location=?,Attendance=?, FNo=? WHERE Game_Time = ? AND Location=? AND Attendance=? AND FNo=?'
        parameters = (new_value0,new_value1,new_value2,new_value3,old_value1,old_value2,old_value3,old_value4)
        self.run_query (query, parameters)
        self.edit_wind.destroy()
        self.viewing_records()
        
    def finish(self):
        self.master.destroy()

class PLAY:
    def __init__(self, master):
        self.master = master
        self.master.geometry("700x400")
        self.master.title ('PLAY')
       
        self.frame = LabelFrame (self.master, text = 'Add new record',fg="blue")
        self.frame.grid (row =0 , column = 1)      
        
        self.lable1=Label (self.frame,text = 'PNo').grid (row = 0, column = 1)
        self.PNo = Entry (self.frame)
        self.PNo.grid(row = 1, column = 1)
        self.lable2=Label (self.frame,text = 'TName').grid (row = 0, column = 2)
        self.TName = Entry (self.frame)
        self.TName.grid(row = 1, column = 2)
        self.lable3=Label (self.frame,text = 'GNo').grid (row = 0, column = 3)
        self.GNo = Entry (self.frame)
        self.GNo.grid(row = 1, column = 3)
        
        self.tree = ttk.Treeview (self.master)
        self.tree.grid (row = 4, column = 1,columnspan=6)
        
        ttk.Button (self.frame,text ='Add',command=self.adding).grid (row = 0 , column = 4)
        ttk.Button (self.frame,text ='Quit',command=self.finish).grid (row = 1 , column = 4)
        ttk.Button (self.master,text ='Delect',command=self.delecting).grid (row = 5 , column = 3)
        ttk.Button (self.master,text ='Edit',command=self.editing).grid (row = 5 , column = 1)
        
        Label (self.master,text = 'Result').grid (row = 3, column = 1)
        
        self.viewing_records()

#        self.name = Entry ()
    def adding (self) :
        query = 'INSERT INTO PLAY VALUES ( ?, ?, ?)'
        parameters = (self.PNo.get(), self.TName.get(), self.GNo.get())
        self.run_query (query, parameters)
        self.PNo.delete(0,END)
        self.TName.delete(0,END)
        self.GNo.delete(0,END)
        
        self.viewing_records()

    def run_query (self, query, parameters = () ) :
        with sqlite3.connect (db_name) as conn :
            cursor = conn.cursor()
            query_result = conn.execute (query,parameters)
            conn.commit()
        return query_result
    
    def viewing_records (self) :
        
        records = self.tree.get_children()
        for element in records :
            self.tree.delete (element)

        query="select* from PLAY"
        db_rows=self.run_query(query)
        conn = sqlite3.connect(db_name)
        df = pd.read_sql_query(query, conn)
        t_title=list(df.columns.values)

        self.tree["show"]="headings" 
        self.tree["columns"]=t_title

        for col in t_title:
            self.tree.heading(col,text=col)
        for row in db_rows :
            self.tree.insert ('', 'end',values=row)

        return

    def delecting (self) :
        PNo = self.tree.item (self.tree.selection())['values'][0]
        query = 'DELETE FROM PLAY WHERE PNo = ?'
        self.run_query (query, (PNo,))
        self.viewing_records()
        
    def editing (self):
        #取得要編輯那一列的值
        old_value=[]
        for i in range(3):
            old_value.append(self.tree.item(self.tree.selection())['values'][i])
                
        self.edit_wind = Toplevel ()
        self.edit_wind.title('Editing')

        Label (self.edit_wind, text = 'Old').grid (row = 0, column = 1)
        Label (self.edit_wind, text = 'New').grid (row = 1,column = 1)
        for i in range(3):
            Entry (self.edit_wind , textvariable = StringVar(self.edit_wind, value = old_value[i]), state = 'readonly').grid(row = 0, column = 2+i)
        
        #KEY值不變
        Entry (self.edit_wind , textvariable = StringVar(self.edit_wind, value = self.tree.item(self.tree.selection())['values'][0]), state = 'readonly').grid(row = 1, column = 2)
        
        new_value=[]
        for i in range(2):
            new_value.append(Entry (self.edit_wind))
            new_value[i].grid (row = 1, column =3+i)
            
        Button (self.edit_wind, text = 'Save changes', command = lambda: self.edit_records(
                new_value[0].get(),new_value[1].get(),old_value[1],old_value[2])).grid (row = 2, column = 2, sticky = W)
        
        self.edit_wind.mainloop()

    def edit_records (self,new_value0,new_value1,old_value1,old_value2):
        query = 'UPDATE PLAY SET TName = ?,GNo=? WHERE TName = ? AND GNo=?'
        parameters = (new_value0,new_value1,old_value1,old_value2)
        self.run_query (query, parameters)
        self.edit_wind.destroy()
        self.viewing_records()
        
    def finish(self):
        self.master.destroy()

class SPONSOR:
    def __init__(self, master):
        self.master = master
        self.master.geometry("900x400")
        self.master.title ('SPONSOR')
       
        self.frame = LabelFrame (self.master, text = 'Add new record',fg="blue")
        self.frame.grid (row =0 , column = 1)      
        
        self.lable1=Label (self.frame,text = 'GNo').grid (row = 0, column = 1)
        self.GNo = Entry (self.frame)
        self.GNo.grid(row = 1, column = 1)
        self.lable2=Label (self.frame,text = 'PNo').grid (row = 0, column = 2)
        self.PNo = Entry (self.frame)
        self.PNo.grid(row = 1, column = 2)
        self.lable3=Label (self.frame,text = 'ANo').grid (row = 0, column = 3)
        self.ANo = Entry (self.frame)
        self.ANo.grid(row = 1, column = 3)
        self.lable4=Label (self.frame,text = 'Amount').grid (row = 0, column = 4)
        self.Amount = Entry (self.frame)
        self.Amount.grid(row = 1, column = 4)
        
        self.tree = ttk.Treeview (self.master)
        self.tree.grid (row = 4, column = 1,columnspan=6)
        
        ttk.Button (self.frame,text ='Add',command=self.adding).grid (row = 0 , column = 5)
        ttk.Button (self.frame,text ='Quit',command=self.finish).grid (row = 1 , column = 5)
        ttk.Button (self.master,text ='Delect',command=self.delecting).grid (row = 5 , column = 3)
        ttk.Button (self.master,text ='Edit',command=self.editing).grid (row = 5 , column = 1)
        
        Label (self.master,text = 'Result').grid (row = 3, column = 1)        
        self.viewing_records()

    def adding (self) :
        query = 'INSERT INTO SPONSOR VALUES ( ?, ?, ?, ?)'
        parameters = (self.GNo.get(), self.PNo.get(), self.ANo.get(), self.Amount.get())
        self.run_query (query, parameters)
        self.GNo.delete(0,END)
        self.PNo.delete(0,END)
        self.ANo.delete(0,END)
        self.Amount.delete(0,END)
        self.viewing_records()

    def run_query (self, query, parameters = () ) :
        with sqlite3.connect (db_name) as conn :
            cursor = conn.cursor()
            query_result = conn.execute (query,parameters)
            conn.commit()
        return query_result
    
    def viewing_records (self) :
        
        records = self.tree.get_children()
        for element in records :
            self.tree.delete (element)

        query="select* from SPONSOR"
        db_rows=self.run_query(query)
        conn = sqlite3.connect(db_name)
        df = pd.read_sql_query(query, conn)
        t_title=list(df.columns.values)

        self.tree["show"]="headings" 
        self.tree["columns"]=t_title

        for col in t_title:
            self.tree.heading(col,text=col)
        for row in db_rows :
            self.tree.insert ('', 'end',values=row)

        return

    def delecting (self) :
        GNo = self.tree.item (self.tree.selection())['values'][0]
        query = 'DELETE FROM SPONSOR WHERE GNo = ?'
        self.run_query (query, (GNo,))
        self.viewing_records()
        
    def editing (self):
        old_value=[]
        for i in range(4):
            old_value.append(self.tree.item(self.tree.selection())['values'][i])
                
        self.edit_wind = Toplevel ()
        self.edit_wind.title('Editing')

        Label (self.edit_wind, text = 'Old').grid (row = 0, column = 1)
        Label (self.edit_wind, text = 'New').grid (row = 1,column = 1)
        for i in range(4):
            Entry (self.edit_wind , textvariable = StringVar(self.edit_wind, value = old_value[i]), state = 'readonly').grid(row = 0, column = 2+i)
        
        #KEY值不變
        for i in range(3):
            Entry (self.edit_wind , textvariable = StringVar(self.edit_wind, value = self.tree.item(self.tree.selection())['values'][i]), state = 'readonly').grid(row = 1, column = 2+i)
        
            new_value=Entry (self.edit_wind)
            new_value.grid (row = 1, column =5)
            
        Button (self.edit_wind, text = 'Save changes', command = lambda: self.edit_records(
                new_value.get(),old_value[3])).grid (row = 2, column = 2, sticky = W)
        
        self.edit_wind.mainloop()

    def edit_records (self,new_value,old_value3):
        query = 'UPDATE SPONSOR SET Amount = ? WHERE Amount = ?'
        parameters = (new_value,old_value3)
        self.run_query (query, parameters)
        self.edit_wind.destroy()
        self.viewing_records()
        
    def finish(self):
        self.master.destroy()

class AGENTs:
    def __init__(self, master):
        self.master = master
        self.master.geometry("900x400")
        self.master.title ('AGENTs')
       
        self.frame = LabelFrame (self.master, text = 'Add new record',fg="blue")
        self.frame.grid (row =0 , column = 1)      
        
        self.lable1=Label (self.frame,text = 'PNo').grid (row = 0, column = 1)
        self.PNo = Entry (self.frame)
        self.PNo.grid(row = 1, column = 1)
        self.lable2=Label (self.frame,text = 'ANo').grid (row = 0, column = 2)
        self.ANo = Entry (self.frame)
        self.ANo.grid(row = 1, column = 2)
        self.lable3=Label (self.frame,text = 'AName').grid (row = 0, column = 3)
        self.AName = Entry (self.frame)
        self.AName.grid(row = 1, column = 3)
        self.lable4=Label (self.frame,text = 'Age').grid (row = 0, column = 4)
        self.Age = Entry (self.frame)
        self.Age.grid(row = 1, column = 4)
        self.lable5=Label (self.frame,text = 'Phone_Number').grid (row = 0, column = 5)
        self.Phone_Number = Entry (self.frame)
        self.Phone_Number.grid(row = 1, column = 5)
        
        self.tree = ttk.Treeview (self.master)
        self.tree.grid (row = 4, column = 1,columnspan=6)
        
        ttk.Button (self.frame,text ='Add',command=self.adding).grid (row = 0 , column = 6)
        ttk.Button (self.frame,text ='Quit',command=self.finish).grid (row = 1 , column = 6)
        ttk.Button (self.master,text ='Delect',command=self.delecting).grid (row = 5 , column = 3)
        ttk.Button (self.master,text ='Edit',command=self.editing).grid (row = 5 , column = 1)
        
        Label (self.master,text = 'Result').grid (row = 3, column = 1)        
        self.viewing_records()

    def adding (self) :
        query = 'INSERT INTO AGENTs VALUES ( ?, ?, ?, ?, ?)'
        parameters = (self.PNo.get(), self.ANo.get(), self.AName.get(), self.Age.get(), self.Phone_Number.get())
        self.run_query (query, parameters)
        self.PNo.delete(0,END)
        self.ANo.delete(0,END)
        self.AName.delete(0,END)
        self.Age.delete(0,END)
        self.Phone_Number.delete(0,END)
        self.viewing_records()

    def run_query (self, query, parameters = () ) :
        with sqlite3.connect (db_name) as conn :
            cursor = conn.cursor()
            query_result = conn.execute (query,parameters)
            conn.commit()
        return query_result
    
    def viewing_records (self) :
        
        records = self.tree.get_children()
        for element in records :
            self.tree.delete (element)

        query="select* from AGENTs"
        db_rows=self.run_query(query)
        conn = sqlite3.connect(db_name)
        df = pd.read_sql_query(query, conn)
        t_title=list(df.columns.values)

        self.tree["show"]="headings" 
        self.tree["columns"]=t_title

        for col in t_title:
            self.tree.heading(col,text=col)
        for row in db_rows :
            self.tree.insert ('', 'end',values=row)

        return

    def delecting (self) :
        PNo = self.tree.item (self.tree.selection())['values'][0]
        query = 'DELETE FROM AGENTs WHERE PNo = ?'
        self.run_query (query, (PNo,))
        self.viewing_records()
        
    def editing (self):
        old_value=[]
        for i in range(5):
            old_value.append(self.tree.item(self.tree.selection())['values'][i])
                
        self.edit_wind = Toplevel ()
        self.edit_wind.title('Editing')

        Label (self.edit_wind, text = 'Old').grid (row = 0, column = 1)
        Label (self.edit_wind, text = 'New').grid (row = 1,column = 1)
        for i in range(5):
            Entry (self.edit_wind , textvariable = StringVar(self.edit_wind, value = old_value[i]), state = 'readonly').grid(row = 0, column = 2+i)
        
        #KEY值不變
        for i in range(2):
            Entry (self.edit_wind , textvariable = StringVar(self.edit_wind, value = self.tree.item(self.tree.selection())['values'][i]), state = 'readonly').grid(row = 1, column = 2+i)
        
        new_value=[]
        for j in range(2):
            new_value.append(Entry (self.edit_wind))
            new_value[j].grid (row = 1, column =4+j)
            
        Button (self.edit_wind, text = 'Save changes', command = lambda: self.edit_records(
                new_value[0].get(),new_value[1].get(),new_value[2].get(),old_value[2],old_value[3],old_value[4])).grid (row = 2, column = 2, sticky = W)
        
        self.edit_wind.mainloop()

    def edit_records (self,new_value0,new_value1,new_value2,old_value2,old_value3,old_value4):
        query = 'UPDATE AGENTs SET AName = ?,Age=?, Phone_Number=? WHERE AName = ? AND Age=? AND Phone_Number=?'
        parameters = (new_value0,new_value1,new_value2,old_value2,old_value3,old_value4)
        self.run_query (query, parameters)
        self.edit_wind.destroy()
        self.viewing_records()
        
    def finish(self):
        self.master.destroy()

class BELONG_TO:
    def __init__(self, master):
        self.master = master
        self.master.geometry("700x400")
        self.master.title ('BELONG_TO')
       
        self.frame = LabelFrame (self.master, text = 'Add new record',fg="blue")
        self.frame.grid (row =0 , column = 1)      
        
        self.lable1=Label (self.frame,text = 'PNo').grid (row = 0, column = 1)
        self.PNo = Entry (self.frame)
        self.PNo.grid(row = 1, column = 1)
        self.lable2=Label (self.frame,text = 'TName').grid (row = 0, column = 2)
        self.TName = Entry (self.frame)
        self.TName.grid(row = 1, column = 2)
        self.lable3=Label (self.frame,text = 'Contract').grid (row = 0, column = 3)
        self.Contract = Entry (self.frame)
        self.Contract.grid(row = 1, column = 3)
        
        self.tree = ttk.Treeview (self.master)
        self.tree.grid (row = 4, column = 1,columnspan=6)
        
        ttk.Button (self.frame,text ='Add',command=self.adding).grid (row = 0 , column = 4)
        ttk.Button (self.frame,text ='Quit',command=self.finish).grid (row = 1 , column = 4)
        ttk.Button (self.master,text ='Delect',command=self.delecting).grid (row = 5 , column = 3)
        ttk.Button (self.master,text ='Edit',command=self.editing).grid (row = 5 , column = 1)
        
        Label (self.master,text = 'Result').grid (row = 3, column = 1)
        
        self.viewing_records()

#        self.name = Entry ()
    def adding (self) :
        query = 'INSERT INTO BELONG_TO VALUES ( ?, ?, ?)'
        parameters = (self.PNo.get(), self.TName.get(), self.Contract.get())
        self.run_query (query, parameters)
        self.PNo.delete(0,END)
        self.TName.delete(0,END)
        self.Contract.delete(0,END)
        
        self.viewing_records()

    def run_query (self, query, parameters = () ) :
        with sqlite3.connect (db_name) as conn :
            cursor = conn.cursor()
            query_result = conn.execute (query,parameters)
            conn.commit()
        return query_result
    
    def viewing_records (self) :
        
        records = self.tree.get_children()
        for element in records :
            self.tree.delete (element)

        query="select* from BELONG_TO"
        db_rows=self.run_query(query)
        conn = sqlite3.connect(db_name)
        df = pd.read_sql_query(query, conn)
        t_title=list(df.columns.values)

        self.tree["show"]="headings" 
        self.tree["columns"]=t_title

        for col in t_title:
            self.tree.heading(col,text=col)
        for row in db_rows :
            self.tree.insert ('', 'end',values=row)

        return

    def delecting (self) :
        PNo = self.tree.item (self.tree.selection())['values'][0]
        query = 'DELETE FROM BELONG_TO WHERE PNo = ?'
        self.run_query (query, (PNo,))
        self.viewing_records()
        
    def editing (self):
        #取得要編輯那一列的值
        old_value=[]
        for i in range(3):
            old_value.append(self.tree.item(self.tree.selection())['values'][i])
                
        self.edit_wind = Toplevel ()
        self.edit_wind.title('Editing')

        Label (self.edit_wind, text = 'Old').grid (row = 0, column = 1)
        Label (self.edit_wind, text = 'New').grid (row = 1,column = 1)
        for i in range(3):
            Entry (self.edit_wind , textvariable = StringVar(self.edit_wind, value = old_value[i]), state = 'readonly').grid(row = 0, column = 2+i)
        
        #KEY值不變
        Entry (self.edit_wind , textvariable = StringVar(self.edit_wind, value = self.tree.item(self.tree.selection())['values'][0]), state = 'readonly').grid(row = 1, column = 2)
        
        new_value=[]
        for i in range(2):
            new_value.append(Entry (self.edit_wind))
            new_value[i].grid (row = 1, column =3+i)
            
        Button (self.edit_wind, text = 'Save changes', command = lambda: self.edit_records(
                new_value[0].get(),new_value[1].get(),old_value[1],old_value[2])).grid (row = 2, column = 2, sticky = W)
        
        self.edit_wind.mainloop()

    def edit_records (self,new_value0,new_value1,old_value1,old_value2):
        query = 'UPDATE BELONG_TO SET TName = ?,Contract=? WHERE TName = ? AND Contract=?'
        parameters = (new_value0,new_value1,old_value1,old_value2)
        self.run_query (query, parameters)
        self.edit_wind.destroy()
        self.viewing_records()
        
    def finish(self):
        self.master.destroy()

        
if __name__== '__main__':
    master = Tk()
    master.geometry("700x450")
    application = Sports_industry_chain (master) #必要，不然無法執行上述內容
    master.mainloop()
    