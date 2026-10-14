 
TABLE_SIZE = 10
DELETED = object()
table = [None] * TABLE_SIZE


def hash_function(student_id):
    return student_id % TABLE_SIZE


def read_student_id(prompt):
    try:
        return int(input(prompt))
    except ValueError:
        print("Please enter a valid numeric Student ID.")
        return None


def find_student_index(student_id):
    start = hash_function(student_id)

    for step in range(TABLE_SIZE):
        index = (start + step) % TABLE_SIZE
        record = table[index]

        if record is None:
            return -1

        if record is not DELETED and record[0] == student_id:
            return index

    return -1


def find_insert_index(student_id):
    start = hash_function(student_id)
    first_deleted = None

    for step in range(TABLE_SIZE):
        index = (start + step) % TABLE_SIZE
        record = table[index]

        if record is DELETED:
            if first_deleted is None:
                first_deleted = index

        elif record is None:
            if first_deleted is not None:
                return first_deleted
            return index

        elif record[0] == student_id:
            return -2

    if first_deleted is not None:
        return first_deleted

    return -1


def add_student():
    student_id = read_student_id("Enter Student ID: ")

    if student_id is None:
        return

    index = find_insert_index(student_id)

    if index == -2:
        print("Student ID already exists.")
        return

    if index == -1:
        print("Hash table is full.")
        return

    name = input("Enter Student Name: ").strip()

    try:
        marks = float(input("Enter Marks: "))
    except ValueError:
        print("Please enter valid numeric marks.")
        return

    if index != hash_function(student_id):
        print("Collision detected. Linear Probing applied.")

    table[index] = [student_id, name, marks]

    print("Student record added successfully at index", index)


def search_student():
    student_id = read_student_id("Enter Student ID to search: ")

    if student_id is None:
        return

    index = find_student_index(student_id)

    if index == -1:
        print("Student record not found.")
    else:
        record = table[index]

        print("\nStudent Record Found")
        print("Hash Table Index :", index)
        print("Student ID       :", record[0])
        print("Student Name     :", record[1])
        print("Marks            :", f"{record[2]:.2f}")


def update_student():
    student_id = read_student_id("Enter Student ID to update: ")

    if student_id is None:
        return

    index = find_student_index(student_id)

    if index == -1:
        print("Student record not found.")
        return

    new_name = input("Enter updated name: ").strip()

    try:
        new_marks = float(input("Enter updated marks: "))
    except ValueError:
        print("Please enter valid numeric marks.")
        return

    table[index][1] = new_name
    table[index][2] = new_marks

    print("Student record updated successfully.")


def delete_student():
    student_id = read_student_id("Enter Student ID to delete: ")

    if student_id is None:
        return

    index = find_student_index(student_id)

    if index == -1:
        print("Student record not found.")
    else:
        table[index] = DELETED
        print("Student record deleted successfully.")


def display_records():
    print("\n============== HASH TABLE RECORDS ==============")
    print(f"{'Index':<8}{'Student ID':<14}{'Student Name':<22}{'Marks':<10}")
    print("-" * 54)

    for index, record in enumerate(table):
        if record is None:
            print(f"{index:<8}{'-':<14}{'Empty':<22}{'-':<10}")

        elif record is DELETED:
            print(f"{index:<8}{'-':<14}{'Deleted':<22}{'-':<10}")

        else:
            print(
                f"{index:<8}{record[0]:<14}"
                f"{record[1]:<22}{record[2]:<10.2f}"
            )

    print("-" * 54)


print("=" * 48)
print("  STUDENT RECORD MANAGEMENT USING HASHING")
print("=" * 48)

while True:
    print("\n1. Add Student")
    print("2. Search Student")
    print("3. Update Student")
    print("4. Delete Student")
    print("5. Display All Records")
    print("6. Exit")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        add_student()

    elif choice == "2":
        search_student()

    elif choice == "3":
        update_student()

    elif choice == "4":
        delete_student()

    elif choice == "5":
        display_records()

    elif choice == "6":
        print("Thank you for using the system!")
        break

    else:
        print("Invalid choice. Please try again.")
