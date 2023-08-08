import random

class Chance:
    def has(self, percent: int) -> bool:
        number = random.randint(1, 100)

        return number <= percent
