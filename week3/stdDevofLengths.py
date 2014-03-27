
def stdDevOfLengths(L):
	N = len(L)
	if L is None or N == 0: return float('NaN')
	# compute mean
	tot = 0.0
	for l in L:
		tot += len(l)
	mean = tot / float(N)
	tot = 0.0
	for l in L:
		tot += (len(l) - mean)**2
	return (tot / N) ** 0.5

print "should be NaN", stdDevOfLengths("")
print "should be 0", stdDevOfLengths(['a','z','p'])
print "should be 1.8708", stdDevOfLengths(['apples','oranges','kiwis','pineapples'])
