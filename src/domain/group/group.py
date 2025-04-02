from dataclasses import dataclass


@dataclass
class Group:
    id: int
    title: str
    owner_id: int
    participants: list[int]

    def add_participant(self, user_id: int):
        if user_id not in self.participants:
            self.participants.append(user_id)
