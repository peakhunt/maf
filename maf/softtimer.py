import maf.dllist as dllist

TIMER_NUM_BUCKETS = 8

class TimerElem(object):
  def __init__(self, cb, cb_arg):
    self.le       = dllist.ListHead()
    self.le.item  = self
    self.cb       = cb
    self.cb_arg   = cb_arg
    self.tick     = 0

  def is_running(self):
    if self.le.next != None and self.le.prev != None:
      return True
    return False

class Timer(object):
  def __init__(self, tick_rate):
    self.tick_rate  = tick_rate
    self.tick       = 0
    self.buckets    = [None] * TIMER_NUM_BUCKETS

    for i in range(TIMER_NUM_BUCKETS):
      self.buckets[i] = dllist.DLList()

  def __get_tick_from_msec(self, msec):
    tick = msec // self.tick_rate
    mod  = msec % self.tick_rate

    if mod != 0:
      tick += 1

    return tick

  def add_timer(self, elem, expires):
    if elem.is_running():
      assert True, "trying to add timer that is already running"
      return

    elem.tick = self.tick + self.__get_tick_from_msec(expires)
    head = self.buckets[elem.tick % TIMER_NUM_BUCKETS]

    head.add_tail(elem.le)

  def del_timer(self, elem):
    if not elem.is_running():
      assert True, "trying to delete timer that is not running"
      return

    elem.le.del_list()

  def drive(self):
    temp_list = dllist.DLList()

    self.tick += 1
    current = self.buckets[self.tick % TIMER_NUM_BUCKETS]

    for l in current:
      x = l.item
      if x.tick == self.tick:
        current.del_list(x.le)
        temp_list.add_tail(x.le)

    while temp_list.is_empty() == False:
      t = temp_list.first().item
      temp_list.del_list(t.le)
      t.cb(t.cb_arg)

"""
if __name__ == "__main__":
  tx_called = [ False, False, False, False ]
  print("creating a timer")
  timer = Timer(1)    # 1ms tick simulation

  def t1_callback(arg):
    print("t1_callback called")
    tx_called[0] = True

  def t2_callback(arg):
    print("t2_callback called")
    tx_called[1] = True

  def t3_callback(arg):
    print("t3_callback called")
    timer.add_timer(arg, 1)
    tx_called[2] = True

  def t4_callback(arg):
    print("t4_callback called")
    tx_called[3] = True

  print("starting test...")


  print("first a few test driver")
  timer.drive()
  timer.drive()
  timer.drive()

  print("adding a timer")
  t1 = TimerElem(t1_callback, None)

  assert t1.is_running() == False, "BUG: is_running() should be False"

  timer.add_timer(t1, 1)
  assert t1.is_running() == True, "BUG: is_running() should be True"
  assert tx_called[0] == False, "BUG: t1_callback called"

  timer.drive()
  assert tx_called[0] == True, "BUG: t1_callback not called"
  assert t1.is_running() == False, "BUG: t1 is still running"

  tx_called[0] = False

  t2 = TimerElem(t2_callback, None)

  timer.add_timer(t1, 1)
  timer.add_timer(t2, 2)

  # tick 1
  timer.drive()
  assert tx_called[0] == True, "BUG: t1_callback not called"
  assert tx_called[1] == False, "BUG: t2_callback called"

  timer.drive()
  assert tx_called[1] == True, "BUG: t2_callback not called"

  tx_called[0] = False
  tx_called[1] = False

  # cancel test
  print("Timer cancel test")
  timer.add_timer(t1, 3)
  timer.add_timer(t2, 5)

  # tick 1
  timer.drive()
  assert tx_called[0] == False, "BUG: t1_callback called"
  assert tx_called[1] == False, "BUG: t2_callback called"

  # tick 2
  timer.drive()
  assert tx_called[0] == False, "BUG: t1_callback called"
  assert tx_called[1] == False, "BUG: t2_callback called"

  timer.del_timer(t1)
  assert t1.is_running() == False, "BUG: t1 not cancelled"

  # tick 3
  timer.drive()
  assert tx_called[0] == False, "BUG: t1_callback called"
  assert tx_called[1] == False, "BUG: t2_callback called"

  # tick 4
  timer.drive()
  assert tx_called[0] == False, "BUG: t1_callback called"
  assert tx_called[1] == False, "BUG: t2_callback called"

  # tick 5
  timer.drive()
  assert tx_called[0] == False, "BUG: t1_callback called"
  assert tx_called[1] == True, "BUG: t2_callback not called"

  # adding timer inside callback
  print("Timer repeat test")
  t3 = TimerElem(t3_callback, None)
  t3.cb_arg = t3

  timer.add_timer(t3, 1)

  for i in range(10):
    assert tx_called[2] == False, "BUG: t3_callback called"

    timer.drive()

    assert tx_called[2] == True, "BUG: t3_callback not called"
    tx_called[2] = False

  tx_called[2] = False
  timer.del_timer(t3)

  timer.drive()
  assert tx_called[2] == False, "BUG: t3_callback called"

  # last test
  print("running 3 timers")
  tx_called = [ False, False, False, False ]
  t4 = TimerElem(t4_callback, None)

  timer.add_timer(t1, 10)
  timer.add_timer(t2, 20)
  timer.add_timer(t4, 30)

  for tick in range(30):
    timer.drive()

    if tick == 9:
      assert tx_called[0] == True, "BUG: t1_callback not called"
    elif tick == 19:
      assert tx_called[1] == True, "BUG: t2_callback not called"
    elif tick == 29:
      assert tx_called[3] == True, "BUG: t4_callback not called"

  for h in timer.buckets:
    assert h.is_empty() == True, "BUG: bucket list is not empty"

  print("test finished")
"""
