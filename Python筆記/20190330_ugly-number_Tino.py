class Solution:

	def uglyNumber(self, n):
		if n <= 1 or n > 2**31-1:
			return False

		if n==2 or n==3 or n==5:
			return True

		if n % 2 == 0:
			n //= 2
			return self.uglyNumber(n)
		if n % 3 == 0:
			n //= 3
			return self.uglyNumber(n)
		if n % 5 == 0:
			n //= 5
			return self.uglyNumber(n)		
		return False

if __name__ == '__main__':
	sol = Solution()
	assert sol.uglyNumber(6) is True, 'Fail'
	assert sol.uglyNumber(14) is False, 'Fail'

