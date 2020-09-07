# a5.py
# ymm26
# Sources/people consulted: NONE
# 05/02/2020
# Skeleton by Will Xiao and Prof. Lee, April 2020

# UPDATE: Fri May 1st 8pm Ithaca time: corrected specification of Month.__init__
#         (Month objects have an attribute `month_num`, not `month`)

import a3_classes # for the Day and Task class

"""Classes for a more sophisticated todo-list and calendar processing,
   expanding on the class Task from A3."""


class SplittableTask(a3_classes.Task):
    """
    An instance represents a task that can be scheduled within a Day.

    SplittableTasks do not have to be scheduled for a single block of consecutive
    hours, but rather can be split up and scheduled in multiple smaller intervals.

    Instance attributes (IN ADDITION TO THOSE IN THE PARENT Task CLASS):
        time_unscheduled: the remaining amount of time left in this task that
                          has yet to be scheduled within a Day
                          [int >= 0, and no more than this Task's length]

    Class invariant:
    the amount of time this SplittableTask has been budgeted for in some
       presumed calendar of interest,
    plus this SplittableTask's time_unscheduled,
    equals this SplittableTask's length.
    """

    def __init__(self, n, time_needed):
        """
        Initializer: a new, completely unscheduled SplittableTask with name `n`
        and length `time_needed`

        Preconditions:
            `n`: nonempty string
            `time_needed`:  int in 1..24
        """
        super().__init__(n, time_needed)
        self.time_unscheduled = time_needed

    def isAllScheduled(self):
        """
        Returns: True if this SplittableTask is fully scheduled, False otherwise.

        A SplittableTask is fully scheduled if it has 0 unscheduled time left.
        """
        return self.time_unscheduled == 0


    def updateUnsched(self, d, hr):
        """
        Schedules one of this SplittableTask's unscheduled hours for Day `d` at
        time `hr`. Note that `d` thus is altered.
        Preconditions:
            This SplittableTask has at least one unscheduled hour left.
            `hr` is a legitimate time for day `d`.
            `d` has hour `hr` free.
        """
        d.time_slots[hr] = self
        self.time_unscheduled -= 1


    def scheduleSome(self, day):
        """
        Returns: True if a non-zero amount of the unscheduled time in this
          SplittableTask can be scheduled into `day`;
          and if so, this method does the scheduling of as much of the
          unscheduled time into `day` as possible, using the earliest empty
          time slots.
        Returns: True *also* in the case that this SplittableTask already has
          no more unscheduled time left.
        Returns False otherwise (i.e., there's still more of this SplittableTask
        to do but `day` is already full), with no alteration of `day`.

        Parameter `day`: the Day to try to schedule some of this SplittableTask
           into.
        Precondition: `day` is a Day object (not None)
        """
        if None in day.time_slots and not self.isAllScheduled():
            possible = None in day.time_slots and not self.isAllScheduled()
            while possible:
                if self not in day.time_slots:
                    day.num_tasks_scheduled += 1
                hr = day.time_slots.index(None)
                self.updateUnsched(day, hr)
                possible = None in day.time_slots and not self.isAllScheduled()
            return True
        elif self.isAllScheduled():
            return True
        else:
            return False

    def __str__(self):
        """
        Returns: A string representation of this SplittableTask.

        The string is formatted as:
            "SplittableTask with name: <name>, length: <length>, and time unscheduled <time_unscheduled>"

        where <name> is the name attribute,
        <length> is the length attribute,
        and <time_unscheduled> is the time_unscheduled attribute.
        Example: if we executed
            sleep = SplittableTask("nap", 8)
        then the result of __str__ at that point should be the string
            'SplittableTask with name: nap, length: 8, and time unscheduled 8'
        """
        return ("SplittableTask with name: " + self.name +
                                ", length: " + str(self.length) +
                                ", and time unscheduled " + str(self.time_unscheduled))



class Month():
    """
    An instance represents one of January, February, March, ..., December.

    Instance attributes:
        month_num: The number of this month [int in 1..12]
        day_list: The days in this month [list of a3_classes.Day objects]
            Constraints on day_list:
            - The number of Day objects in day_list equals the number of days
              in the month corresponding to this Month.
              Note: in the Land of A5, February always has exactly 28 days.
            - For each Day in day_list, the Day object's name has format
              "<month number>/<day number>".
              Example: if this Month's month_num is 5, the item at index 0 in
                `day_list` should have name "5/1", for the 1st day of May.
            - The Day objects are in ascending order by day number as
              listed in the Day's names; e.g., the Day with name "5/9"
              immediately the precedes the Day with name "5/10".
    """

    def __init__(self, month):
        """
        Initializer: Creates a Month with month number `month_num` and `day_list`
        as specified in the invariant for class Month.

        Precondition: `month_num` is an int in 1..12.
        """
        self.month_num = month
        self.day_list = []
        if month is 2:
            self.addDay(28)

        elif month in [4,6,9,11]:
            self.addDay(30)

        else:
            self.addDay(31)


    # ...STUDENT Added Helper Function...
    def addDay(self, mlen):
        """
        Adds mlen number of Day objects to self's day_list in ascending order.
        Each Day object added has name of format "<month number>/<day number>"

        PRECONDITIONS:
        mlen: an int in the list [28,30,31], and equals the number of days
                corresponding to this  month (self).
        """
        day = 1
        while day < mlen + 1:
            name = f'{self.month_num}/{day}'
            self.day_list.append(a3_classes.Day(name))
            day += 1
