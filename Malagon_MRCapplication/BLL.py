from DAL import DBConnection, Vessel, Passenger, Trip
from datetime import date, time, datetime, timedelta
from decimal import Decimal

class MRCBusinessLogic:
    def __init__(self):
        self.db_connection = None
    
    def initialize_database_connection(self, user, password, database, host='localhost'):
        """Initialize database connection with provided credentials"""
        self.db_connection = DBConnection(host=host, user=user, password=password, database=database)
        return self.db_connection.connect()
    
    def close_connection(self):
        """Close database connection"""
        if self.db_connection:
            self.db_connection.close()
    
    def get_total_revenue_by_vessel(self):
        """Get formatted total revenue by vessel data"""
        if not self.db_connection:
            return "Database connection not established"
        
        revenue_data = Trip.get_total_revenue_by_vessel(self.db_connection)
        
        if not revenue_data:
            return "No revenue data found"
        
        return revenue_data
    
    def get_vessel_id_with_validation(self, vessel_name):
        """Get vessel ID with business logic validation"""
        if not self.db_connection:
            return {"error": "Database connection not established"}
        
        if not vessel_name or vessel_name.strip() == "":
            return {"error": "Vessel name cannot be empty"}
        
        vessel_id = Vessel.get_vessel_id(vessel_name, self.db_connection)
        
        if vessel_id == -1:
            return {
                "vessel_name": vessel_name,
                "vessel_id": None,
                "found": False,
                "message": f"Vessel '{vessel_name}' not found in database"
            }
        else:
            return {
                "vessel_name": vessel_name,
                "vessel_id": vessel_id,
                "found": True,
                "message": f"Vessel '{vessel_name}' found with ID: {vessel_id}"
            }
    
    def add_new_trip_existing_entities(self, vessel_name, passenger_first_name, passenger_last_name,
                                     trip_date, departure_time, length_in_hours, total_passengers):
        """Add a trip for existing vessel and passenger with business validation"""
        if not self.db_connection:
            return "Database connection not established"
        
        # Validate inputs
        if not all([vessel_name, passenger_first_name, passenger_last_name, trip_date, departure_time]):
            return "All required fields must be provided"
        
        if length_in_hours <= 0:
            return "Trip length must be greater than 0"
        
        if total_passengers <= 0:
            return "Total passengers must be greater than 0"
        
        # Check for double booking
        booking_check = self.check_double_booking(
            vessel_name, passenger_first_name, passenger_last_name,
            trip_date, departure_time, length_in_hours
        )
        
        if booking_check["conflict"]:
            return f"Booking conflict: {booking_check['message']}"
        
        
        # Add the trip
        result = Trip.add_trip(
            vessel_name, passenger_first_name, passenger_last_name,
            trip_date, departure_time, length_in_hours, total_passengers,
            self.db_connection
        )
        
        # Interpret result
        if isinstance(result, int):
            if result == 0:
                return f"Error: Duplicate trip found for {vessel_name} on {trip_date} at {departure_time}"
            elif result == -1:
                return f"Error: Vessel '{vessel_name}' not found"
            elif result == -2:
                return f"Error: Passenger '{passenger_first_name} {passenger_last_name}' not found"
            elif result == -3:
                return f"Error: Both vessel '{vessel_name}' and passenger '{passenger_first_name} {passenger_last_name}' not found"
        
        return f"Trip successfully added for {vessel_name} with {passenger_first_name} {passenger_last_name}"
    
    def add_new_trip_with_new_entities(self, vessel_name, vessel_cost_per_hour,
                                     passenger_first_name, passenger_last_name, passenger_phone,
                                     trip_date, departure_time, length_in_hours, total_passengers):
        """Add a trip with new vessel and passenger"""
        if not self.db_connection:
            return "Database connection not established"
        
        # Validate inputs
        if not all([vessel_name, passenger_first_name, passenger_last_name, passenger_phone]):
            return "All required fields must be provided"
        
        if vessel_cost_per_hour <= 0:
            return "Vessel cost per hour must be greater than 0"
        
        if length_in_hours <= 0:
            return "Trip length must be greater than 0"
        
        if total_passengers <= 0:
            return "Total passengers must be greater than 0"
        
        # Check for double booking (even with new entities, there might be existing bookings)
        booking_check = self.check_double_booking(
            vessel_name, passenger_first_name, passenger_last_name,
            trip_date, departure_time, length_in_hours
        )
        
        if booking_check["conflict"]:
            return f"Booking conflict: {booking_check['message']}"
        
        # First, add the new vessel
        vessel_id = Vessel.add_vessel(vessel_name, vessel_cost_per_hour, self.db_connection)
        if vessel_id == -1:
            return f"Error adding vessel '{vessel_name}'"
        
        # Then, add the new passenger
        passenger_id = Passenger.add_passenger(passenger_first_name, passenger_last_name, passenger_phone, self.db_connection)
        if passenger_id == -1:
            return f"Error adding passenger '{passenger_first_name} {passenger_last_name}'"
        
        # Finally, add the trip
        result = Trip.add_trip(
            vessel_name, passenger_first_name, passenger_last_name,
            trip_date, departure_time, length_in_hours, total_passengers,
            self.db_connection
        )
        
        return f"Successfully added new vessel '{vessel_name}', passenger '{passenger_first_name} {passenger_last_name}', and trip"
    
    def get_all_vessels_list(self):
        """Get all vessels as a list for dropdowns"""
        if not self.db_connection:
            return []
        
        vessels = Vessel.get_all_vessels(self.db_connection)
        return vessels if vessels else []
    
    def get_all_passengers_list(self):
        """Get all passengers as a list for dropdowns"""
        if not self.db_connection:
            return []
        
        passengers = Passenger.get_all_passengers(self.db_connection)
        return passengers if passengers else []
    
    def validate_vessel_exists(self, vessel_name):
        """Validate that a vessel exists in the database"""
        if not self.db_connection:
            return False
        
        vessel_id = Vessel.get_vessel_id(vessel_name, self.db_connection)
        return vessel_id != -1
    
    def get_all_trips_formatted(self):
        """Get all trips with user-friendly formatting"""
        if not self.db_connection:
            return "Database connection not established"
        
        trips = Trip.get_all_trips(self.db_connection)
        
        if not trips:
            return "No trips found"
        
        return trips
    
    def validate_passenger_exists(self, first_name, last_name):
        """Validate that a passenger exists in the database"""
        if not self.db_connection:
            return False
        
        passenger_id = Passenger.get_passenger_id(first_name, last_name, self.db_connection)
        return passenger_id != -1
    
    def format_currency(self, amount):
        """Format currency for display"""
        if isinstance(amount, str) and amount.startswith('$'):
            return amount
        return f"${amount:,.2f}"
    
    def validate_date_format(self, date_str):
        """Validate and convert date string to date object"""
        try:
            return date.fromisoformat(date_str)
        except ValueError:
            return None
    
    def validate_time_format(self, time_str):
        """Validate and convert time string to time object"""
        try:
            return time.fromisoformat(time_str)
        except ValueError:
            return None
        
    def format_decimal_for_display(self, decimal_value):
        """Format decimal values for user-friendly display"""
        if isinstance(decimal_value, Decimal):
            return float(decimal_value)
        return decimal_value
    
    def check_double_booking(self, vessel_name, passenger_first_name, passenger_last_name,
                       trip_date, departure_time, length_in_hours):
        """Check if a trip would create a double booking conflict"""
        if not self.db_connection:
            return {"conflict": True, "message": "Database connection not established"}
        
        try:
            # Get all existing trips (now includes actual trip length)
            all_trips = Trip.get_all_trips(self.db_connection)
            if not all_trips:
                return {"conflict": False, "message": "No existing trips to check against"}
            
            # Convert our trip to datetime objects for comparison
            trip_start = datetime.combine(trip_date, departure_time)
            trip_end = trip_start + timedelta(hours=length_in_hours)
            
            passenger_full_name = f"{passenger_first_name} {passenger_last_name}"
            
            for existing_trip in all_trips:
                try:
                    existing_datetime_str = str(existing_trip['date_time'])
                    
                    existing_start = None
                    try:
                        existing_start = datetime.strptime(existing_datetime_str, '%m/%d/%Y @ %I:%M %p')
                    except ValueError:
                        try:
                            existing_start = datetime.strptime(existing_datetime_str, '%Y-%m-%d %H:%M:%S')
                        except ValueError:
                            print(f"Could not parse datetime: {existing_datetime_str}")
                            continue
                    
                    existing_length_hours = existing_trip['trip_length_hours']
                    existing_end = existing_start + timedelta(hours=existing_length_hours)
                    
                    # Check for time overlap
                    if self._times_overlap(trip_start, trip_end, existing_start, existing_end):
                        
                        # Check vessel conflict
                        if existing_trip['vessel_name'] == vessel_name:
                            return {
                                "conflict": True,
                                "message": f"Vessel '{vessel_name}' is already booked from {existing_start.strftime('%Y-%m-%d %H:%M')} to {existing_end.strftime('%H:%M')} ({existing_length_hours} hour trip)"
                            }
                        
                        # Check passenger conflict
                        if existing_trip['passenger_name'] == passenger_full_name:
                            return {
                                "conflict": True,
                                "message": f"Passenger '{passenger_full_name}' is already booked from {existing_start.strftime('%Y-%m-%d %H:%M')} to {existing_end.strftime('%H:%M')} ({existing_length_hours} hour trip)"
                            }
                
                except (ValueError, KeyError, TypeError) as e:
                    print(f"Error processing trip: {e}")
                    continue
            
            return {"conflict": False, "message": "No booking conflicts found"}
            
        except Exception as e:
            return {"conflict": True, "message": f"Error checking bookings: {str(e)}"}

    def _times_overlap(self, start1, end1, start2, end2):
        """Check if two time periods overlap"""
        overlap = start1 < end2 and end1 > start2
        return overlap
    
    def add_new_passenger(self, first_name, last_name, phone):
        """Add a new passenger with business logic validation"""
        if not self.db_connection:
            return {"success": False, "message": "Database connection not established"}
        
        # Validate inputs
        validation_result = self.validate_passenger_input(first_name, last_name, phone)
        if not validation_result["valid"]:
            return {"success": False, "message": validation_result["message"]}
        
        try:
            existing_id = Passenger.get_passenger_id(first_name, last_name, self.db_connection)
            returned_id = Passenger.add_passenger(first_name, last_name, phone, self.db_connection)

            if existing_id != -1 and existing_id == returned_id:
                return {
                    "success": False,
                    "message": f"Passenger '{first_name} {last_name}' already exists with ID {existing_id}"
                }

            elif returned_id != -1:
                return {
                    "success": True,
                    "passenger_id": returned_id,
                    "message": f"Passenger '{first_name} {last_name}' added successfully with ID {returned_id}"
                }

            else:
                return {
                    "success": False,
                    "message": "Failed to add passenger to database"
                }

        except Exception as e:
            return {"success": False, "message": f"Error adding passenger: {str(e)}"}

    def validate_passenger_input(self, first_name, last_name, phone):
        """Validate passenger input data according to business rules"""
        errors = []
        
        # Name validation
        if not first_name or not first_name.strip():
            errors.append("First name is required")
        elif len(first_name.strip()) < 2:
            errors.append("First name must be at least 2 characters")
        elif len(first_name.strip()) > 50:
            errors.append("First name must be less than 50 characters")
        
        if not last_name or not last_name.strip():
            errors.append("Last name is required")
        elif len(last_name.strip()) < 2:
            errors.append("Last name must be at least 2 characters")
        elif len(last_name.strip()) > 50:
            errors.append("Last name must be less than 50 characters")
        
        # Phone validation
        if not phone or not phone.strip():
            errors.append("Phone number is required")
        else:
            # Remove all non-digit characters for validation
            phone_digits = ''.join(filter(str.isdigit, phone))
            if len(phone_digits) < 10:
                errors.append("Phone number must have at least 10 digits")
            elif len(phone_digits) > 15:
                errors.append("Phone number is too long")
        
        if errors:
            return {"valid": False, "message": "; ".join(errors)}
        else:
            return {"valid": True, "message": "Input validation passed"}

    def validate_passenger_exists_by_id(self, passenger_id):
        """Validate that a passenger exists by ID"""
        if not self.db_connection:
            return False
        
        try:
            passengers = Passenger.get_all_passengers(self.db_connection)
            if passengers:
                return any(p.passenger_id == passenger_id for p in passengers)
            return False
        except Exception:
            return False

    def delete_passenger_by_id(self, passenger_id):
        """Delete a passenger with business logic validation"""
        if not self.db_connection:
            return {"success": False, "message": "Database connection not established"}
        
        # Validate passenger ID
        if passenger_id is None or passenger_id <= 0:
            return {"success": False, "message": "Invalid passenger ID provided"}
        
        try:
            passenger_exists = self.validate_passenger_exists_by_id(passenger_id)
            if not passenger_exists:
                return {"success": False, "message": f"Passenger with ID {passenger_id} not found"}
            
            success = Passenger.delete_passenger(passenger_id, self.db_connection)
            
            if success:
                return {
                    "success": True, 
                    "message": f"Passenger with ID {passenger_id} deleted successfully"
                }
            else:
                return {
                    "success": False, 
                    "message": "Failed to delete passenger. Passenger may have existing bookings or database error occurred."
                }
                
        except Exception as e:
            return {"success": False, "message": f"Error deleting passenger: {str(e)}"}

    def add_new_vessel(self, vessel_name, cost_per_hour):
        """Add a new vessel with business logic validation"""
        if not self.db_connection:
            return {"success": False, "message": "Database connection not established"}
        
        # Validate inputs
        validation_result = self.validate_vessel_input(vessel_name, cost_per_hour)
        if not validation_result["valid"]:
            return {"success": False, "message": validation_result["message"]}
        
        try:
            existing_id = Vessel.get_vessel_id(vessel_name, self.db_connection)
            returned_id = Vessel.add_vessel(vessel_name, cost_per_hour, self.db_connection)

            if existing_id != -1 and existing_id == returned_id:
                return {
                    "success": False,
                    "message": f"Vessel '{vessel_name}' already exists with ID {existing_id}"
                }
            elif returned_id != -1:
                return {
                    "success": True,
                    "vessel_id": returned_id,
                    "message": f"Vessel '{vessel_name}' added successfully with ID {returned_id}"
                }
            else:
                return {
                    "success": False,
                    "message": "Failed to add vessel to database"
                }
                
        except Exception as e:
            return {"success": False, "message": f"Error adding vessel: {str(e)}"}

    def validate_vessel_input(self, vessel_name, cost_per_hour):
        """Validate vessel input data according to business rules"""
        errors = []
        
        # Vessel name validation
        if not vessel_name or not vessel_name.strip():
            errors.append("Vessel name is required")
        elif len(vessel_name.strip()) < 2:
            errors.append("Vessel name must be at least 2 characters")
        elif len(vessel_name.strip()) > 50:
            errors.append("Vessel name must be less than 50 characters")
        
        # Cost validation
        if cost_per_hour is None:
            errors.append("Cost per hour is required")
        elif cost_per_hour <= 0:
            errors.append("Cost per hour must be greater than 0")
        elif cost_per_hour > 10000:
            errors.append("Cost per hour seems unreasonably high (max $10,000)")
        
        if errors:
            return {"valid": False, "message": "; ".join(errors)}
        else:
            return {"valid": True, "message": "Input validation passed"}

    def delete_vessel_by_id(self, vessel_id):
        """Delete a vessel with business logic validation"""
        if not self.db_connection:
            return {"success": False, "message": "Database connection not established"}
        
        if vessel_id is None or vessel_id <= 0:
            return {"success": False, "message": "Invalid vessel ID provided"}
        
        try:
            vessel_exists = self.validate_vessel_exists_by_id(vessel_id)
            if not vessel_exists:
                return {"success": False, "message": f"Vessel with ID {vessel_id} not found"}
            
            success = Vessel.delete_vessel(vessel_id, self.db_connection)
            if success:
                return {
                    "success": True, 
                    "message": f"Vessel with ID {vessel_id} deleted successfully"
                }
            else:
                return {
                    "success": False, 
                    "message": "Failed to delete vessel. Vessel may have existing trips or database error occurred."
                }
                
        except Exception as e:
            return {"success": False, "message": f"Error deleting vessel: {str(e)}"}

    def validate_vessel_exists_by_id(self, vessel_id):
        """Validate that a vessel exists by ID"""
        if not self.db_connection:
            return False
        
        try:
            vessels = Vessel.get_all_vessels(self.db_connection)
            if vessels:
                return any(v.vessel_id == vessel_id for v in vessels)
            return False
        except Exception:
            return False