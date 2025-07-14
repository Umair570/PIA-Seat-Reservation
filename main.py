#################################
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import *

class PIAManagement:
    def __init__(self):
        # Create Main Window
        self.plane = Plane(2000)
        self.mainWindow = Tk()
        self.mainWindow.title("PIA Airline Reservation")

        self.createLayout()

    def createLayout(self):
        # Create the main window labels
        self.label = Label(self.mainWindow, text="PIA Ticket Reservation", font=("Arial", 20, "bold"))
        self.label.pack()
        
        # Create Main buttons
        self.button1 = Button(self.mainWindow, text="Seat Reservation", command=self.seatReservation)
        self.button1.pack()

        self.button2 = Button(self.mainWindow, text="Seat Cancellation", command=self.seatCancellation)
        self.button2.pack()

        self.button3 = Button(self.mainWindow, text="Load From File", command=self.loadFile)
        self.button3.pack(pady=(20, 0))

        self.button4 = Button(self.mainWindow, text="Save To File", command=self.saveFile)
        self.button4.pack()

        self.frame1 = Frame(self.mainWindow)

        self.label1F = Label(self.frame1, text="Business Class", font=("Arial", 15), fg="Blue")
        self.label1F.grid(row=0, column=0, padx=25)

        # Create Listboxes
        self.listbox1 = Listbox(self.frame1)
        self.listbox1.grid(row=1, column=0, sticky='nsew')
        self.listbox1.bind("<<ListboxSelect>>", self.onSelect)

        self.label2F = Label(self.frame1, text="Economy Class", font=("Arial", 15), fg='Blue')
        self.label2F.grid(row=0, column=1, padx=25)

        self.listbox2 = Listbox(self.frame1)
        self.listbox2.grid(row=1, column=1, sticky='nsew')
        self.listbox2.bind("<<ListboxSelect>>", self.onSelect)

        self.label3F = Label(self.frame1, text="Student Class", font=("Arial", 15), fg='Blue')
        self.label3F.grid(row=0, column=2, padx=25)

        self.listbox3 = Listbox(self.frame1)
        self.listbox3.grid(row=1, column=2, sticky='nsew')
        self.listbox3.bind("<<ListboxSelect>>", self.onSelect)

        self.frame1.pack()

        # Create Planes Seating Plan Window
        self.child = Tk()
        self.child.title("Seating Plan")
        self.child.geometry('300x600+700+20')
        self.frame2 = Frame(self.child)

        self.label1F2 = Label(self.frame2, text="Plane # 1", font=("Arial", 20))
        self.label1F2.grid(row=0, column=0)

        self.label2F2 = Label(self.frame2, text="Business Class", bg="Navy", fg="Beige", font=("Arial", 12))
        self.label2F2.grid(row=1, column=0)
        self.frameABC = Frame(self.frame2)

        self.businessSeats = {}
        self.economySeats = {}
        self.studentSeats = {}

        self.allIDs = {}

        # Create business class seats
        for i in range(3):
            for j in range(4):
                count = i * 4 + j + 1
                self.buttonsBC = Button(self.frameABC, text=f"{count}", width=5, fg="Grey", bg="White", state=DISABLED)
                self.buttonsBC.grid(row=i, column=j)
                self.businessSeats[count] = self.buttonsBC

        self.frameABC.grid(row=2, column=0)

        self.label3F2 = Label(self.frame2, text="Economy Class", bg="Navy", fg="Beige", font=("Arial", 12))
        self.label3F2.grid(row=3, column=0)
        self.frameBEC = Frame(self.frame2)
        
        # Create economy class seats
        for i in range(6):
            for j in range(4):
                count = i * 4 + j + 1
                self.buttonsEC = Button(self.frameBEC, text=f"{count}", width=5, fg="Grey", bg="White", state=DISABLED)
                self.buttonsEC.grid(row=i, column=j)
                self.economySeats[count] = self.buttonsEC

        self.frameBEC.grid(row=4, column=0)

        self.label4F2 = Label(self.frame2, text="Student Class", bg="Navy", fg="Beige", font=("Arial", 12))
        self.label4F2.grid(row=5, column=0)
        self.frameCSC = Frame(self.frame2)
        
        # Create student class seats
        for i in range(2):
            for j in range(4):
                count = i * 4 + j + 1
                self.buttonsSC = Button(self.frameCSC, text=f"{count}", width=5, fg="Grey", bg="White", state=DISABLED)
                self.buttonsSC.grid(row=i, column=j)
                self.studentSeats[count] = self.buttonsSC

        self.frameCSC.grid(row=6, column=0)

        self.labelSO = Label(self.frame2, text="Seats Occupied: ", font=("Arial", 15))
        self.labelSO.grid(row=7, column=0, pady=(10, 0))

        self.labelCF = Label(self.frame2, text="Cargo Filled: ", font=("Arial", 15))
        self.labelCF.grid(row=8, column=0)

        self.labelR = Label(self.frame2, text="Revenue: ", font=("Arial", 15))
        self.labelR.grid(row=9, column=0)

        self.frame2.pack()

        self.mainWindow.mainloop()

    def loadFile(self):
        # Load data from isidata
        fname = askopenfilename(filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        with open(fname, "r") as file:
            for i in file:
                data = i.strip().split('\t\t')
                if len(data) >= 2:
                    passengerId, status = data[0], data[1]
                    print(passengerId,status)
                    self.allIDs[passengerId] = status
        return self.allIDs

    def saveFile(self):
        fname = asksaveasfile(mode='w+', defaultextension=".txt")
        if fname is None:
            return

        # Read file content
        try:
            with open(fname.name, 'r') as file:
                existingData = file.read()
        except:
            existingData = ""  # If no file exists we will create a new

        # Append new data
        text2save = existingData

        # Add headers and seat data for all classes
        text2save += "\n\nBusiness Class Seats:\n"
        for seat in self.plane.businessSeats:
            text2save += f"{seat.id}\t{seat.name}\t{seat.seatNumber}\t{seat.luggage}\n"

        text2save += "\nEconomy Class Seats:\n"
        for seat in self.plane.economySeats:
            text2save += f"{seat.id}\t{seat.name}\t{seat.seatNumber}\t{seat.luggage}\n"

        text2save += "\nStudent Class Seats:\n"
        for seat in self.plane.studentSeats:
            text2save += f"{seat.id}\t{seat.name}\t{seat.seatNumber}\t{seat.luggage}\n"

        # Add cargo and revenue
        text2save += f"\nCargo: {self.plane.cargo}/{self.plane.maxCargoLimit}\n"
        businessTicket = 200000
        economyTicket = 100000
        studentTicket = 40000
        revenueBusiness = len(self.plane.businessSeats) * businessTicket
        revenueEconomy = len(self.plane.economySeats) * economyTicket
        revenueStudent = len(self.plane.studentSeats) * studentTicket
        totalRevenue = revenueBusiness + revenueEconomy + revenueStudent
        text2save += f"Revenue: ${totalRevenue}\n"

        # Save to file 
        with open(fname.name, 'w') as file:
            file.write(text2save)

        messagebox.showinfo(title="Success", message="File saved successfully")

    def seatReservation(self):
        # Create Reservation Window and Labels
        self.srWin = Tk()
        self.srWin.title("Reserve a Seat")
        self.labelN = Label(self.srWin, text="Name:")
        self.labelN.grid(row=0, column=0, padx=10)
        self.entryN = Entry(self.srWin)
        self.entryN.grid(row=0, column=1)
        self.labelID = Label(self.srWin, text="ID:")
        self.labelID.grid(row=1, column=0, padx=10)
        self.entryID = Entry(self.srWin)
        self.entryID.grid(row=1, column=1)
        self.labelSC = Label(self.srWin, text="Seat Class:")
        self.labelSC.grid(row=2, column=0, padx=10)

        self.combo = ttk.Combobox(self.srWin, values=['Business', 'Economy', 'Student'])
        self.combo.grid(row=2, column=1)
        self.combo.set("Business")
        self.combo["state"] = "readonly"

        self.labelSN = Label(self.srWin, text="Seat Number:")
        self.labelSN.grid(row=3, column=0, padx=10)
        self.entrySN = Entry(self.srWin)
        self.entrySN.grid(row=3, column=1)

        self.labelLW = Label(self.srWin, text="Luggage Weight:")
        self.labelLW.grid(row=4, column=0, padx=10)
        self.entryLW = Entry(self.srWin)
        self.entryLW.grid(row=4, column=1)

        self.buttonR = Button(self.srWin, text="Reserve", width=10, command=self.reserve)
        self.buttonR.grid(row=5, column=0, pady=10)

    def reserve(self):
        name = self.entryN.get()
        passengerId = self.entryID.get()
        passengerSeatClass = self.combo.get()
        passengerSeatNumber = self.entrySN.get()
        luggage = self.entryLW.get()

        if not (passengerId.isdigit() and len(passengerId) == 7):
            messagebox.showerror(title="Error", message="ID must be a 7-digit numerical value")
            return

        # Check for duplicate passenger IDs
        for i in [self.plane.businessSeats, self.plane.economySeats, self.plane.studentSeats]:
            for j in i:
                if j.id == passengerId:
                    messagebox.showerror(title="Error", message="Passenger with same id already exists.")
                    return

        # Check for seat availability
        duplicateSeat = False
        if passengerSeatClass == 'Business':
            for passenger in self.plane.businessSeats:
                if passenger.seatNumber == passengerSeatNumber:
                    duplicateSeat = True
                    break
        elif passengerSeatClass == 'Economy':
            for passenger in self.plane.economySeats:
                if passenger.seatNumber == passengerSeatNumber:
                    duplicateSeat = True
                    break
        elif passengerSeatClass == 'Student':
            for passenger in self.plane.studentSeats:
                if passenger.seatNumber == passengerSeatNumber:
                    duplicateSeat = True
                    break

        if duplicateSeat:
            messagebox.showerror(title="Error", message="Seat number already taken.")
            return

        if int(luggage) > 100:
            messagebox.showerror(title="Error", message="Luggage weight can't exceed 100")
            return

        passenger = Passenger(name, passengerId, passengerSeatClass, passengerSeatNumber, luggage)

        # Set the seat color based on the ID status
        if passenger.id in self.allIDs:
            if self.allIDs[passenger.id] == "TERRORIST":
                passenger.seatColor = 'Red'
            elif self.allIDs[passenger.id] == "CLEAN":
                passenger.seatColor = 'Green' 
        else:
            passenger.seatColor = 'Orange'  # For passengers not in the database

        # Handle seat reservation for the classes
        if passengerSeatClass == 'Business' and int(passengerSeatNumber) <= 12:
            self.handleSeatReservation('Business', passenger, passengerSeatNumber)
        elif passengerSeatClass == 'Economy' and int(passengerSeatNumber) <= 24:
            self.handleSeatReservation('Economy', passenger, passengerSeatNumber)
        elif passengerSeatClass == 'Student' and int(passengerSeatNumber) <= 8:
            self.handleSeatReservation('Student', passenger, passengerSeatNumber)
        else:
            messagebox.showerror(title="Error", message="Invalid Seat Class or Seat Number")

        self.updateLabels()
        self.srWin.destroy()

    def handleSeatReservation(self, seatClass, passenger, passengerSeatNumber):
        if passenger.id in self.allIDs:
            if self.allIDs[passenger.id] == "TERRORIST":
                self.updateSeatColor(seatClass, passengerSeatNumber, 'Red')
            elif self.allIDs[passenger.id] == "CLEAN":
                self.updateSeatColor(seatClass, passengerSeatNumber, 'Green')
        else:
            self.updateSeatColor(seatClass, passengerSeatNumber, 'Orange')

        # Add passenger to plane and the corresponding listbox
        if seatClass == 'Business':
            self.plane.addPassenger(passenger)
            self.listbox1.insert(END, passenger.name)
        elif seatClass == 'Economy':
            self.plane.addPassenger(passenger)
            self.listbox2.insert(END, passenger.name)
        elif seatClass == 'Student':
            self.plane.addPassenger(passenger)
            self.listbox3.insert(END, passenger.name)

        messagebox.showinfo(title="Success", message="Seat reserved successfully")
    
    def seatCancellation(self):
        # Create Cancellation Window and labels
        self.scWin=Tk()
        self.scWin.title("Cancel a Seat")
        self.frameSC=Frame(self.scWin)

        self.labelSCID=Label(self.frameSC,text="ID:")
        self.labelSCID.grid(row=0,column=0,padx=10)

        self.entrySCID=Entry(self.frameSC)
        self.entrySCID.grid(row=0,column=1)

        self.buttonSC=Button(self.frameSC,text="Cancel Seat",command=self.cancel)
        self.buttonSC.grid(row=1,column=0,pady=10)

        self.frameSC.pack() 

    def cancel(self):
        passengerId = self.entrySCID.get()
        if not (passengerId.isdigit() and len(passengerId) == 7):
            messagebox.showerror(title="Error", message="ID must be a 7-digit numerical value")
            return
        
        found = False
        # Check Business Seats
        for i in self.plane.businessSeats:
            if i.id == passengerId:
                self.plane.removePassenger(i)
                name = self.listbox1.get(0, "end")
                nameIndexB = name.index(i.name)
                self.listbox1.delete(nameIndexB)
                self.updateSeatColor('Business', i.seatNumber, 'White')
                found = True
                break

        # Check Economy Seats
        for i in self.plane.economySeats:
            if i.id == passengerId:
                self.plane.removePassenger(i)
                name = self.listbox2.get(0, "end")
                nameIndexE = name.index(i.name)
                self.listbox2.delete(nameIndexE)
                self.updateSeatColor('Economy', i.seatNumber, 'White')
                found = True
                break

        # Check Student Seats
        for i in self.plane.studentSeats:
            if i.id == passengerId:
                self.plane.removePassenger(i)
                name = self.listbox3.get(0, "end")
                nameIndexS = name.index(i.name)
                self.listbox3.delete(nameIndexS)
                self.updateSeatColor('Student', i.seatNumber, 'White')
                found = True
                break          

        if found:
            # Recalculate cargo
            self.updateLabels()
            messagebox.showinfo(title="Success", message="Reservation cancelled successfully.")
        else:
            messagebox.showerror(title="Error", message="Passenger not found.")
        
        self.updateLabels()
        self.scWin.destroy()

        
    def onSelect(self, event):
        listbox = event.widget
        selectedName = listbox.curselection()

        # If a name in listbox selected, highlight it yellow
        if selectedName:
            name = listbox.get(selectedName)
            self.highlightSeat(name)
        else:
            # On deselection reset the previously selected seat to green
            self.highlightSeat(None)

    def highlightSeat(self, name):
        allPassengers = self.plane.businessSeats + self.plane.economySeats + self.plane.studentSeats

        if self.plane.previousSelectedSeat is not None:
            self.updateSeatColor(self.plane.previousSelectedSeat.seatClass, self.plane.previousSelectedSeat.seatNumber, self.plane.previousSelectedSeat.seatColor)

        # If a new seat is selected turn it yellow and update the previously selected seat
        if name:
            for i in allPassengers:
                if i.name == name:
                    self.updateSeatColor(i.seatClass, i.seatNumber, 'Yellow')
                    self.plane.previousSelectedSeat = i
                    break
        else:
            self.plane.previousSelectedSeat = None

    def updateSeatColor(self, seatClass, seatNumber, color):
        seatNumber = int(seatNumber)
        if seatClass == 'Business':
            if seatNumber in self.businessSeats:
                self.businessSeats[seatNumber].configure(bg=color)
        elif seatClass == 'Economy':
            if seatNumber in self.economySeats:
                self.economySeats[seatNumber].configure(bg=color)
        elif seatClass == 'Student':
            if seatNumber in self.studentSeats:
                self.studentSeats[seatNumber].configure(bg=color)

    def updateLabels(self):
        totalOccupiedSeats = len(self.plane.businessSeats) + len(self.plane.economySeats) + len(self.plane.studentSeats)
        
        # Make sure the cargo percentage is calculated based on the updated cargo
        totalCargoFilled = (self.plane.cargo / self.plane.maxCargoLimit) * 100

        businessTicket = 200000
        economyTicket = 100000
        studentTicket = 40000

        revenueBusiness = len(self.plane.businessSeats) * businessTicket
        revenueEconomy = len(self.plane.economySeats) * economyTicket
        revenueStudent = len(self.plane.studentSeats) * studentTicket
        totalRevenue = revenueBusiness + revenueEconomy + revenueStudent

        self.labelSO.config(text=f"Seats Occupied = {totalOccupiedSeats}")
        self.labelCF.config(text=f"Cargo Filled: {totalCargoFilled:.2f}%")
        self.labelR.config(text=f"Revenue: ${totalRevenue}")

# Plane and Passenger classes

#Plane Class
class Plane:
    def __init__(self, maxCargoLimit):
        self.maxCargoLimit = maxCargoLimit
        self.passengers = []
        self.businessSeats = []  
        self.economySeats = []   
        self.studentSeats = []   
        self.cargo = 0          
        self.previousSelectedSeat = None

    # Add Passenger
    def addPassenger(self, passenger):
        if self.cargo + int(passenger.luggage) <= self.maxCargoLimit:
            self.passengers.append(passenger)
            if passenger.seatClass == 'Business':
                self.businessSeats.append(passenger)
            elif passenger.seatClass == 'Economy':
                self.economySeats.append(passenger)
            elif passenger.seatClass == 'Student':
                self.studentSeats.append(passenger)
            self.cargo += int(passenger.luggage)
            
    # Remove Passenger
    def removePassenger(self, passenger):
        if passenger in self.passengers:
            self.passengers.remove(passenger)
            if passenger.seatClass == 'Business':
                self.businessSeats.remove(passenger)
            elif passenger.seatClass == 'Economy':
                self.economySeats.remove(passenger)
            elif passenger.seatClass == 'Student':
                self.studentSeats.remove(passenger)
            self.cargo -= int(passenger.luggage)
# Passenger Class
class Passenger():
    def __init__(self, name, id, seatClass, seatNumber, luggage):
        self.name = name
        self.id = id
        self.seatClass = seatClass
        self.seatNumber = seatNumber
        self.luggage = luggage

win = PIAManagement()

####################################