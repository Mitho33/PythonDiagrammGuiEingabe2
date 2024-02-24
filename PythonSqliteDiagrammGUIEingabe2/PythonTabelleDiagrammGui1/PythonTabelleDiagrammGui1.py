#GUI
from tkinter import * 
#Datenbank
import sqlite3
import tkinter
from turtle import color
#Projektmappenexplorer , Python Umgebungen, RMT alle Python Umgebungen
#Übersicht klicken, wechseln auf Pakete, in die suche maplotlib eingeben
#Diagramm
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk)
#Durchführung math. oder statische Operationen
import numpy as np
#Messagebox
import easygui




#window 
fenster =Tk()
fenster.title("Hallo")
fenster.geometry("600x800")
fenster.config(bg='red')

#Label im Window platziert
Label(fenster, text="Id").place(x=100,y=500)
Label(fenster, text="Monat").place(x=200,y=500)
Label(fenster, text="Umsatz").place(x=300,y=500)

#Entries im window platziert
e1 = Entry(fenster)
e2 = Entry(fenster)
e3=  Entry(fenster)
e1.place(x=100,y=600)
e2.place(x=200,y=600)
e3.place(x=300,y=600)

#Listen zum Druck
s=[]
t=[]
rows=[]

#Datenbankverbindung wird erzeugt und bisherigen einträge werden angezeigt
connection = sqlite3.connect("test.db")
#Druck der Veränderungen
print(connection.total_changes)

#cursor Objekt wird für Befehle in SQL benötigt
cursor = connection.cursor()
#alle werden ausgewählt
cursor.execute("SELECT * FROM example")
#Variable wird initialsiert
rows = cursor.fetchall()
#alle Zeile werden in Zeilen gedruckt
for row in rows:
        print(row)

connection.close()

#Werte der Entries werden geholt und in string konvertiert




#Eingaben werden angezeigt
def show_entry_fields():
   #Platzhalter und Absatz
   print("Id: %s\n Jahr: %s\n Umsatz: %s" % (e1.get(), e2.get(), e3.get()))
#Pdf wird erzeugt
def build_pdf():
     plt.savefig("Diagramm2.pdf")#speichert das Diagramm als PDF
     easygui.msgbox("PDF erfolgreich erzeugt!", title="simple gui")

def delete_db():
    
     try:
        r=str(e1.get())
        connection = sqlite3.connect("test.db")
        #print(connection.total_changes)
        #cursor Objekt wird für Befehle in SQL benötigt
        cursor = connection.cursor()
        #löscht alles
        #cursor.execute("DELETE FROM example ")
        #löscht nur eine Zeile
        cursor.execute("DELETE FROM example WHERE id = ?",(r))
        connection.commit()
        cursor.execute("SELECT * FROM example")
        s=[]
        t=[]
        rows=[]
        rows = cursor.fetchall()

        #alle Zeile werden gedruckt
        for row in rows:
            s.append(row[0])
            t.append(row[1])
            print(row)

        connection.close()
        
     except:
        easygui.msgbox ("Loeschen nicht erfolgreich!", title="simple gui",)
       


# #Methode zum Speichern der Eingabe und Ausgabe im Diagramm
def speichern_datenbank():
        #Initialisierung mit Entry
        r=str(e1.get())
        s=str(e2.get())
        t=str(e3.get())
     
            # Länge von Entry wird überprüft, bei keiner Eingabe =0, and Verknüpfungsoperator
        if len(e1.get()) != 0 and len(e2.get()) != 0 and len(e3.get()) != 0 : 
       
            #Datenbankverbindung wird erzeugt
            connection = sqlite3.connect("test.db")

            print(connection.total_changes)

            #cursor Objekt wird für Befehle in SQL benötigt
            cursor = connection.cursor()

            #In der Datenbank wird eine Tabelle angelegt
            cursor.execute("CREATE TABLE IF NOT EXISTS example (id  , monat , umsatz )")
            #In der Tabelle werden mit Hilfe der Variablen die Werte eingefügt
            cursor.execute("INSERT INTO example VALUES (?, ?, ?)",(r,s,t))
            #Änderungen werden geprüft und ausgeführt
            connection.commit()
            #List als Zwischenspeicher deklariert

            s=[]
            t=[]
            rows=[]
 
            #10 Ergebnisse aus monat, umsatz werden ausgewählt
            cursor.execute("SELECT monat, umsatz FROM example LIMIT 10 ")

            rows = cursor.fetchall()
            for row in rows:
              #  Die Methode append fügt ein Objekt am Ende einer Liste ein
                #hier
                s.append(row[0])
                t.append(row[1])
                print(row) 
            connection.close()
            easygui.msgbox ("Speichern erfolgreich!", title="simple gui",)
        else:
            easygui.msgbox ("Speichern nicht erfolgreich!", title="simple gui",)
  
def zeichnen_daten():
    connection = sqlite3.connect("test.db")
        #print(connection.total_changes)
        #cursor Objekt wird für Befehle in SQL benötigt
    cursor = connection.cursor()
   # Liste deklariert
    s=[]
    t=[]
    rows=[] 
    #auswahl der Daten für x-/y-Achse
    cursor.execute("SELECT monat, umsatz FROM example LIMIT 10 ")
    #Initialisierung mit Auswahl
    rows = cursor.fetchall()
     #alle Zeile werden gedruckt
    for row in rows:
            # hinzufügen  von s in den ersten Index und in den zweiten Index wird t der Liste row hinzugefügt, 
            # durch for Schleife wird dann Zeile für Zeile erstellt   
            s.append(row[0])
            t.append(row[1])
          
    # Verbindung wird geschlossen
    connection.close()
    
    #Figur, und Achsen werden Initialsiert
    fig, ax=plt.subplots()
    #Balkendiagramm wird initialisiert
    bar_container=ax.bar(s,t, color='red' )
    #Achsenbeschriftung
    ax.set(xlabel='Jahr', ylabel='Umsatz/Mrd.', title=' Jahr 2017')
    #Gitterlinien
    ax.grid()
    
    # #Zeigt Diagramm in eigenem GUI an, hier überflüssig, da Ausgabe im GUI erfolgt
    ##plt.show()
    #Canvas mit Figur wird dem Window hinzugefügt
    canvas = FigureCanvasTkAgg(fig, master=fenster)
    #Canvas wird gezeichnet
    canvas.draw() 
    #Komponente wird ins Canvas gepackt
    canvas.get_tk_widget().pack()

#Button im Canvas platziert
Button(fenster, text='Quit', command=fenster.quit).place(x=100,y=700)
Button(fenster, text='Show', command=show_entry_fields).place(x=180,y=700)
Button(fenster, text='Speichern', command=speichern_datenbank).place(x=240,y=700)
Button(fenster, text='Zeichnen', command=zeichnen_daten).place(x=320,y=700)
Button(fenster, text='Loeschen', command=delete_db).place(x=400,y=700)
Button(fenster, text='PDF', command=build_pdf).place(x=480,y=700)
#Ausführende Methode für TKinter
mainloop()