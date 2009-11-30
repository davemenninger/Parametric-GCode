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




#Fractal Object
#Uses recursion to issue relative commands
# which produce the fractal shape.
# The basic concept here is that the snowflake
# fractal consists of only two kinds of turns,
# -120 degree and +60 degree turns.  Calling the
# proper sequence of these turns creates the
# fractal.  Here we call +60 turns "A turns" and
# the -120 degree ones "B turns".
#
#In terms of turns, the sequence for the result of
# creating a single "bump" from a line segment is
# ABA, for turning up the bump, down it, and then
# back to straight.  To interject more bumps on
# that segment, We put an ABA segment in between
# each turn.  From there, we can see that the
# general formula for a branch of the fractal is
# *A*B*A*, where each asterisk is the smaller
# points.  The member functions CallBottom and
# CallBelow represent these two patterns,
# respectively.
#
#To bend the loop around to make the classic
# snowflake look, CallTop alters the pattern from
# CallBelow to *B*B*B* for a complete circle.
#
class Flake:
	#Constructor takes a "start" XYZ pos
	def __init__(self, n=3, X=0, Y=0, Z=0):
		self.n = n
		self.FlakeCode = G1Code(X, Y, Z, F=500)
		self.Dir = 0
		self.CodeList=[]

	#The User calls this function to perform the top-level
	#function, which inserts B-steps to bend the three
	#"arms" of the flake around into a loop
	def CallTop(self, n):
		self.CallBelow(n-1)
		self.StepB()
		self.CallBelow(n-1)
		self.StepB()
		self.CallBelow(n-1)
		self.StepB()

	#Create the *A*B*A* pattern.
	def CallBelow(self, n):
		if(n==0):
			self.CallBottom()
		else:
			self.CallBelow(n-1)
			self.StepA()
			self.CallBelow(n-1)
			self.StepB()
			self.CallBelow(n-1)
			self.StepA()
			self.CallBelow(n-1)

	#Every minimal line segment is ABA
	def CallBottom(self):
		self.StepA()
		self.StepB()
		self.StepA()

	#In an arbitrary recursive-direction fractal, we'd need
	# to employ sin and cos functions to compute each angle
	# turn's coordinates.  Since +60 and -120 turns never
	# take us anywhere but six directions, I'm just skipping
	# between these.
	def StepForward(self):
		if(self.Dir==0):
			self.FlakeCode.relative_move(1.0, 0)
		if(self.Dir==1):
			self.FlakeCode.relative_move(0.5, 0.866025)
		if(self.Dir==2):
			self.FlakeCode.relative_move(-0.5, 0.866025)
		if(self.Dir==3):
			self.FlakeCode.relative_move(-1.0, 0)
		if(self.Dir==4):
			self.FlakeCode.relative_move(-0.5, -0.866025)
		if(self.Dir==5):
			self.FlakeCode.relative_move(0.5, -0.866025)
		self.CodeList.append(self.FlakeCode.Clone())

	#A Steps turn us one increment anticlockwise.
	def StepA(self):
		self.Dir = self.Dir + 1
		if(self.Dir>5): self.Dir = 0
		self.StepForward()

	#B Steps turn us two decrements clockwise.
	def StepB(self):
		self.Dir = self.Dir - 2
		if(self.Dir<0): self.Dir = self.Dir + 6
		self.StepForward()




filename = "test.gcode"
ThisGCode = G1Code(X=0, Y=0, Z=0, F=700)
Zsteps = 0
TotalHeight = 10 # in layers
myFlake = Flake(2, -40, 20, 0)
myFlake.CallTop(4)

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

	for x in myFlake.CodeList:
		x.Z = 0.4 * Zsteps
		FILE.writelines(str(x)+"\n")



FILE.writelines("M103\n")
ThisGCode.Z = ThisGCode.Z + 10
FILE.writelines(str(ThisGCode)+ "\n")
FILE.writelines("M104 S0\n")

FILE.close