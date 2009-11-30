#Parametric GCode Example 8: Snowflake Curve
#
#
#Going to go pretty crazy here!
#
#Recursive algorithm will provide relative coordinates.
# We'll translate them into absolutes and then spit
# them into the GCode file to render the fractal in plastic!


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

filename = "test.gcode"
ThisGCode = G1Code(X=0, Y=0, Z=0, F=700)
Zsteps = 0
TotalHeight = 10 # in layers

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
	ThisGCode.Z = 0.4 * Zsteps

	for a in range(6):
		angle = math.radians(60*a)
		
		ThisGCode.X = 0.5
		ThisGCode.Y = 0.5
		ThisGCode.rotate(angle)
		FILE.writelines(str(ThisGCode)+ "\n")
	
		ThisGCode.X = 0.5
		ThisGCode.Y = 10
		ThisGCode.rotate(angle)
		FILE.writelines(str(ThisGCode)+ "\n")

		ThisGCode.X = 0
		ThisGCode.Y = 10.5
		ThisGCode.rotate(angle)
		FILE.writelines(str(ThisGCode)+ "\n")

		ThisGCode.X = -0.5
		ThisGCode.Y = 10
		ThisGCode.rotate(angle)
		FILE.writelines(str(ThisGCode)+ "\n")

		ThisGCode.X = -0.5
		ThisGCode.Y = 0.5
		ThisGCode.rotate(angle)
		FILE.writelines(str(ThisGCode)+ "\n")


FILE.writelines("M103\n")
ThisGCode.Z = ThisGCode.Z + 10
FILE.writelines(str(ThisGCode)+ "\n")
FILE.writelines("M104 S0\n")

FILE.close