import datetime


def getImagePathTailHdf5Mod(dateTime,labelIn):
    mod = round(dateTime.microsecond/10000)
    pathTail = labelIn+"/"+\
    str(dateTime.year).zfill(4) + \
    "_" +str(dateTime.month).zfill(2) + \
    "_" +str(dateTime.day).zfill(2)+ \
    "_" +str(dateTime.hour).zfill(2) + \
    "_" +str(dateTime.minute).zfill(2)+ \
    "_" +str(dateTime.second).zfill(2)+ \
    "_" +str(mod).zfill(2)+ \
    "_"+labelIn+".h5"

    return pathTail;

while(True):
    dateTime = datetime.datetime.now()  
    # print(dateTime)
    if(round(dateTime.microsecond/10000))%20==0:
        print(getImagePathTailHdf5Mod(dateTime,"LK"))
