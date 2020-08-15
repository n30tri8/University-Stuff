items = ['A', 'B', 'C', 'D', 'E']
support_threshold = 2
confidence_threshold = 1.0


def support_count(item_set_param):
    s = 0
    for t in transactions:
        match = True
        for _item in item_set_param:
            if _item not in t:
                match = False
                break
        if match:
            s += 1
    return s


def hash_item_set(item_set_param):
    string = ''
    for _item in item_set_param:
        string += str(_item)
    return string


def confidence(rule_support, rule_cause_param):
    s = 0
    for t in transactions:
        match = True
        for _item in rule_cause_param:
            if _item not in t:
                match = False
                break
        if match:
            s += 1
    return rule_support/s


def generate_rules():
    confident_rules = dict()
    for k_set in frequent_item_sets:
        for frequent_item_set in k_set:
            if len(frequent_item_set) < 2:
                continue

            confident_rules[hash_item_set(frequent_item_set)] = dict()
            current_set_support = support_count(frequent_item_set)
            current_rules = list()
            current_rules_hash = set()
            # generate 1-item set in consequent
            current_rules.append(list())
            for idx in range(len(frequent_item_set)):
                item_set = frequent_item_set.copy()
                item_set.pop(idx)

                item_set_hash = hash_item_set(item_set)
                if item_set_hash not in current_rules_hash:
                    if confidence(current_set_support, item_set) >= confidence_threshold:
                        current_rules[0].append(item_set)
                        current_rules_hash.add(item_set_hash)

            for k in range(1, len(frequent_item_set) - 1):
                current_rules.append(list())
                for k_minus_one in current_rules[k - 1]:
                    for idx in range(len(k_minus_one)):
                        item_set = k_minus_one.copy()
                        item_set.pop(idx)

                        item_set_hash = hash_item_set(item_set)
                        if item_set_hash not in current_rules_hash:
                            if confidence(current_set_support, item_set) >= confidence_threshold:
                                current_rules[k].append(item_set)
                                current_rules_hash.add(item_set_hash)
                if len(current_rules[k]) == 0:
                    current_rules.pop()
                    break

            confident_rules[hash_item_set(frequent_item_set)]['item set'] = frequent_item_set
            confident_rules[hash_item_set(frequent_item_set)]['rule list'] = current_rules
    return confident_rules


def list_diff(li1, li2):
    li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
    return li_dif


transactions = list()

transactions.append(['A', 'C', 'D'])
transactions.append(['B', 'C', 'E'])
transactions.append(['A', 'B', 'C', 'E'])
transactions.append(['B', 'E'])

frequent_item_sets = list()
frequent_item_sets_hash = set()
# generate 1-frequent item set
frequent_item_sets.append(list())
for item in items:
    item_set = list()
    item_set.append(item)

    item_set_hash = hash_item_set(item_set)
    if item_set_hash not in frequent_item_sets_hash:
        if support_count(item_set) >= support_threshold:
            frequent_item_sets[0].append(item_set)
            frequent_item_sets_hash.add(item_set_hash)


for k in range(1, len(items)):
    frequent_item_sets.append(list())
    for k_minus_one in frequent_item_sets[k - 1]:
        for one_item_set in frequent_item_sets[0]:
            if one_item_set[0] in k_minus_one:
                continue
            k_item_set = k_minus_one.copy()
            k_item_set.append(one_item_set[0])
            k_item_set.sort()

            item_set_hash = hash_item_set(k_item_set)
            if item_set_hash not in frequent_item_sets_hash:
                if support_count(k_item_set) >= support_threshold:
                    frequent_item_sets[k].append(k_item_set)
                    frequent_item_sets_hash.add(item_set_hash)
    if len(frequent_item_sets[k]) == 0:
        frequent_item_sets.pop()
        break

# output
output = open('.\\outputs\\q1\\section2_results.txt', 'w')
# a
output.write('a.\n')
for freq_set in frequent_item_sets:
    for freq in freq_set:
        output.write(str(freq) + '\n')
output.write('---------------------------------\n')
# b
output.write('b.\n')
# rule generation
confidence_threshold = 0.65
confident_65 = generate_rules()
number = 0
for key in confident_65:
    frequent_item = confident_65[key]['item set']
    for rule_set in confident_65[key]['rule list']:
        for rule_cause in rule_set:
            consequent = list_diff(frequent_item, rule_cause)
            output.write(str(rule_cause) + '=>' + str(consequent) + '\n')
            number += 1
output.write('number of rules: ' + str(number) + '\n')
output.write('---------------------------------\n')
# c
output.write('c.\n')
# rule generation
confidence_threshold = 0.8
confident_8 = generate_rules()
for key in confident_8:
    frequent_item = confident_8[key]['item set']
    for rule_set in confident_8[key]['rule list']:
        for rule_cause in rule_set:
            consequent = list_diff(frequent_item, rule_cause)
            output.write(str(rule_cause) + '=>' + str(consequent) + '\n')
output.write('---------------------------------\n')
# d
output.write('d.\n')
numerator = ['C', 'E']
denominator = ['E']
result = support_count(numerator) / support_count(denominator)
output.write(str(result) + '\n')
output.write('---------------------------------\n')
# e
output.write('e.\n')
numerator = ['B', 'C']
denominator = ['B']
result = support_count(numerator) / support_count(denominator)
output.write(str(result) + '\n')
output.write('---------------------------------\n')


