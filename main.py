from flight_registry import *
            



#testing
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

reg.delete("NK10687")
reg.print_table()