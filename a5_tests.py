# a5_tests.py
# PUT YOUR NETID(S) HERE
# Sources/people consulted: FILL IN OR WRITE "NONE"
# PUT DATE YOU COMPLETED THIS HERE
# Skeleton by Will Xiao and Prof. Lee, April 2020

"""
A test module with some functions to test a5.py.
"""
import a5
import a3_classes
import testcase

# For ensuring no attributes are added beyond the official ones
_splittask_attributes = set(["name", "length", "time_unscheduled"])


def test_month_init():
    """
    Tests whether to see the Month initializer is working properly.
    """
    print("Testing month initializer")
    # Testing a month with 31 days (January)

    for month_number in range(1, 13):
        month = a5.Month(month_number)
        _assert_month(month_number, month)

    print("Passed tests for month initializer")

def test_splittable_task_init():
    """
    Tests whether the initializer for SplittableTask is working properly.
    """

    print("Testing splittable task initializer")
    # task of length 1
    workout = a5.SplittableTask("go to the gym", 1)
    _assert_attr_set(workout, _splittask_attributes)
    testcase.assert_equals("go to the gym", workout.name)
    testcase.assert_equals(1, workout.length)
    testcase.assert_equals(1, workout.time_unscheduled)


    # task of length 1 < length < 24
    sleep = a5.SplittableTask("go to bed", 8)
    _assert_attr_set(sleep, _splittask_attributes)
    testcase.assert_equals("go to bed", sleep.name)
    testcase.assert_equals(8, sleep.length)
    testcase.assert_equals(8, sleep.time_unscheduled)


    # task of length 24
    your_duty = a5.SplittableTask("try your best", 24)
    _assert_attr_set(your_duty, _splittask_attributes)
    testcase.assert_equals("try your best", your_duty.name)
    testcase.assert_equals(24, your_duty.length)
    testcase.assert_equals(24, your_duty.time_unscheduled)


    print("Finished testing splittable task initializer")


def test_is_all_scheduled():
    """
    Tests whether the isAllScheduled function for SplittableTask is working properly.
    """
    print("Testing splittable task isAllScheduled")
    # same test cases as before, but with a different method
    # task is unscheduled
    sleep = a5.SplittableTask("nap", 8)
    testcase.assert_false(sleep.isAllScheduled())

    # task is partially scheduled
    sleep.time_unscheduled = 4
    testcase.assert_false(sleep.isAllScheduled())

    # task is fully scheduled
    sleep.time_unscheduled = 0
    testcase.assert_true(sleep.isAllScheduled())
    print("Finished testing splittable task isAllScheduled")


def test_update_unscheduled():
    """
    Tests whether the updateUnsched method in SplittableTask is working properly.
    """
    print("Testing update_unscheduled")

    # 1 hour task, to schedule
    practice = a5.SplittableTask("practice piano", 1)
    day = a3_classes.Day("Monday")
    practice.updateUnsched(day, 7)
    _assert_attr_set(practice, _splittask_attributes) # Should not have changed
    expected_timeslots = [None] * 24
    expected_timeslots[7] = practice
    testcase.assert_equals(expected_timeslots, day.time_slots)
    testcase.assert_equals(0, practice.time_unscheduled)
    testcase.assert_equals(1, practice.length)

    # Multi hour task, to schedule
    hacker_typer = a5.SplittableTask("hack into the mainframe", 4)
    hacker_typer.updateUnsched(day, 12)
    _assert_attr_set(hacker_typer, _splittask_attributes)
    expected_timeslots[12] = hacker_typer
    testcase.assert_equals(expected_timeslots, day.time_slots)
    testcase.assert_equals(3, hacker_typer.time_unscheduled)
    testcase.assert_equals(4, hacker_typer.length)

    # Multi hour task, but is partially scheduled already
    hacker_typer.updateUnsched(day, 15)
    _assert_attr_set(hacker_typer, _splittask_attributes)
    expected_timeslots[15] = hacker_typer
    testcase.assert_equals(expected_timeslots, day.time_slots)
    testcase.assert_equals(2, hacker_typer.time_unscheduled)
    testcase.assert_equals(4, hacker_typer.length)

    # Schedule one more hour of it, but adjacent to another occurrence of the same task
    hacker_typer.updateUnsched(day, 16)
    _assert_attr_set(hacker_typer, _splittask_attributes)
    expected_timeslots[16] = hacker_typer
    testcase.assert_equals(expected_timeslots, day.time_slots)
    testcase.assert_equals(1, hacker_typer.time_unscheduled)
    testcase.assert_equals(4, hacker_typer.length)
    print("Done testing update_unscheduled")


def test_schedule_some():
    """
    Tests whether the scheduleSome method in SplittableTask is working properly.
    """
    print("Testing scheduleSome")
    # scheduling into an empty day
    sleep = a5.SplittableTask("sleep 2.0", 8)
    day = a3_classes.Day("Just a normal Friday")
    result = sleep.scheduleSome(day)
    _assert_attr_set(sleep, _splittask_attributes)
    testcase.assert_true(result)
    testcase.assert_equals(1, day.num_tasks_scheduled)
    expected_timeslots = [sleep] * 8 + [None] * 16
    testcase.assert_equals(expected_timeslots, day.time_slots)
    testcase.assert_equals(0, sleep.time_unscheduled)
    testcase.assert_equals(8, sleep.length)

    # scheduling more in the same day
    classes = a5.SplittableTask("answer email", 12)
    result = classes.scheduleSome(day)
    _assert_attr_set(classes, _splittask_attributes)
    testcase.assert_true(result)
    testcase.assert_equals(2, day.num_tasks_scheduled)
    expected_timeslots[8:20] = [classes] * 12
    testcase.assert_equals(expected_timeslots, day.time_slots)
    testcase.assert_equals(0, classes.time_unscheduled)
    testcase.assert_equals(12, classes.length)

    # scheduling more, but would spill over (cannot fit all in same day)
    assignments = a5.SplittableTask("finishing psets", 9)
    result = assignments.scheduleSome(day)
    _assert_attr_set(assignments, _splittask_attributes)
    testcase.assert_true(result)
    testcase.assert_equals(3, day.num_tasks_scheduled)
    expected_timeslots[20:24] = [assignments] * 4
    testcase.assert_equals(expected_timeslots, day.time_slots)
    testcase.assert_equals(5, assignments.time_unscheduled)
    testcase.assert_equals(9, assignments.length)

    # day is already full, but new task
    self_care = a5.SplittableTask("treat yo self", 4)
    result = self_care.scheduleSome(day)
    _assert_attr_set(self_care, _splittask_attributes)
    testcase.assert_false(result)
    testcase.assert_equals(3, day.num_tasks_scheduled)
    testcase.assert_equals(expected_timeslots, day.time_slots)
    testcase.assert_equals(4, self_care.time_unscheduled)
    testcase.assert_equals(4, self_care.length)

    # only partially schedule a task earlier on, then call scheduleSome with rest
    new_day = a3_classes.Day("Saturday")
    errands = a5.SplittableTask("running errands", 4)
    new_day.time_slots[20] = new_day.time_slots[21] = errands
    new_day.num_tasks_scheduled = 1
    errands.time_unscheduled = errands.time_unscheduled - 2
    # actually try and schedule now
    result = errands.scheduleSome(new_day)
    _assert_attr_set(errands, _splittask_attributes)
    testcase.assert_true(result)
    expected_timeslots = [errands] * 2 + [None] * 18 + [errands] * 2 + [None] * 2
    testcase.assert_equals(1, new_day.num_tasks_scheduled)
    testcase.assert_equals(expected_timeslots, new_day.time_slots)
    testcase.assert_equals(0, errands.time_unscheduled)
    testcase.assert_equals(4, errands.length)

    # call scheduleSome where it must be split over noncontiguous blocks of time
    netflix = a5.SplittableTask("watch netflix", 2)
    disney = a5.SplittableTask("watch disney+", 3)
    netflix.scheduleSome(new_day)
    disney.scheduleSome(new_day)
    _assert_attr_set(netflix, _splittask_attributes)
    _assert_attr_set(disney, _splittask_attributes)
    # as of now, schedule is: 0-2: errands, 2-4: netflix, 4-7, disney+. Let's move stuff.
    # now let's move around some hours
    new_day.time_slots[8] = new_day.time_slots[4] # moving one hour of disney+ from hour 4 to hour 8
    new_day.time_slots[4] = None
    new_day.time_slots[10] = new_day.time_slots[2] # moving one hour of netflix from hour 2 to hour 10
    new_day.time_slots[2] = None
    expected_timeslots[3] = netflix
    expected_timeslots[5] = expected_timeslots[6] = disney
    expected_timeslots[8] = disney
    expected_timeslots[10] = netflix
    testcase.assert_equals(expected_timeslots, new_day.time_slots)
    testcase.assert_equals(3, new_day.num_tasks_scheduled)
    # this is where the actual test kicks in
    thought = a5.SplittableTask("ponder the complexities of human language", 5)
    result = thought.scheduleSome(new_day)
    _assert_attr_set(thought, _splittask_attributes)
    testcase.assert_true(result)
    expected_timeslots[2] = expected_timeslots[4] = expected_timeslots[7] = expected_timeslots[9] = expected_timeslots[11] = thought
    testcase.assert_equals(expected_timeslots, new_day.time_slots)
    testcase.assert_equals(4, new_day.num_tasks_scheduled)
    testcase.assert_equals(0, thought.time_unscheduled)
    testcase.assert_equals(5, thought.length)


    print("Done testing scheduleSome")


def run_tests():
    """
    Runs all the tests for A5 functions.
    """
    # STUDENTS: Comment out functions in test_fns that you want to (temporarily)
    # skip.  The default behavior is to test everything.
    # Your course staff STRONGLY recommends doing a final check with all the
    # test functions uncommented before your final submission.

    print("Running all tests")
    test_fns = [test_splittable_task_init,
                test_is_all_scheduled,
                test_update_unscheduled,
                test_schedule_some,
                test_month_init]
    num_ran = 0
    for fun in test_fns:
        fun()
        num_ran+=1
        print()
    print("Ran and passed " +str(num_ran)+ " of 5 testing functions.")
    if num_ran < 5:
        print("You should probably check all 5 testing functions eventually.")
    else:
        print("Looks like you were up to the (A5) task!")


# Helper testing methods
def _assert_month(month_num, computed_month):
    """
    Asserts that `computed_month` has month_num as its month number and
    has the proper configuration for that month number.

    Precondition:
        computed_month is an a5.Month
        month_num: int in 1..12
    """
    testcase.assert_true(isinstance(computed_month, a5.Month))
    # Test that right set of attributes were added
    _assert_attr_set(computed_month, set(["month_num", "day_list"]))

    if month_num == 2: # February
        days_in = 28
    elif month_num in [4, 6, 9, 11]: # the months with 30 days
        days_in = 30
    else:
        # Any month that makes it to this point has 31 days in it
        days_in = 31

    testcase.assert_equals(month_num, computed_month.month_num)
    testcase.assert_equals(days_in, len(computed_month.day_list))
    empty_day_list = [None] * 24
    for i in range(days_in):
        cmp_day = computed_month.day_list[i]
        testcase.assert_true(isinstance(cmp_day, a3_classes.Day))
        testcase.assert_equals("/".join([str(month_num), str(i + 1)]), cmp_day.name)
        testcase.assert_equals(empty_day_list, cmp_day.time_slots)
        testcase.assert_equals(0, cmp_day.num_tasks_scheduled)


def _assert_attr_set(obj, expected_attr_set):
    """Asserts that the (names of the) set of attributes for object obj is the same
    as the set of strings `expected_attr_set."""
    actual_attr_set = set([a for a in obj.__dict__])
    assert actual_attr_set == expected_attr_set, \
        "Object of type " + str(type(obj)) + \
        " has attributes " + str(actual_attr_set) + \
        " but should have attributes " + str(expected_attr_set)

if __name__ == '__main__':
    run_tests()
