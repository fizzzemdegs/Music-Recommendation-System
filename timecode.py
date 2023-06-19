from datetime import datetime
def time_code_generator():
    now = datetime.now()

    current_time = int(now.strftime("%H"))
    print("Current Time =", current_time)

    time_slot = ""

    if 4 <= current_time <= 11:
        time_slot = "M"
    elif 11 < current_time <= 16:
        time_slot = "A"
    elif 16 < current_time <= 19:
        time_slot = "E"
    elif (0 <= current_time < 4) or current_time > 19:
        time_slot = "N"

    return time_slot
