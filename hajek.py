#!/usr/bin/python
import sys
from math import sqrt, pi
from operator import itemgetter
from optparse import OptionParser


def xuniqueCombinations(items, n):
    if n==0: yield []
    else:
        for i in xrange(len(items)-n+1):
            for cc in xuniqueCombinations(items[i+1:],n-1):
                yield [items[i]]+cc


def get_data(filename):
    g=10**-3
    data = sorted([line.strip().split() for line in file(filename)], key=itemgetter(0))
    return [[float(i[0]), float(i[1])*g] for i in data]


def calculate(comb):
    x1 = comb[0][0]
    x2 = comb[1][0]
    x3 = comb[2][0]

    r1 = comb[0][1]
    r2 = comb[1][1]
    r3 = comb[2][1]



    r0s = (x1-x3)/(((r2**2 - r1**2)/(x2 - x1) - (r3**2 - r2**2)/(x3 - x2)))
    x0 = (x1 + x2)/2.0  - (r0s/2.0)*(r2**2-r1**2)/(x2-x1)
    w = wavelength*sqrt(r0s)/pi
    return (x0, w)




def main():
    usage = "usage: %prog [options] input_file"
    description = "Waist finding program"
    parser = OptionParser(usage=usage, description=description)
    parser.set_defaults(freq=.85209, solver="0")
    parser.add_option("-f", "--freq", help="set frequency of laser in nm", type="float")
    (options, args) = parser.parse_args()
    return (options, args)
    
def show_plot():
    return True

if __name__ == "__main__":
    options, args = main()
    wavelength = options.freq
    data = get_data(args[0])
    results = []
    
    for comb in xuniqueCombinations(data, 3):
        results.append(calculate(comb))


    zsum = wsum = 0
    for r in results:
        zsum += r[0]
        wsum += r[1]
        print round(r[0],1), round(r[1],2)

  
    z = zsum/len(results)
    w = wsum/len(results)
    print "----------------"
    print "Mean waist results"
    print  "Position: %s mm  Size: %s um" % (round(z,1), round(w,2) )
