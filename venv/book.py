class Book:
    def __init__(self, id: int, name: str, available: bool):
        self.id = id
        self.name = name
        self.available = available
        
        print(f'The book {name} is created')
        
    def update(self, id: int, name: str, available: bool):
        self.id = id
        self.name = name
        self.available = available

        print(f'The book {name} is updated')
        