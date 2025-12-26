"""
Problem Statement:
Design a Parking Lot system that supports parking and unparking of vehicles.

Core Requirements (MVP):
1. Multiple parking slots
2. Vehicles can be parked and unparked
3. Each vehicle gets a ticket on entry
4. Slot allocation is first available / nearest
5. Different vehicle types (Car, Bike, Truck)

Assumptions:
1. In-memory only
2. Single-threaded
3. No persistence
4. No payment processing (can be extended)
5. Fixed number of slots per vehicle type
"""

from enum import Enum
from datetime import datetime
import uuid
from typing import Dict, List, Optional, Set


class VehicleType(Enum):
    CAR = "CAR"
    BIKE = "BIKE"
    TRUCK = "TRUCK"


class Vehicle:
    def __init__(self, vehicle_id: str, vehicle_type: VehicleType):
        self.vehicle_id = vehicle_id
        self.vehicle_type = vehicle_type


class ParkingSlot:
    def __init__(self, slot_id: int, slot_type: VehicleType):
        self.slot_id = slot_id
        self.slot_type = slot_type
        self._is_occupied = False

    @property
    def is_occupied(self) -> bool:
        return self._is_occupied

    @is_occupied.setter
    def is_occupied(self, value: bool):
        self._is_occupied = value


class Ticket:
    def __init__(self, vehicle_id: str, slot_id: int):
        self._id = str(uuid.uuid4())
        self.vehicle_id = vehicle_id
        self.slot_id = slot_id
        self.entry_time = datetime.now()

    @property
    def id(self) -> str:
        return self._id


class ParkingLot:
    def __init__(self, slots: List[ParkingSlot]):
        self.tickets: Set[str] = set()
        self.slots: List[ParkingSlot] = slots

    def park(self, vehicle: Vehicle) -> Optional[Ticket]:
        slot = None
        for s in self.slots:
            if not s.is_occupied:
                slot = s
        if not slot:
            return None
        ticket = Ticket(
            vehicle_id=vehicle.vehicle_id,
            slot_id=slot.slot_id
        )
        slot.is_occupied = True
        self.tickets.add(ticket.id)
        return ticket

    def unpark(self, ticket: Ticket) -> Optional[bool]:
        if ticket.id not in self.tickets:
            return None
        self.tickets.remove(ticket.id)
        for slot in self.slots:
            if slot.slot_id == ticket.slot_id:
                slot.is_occupied = False
                return True
        return None



def main():
    slots = [
        ParkingSlot(1, VehicleType.CAR),
        ParkingSlot(2, VehicleType.CAR),
        ParkingSlot(3, VehicleType.BIKE),
    ]

    parking_lot = ParkingLot(slots)

    car = Vehicle("KA01AB1234", VehicleType.CAR)
    ticket = parking_lot.park(car)

    print("Parked with ticket:", ticket.id)

    parking_lot.unpark(ticket)
    print("Vehicle unparked successfully")


if __name__ == "__main__":
    main()
