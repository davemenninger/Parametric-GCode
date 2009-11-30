#Parametric GCode Example 4: Build a worm gear
#
#
#This demonstration shows off the usefulness of
# building parametric models with conditional statements
# in the descriptors.
#The vertical cross section of the worm gear is
# constructed by having the print head jog out and
# away from the center occasionally.  Rotating this
# at each vertical step accomplishes a twisting
# extrusion operation.


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

#Worm Gear
Radius = 8
ToothScale = 1.2  #Ratio


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
	ThisGCode.Z = 0.4 + 0.3 * Zsteps
	#FILE.writelines(str(ThisGCode)+ "\n")
	
	#The Tsteps define the parametric equation for a circle:
	# X = R cos (T), Y = R sin (T)
	# The range of T should be 0 to 2pi
	for Tsteps in range(31):
		ThisGCode.X = Radius * math.cos(Tsteps / 5.0)
		ThisGCode.Y = Radius * math.sin(Tsteps / 5.0)
		if (Tsteps > 20)&(Tsteps < 26):
			ThisGCode.X = ThisGCode.X * ToothScale
			ThisGCode.Y = ThisGCode.Y * ToothScale


		#Rotation as a function of the height in Z
		ThisGCode.rotate(Zsteps/10.0)
		FILE.writelines(str(ThisGCode)+"\n")


FILE.writelines("M103\n")
ThisGCode.Z = ThisGCode.Z + 10
FILE.writelines(str(ThisGCode)+ "\n")
FILE.writelines("M104 S0\n")

FILE.close