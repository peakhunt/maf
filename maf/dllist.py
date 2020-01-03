"""
Minimum Doubly Linked List implementation for MycroPython

Python List seems quite inefficient for micro controller use. That's why.

"""

class ListHead(object):
  def __init__(self):
    """ initialize a list head """
    self.next = None
    self.prev = None
    self.item = None

  def add_list(self, p, n):
    """ add self between p and n """
    n.prev    = self
    self.next = n
    self.prev = p
    p.next    = self

  def del_list(self):
    """ remove self from a list """
    p = self.prev
    n = self.next

    n.prev = p
    p.next = n

    self.next = None
    self.prev = None


"""
 DO NOT

 a) add while iterating
"""
class DLList(object):
  def __init__(self):
    """ initialize a doubly linked list """
    self.head = ListHead()
    self.head.next = self.head
    self.head.prev = self.head
    self.current = None

  def add_head(self, n):
    """ add a list head item to the head of the list """
    n.add_list(self.head, self.head.next)

  def add_tail(self, n):
    """ add a list head item to the tail of the list """
    n.add_list(self.head.prev, self.head)

  def del_list(self, n):
    """ remove a list head item from the list """
    # is this really gonna be ok with removal during iteration?
    if n == self.current:
      self.current = n.next

    n.del_list()

  def is_empty(self):
    """ check if list item is empty """
    return self.head.next == self.head

  def first(self):
    """ return first list head item """
    return self.head.next

  def __iter__(self):
    """ prepare to begin iteration """
    self.current = self.head.next
    return self

  def next(self):
    return self.__next__()

  def __next__(self):
    """ return next item while iteration """
    if self.current != self.head:
      r = self.current
      self.current = self.current.next
      return r
    else:
      raise StopIteration

"""
if __name__ == "__main__":
  print("starting test...")

  l = DLList()
  assert l.is_empty() == True, "Error: list is not empty after creation"
  print("list creation done!")

  for x in range(10):
    i = ListHead()
    i.item = x

    l.add_tail(i)

  print("added items done")
  assert l.is_empty() == False, "Error: list is empty after additions"

  print("iteration test")
  expected = 0
  for x in l:
    v = x.item
    assert v == expected, "Error: item mismatch"
    expected += 1

  print("remove test")
  expected = 0
  while l.is_empty() != True:
    assert expected < 10, "Error: expected >= 10"
    x = l.first()
    assert x.item == expected, "Error: list remove fail"
    l.del_list(x)
    expected += 1

  #unfortunately removing while iteration isn't handy in python
  print("removing while iteration")
  for x in range(10):
    i = ListHead()
    i.item = x

    l.add_tail(i)

  l2 = DLList()
  for x in l:
    if (x.item > 3 and x.item < 7) or x.item == 0 or x.item == 9:
      l.del_list(x)
      l2.add_tail(x)

  e = [1, 2, 3, 7, 8]
  ndx = 0
  for x in l:
    assert x.item == e[ndx], "Error: weird item in the list after removal during iteration"
    print('l ' + str(ndx) + ' : ' + str(x.item))
    ndx += 1

  e = [0, 4, 5, 6, 9]
  ndx = 0
  for x in l2:
    assert x.item == e[ndx], "Error: weird item in the list after removal during iteration"
    print('l2 ' + str(ndx) + ' : ' + str(x.item))
    ndx += 1
"""
