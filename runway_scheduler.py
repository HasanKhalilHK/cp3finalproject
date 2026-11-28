from datetime import datetime
from registry import reg
from flight_record import convert_time
            
class RunwayNode:
    def __init__(self, start_time="", end_time="", flight_id=""):
        
        self.start_time = convert_time(start_time)
        self.end_time = convert_time(end_time)
        self.flight_id = flight_id
        self.parent = None
        self.left = None
        self.right = None

    def get_start_time(self): #! from ai
        dt = datetime.fromtimestamp(self.start_time)
        return dt.strftime("%Y-%m-%d %H:%M")

    def get_end_time(self): #! from ai
            dt = datetime.fromtimestamp(self.end_time)
            return dt.strftime("%Y-%m-%d %H:%M")
         

class RunwayScheduler:
    def __init__(self, runway):
        self.runway = runway
        self.root = None

    def insert(self, start_time, end_time, flight_id):
        node = RunwayNode(start_time, end_time, flight_id)
        if self.root is None:
            self.root = node
            return {"success": True} 

        current = self.root
        while current is not None:
            if node.start_time < current.start_time:
                if current.left is None: 
                    node.parent = current
                    current.left = node
                    return {"success": True}
                current = current.left
            elif node.start_time > current.start_time:
                if current.right is None: 
                    node.parent = current
                    current.right = node
                    return {"success": True}
                current = current.right
            elif node.start_time == current.start_time:
                if node.flight_id < current.flight_id:
                    if current.left is None: 
                        node.parent = current
                        current.left = node
                        return {"success": True}
                    current = current.left
                elif node.flight_id > current.flight_id:
                    if current.right is None: 
                        node.parent = current
                        current.right = node
                        return {"success": True}
                    current = current.right
                elif node.flight_id == current.flight_id:
                    return {"success": False, "reason": "Flight already exists in tree"} 

    def search(self, start_time, flight_id):
        current = self.root

        if current is None:
            return {"success": False, "reason": "Tree is empty"} 

        while current is not None:
            if start_time < current.start_time:
                current = current.left
            elif start_time > current.start_time:
                current = current.right
            elif start_time == current.start_time:
                if flight_id < current.flight_id:                                                   
                    current = current.left                                                           
                elif flight_id > current.flight_id:                                               
                    current = current.right                                                          
                elif flight_id == current.flight_id:                                            
                    return {"success": True, "node": current} 

        return {"success": False, "reason": "Node doesn't exist in tree"} 

    def delete(self, start_time, flight_id):
        current = self.root

        if current is None:
            return {"success": False, "reason": "Tree is empty"}

        res = self.search(start_time, flight_id)
        node_to_delete = None
        if res["success"]: node_to_delete = res["node"]
        else:
            return {"success": False, "reason": "Node doesn't exist in tree"}

        node_is_root = False
        node_on_right = False
        node_on_left = False

        if node_to_delete.parent is None: node_is_root = True
        elif node_to_delete.parent.left == node_to_delete: node_on_left = True
        else: node_on_right = True

        if node_to_delete.right is None:
            if node_to_delete.left is not None: #has only one child (left)
                if node_is_root:
                    self.root = node_to_delete.left
                    self.root.parent = None
                elif node_on_left:
                    node_to_delete.parent.left = node_to_delete.left
                    node_to_delete.left.parent = node_to_delete.parent
                elif node_on_right:
                    node_to_delete.parent.right = node_to_delete.left
                    node_to_delete.left.parent = node_to_delete.parent
                return {"success": True}

        if node_to_delete.left is None:
            if node_to_delete.right is not None: #has only one child (right)
                if node_is_root:
                    self.root = node_to_delete.right
                    self.root.parent = None
                elif node_on_left:
                    node_to_delete.parent.left = node_to_delete.right
                    node_to_delete.right.parent = node_to_delete.parent
                elif node_on_right:
                    node_to_delete.parent.right = node_to_delete.right
                    node_to_delete.right.parent = node_to_delete.parent
                return {"success": True}
        
        if node_to_delete.left is not None and node_to_delete.right is not None:
            successor = node_to_delete.right
            while successor.left is not None:
                successor = successor.left
            if successor.parent != node_to_delete:
                successor.parent.left = successor.right
                if successor.right is not None:
                    successor.right.parent = successor.parent

                successor.right = node_to_delete.right
                successor.right.parent = successor

            if node_is_root:
                self.root = successor
                successor.parent = None
            elif node_on_left:
                node_to_delete.parent.left = successor
                successor.parent = node_to_delete.parent
            elif node_on_right:
                node_to_delete.parent.right = successor
                successor.parent = node_to_delete.parent

            successor.left = node_to_delete.left
            successor.left.parent = successor

            return {"success": True}

    def inorder_traverse(self, node):
        if node is not None:
            self.inorder_traverse(node.left)
            print(f"Start Time: {node.get_start_time()} End Time: {node.get_end_time()} Flight ID: {node.flight_id}")
            self.inorder_traverse(node.right)

    def time_range_search(self, start_time, end_time):
        start = 0
        end = 0
        start = convert_time(start_time)
        end = convert_time(end_time)


        flights_in_range = []
        self.time_range_search_helper(self.root, start, end, flights_in_range)
        return flights_in_range

    def time_range_search_helper(self, current, start, end, flights_in_range):
        if current is None:
            return

        if current.start_time >= start:
            self.time_range_search_helper(current.left, start, end, flights_in_range)

        if current.start_time < end and current.end_time > start:
            flights_in_range.append(current)

        if current.start_time <= end:
            self.time_range_search_helper(current.right, start, end, flights_in_range)




    def mass_closure(self, start_time, end_time):
        flights = self.time_range_search(start_time, end_time)

    def mass_cancel(self, start_time, end_time):
        flights = self.time_range_search(start_time, end_time)
        for flight in flights:
            reg.cancel_flight(flight.flight_id)
            self.delete(flight.start_time, flight.flight_id)
            print(f"Cancelled flight with ID: {flight.flight_id}, start_time: {flight.get_start_time()}, end_time: {flight.get_end_time()}")

    def cancel_runway(self, reg):
        self.cancel_runway_helper(self.root, reg)
        self.root = None

    def cancel_runway_helper(self, node, reg):
        if node is not None:
            self._cancel_runway_helper(node.left, reg)
            reg.cancel_flight(node.flight_id)
            self._cancel_runway_helper(node.right, reg)



    #TODO: predecessor, successor