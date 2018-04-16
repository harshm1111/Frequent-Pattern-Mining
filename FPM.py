# Enter your code here. Read input from STDIN. Print output to STDOUT
import argparse
from itertools import chain, combinations
import operator
import math


def joinset(itemset, k):
    return set([i.union(j) for i in itemset for j in itemset if len(i.union(j)) == k])


def subsets(itemset):
    return chain(*[combinations(itemset, i + 1) for i, a in enumerate(itemset)])


def itemset_from_data(data):
    itemset = set()
    transaction_list = list()
    for row in data:
        transaction_list.append(frozenset(row))
        for item in row:
            if item:
                itemset.add(frozenset([item]))
    return itemset, transaction_list


def itemset_support(transaction_list, itemset, min_support=0):
    len_transaction_list = len(transaction_list)
    l = [
        (item, float(sum(1 for row in transaction_list if item.issubset(row)))/len_transaction_list)
        for item in itemset
    ]
    return dict([(item, support) for item, support in l if support >= min_support])


def freq_itemset(transaction_list, c_itemset, min_support):
    f_itemset = dict()

    k = 1
    while True:
        if k > 1:
            c_itemset = joinset(l_itemset, k)
        l_itemset = itemset_support(transaction_list, c_itemset, min_support)
        if not l_itemset:
            break
        f_itemset.update(l_itemset)
        k += 1

    return f_itemset


def apriori(data, min_support, min_confidence):
    # Get first itemset and transactions
    itemset, transaction_list = itemset_from_data(data)

    # Get the frequent itemset
    f_itemset = freq_itemset(transaction_list, itemset, min_support)

    # Association rules
    rules = list()
    for item, support in f_itemset.items():
        if len(item) > 1:
            for A in subsets(item):
                B = item.difference(A)
                if B:
                    A = frozenset(A)
                    AB = A | B
                    confidence = float(f_itemset[AB]) / f_itemset[A]
                    if confidence >= min_confidence:
                        rules.append((A, B, confidence))
    return rules, f_itemset



def generate_closed(frequent_dataset):
    output = {}

    for i in range(len(frequent_dataset)):
        current_element = frequent_dataset[i][0]
        current_support = frequent_dataset[i][1]
        current_list = frequent_dataset[:i] + frequent_dataset[i+1 :]

        counts = 0

        for each in current_list:
            temp_count = 0
            temp_support = each[1]
            temp_element = each[0]
            for items in current_element:
                if items in temp_element:
                    temp_count += 1

            if temp_count == len(current_element) and current_support <= temp_support:
                counts += 1


        if counts == 0:
            output[current_element] = current_support


    return output


def print_report(rules, f_itemset, input_length):
    dicts = {}
    for item, support in sorted(f_itemset.items(), key=lambda (item, support): support):
        dicts[tuple(sorted(list(item)))] = int(math.ceil(support*input_length))

    frequent_list = []

    for k,v in sorted(dicts.items(),key=lambda x:(-x[1],x[0])):
        a = str(v) + " " + str([' '.join(k).strip()])
        frequent_list.append([k, v])
        print a.replace("'", "")

    print ""
    outputs =  generate_closed(frequent_list)
    for k,v in sorted(outputs.items(),key=lambda x:(-x[1],x[0])):
        a = str(v) + " " + str([' '.join(k).strip()])
        print a.replace("'", "")


def data_from_csv(filename):
    f = open(filename, 'rU')
    for l in f:
        row = map(str.strip, l.split(','))
        print row
        yield row


def main():
    support = int(raw_input())
    input_data = []

    while True:
        try:
            temp = raw_input()
            if temp:
                input_data.append(temp.split())
        except EOFError:
            break;

    min_support = float(support)/(len(input_data) * 1.0)
    data = input_data
    rules, itemset = apriori(data, min_support, 0.8)
    print_report(rules, itemset, len(input_data))


if __name__ == '__main__':
    main()
