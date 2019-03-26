class Solution:
	def roman2Int(self, s):
		integer = s.count("I") + s.count("V")*5  + s.count("X")*10  + s.count("L")*50  + s.count("C")*100  + s.count("D")*500  + s.count("M")*1000 
		
		if "IV" in s:
			integer -= 2		
		if "IX" in s:
			integer -= 2
		if "XL" in s:
			integer -= 20		
		if "XC" in s:
			integer -= 20		
		if "CD" in s:
			integer -= 200		
		if "CM" in s:
			integer -= 200
		
		return integer

if __name__ == '__main__':
	sol = Solution()
	assert sol.roman2Int("IX") == 9, 'Fail'