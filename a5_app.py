#a5_app.py
# Will Xiao and Lillian Lee, Apr 2020
"""
A simple module that shows off a5's functionality. 
"""
import a5
import a3_todo
import a3_classes


def quit_if_input(s):
    """
    Quits Python if s is either 'q' or 'quit', printing a goodbye in the process.

    Parameter s: the string to check.
    Precondition: s is a string.
    """
    if s in ['q', 'quit']:
        print('Goodbye!')
        quit()


def get_name_and_length():
    """Prompts user for length info, returns tuple (name, length),
       with name a string, and length an int. """
    name = input('What is the name of your task? \n> ')
    while len(name) == 0:
        print("Sorry, cannot accept an empty name")
        name = input('What is the name of your task? \n> ')
    msg = 'How many hours will your task take (integers please)? \n> '
    length = input(msg).strip().lower()
    while not length.isnumeric():
        print("Sorry, that's not a valid number!")
        length = input(msg).strip().lower()
    return (name, int(length))


def get_target_day():
    """Prompts user for day number, returns day as int"""
    msg = 'What day number would you like to add this task to?\n> '
    day = input(msg).strip().lower()
    while not (day.isdigit() and 1 <= int(day) and int(day) <= len(month.day_list)):
        print("Sorry, that's not a valid day!")
        day = input(msg).strip().lower()
    return int(day)


def add_regular_task():
    """
    Prompts user input get new task info, and then add that task to the
    to-do list (if possible).
    """
    name, length = get_name_and_length()
    new_task = a3_classes.Task(name, length)
    
    day = get_target_day()

    msg = 'What hour will your task start (24 hour time please)? \n> '
    start = input(msg).strip().lower()
    while not start.isnumeric() and not (0 <= start < 24):
        print("Sorry, that's not a valid hour!")
        start = input(msg).strip().lower()
    start = int(start)

    if not a3_todo.add_task(month.day_list[day-1], new_task, start):
        print("Sorry, couldn't add it to your schedule at that time!")
    else:
        print("Successfully added!")


def add_splittable_task():
    """
    Prompts user input get new task info, and then add that splittable task to the
    to-do list (if possible).
    """
    name, length = get_name_and_length()
    new_task = a5.SplittableTask(name, length)

    day = get_target_day()

    scheduled_some = new_task.scheduleSome(month.day_list[day-1])
    not_fully_scheduled = not new_task.isAllScheduled()
    if not scheduled_some:
        print("Sorry, that day was full!")
        return 
    if not_fully_scheduled:
        print("Some of the task was scheduled, but we couldn't fit all of it in that day!")
    else:
        print("The task was successfully fully added!")

def sirialize_redux(day):
    """
    Returns: a string containing a serialized version of `day`, or None if `day`
    is empty. 

    Parameter day: the object to serialize. 
    Precondition: day is a Day object.
    """
    # The sirialize from a3_todo.py could not be reused because it assumed
    # that Tasks could not be split across noncontiguous time blocks.
    events = []
    i = 0
    while i < len(day.time_slots):
        potential_event = day.time_slots[i]
        if potential_event is None:
            i += 1
        else:
            start_time = i
            end_time = i + 1 # update as we find more
            while (end_time < len(day.time_slots)
                    and day.time_slots[end_time] is not None
                    and potential_event == day.time_slots[end_time]):
                end_time += 1
            event = (potential_event.name, start_time, end_time)
            events.append(event)
            i = end_time

    if len(events) == 0:
        return None
    event_strs = [day.name + ":"]
    for (task_name, start_time, end_time) in events:
        time = str(start_time) + ":00-" + str(end_time) + ":00"
        time = time.ljust(15, ' ')
        event_str = time + task_name
        event_strs.append(event_str)
    return '\n'.join(event_strs) 

def parse_input(s):
    """
    Returns: a list containing all the space-separated words in s, with extra
    empty strings removed. 

    Parameter s: the string to parse. 
    Precondition: s is a string.
    """
    return list(filter(lambda v : v != '', s.split(' ')))


if __name__ == '__main__':
    welcome = "Welcome to the Tre1110 planner redux!\n"
    welcome += "Here, you can plan out an entire month.\n"
    welcome += "What month would you like to plan for? (Please enter an int in 1..12.)"
    print(welcome)

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 
                'August', 'September', 'October', 'November', 'December']
    month_num = input('> ').strip().lower()
    while not (month_num.isnumeric() and 1 <= int(month_num) and int(month_num) <= 12):
        print("That's an invalid month! Please enter an int in 1..12.")
        month_num = input('> ').strip().lower()
    month_num = int(month_num)
    month_name = months[month_num - 1]
    message = "You have chosen the month: " + month_name + ".\n"

    month = a5.Month(month_num)
    
    message = "From your implementation, the month you have chosen ("  
    message += month_name + ") has " + str(len(month.day_list)) + " days.\n"
    message += "If this seems off, please check it!\n\n"

    message += "Type 'print <day_number>' to view your schedule for that day, "
    message += "or 'print all' to view your whole month at once.\n"
    message += "To add a task to the planner, type 'add task'.\n"
    message += "Type 'q' to quit.\n"
    message += "What would you like to do?"
    print(message)

    PRINT_ALL = ['print', 'all']
    QUIT_WORDS = ['q', 'quit']
    ADD_TASK = ['add', 'task']

    msg = input('> ').strip().lower()
    while msg not in QUIT_WORDS:
        words = parse_input(msg)
        if words == PRINT_ALL:
            cal = "Here is your calendar for the month of " + month_name + ":\n"
            day_strs = []
            for day in month.day_list:
                day_str = sirialize_redux(day)
                if day_str is not None:
                    day_strs.append(day_str)
            if len(day_strs) == 0:
                cal += "You have no events scheduled this month.\n"
            else:
                cal += '\n\n'.join(day_strs)
            print(cal + '\n')
        elif words[0] == 'print' and words[1].isdigit():
            day_num = int(words[1])
            if day_num < 1 or day_num > len(month.day_list):
                print("Sorry, that day number is invalid for this month!")
            else:
                day_str = sirialize_redux(month.day_list[day_num-1])
                cal = "You have no events scheduled that day." if day_str is None else day_str
                print(cal)
        elif words == ADD_TASK:
            print("What type of task would you like to add? Enter either 'r' (for regular) or 's' (for splittable)'.")
            task_type = input('> ').strip().lower()
            if task_type == 'r':
                add_regular_task()
            elif task_type == 's':
                add_splittable_task()
            else:
                print("Unrecognized task type entered!")
        else:
            print("Sorry, your command was not recognized, please try again!")
        print("What would you like to do now? (add task, print <day num>, print all, q)")
        msg = input('> ').strip().lower()

    print('Goodbye and good luck getting all your tasks done!')