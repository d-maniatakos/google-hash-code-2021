class Street:
	def __init__(self,start,end,name,distance):
		self.name=name
		self.start=start
		self.end=end
		self.distance=distance

	def display(self):
		print("Street("+str(self.name)+")")
		print("\tStart: "+str(self.start))
		print("\tEnd: "+str(self.end))
		print("\tDistance: "+str(self.distance))

class Car:
	def __init__(self,carID,path):
		self.carID=carID
		self.path=path
		self.leftPath=path

	def display(self):
		print("Car("+str(self.carID)+")")
		print("\tPath: "+str(self.path))
		print("\tLeft Path:"+str(self.leftPath))

class Intersection:
	def __init__(self,intersectionID):
		self.intersectionID=intersectionID
		self.inStreets=[]
		self.outStreets=[]
		self.greenStreet=None
		self.schedule=[]

	def display(self):
		print("Intersection("+str(self.intersectionID)+")")
		print("\tInStreets: "+str(self.inStreets))
		print("\tOutStreets: "+str(self.outStreets))
		print("\tSchedule: "+str(self.schedule))

instanceName="a"

f=open("input/"+instanceName+".txt","r")    #open input file

firstLine=f.readline()
firstIntLine=[]
for i in firstLine.split(): #convert first line elements to integers
	firstIntLine.append(int(i))

simulationTime,intersectionCount,streetCount,carCount,bonus=firstIntLine
streets=[]
cars=[]
intersections=[]
streetDict={}  #used for street congestion heuristic

#read streets from input file and create street objects
for i in range(0,streetCount):
	tempLine=f.readline().split()
	newStreet=Street(int(tempLine[0]),int(tempLine[1]),tempLine[2],int(tempLine[3]))
	streets.append(newStreet)
	streetDict[tempLine[2]]=0   #street congestion depths initialized to 0

#read cars from input file and create car objects
for i in range(0,carCount):
	path=f.readline().split() #read car's path
	del path[0]	
	for street in path:
		streetDict[street]+=1
	newCar=Car(i,path)
	cars.append(newCar)

#create intersection objects
for i in range(0,intersectionCount):
	newIntersection=Intersection(i)
	intersections.append(newIntersection)

#append streets to intersection's in/out streets lists
for street in streets:
	intersections[street.start].outStreets.append(street)
	intersections[street.end].inStreets.append(street)	

#create traffic light schedule
for intersection in intersections:
	sum=0
	#sort intersection's incoming streets by increasing order of total congestion
	streetsList=[]
	for i in range(0,len(intersection.inStreets)):
		tempName=intersection.inStreets[i].name
		streetsList.append((tempName,streetDict[tempName]))
		sum+=streetDict[tempName]
	sortedList=sorted(streetsList,key=lambda tup: tup[1]) 
	#schedule increasing order of green light time slices to streets(sorted by their total congestion) 
	for i in range(0,len(intersection.inStreets)):
		intersection.schedule.append((sortedList[i][0],i+1))



#create output file
outputLines=[]
outputLines.append(str(intersectionCount))

for intersection in intersections:
	outputLines.append(str(intersection.intersectionID))
	outputLines.append(str(len(intersection.inStreets)))
	for i in range(0,len(intersection.inStreets)):
		outputLines.append(intersection.schedule[i][0]+" "+str(intersection.schedule[i][1]))

output = open("output/"+instanceName+"_output", "w")

for line in outputLines:
	output.write(line+"\n")

f.close()
output.close()