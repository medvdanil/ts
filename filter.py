def all_valid(fname, foname):
    f = open(fname, "r")
    fo = open(foname, "w")
    line=f.readline();
    while(line):
        tk = line.split(',')
        b = 1
        for i in range(6, len(tk)):
            if(tk[i] == '-1' or tk[i] == '0'):
                b = 0
        if(b == 1):
            fo.write(line)
        line=f.readline()