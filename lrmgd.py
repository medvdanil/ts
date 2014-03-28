import numpy

def delJ(a, x, y):
    res = []
    tmp = []
    for j in range(0, len(x)):
        s = 0
        for i in range(0, len(x[j])):
            s += x[j][i]*a[i];
        tmp.append(s - y[j])

    for i in range(0, len(a)):
        s = 0
        for j in range(0, len(x)):
            s += 2*x[j][i]*tmp[j]
        res.append(s)
    return numpy.array(res)/numpy.sqrt(numpy.dot(numpy.array(res), numpy.array(res)))

def delJ2(a, x, y):
    res = [2*a[0], 2*a[1]]
    return numpy.array(res)
def gradient_descent(x, y, a=numpy.array([])):
    if(not a):
        a = numpy.array([1.0]*len(x[0]))
    step = 10000.0
    v = 1.0
    i = 1
    while v > 0.0001:
        da = delJ(a, x, y)
        #print(str(a), str(da))
        v = numpy.dot(da, da)*step
        a = a - da*step
        step /= 1.1
    return a
def friends(flearn, ftest):
    f = open(flearn, "r")
    x = []
    y = []
    line=f.readline();
    while(line):
        tk = line.split(',')
        x.append([float(tk[3]),float(tk[6]), float(tk[7]), float(tk[8]), 1.0])
        y.append(float(tk[-1]))
        line=f.readline()
    f.close()
    print(str(x))
    a = gradient_descent(x, y)

    f = open(ftest, "r")
    line=f.readline();
    sumsq = 0
    i = 0
    while(line):
        tk = line.split(',')
        t = numpy.array([float(tk[3]),float(tk[6]), float(tk[7]), float(tk[8]), 1.0])
        print(str([float(tk[-1]), numpy.dot(a, t)]))
        sumsq = sumsq + (float(tk[-1])-numpy.dot(a, t))**2
        i = i + 1
        line=f.readline()
    print(str(a))
    print("Standard deviation: " + str(numpy.sqrt(sumsq/i)))
    f.close()