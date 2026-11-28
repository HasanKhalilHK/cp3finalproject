from datetime import datetime
def convert_time(time):
    if time != "":
        start_date = time.split(" ")
        start_date_time = start_date[1]
        start_hour = start_date_time.split(":")

        start_minute = start_hour[1]
        start_hour = start_hour[0]

        start_date = start_date[0]
        start_year = start_date.split("-")

        start_month = start_year[1]
        start_day = start_year[2]
        start_year = start_year[0]

        start = datetime(int(start_year), int(start_month), int(start_day), int(start_hour), int(start_minute))
        return start.timestamp()
    return ""
class FlightRecord:
    def __init__(self, flight_id="", airline="", origin="", destination="", runway="", start_time="", end_time="", priority=-1, status=""):
        self.flight_id = flight_id
        self.airline = airline
        self.origin = origin
        self.destination = destination
        self.runway = runway

        self.start_time = convert_time(start_time)
        self.end_time = convert_time(end_time)

        self.priority = priority
        self.status = status

    def get_start_time(self): #! from ai
            dt = datetime.fromtimestamp(self.start_time)
            return dt.strftime("%Y-%m-%d %H:%M")

    def get_end_time(self): #! from ai
            dt = datetime.fromtimestamp(self.end_time)
            return dt.strftime("%Y-%m-%d %H:%M")


    def print_record(self):
         print(f"Flight ID: {self.flight_id}, airline: {self.airline}, origin: {self.origin}, destination: {self.destination}, runway: {self.runway}, start time: {self.get_start_time()}, end time: {self.get_end_time()}, priority: {self.priority}, status: {self.status}")