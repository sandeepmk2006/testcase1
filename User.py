from dataclasses import dataclass, field
from typing import Optional

@dataclass
class TrackerEvent:
    id: int
    name: str

@dataclass
class User(TrackerEvent):
    username: str
    email: str

    def get_details(self) -> str:
        return f"User: {self.name} (@{self.username})"

    def __str__(self) -> str:
        return f"{self.name} (@{self.username})"

# Example usage:
user = User(1, "John Doe", "johndoe", "johndoe@example.com")
print(user.get_details())
print(user)