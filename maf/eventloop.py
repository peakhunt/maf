"""
Minimum Eventloop implementation for MicroPython

This module is developed In the spirit of 'simple is beautiful'.

"""

import pyb
import maf.defs as defs

tick_timer = None

def init_tick_timer():
  tick_timer = pyb.Timer(defs.TICK_TIMER_NUMBER)
  tick_timer.init(freq = defs.TICK_FREQUENCY)
  tick_timer.callback(lambda t: set_event(defs.EVENT_SYS_TICK))

class EventLoop(object):
  def __init__(self):
    self.flags = 0x0
    self.handlers = {}
    init_tick_timer()

  def set_event(self, evt):
    irq_state = pyb.disable_irq()
    self.flags |= (1 << evt)
    pyb.enable_irq(irq_state)

  def register_handler(self, handler, evt):
    self.handlers[evt] = handler

  def dispatch(self):
    irq_state = pyb.disable_irq()
    flags = self.flags
    self.flags = 0
    pyb.enable_irq(irq_state)

    for i in range(32):
      if (flags & (1 << i)) != 0:
        handler = self.handlers.get(i)
        if handler != None:
          handler()

default_loop = EventLoop()

def set_event(evt):
  default_loop.set_event(evt)

def register_handler(handler, evt):
  default_loop.register_handler(handler, evt)

def dispatch():
  default_loop.dispatch()
