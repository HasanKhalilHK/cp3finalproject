from datetime import datetime

class FlightRecord:
    def __init__(self, flight_id="", airline="", origin="", destination="", runway="", start_time="", end_time="", priority=-1, status=""):
        self.flight_id = flight_id
        self.airline = airline
        self.origin = origin
        self.destination = destination
        self.runway = runway

        if start_time != "":
            start_date = start_time.split(" ")
            start_date_time = start_date[1]
            start_hour = start_date_time.split(":")

            start_minute = start_hour[1]
            start_hour = start_hour[0]

            start_date = start_date[0]
            start_year = start_date.split("-")

            start_month = start_year[1]
            start_day = start_year[2]
            start_year = start_year[0]

            start = datetime(start_year, start_month, start_day, start_hour, start_minute)

            self.start_time = start.timestamp()
        else: self.start_time = ""
        if start_time != "":
            end_date = end_time.split(" ")                                            
            end_date_time = end_date[1]                                               
            end_hour = end_date_time.split(":")                                       
        
            end_minute = end_hour[1]                                                  
            end_hour = end_hour[0]                                                    
        
            end_date = end_date[0]                                                    
            end_year = end_date.split("-")                                            
        
            end_month = end_year[1]                                                   
            end_day = end_year[2]                                                     
            end_year = end_year[0]                                                    
            
            end = datetime(end_year, end_month, end_day, end_hour, end_minute)
            
            self.end_time = end.timestamp()
        else: self.end_time = ""

        self.priority = priority
        self.status = status