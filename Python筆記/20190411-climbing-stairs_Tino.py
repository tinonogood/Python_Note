def recur(n):
	result = 0
	if n==1 or n==0:
		result=1
	else:
		result= n*recur(n-1)
	return result

def climbing_stairs(num):
	combination = 0
	a = num//2
	b = num%2
	while a >= 0:
		combination +=recur(a+b) / (recur(a)*recur(b))
		a -= 1
		b += 2
	return combination


assert climbing_stairs(1) == 1, 'Fail'
assert climbing_stairs(2) == 2, 'Fail'
assert climbing_stairs(3) == 3, 'Fail'
assert climbing_stairs(4) == 5, 'Fail'
assert climbing_stairs(5) == 8, 'Fail'
assert climbing_stairs(6) == 13, 'Fail'
assert climbing_stairs(45) == 1836311903, 'Fail'