 
def to_minutes(time):
    hours, minutes = map(int, time.split(":"))
    total_minutes = hours * 60 + minutes
    return total_minutes


def merge_sort(lectures):
    if len(lectures) <= 1:
        return lectures

    middle = len(lectures) // 2

    left_half = merge_sort(lectures[:middle])
    right_half = merge_sort(lectures[middle:])

    sorted_lectures = []

    i = 0
    j = 0

    while i < len(left_half) and j < len(right_half):
        left_end = to_minutes(left_half[i][3])
        right_end = to_minutes(right_half[j][3])

        if left_end <= right_end:
            sorted_lectures.append(left_half[i])
            i += 1
        else:
            sorted_lectures.append(right_half[j])
            j += 1

    while i < len(left_half):
        sorted_lectures.append(left_half[i])
        i += 1

    while j < len(right_half):
        sorted_lectures.append(right_half[j])
        j += 1

    return sorted_lectures


def display_lectures(lectures):
    print("-" * 65)
    print(f"{'ID':<8}{'SUBJECT':<18}{'START TIME':<18}{'END TIME':<15}")
    print("-" * 65)

    for lecture in lectures:
        lecture_id = lecture[0]
        subject = lecture[1]
        start_time = lecture[2]
        end_time = lecture[3]

        print(
            f"{lecture_id:<8}"
            f"{subject:<18}"
            f"{start_time:<18}"
            f"{end_time:<15}"
        )

    print("-" * 65)


print("=" * 65)
print("       COLLEGE TIMETABLE MANAGEMENT SYSTEM")
print("=" * 65)

number = int(input("Enter number of lectures: "))

lectures = []

for i in range(number):
    print("\nEnter details for Lecture", i + 1)

    subject = input("Enter subject name: ")
    start_time = input("Enter start time (HH:MM): ")
    end_time = input("Enter end time (HH:MM): ")

    lecture_id = "L" + str(i + 1)

    lecture = (
        lecture_id,
        subject,
        start_time,
        end_time
    )

    lectures.append(lecture)


print("\nSTEP 1: SORTING LECTURES USING MERGE SORT")

sorted_lectures = merge_sort(lectures)

display_lectures(sorted_lectures)


print("\nSTEP 2: SELECTING LECTURES USING GREEDY STRATEGY")

selected_lectures = []
last_end_time = -1

for lecture in sorted_lectures:
    start_time = to_minutes(lecture[2])
    end_time = to_minutes(lecture[3])

    if start_time >= last_end_time:
        selected_lectures.append(lecture)
        last_end_time = end_time


selected_ids = []

for lecture in selected_lectures:
    selected_ids.append(lecture[0])


rejected_lectures = []

for lecture in sorted_lectures:
    if lecture[0] not in selected_ids:
        rejected_lectures.append(lecture)


print("\nFINAL COLLEGE TIMETABLE")
display_lectures(selected_lectures)


print("\nLECTURES NOT SCHEDULED")

if len(rejected_lectures) == 0:
    print("All lectures have been scheduled successfully.")
else:
    display_lectures(rejected_lectures)


print("\nFINAL SUMMARY")
print("-" * 40)
print("Total lectures entered   :", number)
print("Lectures scheduled       :", len(selected_lectures))
print("Lectures not scheduled   :", len(rejected_lectures))
print("-" * 40)
print("Timetable generation completed.")
