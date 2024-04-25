class Library:
    """Here in this console version of the app"""

    def __init__(self):
        self.books = {
            1: {"name": "Les Misérables", "availability": "Free"},
            2: {"name": "The Hunchback of Notre-Dame", "availability": "Free"},
            3: {"name": "Ninety-Three", "availability": "Free"}
        }
        self.borrowers = {}

    def displayBooks(self) -> None:
        """Display available books."""
        try:
            if not self.books:
                print("No books available.")
            else:
                print("Available Books:")
                sortedBooks = sorted(self.books.items(), key=lambda x: int(x[0]))
                for bookId, bookInfo in sortedBooks:
                    print(f"Book ID: {bookId}, Name: {bookInfo['name']}, Availability: {bookInfo['availability']}")
        except Exception as e:
            print(f"Error: {e}")

    def borrowBook(self, username: str, bookName: str) -> None:
        """Borrow a book"""
        try:
            bookFound = False
            for bookInfo in self.books.values():
                if bookInfo["name"] == bookName:
                    if bookInfo["availability"] == "Free":
                        bookInfo["availability"] = "Not available"
                        print(f"Book '{bookName}' borrowed by {username}.")
                        self.borrowers.setdefault(username, []).append(bookName)
                    else:
                        print(f"'{bookName}' is already borrowed.")
                    bookFound = True
                    break
            if not bookFound:
                print(f"Book '{bookName}' not found in the library.")
        except Exception as e:
            print(f"Error: {e}")

    def returnBook(self, borrowerName: str, bookName: str) -> None:
        #Return a book
        try:
            bookFound = False
            for bookInfo in self.books.values():
                if bookInfo["name"] == bookName:
                    bookFound = True
                    for key, item in self.borrowers.items():
                        if key == borrowerName and bookName in item:
                            item.remove(bookName)
                            print(f"Book '{bookName}' is returned.")
                            bookInfo["availability"] = "Free"
                    break
            if not bookFound:
                print(f"Book '{bookName}' was not found.")
        except Exception as e:
            print(f"Error: {e}")

    def viewBooks(self, username: str) -> None:
        #View books borrowed
        try:
            userBooks = [bookName for bookName, bookInfo in self.books.items() if bookInfo["availability"] == "Not available"]
            if userBooks:
                print(f"Books borrowed by {username}:")
                for bookName in userBooks:
                    print(bookName)
            else:
                print(f"No books borrowed by {username}.")
        except Exception as e:
            print(f"Error: {e}")

    def addBook(self, bookId: int, bookName: str, availability: str) -> None:
        """Add a new book to the library."""
        try:
            if not isinstance(bookId, int):
                raise ValueError("Book ID must be an integer.")
            if bookName not in self.books and availability == "Free" or availability == "Not available":
                self.books[bookId] = {"name": bookName, "availability": availability}
                print(f"Book '{bookName}' with ID {bookId} added to the library.")
            else:
                print(f"Book '{bookName}' already exists in the library or the availability is wrong.")
        except ValueError as ve:
            print(f"Error: {ve}")
        except Exception as e:
            print(f"Error: {e}")

    def removeBook(self, bookId: int) -> None:
        """ Remove a book """
        try:
            bookRemoved = False
            for bookId, bookInfo in self.books.items():
                if bookId == bookId:
                    del self.books[bookId]
                    print(f"Book with ID {bookId} is removed.")
                    bookRemoved = True
                    break
            if not bookRemoved:
                print(f"No book found with ID {bookId}.")
        except Exception as e:
            print(f"Error: {e}")

    def exitSystem(self) -> None:
        """Exit the library management system."""
        print("Exiting the library.")

    def run(self) -> None:
        """Run the library management system"""
        try:
            while True:
                print("\nMenu:")
                print("1) Display Available Books \n2) Borrow a Book \n3) Return a Book \n4) View your Books \n5) Add a book \n6) Remove \n7) Exit")
                choice = input("Enter your choice: ")

                if choice == "1":
                    self.displayBooks()
                elif choice == "2":
                    username = input("Enter your username: ")
                    bookName = input("Enter the name of the book to borrow: ")
                    self.borrowBook(username, bookName)
                elif choice == "3":
                    borrowerName = input("Enter the name of the borrower: ")
                    bookName = input("Enter the name of the book to return: ")
                    self.returnBook(borrowerName, bookName)
                elif choice == "4":
                    username = input("Enter your username: ")
                    self.viewBooks(username)
                elif choice == "5":
                    try:
                        bookId = int(input("Enter the ID of the book: "))
                        bookName = input("Enter the name of the book: ")
                        availability = input("Enter Free/Not available: ")
                        self.addBook(bookId, bookName, availability)
                    except ValueError:
                        print("Error: Book ID must be an integer.")
                elif choice == "6":
                    try:
                        bookId = int(input("Enter the ID of the book to remove: "))
                        self.removeBook(bookId)
                    except ValueError:
                        print("Error: Book ID must be an integer.")
                elif choice == "7":
                    self.exitSystem()
                    break
                else:
                    print("Invalid choice! Please enter a number from 1 to 6.")
        except Exception as e:
            print(f"Error: {e}")
