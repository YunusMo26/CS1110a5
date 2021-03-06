# a3_todo_test.py
# ymm26, jtg242
# Sources/people consulted: NONE
# 04/07/2020

"""
A module containing some functions to update a todo list.

Skeleton authors: William Xiao (wmx2)
    w/ input from Rhea Bansal (rab378), Kevin Cook (kjc244), Lillian Lee (LJL2)

Date: Mar 1, 2020
"""

# Utility printing functions
# (This one is complete, students need not do anything)
def sirialize(day):
    """
    Prints out the tasks scheduled in Day `day` in chronological order.

    Parameter day: the Day whose data should be printed out.
    Precondition: day is a Day object.
    """

    # collect the unique events / tasks in the day, with their start time
    events = []
    tasks_already_collected = []
    for time in range(len(day.time_slots)):
        task = day.time_slots[time]
        if task is not None and task not in tasks_already_collected:
            tasks_already_collected.append(task)
            event = (time, task)  # This is a tuple, a "non-changeable list"
            events.append(event)

    # print them out
    print(day.name + ":")
    if len(events) == 0:
        print("No events scheduled.")
        return

    for start_time, task in events:
        end_time = start_time + task.length
        start_str = str(start_time) + ":00"
        end_str = str(end_time) + ":00"
        print(start_str + "-" + end_str + " " + task.name)



def sirialize_days(day_list):
    """
    Prints out the tasks for each day in day_list, first by day in the order
    in which they appear in day_list, and then chronologically within each day.

    Parameter day_list: The list of days to print data out for.
    Precondition: day_list is non-empty list of Day objects (no None objects).
    """
    for day in day_list:
        sirialize(day)

def num_hours_busy(day):
    """
    Returns: the number of hours that are busy in Day `day`.

    Parameter day: the Day to check.
    Precondition: day is a Day object.
    """
    # STUDENTS: Your implementation MUST make use of an explicit for-loop
    # in a meaningful way.
    # That is, use a for-loop to count the number of non-None timeslots;
    # do *not* use the list `count` method or the such-like.
    c=0
    for i in range(24):
        if day.time_slots[i] != None:
            c+=1
        #else:
            #c+=1
    return c



def space_available(slots, start_time, end_time):
    """
    Returns: True if there is space available to schedule an event in `slots`
    from `start_time` (inclusive) to `end_time` (exclusive), and False otherwise.
    So, `space_available(agenda, 14, 16)` queries whether 2-4 pm is available,
    and it doesn't matter is something is scheduled at 4pm.

    There is space available if all the elements of slots starting from
    `start_time` (inclusive) to `end_time` (exclusive) are all None.

    Parameter slots: The list of timeslots to check.
    Precondition: slots is a list of length 24, each element of which is either
    a Task object or None.

    Parameter start_time: The starting time to check from, inclusive.
    Precondition: start_time is an int, and a valid index into `slots`
    (0 <= start_time < 24), and start_time < end_time.

    Parameter end_time: The ending time to check to, exclusive.
    Precondition: end_time is an int for a valid ending time
    (0 <= end_time <= 24), and start_time < end_time.
    """
    # STUDENTS: Your implementation MUST use a "for-each" loop meaningfully
    # (i.e. you cannot use range() in your loop, or list methods).
    for x in slots[start_time: end_time]:
        if x != None:
            return False
    return True


def add_task(day, task, start_time):
    """
    Returns: True if Task `task` is added to Day `day` at time `start_time`
    successfully, False otherwise.

    This function attempts to add the given task to the given day and time.
    If the specified timeslot is free, then the `time_slots` attribute of the
    Day object is modified to reflect that the task has been added, meaning that
    each hour timeslot that this task occupies must be filled in the list.
    This means that if a task takes multiple hours, there must be multiple
    references to that Task object in the timeslot list, one for each hour
    the task takes.

    If the task can successfully be added, this function also increments the
    num_tasks_scheduled attribute of Day `day` by 1 to reflect this new task.

    A task cannot be added to the Day object if any Task that is currently
    scheduled for that day would overlap with `task` if it were added at
    `start_time`. For example, adding a 3 hour long task at 2:00 should fail if
    there are any tasks scheduled between the hours of 2:00 and 5:00.

    A task also cannot be added if scheduling the task at the given
    time would require rolling over to the next day to finish. As an example,
    trying to schedule a task that takes two hours to complete at 23:00
    (i.e. start_time == 23) should fail.

    If the given task cannot be added, this function returns False and does
    not modify anything.

    Parameter day: The Day object to attempt to add Task `task` to.
    Precondition: day is a Day object.

    Parameter task: The Task object to add to Day `day`.
    Precondition: task is a Task object.

    Parameter start_time: The hour to start this task at.
    Precondition: start_time is an int , and 0 <= start_time < 24.
    """
    # STUDENTS: Your implementation MUST make meaningful use space_available
    # as a helper.
    # You must make meaningful use of for-loop in your implementation that
    # loops over a range (i.e., has a call to range()).
    # You may not create new lists in your code.
    if space_available(day.time_slots,start_time,start_time+task.length):
        day.num_tasks_scheduled += 1
        for x in range(task.length):
            day.time_slots[start_time+x] = task
        return True
    else:
        return False
