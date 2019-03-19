class Solution:
	def sumReversedList(self, list1, list2):

		maxLength = max(len(list1),len(list2))
		list1 += [0] * (maxLength - len(list1))
		list2 += [0] * (maxLength - len(list2))

		carry = 0
		answer = []

		for i in range(maxLength):
			bit_sum = list1[i] + list2[i] + carry
			answer.append(bit_sum%10)
			carry = bit_sum//10
		return answer


if __name__ == '__main__':
    sol = Solution()
    assert sol.sumReversedList([1,2,3], [4,5,8,4]) == [5,7,1,5], 'Fail'