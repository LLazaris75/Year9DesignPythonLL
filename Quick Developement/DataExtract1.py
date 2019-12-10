data = open("dataAnalysis1.txt","r");

dataString = data.read()
print(dataString)
#dataList is the list that will hold the contents of the string where the elements are split base on the new line. 
#Example 
#
#dataString = "cat\ndog\nfish"
#dataList = ["cat","dog","fish"]
#

dataList = dataString.split("\n")


for i in range(0, len(dataList),1):
    #Big Skill: Casting
    dataList[i] = dataList[i].replace(",","")
    dataList[i] = float(dataList[i])

    #Big Skill: Removing Elements

print(dataList)
