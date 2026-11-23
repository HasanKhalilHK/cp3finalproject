import random

class SlotState: #! from ai 
    empty = 0
    occupied = 1
    tombstone = 2

class FlightRegistryRecord:
    def __init__(self, flight_id=-1):
        self.flight_id = flight_id
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
                return #TODO: return error for duplicate record
            
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
                return #TODO: return successful insert

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
                    return #TODO: return record with appropriate message

            if slot.slot_state == SlotState.empty:
                return #TODO: return error for missing id

            i = (i + 1) % self.m #loop around if probing reaches end of table

        return #TODO: return error for missing id (in this case because table was completely full)




    def print_table(self):
        print(f"m: {self.m}")
        print(f"items: {self.items}")
        print(f"tombstones: {self.tombstones}")
        print(f"items: {self.items}")
        print(f"load_factor: {self.load_factor}")

        for i in range(self.m):
            print(f"Flight ID: {self.table[i].flight_id} State: {self.table[i].slot_state}")

        
            


reg = FlightRegistry()

print(reg.h(reg.id_to_int("NK10687")))
print(reg.h(reg.id_to_int("BA10309")))
print(reg.h(reg.id_to_int("B610365")))
print(reg.h(reg.id_to_int("WN10914"))) 
print(reg.h(reg.id_to_int("WN10774"))) 
print(reg.h(reg.id_to_int("UA10223"))) 
print(reg.h(reg.id_to_int("AA10371"))) 
# print(reg.h(reg.id_to_int("B610625"))) 


reg.insert(FlightRegistryRecord("NK10687"))
reg.insert(FlightRegistryRecord("BA10309"))
reg.insert(FlightRegistryRecord("B610365"))
reg.insert(FlightRegistryRecord("WN10914"))
reg.insert(FlightRegistryRecord("WN10774"))
reg.insert(FlightRegistryRecord("UA10223"))
reg.insert(FlightRegistryRecord("AA10371"))
# reg.insert(FlightRegistryRecord("B610625"))

reg.print_table()