#Parametric GCode Example 1: Build A Prism

#G1 Code Object
class G1Code:
	def __init__(self, X=0, Y=0, Z=0, F=0):
		self.X =X
		self.Y =Y
		self.Z = Z
		self.F = F

	def __str__(self):
		string = "G1 X" + str(self.X) + " Y" + str(self.Y) + " Z" + str(self.Z) + " F" + str(self.F)
		return string


filename = "test.gcode"
Zsteps = 0
ThisGCode = G1Code(X=0, Y=0, Z=0, F=1000)

#Open the output file and paste on the "headers"
FILE = open(filename,"w")
FILE.writelines("G21\n")
FILE.writelines("G90\n")
FILE.writelines("M103\n")
FILE.writelines("M105\n")
FILE.writelines("M104 S220.0\n")
FILE.writelines("M101\n")

#Step through the Z range of the object.  This loop
#is the only truly mandatory part of it.
for Zsteps in range(30):
	#Hop up to the next level, staying put
	ThisGCode.Z = 0.4 * Zsteps
	FILE.writelines(str(ThisGCode)+ "\n")
	
	#Trace out the prism	
	ThisGCode.X = 0
	ThisGCode.Y = 0
	FILE.writelines(str(ThisGCode)+ "\n")	
	ThisGCode.X = 0
	ThisGCode.Y = -10
	FILE.writelines(str(ThisGCode)+ "\n")	
	ThisGCode.X = -10
	ThisGCode.Y = 0
	FILE.writelines(str(ThisGCode)+ "\n")	

ThisGCode.Z = ThisGCode.Z + 4
FILE.writelines(str(ThisGCode)+ "\n")
FILE.writelines("M104 S0\n")

FILE.close