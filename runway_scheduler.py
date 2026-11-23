from datetime import datetime
            
class RunwayNode:
    def __init__(self, start_time="", flight_id=""):
        
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
        self.flight_id = flight_id
        self.parent = None
        self.left = None
        self.right = None

    def get_start_time(self): #! from ai
        dt = datetime.fromtimestamp(self.start_time)
        return dt.strftime("%Y-%m-%d %H:%M")
         

class RunwayScheduler:
    def __init__(self, runway):
        self.runway = runway
        self.root = None

    def insert(self, node):
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
                    return {"success": True, "noce": current} 

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
            print(f"Start Time: {node.get_start_time()} Flight ID: {node.flight_id}")
            self.inorder_traverse(node.right)


    #TODO: predecessor, successor and time-range search