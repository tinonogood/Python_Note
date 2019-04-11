def longestCommonPrefix(strings):
	substring = min(strings, key=len)
	for i in strings:
		while i[len(substring)-1] != substring[-1]:
			substring = substring[:-1]
			if len(substring) == 0:
				return ""

	return substring

assert longestCommonPrefix(["flower","flow","flight"]) == "fl", 'Fail'
assert longestCommonPrefix(["dog","racecar","car"]) == "", 'Fail'

