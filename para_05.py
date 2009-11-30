#Parametric GCode Example 5: Build a parabolic surface
#
#
#Demonstration of a scaling function dependent on Z.
#Lays down a paraboloid, leaving off an end cap for,
# say, an LED.

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



filename = "test.gcode"
ThisGCode = G1Code(X=0, Y=0, Z=0, F=700)
Zsteps = 0
Tsteps = 0
Scale = 1.0

#Paraboloid Parameters
BaseRadius = 15
Apex = 70.0 #in number of layers


#Open the output file and paste on the "headers"
FILE = open(filename,"w")
FILE.writelines("G21\n")
FILE.writelines("G90\n")
FILE.writelines("M103\n")
FILE.writelines("M105\n")
FILE.writelines("M104 S220.0\n")
FILE.writelines("M101\n")

#Step through the Z range of the object.
for Zsteps in range(60):
	#Hop up to the next level, staying put
	ThisGCode.Z = 0.4 * Zsteps
	#FILE.writelines(str(ThisGCode)+ "\n")
	
	#The Tsteps define the parametric equation for a circle:
	# X = R cos (T), Y = R sin (T)
	# The range of T should be 0 to 2pi
	for Tsteps in range(31):
		ThisGCode.X = BaseRadius * math.cos(Tsteps / 5.0)
		ThisGCode.Y = BaseRadius * math.sin(Tsteps / 5.0)
		Scale = math.sqrt( 1 - (Zsteps / Apex) )
		

		ThisGCode.X = ThisGCode.X * Scale
		ThisGCode.Y = ThisGCode.Y * Scale


		FILE.writelines(str(ThisGCode)+"\n")


FILE.writelines("M103\n")
ThisGCode.Z = ThisGCode.Z + 10
FILE.writelines(str(ThisGCode)+ "\n")
FILE.writelines("M104 S0\n")

FILE.close