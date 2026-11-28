from flight_registry import FlightRegistry
from flight_record import FlightRecord
from runway_scheduler import RunwayScheduler

from registry import reg
runways = {
    "R1": RunwayScheduler("R1"),
    "R2": RunwayScheduler("R2"),
    "R3": RunwayScheduler("R3"),
    "R4": RunwayScheduler("R4"),
    "R5": RunwayScheduler("R5")
}
def load_csv(file_name):
    file = open(file_name, 'r')
    file.readline()

    for line in file:
        record_arr = line.split(",")
        record = FlightRecord(record_arr[0], record_arr[1], record_arr[2], record_arr[3], record_arr[4], record_arr[5], record_arr[6], record_arr[7], record_arr[8])
        reg.insert(record)
        runway = record_arr[4]
        runways[runway].insert(record_arr[5], record_arr[6], record_arr[0])

    file.close()

def print_options():
    print(f"1. LOAD 2. LIST_RUNWAY")
    print(f"3. FIND 4. ADD")
    print(f"5. CANCEL 6. RESCHEDULE")
    print(f"7. CHECK_CONFLICT 8. RUNWAY_CLOSURE")
    print(f"9. EMERGENCY_INSERT 10. MASS_CANCEL")
    print(f"11. SORT_PRIORITY 12. SORT_ID")
    print(f"13. ANALYZE 14. BENCHMARK")
    print(f"15. STATS")

print_options()
c = input("Please enter the number of the function you want to run, or run a command: ")

while c.lower() != "exit":
    c = c.lower()

    if c == "1":
        file_name = input("Enter the name of the file you want to load (.csv): ")
        load_csv(file_name)
        reg.print_table()
        runways["R1"].inorder_traverse(runways["R1"].root)

    if c == "2":
        runway = input("Which runway do you want to view: ")
        if runway in runways:
            runways[runway].inorder_traverse(runways[runway].root)
        else:
            print(f"Runway {runway} does not exist")

    if c == "3":
        flight_id = input("Enter the flight ID you want to find: ")
        res = reg.lookup(flight_id)
        res["record"].print_record()

    if c == "5":
        flight_id = input("Enter the flight ID of the flight you want to cancel: ")
        reg.cancel_flight(flight_id)
        res = reg.lookup(flight_id)
        flight = res["record"]
        runway = flight[4]
        runways[runway].delete(flight[5], flight_id)

    if c == "8":
        runway = input("Enter the runway you want to close: ")
        runways[runway].cancel_runway(reg)

    if c == "10":
        start_time = input("Enter the start of the range you want to cancel: ")
        end_time = input("Enter the end of the range you want to cancel: ")
        for runway in runways:
            runway.mass_cancel(start_time, end_time)

    if c == "11":
        print("Sorting flights by priority")
        flights = reg.counting_sort_by_priority(reg.get_flights())
        for flight in flights:
            flight.print_record() 

    print_options()
    c = input("Please enter the number of the function you want to run: ")

