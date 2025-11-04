#
# restaurant.py
#
# Restaurant-oriented class definitions.
#

import exceptions
import pytock_data

# Restaurant class
#
# A Restaurant object maintains lists of tables and bookings. It can be 
# expanded to additional restaurant-oriented semantics if needed in the future.
#

class Restaurant:
    def __init__(self):
        self.tables = Tables()
        self.bookings = Bookings()


# Table class
#
# A Table object maintains the information about a specific table, which is the
# number of seats and the name of the table. Tables are created and deleted by
# a restaurant class.
#

class Table:
    # class constants
    MAX_SEATS = 12

    def __init__(self, name: str, seats: int):
        """
        Table::__init__ creates a new table object.

        Args:
            name: The name must be a non-empty, unique string.
            seats: Must be an integer from 1 through MAX_SEATS.

        Returns:
            Returns a table object

        Raises:
            InvalidInputError: invalid name or seats argument

        """
        if not isinstance(name, str) or (name := name.strip()) == "":
            raise exceptions.InvalidInputError(f"invalid name argument '{name}'")
        if not isinstance(seats, int) or seats < 1 or seats > Table.MAX_SEATS:
            raise exceptions.InvalidInputError(f"invalid seats argument '{seats}'")
        
        self.name = name
        self.seats = seats


# Tables class
#
# A Tables object maintains a list of tables and their group semantics, such as
# ensuring a unique name.
#

class Tables:
    # class constants
    MAX_SEATS = 12

    def __init__(self):
        self.tables = []

    def createTable(self, name: str, seats: int) -> Table:
        """
        Create a table and add it to our list.

        Args:
            name: The name must be a non-empty, unique string.
            seats: Must be an integer from 1 through 10.

        Returns:
            The new table object.

        Raises:
            InvalidInputError: invalid name or seats argument
            DuplicateNameError: a table with that name already exists
        """
        for table in self.tables:
            if name == table.name:
                raise exceptions.DuplicateNameError(f"table name {name} already exists")
        table = Table(name, seats)
        self.tables.append(table)

    def deleteTable(self, table: Table) -> None:
        """
        Delete a table from our list

        Args:
            table: Table.

        Returns:
            None.

        Raises:
            ValueError if table is not in list.
        """
        self.tables.remove(table)
    
    def findTable(self, name: str) -> Table:
        """
        Find a table by name.

        Args:
            name: The exact name to find

        Returns:
            Table or None.

        Raises:
            None.
        """
        for table in self.tables:
            if name == table.name:
                return table
        return None


# Booking class
#
# A Booking object tracks the state of a specific booking, which includes the
# table, phone, start time, and reservation period.
#

class Booking:
    def __init__(self, table, name, phone, start, period):
        self.table = table
        self.name = name
        self.phone = phone
        self.start = start
        self.period = period


# Bookings class
#
# A Bookings object maintains a list of bookings and their group semantics, such
# as ensuring that there are no overlapping reservations for the same table, or
# that a name/phone has not been used for double-booking.
#

class Bookings:
    # class constants
    MAX_PERIOD = 8*3600                 # no more than 8 hours

    def tableStatus():
        """
        Report the booking status by tables.

        Args:
            None.

        Returns:
            Dictionary with table names as keys and array of bookings as data.

        Raises:
            None.
        """
