import numpy
import argparse

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
    return numpy.array(res)

def gradient_descent(x, y, a=numpy.array([]), step0=1000.0):
    if(len(a) == 0):
        a = numpy.array([1.0]*len(x[0]))
    else:
        a = numpy.array(a)
    step = step0
    v = 1.0
    daold = numpy.array([0.0]*len(a))
    while v > 0.00001:
        da = delJ(a, x, y)
        #da = da/numpy.sqrt(numpy.sqrt(numpy.dot(da, da)))
        v = step
        vlen = numpy.dot(da, da)
        if(vlen > 0.00001):
            da = da/numpy.sqrt(vlen)

        print(str(a)+ str(da)+ str(step)+" v:"+ str(v))
        a = a - da*numpy.sqrt(step)
        #if(numpy.dot(da, daold)<0):
        step /= 1.005
        #else:
         #   step *= 1.1
        daold = da
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
    a = gradient_descent(x, y, a, 10)

    f = open(ftest, "r")
    line=f.readline();
    sumsq = 0
    i = 0
    while(line):
        tk = line.split(',')
        t = numpy.array([float(tk[3]),float(tk[6]), float(tk[7]), float(tk[8]), 1.0])
        #print(str([float(tk[-1]), numpy.dot(a, t)]))
        sumsq = sumsq + (float(tk[-1])-numpy.dot(a, t))**2
        i = i + 1
        line=f.readline()
    print(str(a))
    print("Standard deviation: " + str(numpy.sqrt(sumsq/i)))
    f.close()


def parse_args():
    parser = argparse.ArgumentParser(description='Linear regression method of gradient descent\nFinding number of friends')
    parser.add_argument('learn_path', nargs=1)
    parser.add_argument('test_path', nargs=1)
    return parser.parse_args()

def main():
    args = parse_args()
    friends(args.learn_path[0], args.test_path[0])

if __name__ == "__main__":
    main()