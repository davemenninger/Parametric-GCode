#Parametric GCode Example 9: Gear
#
#

#Import the math library
import math


#Rounding function
# Input: num=int, float, or string; r=int  
# Output: string  
def myRound(num, r=0):  
	if type(num) is str:  
		num = float(num)  
	num += 0.5/(10**r)  
	if r == 0:  
		return str(int(num))  
	else:
		num = str(num)  
		return num[:num.find('.')+r+1]


#G1 Code Object
class G1Code:
	def __init__(self, X=0, Y=0, Z=0, F=0):
		self.X =X
		self.Y =Y
		self.Z = Z
		self.F = F

	def __str__(self):
		#Added rounding
		string = "G1 X" + myRound(self.X,2) + " Y" + myRound(self.Y,2) + " Z" + myRound(self.Z,2) + " F" + str(self.F)
		return string

	#Rotate the XY point of the GCode
	def rotate(self, Theta):
		OldX = self.X
		OldY = self.Y
		self.X = OldX * math.cos(Theta) - OldY * math.sin(Theta)
		self.Y = OldX * math.sin(Theta) + OldY * math.cos(Theta)

	#Scale the XY point
	def scale(self, Scale):
		self.X = Scale * self.X
		self.Y = Scale * self.Y

	#Add relative moves
	#Note: we're still using the CNC bot's absolute mode!
	#This just allows us to issue relative position commands
	# during this script and translate them *into* absolute mode!
	def relative_move(self, XMove, YMove):
		OldX = self.X
		OldY = self.Y
		self.X = OldX + XMove
		self.Y = OldY + YMove

	#Clone Method
	#Now that we're using lists of objects, we need to
	# call the constructor so that new additions to the
	# lists aren't just references to the first code.
	def Clone(self):
		CloneCode = G1Code(self.X, self.Y, self.Z, self.F)
		return CloneCode



filename = "test.gcode"
ThisGCode = G1Code(X=0, Y=0, Z=0, F=700)
GCodeList = []
TotalHeight = 30
Teeth=8

for Tsteps in range(Teeth*4):
	if(((Tsteps+1)%4)<2):
		ThisGCode.X = 11.0 * math.cos(Tsteps * 3.14159 / (Teeth*2))
		ThisGCode.Y = 11.0 * math.sin(Tsteps * 3.14159 / (Teeth*2))
	else:
		ThisGCode.X = 16.0 * math.cos(Tsteps * 3.14159 / (Teeth*2))
		ThisGCode.Y = 16.0 * math.sin(Tsteps * 3.14159 / (Teeth*2))
	GCodeList.append(ThisGCode.Clone())
		
for Tsteps in range(31):
	ThisGCode.X = 10.8 * math.cos(Tsteps / 5.0)
	ThisGCode.Y = 10.8 * math.sin(Tsteps / 5.0)
	GCodeList.append(ThisGCode.Clone())

for Tsteps in range(31):
	ThisGCode.X = 10.4 * math.cos(Tsteps / 5.0)
	ThisGCode.Y = 10.4 * math.sin(Tsteps / 5.0)
	GCodeList.append(ThisGCode.Clone())

for Tsteps in range(31):
	if(((Tsteps-1)%8)<1):
		ThisGCode.X = 2.0 * math.cos(Tsteps / 5.0)
		ThisGCode.Y = 2.0 * math.sin(Tsteps / 5.0)
	else:
		ThisGCode.X = 10.0 * math.cos(Tsteps / 5.0)
		ThisGCode.Y = 10.0 * math.sin(Tsteps / 5.0)
	GCodeList.append(ThisGCode.Clone())

ThisGCode.X = 2.0
ThisGCode.Y = 2.0
GCodeList.append(ThisGCode.Clone())
ThisGCode.X = -2.0
ThisGCode.Y = 2.0
GCodeList.append(ThisGCode.Clone())
ThisGCode.X = -2.0
ThisGCode.Y = -2.0
GCodeList.append(ThisGCode.Clone())
ThisGCode.X = 2.0
ThisGCode.Y = -2.0
GCodeList.append(ThisGCode.Clone())
ThisGCode.X = 2.0
ThisGCode.Y = 2.0
GCodeList.append(ThisGCode.Clone())
ThisGCode.X = 2.4
ThisGCode.Y = 2.4
GCodeList.append(ThisGCode.Clone())
ThisGCode.X = -2.4
ThisGCode.Y = 2.4
GCodeList.append(ThisGCode.Clone())
ThisGCode.X = -2.4
ThisGCode.Y = -2.4
GCodeList.append(ThisGCode.Clone())
ThisGCode.X = 2.4
ThisGCode.Y = -2.4
GCodeList.append(ThisGCode.Clone())
ThisGCode.X = 2.4
ThisGCode.Y = 2.4
GCodeList.append(ThisGCode.Clone())



#DEBUG
#for x in GCodeList:
#	print(str(x))


#Open the output file and paste on the "headers"
FILE = open(filename,"w")
FILE.writelines("G21\n")
FILE.writelines("G90\n")
FILE.writelines("M103\n")
FILE.writelines("M105\n")
FILE.writelines("M104 S220.0\n")
FILE.writelines("M101\n")

#Step through the Z range of the object.
for Zsteps in range(TotalHeight):

	for x in GCodeList:
		x.Z = 0.4 * Zsteps
		FILE.writelines(str(x)+"\n")


FILE.writelines("M103\n")
ThisGCode.Z = ThisGCode.Z + 10
FILE.writelines(str(ThisGCode)+ "\n")
FILE.writelines("M104 S0\n")

FILE.close