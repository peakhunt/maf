import maf.softtimer as st
import maf.eventloop as ev
import maf.defs as defs

TICK_RATE = 1

_mainloop_timer = None

def tick_callback():
  _mainloop_timer.drive()

def schedule(t, expires):
  _mainloop_timer.add_timer(t, expires)

def cancel(t):
  _mainloop_timer.del_timer(t)

def new(cb, cb_arg):
  t = st.TimerElem(cb, cb_arg)
  return t

_mainloop_timer = st.Timer(TICK_RATE)
ev.register_handler(tick_callback, defs.EVENT_SYS_TICK)
