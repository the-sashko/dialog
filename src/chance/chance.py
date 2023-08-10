import random

class Chance:
    def get(self, percent: int) -> bool:
        number = random.randint(1, 100)

        return number <= percent
