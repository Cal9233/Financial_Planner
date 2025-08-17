import mysql.connector
from decimal import Decimal
from datetime import date, time, datetime

class DBConnection:
    def __init__(self, host='localhost', user=None, password=None, database=None):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None
    
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.connection.cursor()
            print("Successfully connected to database")
            return True
        except mysql.connector.Error as err:
            print(f"Database connection error: {err}")
            return False
    
    def commit(self):
        if self.connection:
            self.connection.commit()
    
    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("Database connection closed")

class Vessel:
    def __init__(self, vessel_id=None, vessel_name=None, cost_per_hour=None):
        self.vessel_id = vessel_id
        self.vessel_name = vessel_name
        self.cost_per_hour = cost_per_hour
    
    def __str__(self):
        return f"Vessel: {self.vessel_name} (ID: {self.vessel_id}, Cost: ${self.cost_per_hour}/hour)"
    
    @staticmethod
    def get_vessel_id(vessel_name, db_connection):
        """Get vessel ID using the getVesselID function"""
        try:
            db_connection.cursor.execute("SELECT getVesselID(%s)", [vessel_name])
            result = db_connection.cursor.fetchone()
            return result[0] if result else -1
        except mysql.connector.Error as err:
            print(f"Error getting vessel ID: {err}")
            return -1
    
    @staticmethod
    def get_all_vessels(db_connection):
        """Get all vessels using the getVesselList procedure"""
        try:
            db_connection.cursor.callproc('getVesselList')
            vessels = []
            for result in db_connection.cursor.stored_results():
                for row in result.fetchall():
                    vessels.append(Vessel(row[0], row[1], row[2]))
            return vessels
        except mysql.connector.Error as err:
            print(f"Error getting vessels: {err}")
            return []
    
    @staticmethod
    def add_vessel(vessel_name, cost_per_hour, db_connection):
        """Add a vessel using the addVessel procedure"""
        try:
            db_connection.cursor.callproc('addVessel', (vessel_name, cost_per_hour))
            db_connection.commit()
            
            vessel_id = None
            for result in db_connection.cursor.stored_results():
                result_data = result.fetchone()
                if result_data:
                    vessel_id = result_data[0]
                    break
            
            return vessel_id if vessel_id is not None else -1
            
        except mysql.connector.Error as err:
            print(f"MySQL error adding vessel: {err}")
            return -1
        except Exception as e:
            print(f"General error adding vessel: {e}")
            return -1
        
    @staticmethod
    def delete_vessel(vessel_id, db_connection):
        """Delete vessel using the deleteVessel procedure"""
        try:
            if vessel_id is None or vessel_id == -1:
                return False
            
            db_connection.cursor.callproc('deleteVessel', (vessel_id,))
            db_connection.commit()
            
            vessel_found = True
            for result in db_connection.cursor.stored_results():
                result_data = result.fetchone()
                if result_data:
                    if result_data[0] == -1:
                        vessel_found = False
                        break
            
            if vessel_found:
                return True
            else:
                return False
            
        except mysql.connector.Error as err:
            print(f"MySQL error deleting vessel {vessel_id}: {err}")
            return False
        except Exception as e:
            print(f"General error deleting vessel {vessel_id}: {e}")
            return False

class Passenger:
    def __init__(self, passenger_id=None, first_name=None, last_name=None, 
                 street=None, city=None, state=None, zip_code=None, phone=None, gets_seasick=None):
        self.passenger_id = passenger_id
        self.first_name = first_name
        self.last_name = last_name
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.phone = phone
        self.gets_seasick = gets_seasick
    
    def __str__(self):
        return f"Passenger: {self.first_name} {self.last_name} (ID: {self.passenger_id})"
    
    @staticmethod
    def get_passenger_id(first_name, last_name, db_connection):
        """Get passenger ID using the getPassengerID function"""
        try:
            db_connection.cursor.execute("SELECT getPassengerID(%s, %s)", (first_name, last_name))
            result = db_connection.cursor.fetchone()
            return result[0] if result else -1
        except mysql.connector.Error as err:
            print(f"Error getting passenger ID: {err}")
            return -1
    
    @staticmethod
    def get_all_passengers(db_connection):
        """Get all passengers using the getPassengerList procedure"""
        try:
            db_connection.cursor.callproc('getPassengerList')
            passengers = []
            for result in db_connection.cursor.stored_results():
                for row in result.fetchall():
                    passengers.append(Passenger(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))
            return passengers
        except mysql.connector.Error as err:
            print(f"Error getting passengers: {err}")
            return []
    
    @staticmethod
    def add_passenger(first_name, last_name, phone, db_connection):
        """Add a passenger using the addPassenger stored procedure"""
        try:
            db_connection.cursor.callproc('addPassenger', (first_name, last_name, phone))
            db_connection.commit()

            for result in db_connection.cursor.stored_results():
                result_data = result.fetchone()
                if result_data:
                    passenger_id = result_data[0]
                    return passenger_id

            return -1

        except mysql.connector.Error as err:
            print(f"MySQL error: {err}")
            return -1
        except Exception as e:
            print(f"General error: {e}")
            return -1


    @staticmethod
    def delete_passenger(passenger_id, db_connection):
        """Delete passenger using the deletePassenger procedure"""
        try:
            if passenger_id is None or passenger_id == -1:
                return False
            
            db_connection.cursor.callproc('deletePassenger', (passenger_id,))
            db_connection.commit()
            
            passenger_found = True
            for result in db_connection.cursor.stored_results():
                result_data = result.fetchone()
                if result_data:
                    if result_data[0] == -1:
                        passenger_found = False
                        break
            
            if passenger_found:
                print(f"Passenger {passenger_id} deleted successfully")
                return True
            else:
                print(f"Passenger {passenger_id} not found")
                return False
            
        except mysql.connector.Error as err:
            print(f"MySQL error deleting passenger {passenger_id}: {err}")
            return False
        except Exception as e:
            print(f"General error deleting passenger {passenger_id}: {e}")
            return False

class Trip:
    def __init__(self, vessel_id=None, passenger_id=None, trip_date=None, 
                 departure_time=None, length_in_hours=None, total_passengers=None):
        self.vessel_id = vessel_id
        self.passenger_id = passenger_id
        self.trip_date = trip_date
        self.departure_time = departure_time
        self.length_in_hours = length_in_hours
        self.total_passengers = total_passengers
    
    def __str__(self):
        return f"Trip: Vessel {self.vessel_id}, Passenger {self.passenger_id}, Date: {self.trip_date}"
    
    # @staticmethod
    # def get_all_trips(db_connection):
    #     """Get all trips using the 'All Trips' view"""
    #     try:
    #         db_connection.cursor.execute("SELECT * FROM `all trips`")
    #         trips = []
    #         for row in db_connection.cursor.fetchall():
    #             trips.append({
    #                 'date_time': row[0],
    #                 'vessel_name': row[1],
    #                 'passenger_name': row[2],
    #                 'passenger_address': row[3],
    #                 'passenger_phone': row[4],
    #                 'total_cost': row[5]
    #             })
    #         return trips
    #     except mysql.connector.Error as err:
    #         print(f"Error getting trips: {err}")
    #         return []

    @staticmethod
    def get_all_trips(db_connection):
        """Get all trips including the actual length from database"""
        try:
            # Modified query to get the actual trip length from the trips table
            query = """
            SELECT 
                CONCAT(DATE_FORMAT(t.date,'%m/%d/%Y'), ' @ ', TIME_FORMAT(t.Departure_Time,'%h:%i %p')) AS date_time,
                v.Vessel as vessel_name,
                CONCAT(p.first_name, ' ', p.last_name) AS passenger_name,
                CONCAT(p.street, ', ', p.city, ', ', p.state, ' ', p.ZIP) AS passenger_address,
                p.Phone AS passenger_phone,
                CONCAT('$',FORMAT(t.Length_in_hours * v.Cost_Per_Hour,2)) AS total_cost,
                t.Length_in_hours AS trip_length_hours
            FROM trips t
            LEFT JOIN vessels v ON v.ID = t.Vessel_ID
            LEFT JOIN passengers p ON p.ID = t.Passenger_ID
            ORDER BY t.date DESC, t.departure_time DESC
            """
            
            db_connection.cursor.execute(query)
            trips = []
            for row in db_connection.cursor.fetchall():
                trips.append({
                    'date_time': row[0],
                    'vessel_name': row[1],
                    'passenger_name': row[2],
                    'passenger_address': row[3],
                    'passenger_phone': row[4],
                    'total_cost': row[5],
                    'trip_length_hours': float(row[6])  # Convert Decimal to float
                })
            return trips
        except mysql.connector.Error as err:
            print(f"Error getting trips: {err}")
            return []
    
    @staticmethod
    def get_total_revenue_by_vessel(db_connection):
        """Get total revenue by vessel using the view"""
        try:
            db_connection.cursor.execute("SELECT * FROM `total revenue by vessel`")
            revenue_data = []
            for row in db_connection.cursor.fetchall():
                revenue_data.append({
                    'vessel_name': row[0],
                    'revenue': row[1]
                })
            return revenue_data
        except mysql.connector.Error as err:
            print(f"Error getting revenue data: {err}")
            return []
    
    @staticmethod
    def add_trip(vessel_name, passenger_first_name, passenger_last_name, 
                trip_date, departure_time, length_in_hours, total_passengers, db_connection):
        """Add a trip using the addTrip procedure"""
        try:
            db_connection.cursor.callproc('addTrip', (
                vessel_name, passenger_first_name, passenger_last_name,
                trip_date, departure_time, length_in_hours, total_passengers
            ))
            db_connection.commit()
            
            # Check for any result messages
            for result in db_connection.cursor.stored_results():
                result_data = result.fetchone()
                if result_data:
                    return result_data[0]
            
            return "Trip added successfully"
        except mysql.connector.Error as err:
            print(f"Error adding trip: {err}")
            return f"Error: {err}"