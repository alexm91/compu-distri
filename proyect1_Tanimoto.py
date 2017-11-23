import time
import threading
import math

f = open('ZINC_chemicals.tsv', 'r')
chemicals = []
chemicals_name = []
f.readline()
for letter in f:
    chemical_compounds = letter.split('\t')
    chemicals.append(chemical_compounds[3])
    chemicals_name.append(chemical_compounds[1])
f.close()


def get_elements(chemical):
    elements = {}
    for element in chemical:
        if elements.has_key(element):
            elements[element] = elements[element] + 1
        else:
            elements[element] = 1
    if elements.has_key('\n'):
        elements.pop('\n')
    if elements.has_key('('):
        elements.pop('(')
    if elements.has_key(')'):
        elements.pop(')')
    if elements.has_key('['):
        elements.pop('[')
    if elements.has_key(']'):
        elements.pop(']')
    if elements.has_key('{'):
        elements.pop('{')
    if elements.has_key('}'):
        elements.pop('}')
    if elements.has_key('/'):
        elements.pop('/')
    if elements.has_key('\\'):
        elements.pop('\\')
    if elements.has_key('='):
        elements.pop('=')
    if elements.has_key('+'):
        elements.pop('+')
    if elements.has_key('-'):
        elements.pop('-')
    if elements.has_key('1'):
        elements.pop('1')
    if elements.has_key('2'):
        elements.pop('2')
    if elements.has_key('3'):
        elements.pop('3')
    if elements.has_key('4'):
        elements.pop('4')
    if '@' in elements is False:
        return elements
    elif elements.get('@') == 1:
        return elements
    else:
        elements['@'] = 1
        return elements


def count_elements(elements):
    num_elements = elements.values()
    total_elements = 0
    for i in range(len(elements)):
        total_elements = total_elements + num_elements[i]
    return float(total_elements)


def equal_elements(chemical_a, chemical_b):
    nc = []
    total_equals = 0
    key_chemical_a = chemical_a.keys()
    key_chemical_b = chemical_b.keys()
    num_chemical_a = chemical_a.values()
    num_chemical_b = chemical_b.values()
    for i in range(len(key_chemical_a)):
        for j in range(len(key_chemical_b)):
            if key_chemical_a[i] == key_chemical_b[j]:
                if num_chemical_a[i] <= num_chemical_b[j]:
                    nc.append(num_chemical_a[i])
                else:
                    nc.append(num_chemical_b[j])
                break
    for i in range(len(nc)):
        total_equals = total_equals + nc[i]
    return float(total_equals)


def coefficient_jt(a, b):
    chemical_a = get_elements(a)
    chemical_b = get_elements(b)
    na = count_elements(chemical_a)
    nb = count_elements(chemical_b)
    nc = equal_elements(chemical_a, chemical_b)
    return round(nc/(na+nb-nc), 2)


def matrix_fill(ini, fin, coefficients):
    for i in range(ini, fin):
        for j in range(0, n):
            if i < j:
                T = coefficient_jt(chemicals[i], chemicals[j])
                coefficients.append(chemicals_name[i])
                coefficients.append(chemicals_name[j])
                coefficients.append(T)
    return coefficients


coe1 = []
coe2 = []
coe3 = []
coe4 = []

n = len(chemicals)
n1 = int(((2-(math.sqrt(3)))/2)*n)
n2 = int(((2-(math.sqrt(2)))/2)*n)
n3 = n/2

start = time.time()
t1 = threading.Thread(target=matrix_fill, args=(0, n1, coe1))
t2 = threading.Thread(target=matrix_fill, args=(n1+1, n2, coe2))
t3 = threading.Thread(target=matrix_fill, args=(n2+1, n3, coe3))
t4 = threading.Thread(target=matrix_fill, args=(n3+1, n, coe4))

t1.start()
t2.start()
t3.start()
t4.start()

t1.join()
t2.join()
t3.join()
t4.join()

time_threads = time.time()

print len(coe1)/3
print len(coe2)/3
print len(coe3)/3
print len(coe4)/3

coe = coe1 + coe2 + coe3 + coe4
data = open('data.txt', 'w')
data.write('Chemical A\tChemical B\tTanimoto Coefficient\n')
for i in range(0, len(coe), 3):
    data.write(coe[i] + '\t' + coe[i+1] + '\t' + str(coe[i+2]) + '\n')
data.close()

end = time.time()
total_threads = time_threads-start
total = end-start
print 'Time Threads = ' + str(total_threads)
print 'Total Execution = ' + str(total)
