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
			
	def Clone(self):
		ClonePolyLine = myPolyLine()
		for gcode in self.listofcodes:
			ClonePolyLine.append(gcode.Clone())
		return ClonePolyLine
		
	def rotate(self,angle):
		for gcode in self.listofcodes:
			gcode.rotate(angle)
			
	def mirrorX(self):
		for gcode in self.listofcodes:
			gcode.Y = -1*(gcode.Y)
			
	def reverse(self):
		self.listofcodes.reverse()

filename = "test.gcode"

#Open the output file and paste on the "headers"
FILE = open(filename,"w")
FILE.writelines("G21\n")
FILE.writelines("G90\n")
FILE.writelines("G92 X0 Y0 Z0\n")
FILE.writelines("M103\n")
FILE.writelines("M105\n")
FILE.writelines("M104 S220.0\n")
FILE.writelines("M6 T0\n")
FILE.writelines("G04 P5000\n")
#FILE.writelines("M101\n")
FILE.writelines("M103\n") 
FILE.writelines("M01 (The heater is warming up and will do a test extrusion.  Click yes after you have cleared the nozzle of the extrusion.)\n")
FILE.writelines("G0 Z0	(Go back to zero.)\n")
FILE.writelines("G21\n")
FILE.writelines("G90\n")
FILE.writelines("G28\n")
FILE.writelines("M103\n")
FILE.writelines("M105\n")
FILE.writelines("M108 S225.0\n")
FILE.writelines("M104 S230.0\n")
FILE.writelines("M101\n")

#make half an arm with "spikes"
arm_length = 10.0
arm_thickness = 1.0
num_spikes = 3
gap_size = (arm_length/num_spikes)/2.0
spike_length = arm_length/2.0

SpikyArm = myPolyLine()
ThisGCode = G1Code(X=arm_thickness/2.0, Y=arm_thickness/2.0, Z=0, F=1500)
SpikyArm.append(ThisGCode)

for spike_n in range(1,num_spikes+1):
	x1 = gap_size*spike_n
	y1 = arm_thickness/2.0
	x2 = x1 + spike_length*math.cos(math.radians(30.0))
	y2 = spike_length*math.sin(math.radians(30.0))
	x3 = x1+ gap_size
	y3 = arm_thickness/2.0
	ThisGCode = G1Code(X=x1, Y=y1, Z=0, F=1500)
	SpikyArm.append(ThisGCode)
	ThisGCode = G1Code(X=x2, Y=y2, Z=0, F=1500)
	SpikyArm.append(ThisGCode)
	ThisGCode = G1Code(X=x3, Y=y3, Z=0, F=1500)
	SpikyArm.append(ThisGCode)

ThisGCode = G1Code(X=10, Y=0.5, Z=0, F=1500)
SpikyArm.append(ThisGCode)

#make a mirror image of the first half of the arm
otherHalf = SpikyArm.Clone()
otherHalf.mirrorX()
otherHalf.reverse()

#make a pointy tip
ThisGCode = G1Code(X=arm_length+(arm_length/10.0),Y=0,Z=0, F=1500)

#join em together
SpikyArm.append(ThisGCode)
SpikyArm.extend(otherHalf)

ThisGCodeStar = myPolyLine()

for a in range(6):
	SpikyArm.rotate(math.radians(60))
	ThisGCodeStar.extend(SpikyArm)

FILE.writelines(str(ThisGCodeStar))

FILE.writelines("M103\n")
ThisGCode.Z = ThisGCode.Z + 10
FILE.writelines(str(ThisGCode)+ "\n")
FILE.writelines("M104 S0\n")

FILE.close