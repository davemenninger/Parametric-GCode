#Parametric GCode Example 7: Star
#
#
#Implements a list of GCode objects
# which can then be manipulated as a
# whole using for loops

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
Zsteps = 0
TotalHeight = 30

#choose start point such that the figure will be centered:
ThisGCode.relative_move(-30,0)
GCodeList.append(ThisGCode.Clone())
#Aseemble a Star
ThisGCode.relative_move(20,10)
GCodeList.append(ThisGCode.Clone())
ThisGCode.relative_move(10,20)
GCodeList.append(ThisGCode.Clone())
ThisGCode.relative_move(10,-20)
GCodeList.append(ThisGCode.Clone())
ThisGCode.relative_move(20,-10)
GCodeList.append(ThisGCode.Clone())
ThisGCode.relative_move(-20,-10)
GCodeList.append(ThisGCode.Clone())
ThisGCode.relative_move(-10,-20)
GCodeList.append(ThisGCode.Clone())
ThisGCode.relative_move(-10,20)
GCodeList.append(ThisGCode.Clone())
ThisGCode.relative_move(-20,10)
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
		x.rotate(0.05)
		FILE.writelines(str(x)+"\n")


FILE.writelines("M103\n")
ThisGCode.Z = ThisGCode.Z + 10
FILE.writelines(str(ThisGCode)+ "\n")
FILE.writelines("M104 S0\n")

FILE.close