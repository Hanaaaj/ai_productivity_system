import threading
import time

def reminder_loop(session_state):
    while True:
        time.sleep(600)  # 10 minutes
        session_state["hydration_alert"] = True

def start_scheduler(session_state):
    thread = threading.Thread(target=reminder_loop, args=(session_state,), daemon=True)
    thread.start()
