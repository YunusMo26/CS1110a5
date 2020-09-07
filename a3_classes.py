# a3_classes.py
# Authors: Kevin Cook, w/ input from Rhea Bansal,  Lillian Lee, William Xiao
# Mar 1, 2020

"""Classes for a basic to-do list and calendar scenario."""


class Task:
    """
    An instance is a single task to be completed in one day.

    Instance Attributes:
        name (nonempty string): the name of this Task
        length (int in [1..24]): how long this Task takes to complete (i.e how
            many time slots it occupies)
    """
    def __init__(self, name, length):
        """
        Initializer: a new Task with the given name and length

        Preconditions:
            name is a nonempty string
            length is an int in [0..24]
        """
        self.name = name
        self.length = length


class Day:
    """
    An instance is 24-hour day during which Tasks can be scheduled for.
    Instance Attributes:
        name (nonempty string): the name of this day. Example: "Monday"
        time_slots (list of Tasks or None, length 24): the time slots that make
            up this day.
        num_tasks_scheduled (int in 0..24): the number of Tasks that have
            been scheduled for this Day.

    Each entry in time_slots is either None(= no Task scheduled for then), or
    contains a Task object, which is thus scheduled during that time slot.
    Note that multiple time slots can contain the same Task, since a Task can
    take more than one hour to complete.
    """
    def __init__(self, name):
        """
        Initializer: a new Day with the given name,
         and all time_slots entries None.

        Preconditions:
            name is a nonempty string
        """
        self.name = name
        self.time_slots = [None] * 24  # Python list-concatenation operation
        self.num_tasks_scheduled = 0


