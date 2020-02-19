def sequenceBatch(exrPath, seqMin, seqMax):
    print("==== Sequence batching ====")
    print("Renaiming the following exrs", exrPath)
    print("From frame :", seqMin)
    print("To frame :", seqMax)
    
    # Opening the exrPath and getting rid of the frame numbers
    # 1 - Keeping only the last item from the path (meaning the actual exr name)
    exrPathSplitted = exrPath.split("/")
    lastItem = len(exrPathSplitted)
    exrName = (exrPathSplitted[lastItem - 1])
    
    # Splitting the exrName in 3 lists in order to have the middle one reprenting the actual frame number
    # The exrName[1] should be equal to the actual frame number
    exrName = exrName.split(".")
    
    # Creating a list with the number of exrName instances between the seq min and seq max
    neededFrames = int(seqMax) - int(seqMin) + 1
    current = 0
    exrRenamed = []
    while current < neededFrames:
        exrRenamed.append(exrName)
        current += 1
    
    # Going through the new list replacing the item[1] with the minSeq and then +1 for each frame in the list
    # The returned list is the new frame list the item [0] contains the names, [1] frame numbers and [0] extensions
    currentFrame = int(seqMin)
    current = 0
    newFrames = [[],[],[]]
    for i in exrRenamed:
        # Adding 0s in front of the current frame if it is not in <f4> format
        exrRenamed[current][1] = str(currentFrame).zfill(4)
        # Appending the values to a new list        
        newFrames[0].append(exrRenamed[current][0])
        newFrames[1].append(exrRenamed[current][1])
        newFrames[2].append(exrRenamed[current][2])
        #print(newFrames[0][current], newFrames[1][current], newFrames[2][current])
        currentFrame += 1
        current += 1
        
    # Joining the newFrames
    current = 0
    sequenceExr = []
    for i in newFrames[0]:
        sequenceExr.append((str(newFrames[0][current])) + "." + (str(newFrames[1][current])) + "." + (str(newFrames[2][current])))  
        current += 1
    
    # Adding back the path before the actual files
    current = 0
    listPath = []
    for i in exrPathSplitted[:-1]:
        listPath.append(exrPathSplitted[current])
        listPath.append("/")
        current += 1
    
    # Joining the path items
    finalPath = "".join(listPath)
    
    
    print("Finished programming the batch sequence, writing the output...")
    
    # Writing the path to the exr in a text file for later referencing
    outExr = open("00_ChosenExr.json", "w")
    current = 0
    for i in sequenceExr:
        outExr.write(finalPath + sequenceExr[current] + "\n")
        current += 1
    outExr.close
    
    print("DONE writing the batch sequence output")
    
    
if __name__ == "__sequenceBatch__":
    sequenceBatch(exrPath, seqMin, seqMax)