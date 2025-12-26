from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict
from collections import defaultdict


class Role(Enum):
    VP = 1
    Director = 2
    Manager = 3
    Dev = 4


class User:
    def __init__(self, username: str, role: Role):
        self.username = username
        self.role = role
        self.is_loggen_in = False

    def __str__(self):
        return self.username


class Event:
    def __init__(
        self,
        event_name: str,
        host: User,
        guests: List[User],
        start_time: datetime,
        end_time: datetime
    ):
        self.event_name = event_name
        self._host = host
        self.guests = guests
        self.start_time = start_time
        self.end_time = end_time

    @property
    def host(self) -> User:
        return self._host

    def __str__(self):
        return self.event_name

    def __repr__(self):
        return self.event_name


class CalendarApp:
    def __init__(self):
        self.logged_in_user: Optional[User] = None
        self.users: List[User] = []
        # self.events: List[Event] = []
        self.user_events: Dict[User, List[Event]] = defaultdict(list)

    def register_user(self, user: User):
        self.users.append(user)

    def login(self, user: User):
        self.logged_in_user = user

    def schedule(self, event_name: str, start_time: datetime, end_time: datetime, guests: List[User]):
        event = Event(
            event_name=event_name,
            host=self.logged_in_user,
            guests=guests,
            start_time=start_time,
            end_time=end_time
        )
        # self.events.append(event)
        self.user_events[event.host].insert(0, event)
        for guest in guests:
            self.user_events[guest].append(event)

    def list_events(self):
        user_events = [event
                       for event in self.user_events[self.logged_in_user]
                       if event.host == self.logged_in_user]
        other_events = [event
                       for event in self.user_events[self.logged_in_user]
                       if event.host != self.logged_in_user]
        user_events.sort(
            key=lambda event: (event.start_time, event.host.role.value)
        )
        other_events.sort(
            key=lambda event: (event.start_time, event.host.role.value)
        )
        while user_events or other_events:
            if user_events and other_events:
                if user_events[0].start_time <= other_events[0].start_time:
                    event = user_events.pop(0)
                else:
                    event = other_events.pop(0)
            elif user_events:
                event = user_events.pop(0)
            else:
                event = other_events.pop(0)
            print(event)

    def edit_event(self, start_time: datetime, end_time: datetime, event_name: str):
        pass

    def delete_event(self, event_name: str):
        event_id = None
        for index, event in enumerate(self.user_events[self.logged_in_user]):
            if event.event_name == event_name:
                event_id = index
                break
        if event_id is not None:
            del self.user_events[self.logged_in_user][event_id]


def main():
    cal = CalendarApp()
    u1 = User("u1", Role.Dev)
    u2 = User("u2", Role.Dev)
    u3 = User("u3", Role.Manager)
    u4 = User("u4", Role.VP)
    u5 = User("u5", Role.Dev)
    users = [u1, u2, u3, u4, u5]
    for user in users:
        cal.register_user(user)
    cal.login(u2)
    cal.schedule(
        event_name="event1",
        start_time=datetime(2025, 12, 27, 14, 0),
        end_time=datetime(2025, 12, 27, 16, 0),
        guests=[u1, u3, u4]
    )
    cal.login(u5)
    cal.schedule(
        event_name="event2",
        start_time=datetime(2025, 12, 27, 13, 0),
        end_time=datetime(2025, 12, 27, 15, 0),
        guests=[u3]
    )
    cal.login(u4)
    cal.schedule(
        event_name="event3",
        start_time=datetime(2025, 12, 27, 14, 0),
        end_time=datetime(2025, 12, 27, 15, 0),
        guests=[u2, u3]
    )
    cal.login(u3)
    cal.schedule(
        event_name="event4",
        start_time=datetime(2025, 12, 27, 14, 00),
        end_time=datetime(2025, 12, 27, 15, 0),
        guests=[u2, u4]
    )
    cal.login(u2)
    cal.list_events()


if __name__ == '__main__':
    main()
