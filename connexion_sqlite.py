import sqlite3

class Comunication():
    def __init__(self):
        self.connexion = sqlite3.connect('data.db')

    def insert_employee(self,data):
        cursor = self.connexion.cursor()
        sql = ("INSERT INTO employees(RH_code,Last_Name,Start_Name,Email) VALUES(?,?,?,?);")
        cursor.excute(sql,data)
        self.connexion.commit()
        self.connexion.close()


    def affichage_employee(self):
        cursor = self.connexion.cursor()
        db = "SELECT * FROM employees"
        cursor.execute(db)
        show = cursor.fetchall()
        return show


    def fetch_last_row(self):
        cursor = self.connexion.cursor()
        db = "SELECT Last_Name,Start_Name FROM employees ORDER BY RH_code DESC LIMIT 1"
        cursor.execute(db)
        show = cursor.fetchall()
        return show

    def chercher_employee(self, id_employee):
        cursor = self.connexion.cursor()
        db = """SELECT * FROM employees WHERE RH_code = {}""".format(id_employee)
        cursor.execute(db)
        nombreX = cursor.fetchall()
        cursor.close()
        return nombreX

    def delete_employee(self, id_employee):
        cursor = self.connexion.cursor()
        db = """DELETE * FROM employees WHERE RH_code = {}""".format(id_employee)
        cursor.execute(db)
        self.connexion.commit()
        cursor.close()