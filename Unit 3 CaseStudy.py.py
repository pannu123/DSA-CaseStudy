 # LIBRARY MANAGEMENT SYSTEM
#  LINKED LIST 
class Node:
    def __init__(self, book_id, name):
        self.book_id = book_id
        self.name = name
        self.status = "Available"
        self.next = None


class Library:
    def __init__(self):
        self.head = None

    # Insert book
    def add_book(self):
        bid = int(input("Enter Book ID: "))
        name = input("Enter Book Name: ")

        new_node = Node(bid, name)

        if self.head is None:
            self.head = new_node
        else:
            temp = self.head
            while temp.next:
                temp = temp.next
            temp.next = new_node

        print("Book added successfully!")

    # Traverse linked list
    def display_books(self):
        if self.head is None:
            print("No books available.")
            return

        temp = self.head
        print("\n--- BOOK LIST ---")

        while temp:
            print(temp.book_id, "-", temp.name, "-", temp.status)
            temp = temp.next

    # Search book
    def search_book(self):
        bid = int(input("Enter Book ID: "))
        temp = self.head

        while temp:
            if temp.book_id == bid:
                print("Book Found:", temp.name)
                print("Status:", temp.status)
                return
            temp = temp.next

        print("Book not found.")

    # Issue book
    def issue_book(self):
        bid = int(input("Enter Book ID: "))
        temp = self.head

        while temp:
            if temp.book_id == bid:
                if temp.status == "Available":
                    temp.status = "Issued"
                    history.append("Issued: " + temp.name)
                    print("Book issued successfully!")
                else:
                    print("Book already issued.")
                return
            temp = temp.next

        print("Book not found.")

    # Return book
    def return_book(self):
        bid = int(input("Enter Book ID: "))
        temp = self.head

        while temp:
            if temp.book_id == bid:
                temp.status = "Available"
                history.append("Returned: " + temp.name)
                print("Book returned successfully!")
                return
            temp = temp.next

        print("Book not found.")


#  STACK  
history = []

def show_stack():
    print("\n--- STACK / HISTORY ---")

    if not history:
        print("Stack is empty.")
        return

    for item in reversed(history):
        print(item)


# QUEUE  
waiting_queue = []

def add_student():
    name = input("Enter Student Name: ")
    waiting_queue.append(name)
    print("Student added to queue.")


def serve_student():
    if waiting_queue:
        student = waiting_queue.pop(0)
        print("Serving Student:", student)
    else:
        print("Queue is empty.")


def show_queue():
    print("\n--- STUDENT QUEUE ---")

    if not waiting_queue:
        print("Queue is empty.")
    else:
        for student in waiting_queue:
            print(student)


#  PRIORITY QUEUE  
priority_queue = []

def add_priority_request():
    name = input("Enter Student Name: ")
    book = input("Enter Book Name: ")
    priority = int(input("Priority (1=High, 2=Medium, 3=Low): "))

    priority_queue.append([priority, name, book])
    priority_queue.sort()

    print("Priority request added.")


def process_priority():
    if priority_queue:
        request = priority_queue.pop(0)

        print("\n--- PRIORITY REQUEST ---")
        print("Student :", request[1])
        print("Book    :", request[2])
        print("Priority:", request[0])
    else:
        print("No priority requests.")


#  MAIN PROGRAM  
library = Library()

while True:

    print("\n================================")
    print("      LIBRARY MANAGEMENT")
    print("================================")
    print("1. Add Book")
    print("2. Display Books")
    print("3. Search Book")
    print("4. Issue Book")
    print("5. Return Book")
    print("6. Add Student to Queue")
    print("7. Serve Student")
    print("8. Show Queue")
    print("9. Add Priority Request")
    print("10. Process Priority Request")
    print("11. Show Stack History")
    print("12. Exit")

    choice = input("\nEnter your choice: ")

    if choice == "1":
        library.add_book()

    elif choice == "2":
        library.display_books()

    elif choice == "3":
        library.search_book()

    elif choice == "4":
        library.issue_book()

    elif choice == "5":
        library.return_book()

    elif choice == "6":
        add_student()

    elif choice == "7":
        serve_student()

    elif choice == "8":
        show_queue()

    elif choice == "9":
        add_priority_request()

    elif choice == "10":
        process_priority()

    elif choice == "11":
        show_stack()

    elif choice == "12":
        print("Thank you!")
        break

    else:
        print("Invalid choice!")