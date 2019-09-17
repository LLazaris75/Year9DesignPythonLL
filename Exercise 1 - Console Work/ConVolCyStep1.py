#Input
#What inputs are needed to calculate the volume of a cylinder?
print("Volume of a Cylinder Formula: ")

name = input("What is your name: ")	#takes users name

radius = input("input radius(cm): ") #input
radius = (float)(radius)	#cast to float

height = input("input height(cm): ") #input
height = (float)(height)	#cast to float

#Process
#What formula is used to calculate the volume of a cylinder?
volume = 3.14 * radius * radius * height
#Output
#What is important about the output?
print(volume)

