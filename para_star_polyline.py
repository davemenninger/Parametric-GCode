#Parametric GCode Star
#
#Generates a six pointed star in GCode.
#Goal is to generate snowflakes algorithmically.
#
#This code is derived from Allan Ecker's
#source: http://www.thingiverse.com/thing:849
#
#License: CC-BY-SA

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
		self.X = X
		self.Y = Y
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

	#Add relative moves
	def relative_move(self, XMove, YMove):
		OldX = self.X
		OldY = self.Y
		self.X = OldX + XMove
		self.Y = OldY + YMove

	#Clone Method
	def Clone(self):
		CloneCode = G1Code(self.X, self.Y, self.Z, self.F)
		return CloneCode

#List of G1Codes
class myPolyLine:
	def __init__(self):
		self.listofcodes = []
		
	def __str__(self):
		string_output = ""
		for gcode in self.listofcodes:
			string_output += str(gcode) + "\n"
		return string_output
		
	def append(self,gcode):
		self.listofcodes.append(gcode)
		
	def extend(self,polyline):
		for gcode in polyline.listofcodes:
			self.listofcodes.append(gcode.Clone())
		
	def rotate(self,angle):
		for gcode in self.listofcodes:
			gcode.rotate(angle)

filename = "test.gcode"

#Open the output file and paste on the "headers"
FILE = open(filename,"w")
FILE.writelines("G21\n")
FILE.writelines("G90\n")
FILE.writelines("M103\n")
FILE.writelines("M105\n")
FILE.writelines("M104 S220.0\n")
FILE.writelines("M101\n")

#build a single arm as a list of GCodes
ThisGCodeArm = myPolyLine()
ThisGCode = G1Code(X=0.5, Y=0.5, Z=0, F=700)
ThisGCodeArm.append(ThisGCode)
ThisGCode = G1Code(X=0.5, Y=10, Z=0, F=700)
ThisGCodeArm.append(ThisGCode)
ThisGCode = G1Code(X=0, Y=10.5, Z=0, F=700)
ThisGCodeArm.append(ThisGCode)
ThisGCode = G1Code(X=-0.5, Y=10, Z=0, F=700)
ThisGCodeArm.append(ThisGCode)
ThisGCode = G1Code(X=-0.5, Y=0.5, Z=0, F=700)
ThisGCodeArm.append(ThisGCode)

#FILE.writelines(str(ThisGCodeArm))

#for a in range(6):
#	ThisGCodeArm.rotate(math.radians(60))
#	FILE.writelines(str(ThisGCodeArm))

ThisGCodeStar = myPolyLine()

for a in range(6):
	ThisGCodeArm.rotate(math.radians(60))
	ThisGCodeStar.extend(ThisGCodeArm)
	
FILE.writelines(str(ThisGCodeStar))

FILE.writelines("M103\n")
ThisGCode.Z = ThisGCode.Z + 10
FILE.writelines(str(ThisGCode)+ "\n")
FILE.writelines("M104 S0\n")

FILE.close
