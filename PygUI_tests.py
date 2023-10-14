import PygUI
import time

PygUI.Notifications.init()

PygUI.Notifications.notify("Python notification", "great ", True, True)
print("Next")

time.sleep(0.75)
PygUI.Notifications.flush()
