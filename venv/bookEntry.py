class BookEntry:
    def __init__(self, idLabel, nameEntry, availabilityVar):
        self.id = idLabel
        self.name = nameEntry
        self.available = availabilityVar

        print(f'The book {self.id} is created')

    def getName(self) -> str:
        return self.name.get()

    def getAvailable(self) -> bool:
        return self.available.get()

    def updateAvailability(self, var: bool):
        self.available.set(var)

    def updateName(self, name: str):
        self.name.insert(0, name)