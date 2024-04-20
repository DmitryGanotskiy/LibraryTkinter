from tkinter import *
from bookEntry import BookEntry

class TK:
    """
    This class represents the main application window.

    Attributes:
        entries (list): A list to store book entries.
        borrowed (list): A list to store borrowed books.
        borrowerDict (dict): A dictionary to store information about borrowers and their borrowed books.
        count (int): Counter to keep track of the number of book entries.
        currentFrame (Frame): Reference to the current frame.
        showFrame (Frame): Reference to the frame used to display book entries.
    """
    def __init__(self):
        """Initialize the TK class."""
        self.entries = []
        self.borrowed = []
        self.borrowerDict = {}
        self.count = 0
        self.currentFrame = None
        self.showFrame = None
        self._setup()
        self._createElements()

    def _setup(self):
        """Configure the main application window."""
        self.tk = Tk()
        self.tk.configure(bg="gray")
        self.tk.geometry("800x500")
        self.tk.minsize(800, 500)
        self.tk.maxsize(800, 500)
        self.tk.title("Grades")

    def _createElements(self):
        """Create GUI elements such as buttons, frames, and canvas."""
        self.scrollFrame = Frame(self.tk)
        self.scrollFrame.pack(fill=BOTH, expand=True)

        self.canvas = Canvas(self.scrollFrame)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)

        self.booksFrame = Frame(self.canvas)
        self.booksFrame.pack(fill=BOTH)

        self.scrollbar = Scrollbar(self.scrollFrame, orient=VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.create_window((0, 0), window=self.booksFrame, anchor="nw")

        try:
            self.addBtn = Button(self.tk, width="10", text="Add", command=self._addBook)
            self.showBtn = Button(self.tk, width="10", text="Show", command=self._show)
            self.serviceBtn = Button(self.tk, width="10", text="Take or Return", command=self._serviceForm)
            self.borrowedBtn = Button(self.tk, width="10", text="Borrowed", command=self._userBooks)
            self.exitBtn = Button(self.tk, width="10", text="Exit", command=self._exit)

            self.addBtn.pack(side=LEFT, padx=(50, 10), pady=10)
            self.showBtn.pack(side=LEFT, padx=(50, 5), pady=10)
            self.serviceBtn.pack(side=LEFT, padx=(50, 5), pady=10)
            self.borrowedBtn.pack(side=LEFT, padx=(50, 5), pady=10)
            self.exitBtn.pack(side=LEFT, padx=(50, 5), pady=10)

            self.borrowedBtn.config(state=DISABLED)
            self.serviceBtn.config(state=DISABLED)
            self.showBtn.config(state=DISABLED)

        except Exception as e:
            print(f"An error occurred while creating buttons: {e}")

        self.booksFrame.bind("<Configure>", self._frameConfigure)

    def _addBook(self):
        """
        Add a book entry to the application.
        If the number of book entries is less than 11, a new entry is added.
        """
        if self.count < 11:
            self.bookEntry = Frame(self.booksFrame)
            self.bookEntry.pack(fill=X, padx=20, pady=5)

            id = len(self.entries)
            idLabel = Label(self.bookEntry, text=f"ID: {id}", width=8)
            idLabel.pack(side=LEFT, padx=(0, 10))

            nameLabel = Label(self.bookEntry, text="Name: ", width=8)
            nameLabel.pack(side=LEFT, padx=(20, 10))
            nameEntry = Entry(self.bookEntry)
            nameEntry.pack(side=LEFT)

            availabilityLabel = Label(self.bookEntry, text="Availability:", width=12)
            availabilityLabel.pack(side=LEFT, padx=(20, 10))
            bolean = BooleanVar()
            availabilityCheckbox = Checkbutton(self.bookEntry, variable=bolean)
            availabilityCheckbox.pack(side=LEFT)

            remove = Button(self.bookEntry, text="Remove", width="5", bg="gray", command= lambda entry = self.bookEntry: self._RemoveVar(entry))
            remove.pack(side=LEFT, padx=(50, 10))

            entry = BookEntry(id, nameEntry, bolean)
            self.entries.append(entry)

            self.count += 1

        else: print("max 11 books")

        self.borrowedBtn.config(state=NORMAL)
        self.serviceBtn.config(state=NORMAL)
        self.showBtn.config(state=NORMAL)

    def _frameConfigure(self, event):
        """Configure canvas scrolling."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _RemoveVar(self, entry):
        """
        Remove a book entry.
        Args: entry (Frame): The entry frame to be removed.
        Raises: Exception: If an error occurs while removing a book.
        """
        try:
            index = self.booksFrame.winfo_children().index(entry)
            self.count-=1

            if index >= 0:
                entry.destroy()
                removed_entry = self.entries.pop(index)

                for i, entry in enumerate(self.entries):
                    entry.id = i

                print("Entry removed and IDs reordered successfully.")
            else:
                print("Entry object not found.")
        except Exception as e:
            print(f"An error occurred while removing a book: {e}")

    def _show(self):
        """Display book entries."""

        self.addBtn.config(state=DISABLED)
        if self.showFrame:
            self.showFrame.destroy()
        if self.currentFrame:
            self.currentFrame.destroy()

        try:
            self.showFrame = Frame(self.booksFrame)
            self.showFrame.pack(side=LEFT, fill=BOTH, expand=True)

            nameCounts = []

            for entry in self.entries:
                name = entry.getName()
                if name in nameCounts:
                    entry.name.delete(0, END)
                    entry.name.insert(0, f"{name}_copy{nameCounts.count(name)}")

                nameCounts.append(name)

                bookEntry = Frame(self.showFrame)
                bookEntry.pack(fill=X, padx=20, pady=5)

                id = len(self.entries)
                idLabel = Label(bookEntry, text=f"ID: {entry.id}", width=8)
                idLabel.pack(side=LEFT, padx=(0, 10))

                nameLabel = Label(bookEntry, text=f"Name: {entry.getName()}", width=20)
                nameLabel.pack(side=LEFT, padx=(20, 10))

                available = entry.getAvailable()
                availabilityLabel = Label(bookEntry, text=f"Availability: {available}", width=12)
                availabilityLabel.pack(side=LEFT, padx=(20, 10))
                self.borrowed.append(availabilityLabel)
        except Exception as e:
            print(f"An error occurred while showing book entries: {e}")

    def _userBooks(self):
        """Display books borrowed by users."""
        if self.currentFrame:
            self.currentFrame.destroy()

        self.addBtn.config(state=DISABLED)
        self.currentFrame = Frame(self.canvas)
        self.currentFrame.pack(side=LEFT, fill=BOTH, expand=True)

        for user, books in self.borrowerDict.items():
            for name, book in books.items():
                borrowEntry = Frame(self.currentFrame)
                borrowEntry.pack(fill=X, padx=20, pady=5)

                nameLabel = Label(borrowEntry, text=f"Name: {name}", width=20)
                nameLabel.pack(side=LEFT, padx=(0, 10))

                booksListbox = Listbox(borrowEntry, width=30, height=5)
                booksListbox.pack(side=LEFT, padx=(0, 10))

                for i in book:
                    booksListbox.insert(END, i)

    def _serviceForm(self):
        """Display the service form."""
        self.addBtn.config(state=DISABLED)
        if self.currentFrame:
            self.currentFrame.destroy()

        self.currentFrame = Frame(self.canvas)
        self.currentFrame.pack(side=LEFT, fill=BOTH, expand=True)

        try:
            borrowerNameLabel = Label(self.currentFrame, text="Name:")
            borrowerNameLabel.pack(pady=(5, 5))
            self.bookName = Entry(self.currentFrame)
            self.bookName.pack(pady=(5, 5))

            bookIDLabel = Label(self.currentFrame, text="Book ID or name:")
            bookIDLabel.pack(pady=(5, 5))
            self.bookIDEntry = Entry(self.currentFrame)
            self.bookIDEntry.pack(pady=(5, 5))

            self.borrowButton = Button(self.currentFrame, text="Borrow", command=self._borrow)
            self.borrowButton.pack(pady=5)
            self.returnButton = Button(self.currentFrame, text="Return", command=self._return)
            self.returnButton.pack(pady=5)
        except Exception as e:
            print(f"An error occurred while displaying the service form: {e}")

    def _borrow(self):
        """Borrow a book."""
        borrower = self.bookName.get()
        name = self.bookIDEntry.get()

        for i, entry in enumerate(self.entries):
            try:
                if entry.available.get():
                    if name == entry.getName():
                        entry.updateAvailability(False)
                        self.borrowed[i].config(text=f"Availability: False")

                        if self.borrowerDict:
                            for users, books in self.borrowerDict.items():
                                for user, book in books.items():
                                    if user == borrower:
                                        book.append(name)
                                        return

                        self.borrowerDict.setdefault(entry.id, {}).setdefault(borrower, []).append(name)
                        self.borrowedBtn.config(state=NORMAL)
                        print(self.borrowerDict)

            except Exception as e:
                print(f"An unexpected error occurred during borrowing: {e}")

    def _return(self):
        """Return a book."""
        returner = self.bookName.get()
        name = self.bookIDEntry.get()

        for key, val in self.borrowerDict.items():
            for borrower, borrowedNames in val.items():
                try:
                    if returner == borrower and name in borrowedNames:
                        self.borrowed[key].config(text="Availability: True")
                        del self.borrowerDict[key][borrower][self.borrowerDict[key][borrower].index(name)]
                        if not self.borrowerDict[key][borrower]:
                            del self.borrowerDict[key][borrower]
                        if not self.borrowerDict[key]:
                            del self.borrowerDict[key]
                        next((entry.updateAvailability(True) for entry in self.entries if entry.id == key), None)
                        return
                except Exception as e:
                    print(f"An unexpected error occurred during returning: {e}")

    def _exit(self):
        """Exit the application."""
        self.tk.destroy()

    def run(self):
        """Run the application."""
        self.tk.mainloop()

if __name__ == "__main__":
    app = TK()
    app.run()
