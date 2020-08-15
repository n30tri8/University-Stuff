from datetime import datetime


C = {}
OCC = {}
Last = []


def bwt(s):
    l = len(s)
    SA = sorted(s[i:] for i in range(l))
    print('passed SA creation')
    Last = [s[l-len(row)-1] for row in SA]

    # constructing C{} and OCC{}
    C = {}
    OCC = {}
    idx = 0
    for row in SA:
        if row[0] not in C:
            C[row[0]] = idx
            OCC[row[0]] = []
            occurances = 0
            for q in range(len(Last)):
                if Last[q] == row[0]:
                    occurances += 1
                OCC[row[0]].append(occurances)              
        idx += 1

    return C, OCC, Last


if __name__ == "__main__":
    input_file = open('./EcoliGenome.fa', 'r')
    ecoli = input_file.readline()
    input_file.close()

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)

    # C, OCC, Last = bwt('GATGCGAGAGATG$')
    C, OCC, Last = bwt(ecoli)
    
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)

    output = open('bwt-ecoli.txt', 'w')
    output.write("".join(Last))
    output.close()

    output = open('bwt-ecoli-c.txt', 'w')
    output.write(str(C))
    output.close()

    output = open('bwt-ecoli-occ.txt', 'w')
    output.write(str(OCC))
    output.close()