#The energy cost per second is calculated based on
#*The static power of each controller(W) x 1s x the cost per joule at the location
#*The energy spent by each controller with requests within 1s x the cost per joule at the 
#location
#*The energy spent by each switch with requests within 1s x the cost per joule at the 
#location
#*The static power of each switch(W) x 1s x the cost per joule at the location

#Since the static cost and processing cost of each switch are constant, they are ommited
#from the objective function

#*costList[i] is the prize per joule at location i
#*cPower is the power of the controller with no requests
def cConstCost(costList,cPower):
	s=str(costList[0]*cPower)+' p0'
	for i in range(1,len(costList)):
		s=s+' + '+str(costList[i]*cPower)+' p'+str(i)
	return s

#*adjMatrix is a square matrix where adjMatrix[i][j] is 1 if and only if there is a controll
#link between the switch at location i and the controller at location j
#*energy[i][j] is the energy cost for sending a message from location i to j
#*cProcEnergy is the energy necessary to process a response at the controller
#*sFreq[i] is the number of requests sent by switch i per second 
def VarCost(costList,adjMatrix,energy,cProcEnergy,sFreq):
	s = ''
	#for each switch
	for i in range(len(adjMatrix)):
		#for each possible location of a controller
		for j in range(len(adjMatrix[i])):
			#if the switch/controller edge exists
			if adjMatrix[i][j]:
				#the name of each variable corresponds to
				#its coordinates.
				
				#energy spent by the switch to process and send a request
				#(Without considering constant costs)
				sEnergy = energy[i][j]
				
				#energy spent by the controller to process and send a response
				#(Without considering constant costs)
				cEnergy = cProcEnergy+energy[j][i]
				
				#total cost for the link i,j within 1 s
				tCost = (sEnergy*costList[i] + cEnergy*costList[j])*sFreq[i]
				
				s = s + '+ '+ str(tCost) + ' e' + str(i) + '_' + str(j) + ' '	
	return s

def generateObjective(costList,cPower,adjMatrix,energy,cProcEnergy,sFreq):
	return('Minimize\n\tobj: '+cConstCost(costList,cPower)+VarCost(\
		costList,adjMatrix,energy,cProcEnergy,sFreq)+'\n')
