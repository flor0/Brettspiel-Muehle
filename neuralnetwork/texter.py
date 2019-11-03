file = open("haha.txt", "w")
_file = open("hahaha.txt", "w")

n = 0
for a in range(3):
    for b in range(8):
        file.write("{}: ({}, {}),\n".format(n, a, b))
        _file.write("({}, {}): {},\n".format(a, b, n))
        n += 1

for a in range(3):
    for b in range(8):
        for c in range(3):
            for d in range(8):
                if a == c and b == d:
                    pass
                else:
                    file.write("{}: [({}, {}), ({}, {})],\n".format(n, a, b, c, d))
                    _file.write("[({}, {}), ({}, {})]: {},\n".format(a, b, c, d, n))
                    n += 1

for a in range(3):
    for b in range(8):
        for c in range(3):
            for d in range(8):
                for e in range(3):
                    for f in range(8):
                        if (a == c and b == d) or (a == e and b == f) or (c == e and d == f):
                            pass
                        else:
                            file.write("{}: [({}, {}), ({}, {}), ({}, {})],\n".format(n, a, b, c, d, e, f))
                            _file.write("[({}, {}), ({}, {}), ({}, {})]: {},\n".format(a, b, c, d, e, f, n))
                            n += 1

file.close()
_file.close()