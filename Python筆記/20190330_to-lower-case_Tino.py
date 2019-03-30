class Solution:
	def toLowerCase(self, str):
		new_str = ""
		for i in str:
			if  64 < ord(i) < 91:
				new_str += chr(ord(i)+32)
			else:
				new_str += i
		return new_str




if __name__ == '__main__':
	sol = Solution()
	assert sol.toLowerCase("AaaZB") == "aaazb", 'Fail'
	assert sol.toLowerCase("") == "", 'Fail'