import afl
import sys

f = open('data','r')
data = f.read()
data = data.split("\n")[1:-1]
stdev = float(sys.argv[1])
print "Assuming stdev of {} degrees".format(stdev)
diffs = []
for datum in data:
    datum = datum.split(" ")
    datum = map(int, datum)
    angle, distance, chance = tuple(datum)
    modelled_chance = afl.probability(afl.difficulty(angle, distance), stdev)*100
    diff = chance - modelled_chance
    diffs.append(diff)
    print "{} deg @ {} m: ch9 {}%; afl.py {:.0f}% (difference {:.0f}%)".format(
        angle, distance, chance, modelled_chance, diff)
print diffs
abs_average = sum([abs(d) for d in diffs]) / len(diffs)
print "Average absolute discrepancy: {:.2f}".format(abs_average)
average = sum([d for d in diffs]) / len(diffs)
print "Average discrepancy: {:.2f}".format(average)
