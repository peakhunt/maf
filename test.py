import maf.eventloop as ev
import maf.defs as defs
import maf.mainloop_timer as mt
from pyb import LED

BLINK_INTERVALS = [83, 115, 237, 543]
leds = [LED(1), LED(2), LED(3), LED(4)]
blink_timers = [None] * len(leds)

def blink_callback(arg):
  ndx = arg
  leds[ndx].toggle()
  mt.schedule(blink_timers[ndx], BLINK_INTERVALS[ndx])

for ndx in range(len(leds)):
  blink_timers[ndx] = mt.new(blink_callback, ndx)
  mt.schedule(blink_timers[ndx], BLINK_INTERVALS[ndx])

while True:
  ev.dispatch()
