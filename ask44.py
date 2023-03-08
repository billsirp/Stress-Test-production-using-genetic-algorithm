import matplotlib.pyplot as plt
import random
import math

def AND(inputs):
    out=inputs[0]
    for x in range(1,len(inputs)):
        out = out*inputs[x]
    return out

def NOT(in1):
    return 1-in1

def OR(inputs):
    out = 1-inputs[0]
    for x in range(1,len(inputs)):
        out = out*(1-inputs[x])
    return 1-out

def NAND(inputs):
    return 1-AND(inputs)

def NOR(inputs):
    return 1-OR(inputs)

def XOR(inputs):
    out = (1-inputs[0])*inputs[1] + inputs[0]*(1-inputs[1]);
    for x in range(2,len(inputs)):
        out = (1-out)*inputs[x] + out*(1-inputs[x])
    return out

def XNOR(inputs):
    return 1-XOR(inputs)

def process(n,els,elType,inTable,outTable):
    inputs = []
    for j in range(0,len(inTable[els[n]])):
        inputs = inputs + [values[inTable[els[n]][j]]]
		
    if elType[n]=="AND":
        finalOut = AND(inputs)
        return finalOut
    elif elType[n]=="OR":
        finalOut = OR(inputs)
        return finalOut
    elif elType[n]=="NOT":
        finalOut = NOT(inputs[0])
        return finalOut
    elif elType[n]=="NAND":
        finalOut = NAND(inputs)
        return finalOut
    elif elType[n]=="NOR":
        finalOut = NOR(inputs)
        return finalOut
    elif elType[n]=="XOR":
        finalOut = XOR(inputs)
        return finalOut
    elif elType[n]=="XNOR":
        finalOut = XNOR(inputs)
        return finalOut
    

def isTop(n):
    for k in range(0,len(filedata)):
        if (filedata[k].split())[1]==n:
            return 0
    return 1

def allInputsAreMarked(currentTops,currentInputs):
    for k in range(2,len(currentInputs)):
        if (currentInputs[k] in currentTops)==False:
            return False
    return True



print("Loading file...")
file = open('inputfile.txt')
filedata = file.readlines()

elementTypes=[]#[["AND","NOT","AND",...]
elements=[]#elements=["E1","E2","E3",...]
signals=[]#signals=["a","b","c",...]
topInputs=[]#topInputs=[0,1,2] where each number is position in signals[]

inputsTable={}#{"E1":(0,1),"E2":(2,),...}
outputsTable={}#outputsTable={"E1":3,"E2":4,"E3":5,...}

#set the elements and signals
basicGates=["AND","OR","NOT","NAND","NOR","XOR","XNOR"]
flag=filedata[0].split()
flag=flag[0]
if (flag in basicGates)==False:
    filedata[0]=filedata[0].strip('\n')
    tmp = filedata[0].split()
    tmp.pop(0)
    topInputs = tmp
    filedata.pop(0)
    for i in range(0,len(filedata)):
        filedata[i]=filedata[i].strip('\n')
else:
    topInputs = []
    for i in range(0,len(filedata)):
        filedata[i]=filedata[i].strip('\n')
        tmp = filedata[i].split()
        for j in range(2,len(tmp)):
            if isTop(tmp[j])==1:# 1->top, 0->not top
                topInputs = topInputs+[tmp[j]]

topInputs=list(dict.fromkeys(topInputs))#so as we have each input once

#sort the elements
sortedElements=[]
unsortedElements=[]
markedInputs=topInputs+[]
markedOutputs=[]

while filedata!=[]:
    markedOutputs=[]
    unsortedElements=[]
    for i in range(0,len(filedata)):
        tmp = filedata[i].split()
        if allInputsAreMarked(markedInputs,tmp):
            sortedElements = sortedElements + [filedata[i]]
            markedOutputs = markedOutputs + [tmp[1]]
        else:
            unsortedElements = unsortedElements + [filedata[i]]
    filedata = unsortedElements + []
    markedInputs = markedInputs + markedOutputs
    

        
filedata = sortedElements + []

for i in range(0,len(filedata)):
    tmp = filedata[i].split()
    elements = elements + ["E"+str(i+1)]
    elementTypes = elementTypes + [tmp[0]]
    tmp.pop(0)
    signals = signals + tmp
    signals=list(dict.fromkeys(signals))
    outputsTable["E"+str(i+1)]=signals.index(tmp[0])
    tmp.pop(0)
    for j in range(0,len(tmp)):
        tmp[j]=signals.index(tmp[j])
    inputsTable["E"+str(i+1)]=tuple(tmp)
    
for i in range(0,len(topInputs)):
    topInputs[i]=signals.index(topInputs[i])

print("---------------------------------")
values=signals+[]
L=2
N=30
G=100
mutation=0.2

for q in range(0,7):
    totalScores=[]#scoreI
    scoreG = [0]
    indiNum=[]
    generationsNum = [0]

    signalsBefore=signals+[]
    signalsAfter=signals+[]

    parent1 = [[],[]]
    parent2 = [[],[]]
    parentsScore = [0,0]

    #print(topInputs)
    #print("gen",1,"----------------------")
    for j in range(0,N):
        signalsBefore=signals+[]
        signalsAfter=signals+[]

        score = 0

        for i in range(0,len(topInputs)):#give random tops
            rand1=random.randrange(0,2,1)
            rand2=random.randrange(0,2,1)
            signalsBefore[topInputs[i]]=rand1
            signalsAfter[topInputs[i]]=rand2
            
        for i in range(0,len(elements)):#find the outputs
            m = outputsTable[elements[i]]
            values = signalsBefore+[]
            signalsBefore[m] = process(i,elements,elementTypes,inputsTable,outputsTable)
            values = signalsAfter+[]
            signalsAfter[m] = process(i,elements,elementTypes,inputsTable,outputsTable)
            if signalsAfter[m]!=signalsBefore[m]:
                score=score+1

        totalScores = totalScores + [score]
        indiNum = indiNum + [j]

        if score>min(parentsScore) and parent1!=[signalsBefore,signalsAfter] and parent2!=[signalsBefore,signalsAfter]:
            if parentsScore.index(min(parentsScore))==0:
                parentsScore[0] = score
                parent1 = [signalsBefore,signalsAfter]
            else:
                parentsScore[1] = score
                parent2 = [signalsBefore,signalsAfter]

    generationsNum = generationsNum + [1]
    scoreG = scoreG + [max(parentsScore)]

    for j in range(1,G):
        for i in range(2,N):

            signalsBefore=signals+[]
            signalsAfter=signals+[]
            score = 0
            
            coin = random.randrange(0,2,1)
            if coin==0:
                signalsBefore=parent1[0]+[]
                signalsAfter=parent2[1]+[]
            else:
                signalsBefore=parent2[0]+[]
                signalsAfter=parent1[1]+[]

            #mutation
            mutrand = random.randrange(0,100,1)
            if mutrand<mutation*100:
                anInput = random.randrange(0,len(topInputs),1)
                signalsBefore[anInput]=1-signalsBefore[anInput]
            mutrand = random.randrange(0,100,1)
            if mutrand<mutation*100:
                anInput = random.randrange(0,len(topInputs),1)
                signalsAfter[anInput]=1-signalsAfter[anInput]

            for i in range(0,len(elements)):#find the outputs
                m = outputsTable[elements[i]]
                
                values = signalsBefore+[]
                signalsBefore[m] = process(i,elements,elementTypes,inputsTable,outputsTable)
                values = signalsAfter+[]
                signalsAfter[m] = process(i,elements,elementTypes,inputsTable,outputsTable)
                if signalsAfter[m]!=signalsBefore[m]:
                    score=score+1
                    
            if score>min(parentsScore) and parent1!=[signalsBefore,signalsAfter] and parent2!=[signalsBefore,signalsAfter]:
                if parentsScore.index(min(parentsScore))==0:
                    parentsScore[0] = score
                    parent1 = [signalsBefore,signalsAfter]
                else:
                    parentsScore[1] = score
                    parent2 = [signalsBefore,signalsAfter]
        generationsNum = generationsNum + [j+1]
        scoreG = scoreG + [max(parentsScore)]
    plt.plot(generationsNum,scoreG)


plt.ylabel('scoreG')
plt.legend()
plt.show()





