class MyCircularQueue:

    def __init__(self, k: int):
        """
        Initialize your data structure here. Set the size of the queue to be k.
        """
        self.queue = []
        self.head = 0
        self.tail = 0
        self.maxSize = k
        self.tagSize = k+1

    def enQueue(self, value: int) -> bool:
        """
        Insert an element into the circular queue. Return true if the operation is successful.
        """
        if self.isFull():
            return False
        else:
            self.tail += 1
            self.tail %= self.tagSize
            self.queue.append(value)
            return True
        

    def deQueue(self) -> bool:
        """
        Delete an element from the circular queue. Return true if the operation is successful.
        """
        if self.isEmpty():
            return False
        else:
            self.head += 1
            self.head %= self.tagSize
            self.queue.pop(0)
            return True
        

    def Front(self) -> int:
        """
        Get the front item from the queue.
        """
        if self.isEmpty():
            return -1
        return self.queue[0]

    def Rear(self) -> int:
        """
        Get the last item from the queue.
        """
        if self.isEmpty():
            return -1
        return self.queue[-1]

    def isEmpty(self) -> bool:
        """
        Checks whether the circular queue is empty or not.
        """
        return self.head - self.tail == 0

    def isFull(self) -> bool:
        """
        Checks whether the circular queue is full or not.
        """
        return self.tail - self.head == -1 or self.tail - self.head == self.maxSize


if __name__ == '__main__':
    obj = MyCircularQueue(3)
    act_1 = obj.enQueue(1)
    assert act_1 == True, 'Fail'
    assert obj.Front() == 1, 'Fail'
    assert obj.Rear() == 1, 'Fail'

    act_2 = obj.enQueue(2)
    assert obj.Rear() == 2, 'Fail'  
    act_3 = obj.enQueue(3)
    print(obj.head,obj.tail,obj.queue)
    assert obj.isFull() == True, 'Fail'
    assert obj.Rear() == 3, 'Fail'
    assert obj.Front() == 1, 'Fail'

    act_4 = obj.deQueue()
    assert act_4 == True, 'Fail'
    assert obj.Front() == 2, 'Fail' 
    act_5 = obj.deQueue()
    act_6 = obj.deQueue()
    assert obj.isEmpty() == True, 'Fail'



# Your MyCircularQueue object will be instantiated and called as such:
# obj = MyCircularQueue(k)
# param_1 = obj.enQueue(value)
# param_2 = obj.deQueue()
# param_3 = obj.Front()
# param_4 = obj.Rear()
# param_5 = obj.isEmpty()
# param_6 = obj.isFull()
