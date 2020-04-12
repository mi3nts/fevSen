import datetime

def getImagePathTailHdf5Mod2(dateTime,labelIn):
 
    pathTail = labelIn+"/"+\
    str(dateTime.year).zfill(4) + \
    "_" +str(dateTime.month).zfill(2) + \
    "_" +str(dateTime.day).zfill(2)+ \
    "_" +str(dateTime.hour).zfill(2) + \
    "_" +str(dateTime.minute).zfill(2)+ \
    "_" +str(dateTime.second).zfill(2)+ \
    "_" +str(dateTime.microsecond)[1]+ \
    "_"+labelIn+".h5"

    return pathTail;

while(True):
    dateTime = datetime.datetime.now()  
    print(getImagePathTailHdf5Mod2(dateTime,"LK"))
