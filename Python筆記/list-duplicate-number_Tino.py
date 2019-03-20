class Solution:
	def checkDuplicate(self, list, interval):
		if len(list) <= interval:
			interval = len(list)-1

		for i in range(len(list)-interval):
			checkList = list[i:i+interval+1]
			if len(set(checkList)) != len(checkList):
				return True

		return False

if __name__ == '__main__':
    sol = Solution()
    assert sol.checkDuplicate([1,2,3,1,5],2) is False, 'Fail'
    assert sol.checkDuplicate([1,2,3,1,5],5) is True, 'Fail'
    assert sol.checkDuplicate([1,2,3,1,5],3) is True, 'Fail'
