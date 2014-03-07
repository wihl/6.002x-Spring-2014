import pylab

def producePlot(lowTemps, highTemps):
        diffTemps = [h - l for h, l in zip(highTemps, lowTemps)]
        pylab.plot(range(1,32), diffTemps)
        pylab.title('Day by Day Ranges in Temperature in Boston in July 2012')
        pylab.xlabel('Days')
        pylab.ylabel('Temperature Ranges')
        pylab.show()

lowTemps = []
highTemps = []
f = open('julyTemps.txt', 'r')
for line in f:
        fields = line.split(' ')
        #print "fields[0]", fields[0]
        #print fields, len(fields)
        
        if len(fields) < 3 or not fields[0].isdigit():
                pass
        else:
                lowTemps.append(int(fields[2]))
                highTemps.append(int(fields[1]))

producePlot(lowTemps, highTemps)
                
