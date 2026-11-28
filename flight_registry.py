import random
from flight_record import FlightRecord
    

class SlotState: #! from ai 
    empty = 0
    occupied = 1
    tombstone = 2

class FlightRegistryRecord(FlightRecord):
    
    def __init__(self, flight_id="", airline="", origin="", destination="", runway="", start_time="", end_time="", priority=-1, status=""):
        super().__init__(flight_id, airline, origin, destination, runway, start_time, end_time, priority, status)
        self.slot_state =  SlotState.empty


class FlightRegistry:
    def __init__(self):

        self.m = 8
        self.p = 2147483647
        self.a = random.randint(1, self.p-1)
        self.b = random.randint(0, self.p-1) 

        self.items = 0
        self.tombstones = 0
        self.load_factor = (self.items + self.tombstones) / self.m 

        self.table = [FlightRegistryRecord() for _ in range(self.m)]

    def id_to_int(self, id):
        total = 0
        for i in range(0, len(id)):
            total+= (ord(id[i]) ** (i+1)) #sum the (unicode value ** index) (better than just summing so values like ab12 and ba21 dont return the same value)
        return total

    def calc_load_factor(self):
        self.load_factor = (self.items + self.tombstones) / self.m 

    def rehash(self):
        self.m *= 2
        old_table = self.table
        self.table = [FlightRegistryRecord() for _ in range(self.m)]
        self.items = 0
        self.tombstones = 0
        self.calc_load_factor()
        for i in old_table:
            if i.slot_state == SlotState.occupied:
                self.insert(i)


    def h(self, k):
        return (( (self.a * k + self.b) % self.p ) % self.m)

    def insert(self, record):
        record = FlightRegistryRecord(record.flight_id, record.airline, record.origin, record.destination, record.runway, record.get_start_time(), record.get_end_time(), record.priority, record.status)
        if self.load_factor >= 0.75:
            self.rehash()
    
        probes = 0
        collisions = 0
        first_tombstone = -1
        id = self.id_to_int(record.flight_id)
        i = self.h(id)

        for _ in range(self.m):
            probes += 1
            slot = self.table[i]

            if slot.slot_state == SlotState.occupied and slot.flight_id == record.flight_id:
                return {"success" : False, "reason": "Record already exists", "probes" : probes, "collisions": collisions, "load_factor": self.load_factor}
            
            if slot.slot_state == SlotState.occupied and slot.flight_id != record.flight_id:
                collisions += 1

            if slot.slot_state == SlotState.tombstone and first_tombstone == -1: 
                first_tombstone = i

            if slot.slot_state == SlotState.empty:
                target = None
                if first_tombstone != -1:
                    self.tombstones -= 1
                    target = first_tombstone
                else:
                    target = i

                self.table[target] = record
                self.table[target].slot_state = SlotState.occupied
                self.items += 1
                self.calc_load_factor()
                return {"success" : True, "probes" : probes, "collisions": collisions, "load_factor": self.load_factor}

            i = (i + 1) % self.m #loop around if probing reaches end of table

    def lookup(self, flight_id):
        probes = 0
        id = self.id_to_int(flight_id)
        i = self.h(id)

        for _ in self.table:
            probes += 1
            slot = self.table[i]

            if slot.slot_state == SlotState.occupied:
                if slot.flight_id == flight_id:
                    return {"success" : True, "record": slot,  "probes" : probes}

            if slot.slot_state == SlotState.empty:
                return {"success" : False, "reason": "Record doesn't exist", "probes" : probes}

            i = (i + 1) % self.m #loop around if probing reaches end of table

        return {"success" : False, "reason": "Record doesn't exist", "probes" : probes}


    def delete(self, flight_id):
        probes = 0
        id = self.id_to_int(flight_id)
        i = self.h(id)

        for _ in self.table:
            probes += 1
            slot = self.table[i]
            
            if slot.slot_state == SlotState.occupied:
                if slot.flight_id == flight_id:
                    tombestone = FlightRegistryRecord()
                    tombestone.slot_state = SlotState.tombstone
                    self.table[i] = tombestone
                    self.tombstones += 1
                    self.items -= 1
                    return {"success" : True, "probes" : probes}

            if slot.slot_state == SlotState.empty:
                return {"success" : False, "reason": "Record doesn't exist", "probes" : probes}

            i = (i + 1) % self.m #loop around if probing reaches end of table

        return {"success" : False, "reason": "Record doesn't exist", "probes" : probes}

    def cancel_flight(self, flight_id):
        res = self.lookup(flight_id)

        if res["success"]:
            record = res["record"]
            if record.status == "CANCELLED":
                return {"success": False, "reason": "Flight is already cancelled"}

            record.status = "CANCELLED"
            return {"success": True, "record": record}
        else:
            return {"success": False, "reason": res["reason"]}


    def get_flights(self):
        flights = []
        for flight in self.table:
            if flight.slot_state == SlotState.occupied:
                flights.append(flight)
        return flights

    def counting_sort_by_priority(self, flights):
        count = [0,0,0,0]
        sorted_flights = [None] * len(flights)
        for flight in flights:
            count[int(flight.priority)] += 1

        count[1] = count[1] + count[0]
        count[2] = count[2] + count[1]
        count[3] = count[3] + count[2]

        for i in range(len(flights) - 1, -1, -1):
            priority = int(flights[i].priority)
            count[priority] -= 1
            sorted_flights[count[priority]] = flights[i]

        return sorted_flights


    def print_table(self):
        print(f"m: {self.m}")
        print(f"items: {self.items}")
        print(f"tombstones: {self.tombstones}")
        print(f"items: {self.items}")
        print(f"load_factor: {self.load_factor}")

        for i in range(self.m):
            print(f"Flight ID: {self.table[i].flight_id} State: {self.table[i].slot_state}")

        