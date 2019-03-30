class Solution:
	def gen_uglyNumber(self, n):
		x = n
		if x <= 1 or x > 2**31-1:
			return False
		if x==2 or x==3 or x==5:
			return True

		if x % 2 == 0:
			x //= 2
			return self.gen_uglyNumber(x)
		if x % 3 == 0:
			x //= 3
			return self.gen_uglyNumber(x)
		if x % 5 == 0:
			x //= 5
			return self.gen_uglyNumber(x)		
		return False

	def uglyNumber(self, i):
		gen_list = [1]
		count =1
		while len(gen_list) < i:
			count +=1
			gen_list.append(count)
			if self.gen_uglyNumber(count) is False:
				gen_list.pop()	
		return gen_list[-1]

if __name__ == '__main__':
	sol = Solution()
	assert sol.uglyNumber(5) == 5, 'Fail'
	assert sol.uglyNumber(10) == 12, 'Fail'
	assert sol.uglyNumber(13) == 18, 'Fail'
	assert sol.uglyNumber(52) == 256, 'Fail'