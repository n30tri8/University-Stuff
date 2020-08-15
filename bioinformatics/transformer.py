C = {}
OCC = {}
Last = []
SA = []


def bwt(s):
    s += '$'
    l = len(s)
    SA = sorted(s[i:] for i in range(l))

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

    return C, OCC, "".join(Last), SA


# def next_char(char):
#     # if char == 'i':
#     #     return 'm'
#     # elif char == 'm':
#     #     return 'p'
#     # elif char == 'p':
#     #     return 's'
#     # else:
#     #     print('undefined next char')
#     #     return ''

#     if char == 'a':
#         return 'c'
#     elif char == 'c':
#         return 'g'
#     elif char == 'g':
#         return 't'
#     else:
#         print('undefined next char')
#         return ''


def backward_search(pattern):
    bot = 1
    top = len(Last) - 1
    pos = len(pattern) - 1
    while pos > -1:
        c = pattern[pos]
        bot = C[c] + OCC[c][bot-1]
        top = C[c] + OCC[c][top]-1
        if top < bot:
            break
        pos -= 1
    
    return bot, top


# def backward_search(pattern):
#     i = len(pattern)
#     pattern = '\1' + pattern
#     c = pattern[i]
#     first = C[c] + 1
#     last = C[next_char(c)]

#     while (first <= last) and i >= 2:
#         c = pattern[i - 1]
#         first = C[c] + OCC[c][first - 1] + 1
#         last = C[c] + OCC[c][last]
#         i = i - 1

#     if last < first:
#         return 'no rows prefixed by  pattern', 'no rows prefixed by  pattern'
#     else:
#         return first, last


if __name__ == "__main__":
    C, OCC, Last, SA = bwt('GATGCGAGAGATG'.lower())
    print('BWT: ' + Last)
    print('C matrix:')
    print(C)
    print('OCC matrix:')
    print(OCC)
    f, l = backward_search('GAT'.lower())
    # print(f)
    print('number of pattern matches:')
    print(l-f+1)
    print('pattern matches:')
    i = f
    while i <= l:
      print(SA[i])
      i += 1