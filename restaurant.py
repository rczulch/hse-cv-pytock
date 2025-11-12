#
# restaurant.py
#
# Restaurant-oriented class definitions.
#

import exceptions
import datetime
import pytock_data


#
# Restaurant class
#

class Restaurant:
    """
    A Restaurant object maintains lists of tables and bookings. It can be 
    expanded to additional restaurant-oriented semantics if needed in the future
    """

    def __init__(self):
        self.tables = Tables()
        self.bookings = Bookings()


#
# Table class
#

class Table:
    """
    A Table object maintains the information about a specific table, which is
    the number of seats and the name of the table. Table objects are created 
    and deleted by a Tables object.
    """

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


#
# Tables class
#

class Tables:
    """
    A Tables object maintains a list of tables and their group semantics, such as
    ensuring a unique name.
    """

    # class constants
    MAX_SEATS = 12

    def __init__(self):
        self.reload()

    def reload(self):
        self.tables = pytock_data.get("restaurant_tables")
        if not self.tables:
            self.tables = [Table("Table 1", 4), Table("Table 2", 4), Table("Table 3", 6)]
            self.save()

    def save(self):
        pytock_data.set("restaurant_tables", self.tables)

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
        self.save()

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
        self.save()

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


#
# Booking class
#

class Booking:
    """
    A Booking object tracks the state of a specific booking, which includes the
    table, phone, start time, and reservation period.
    """

    @classmethod
    def compareByStart(cls, bk1, bk2):
        if bk1.start < bk2.start:
            return -1
        elif bk1.start > bk2.start:
            return 1
        else:
            return 0

    @classmethod
    def defBookingTime(cls):
        """
        Provide a default booking time.
        """

        # get current time + 1 hour
        deftime = datetime.datetime.now()
    
        # Calculate the remaining minutes and seconds to the next hour
        minutes_to_add = (60 - deftime.minute) % 60
        seconds_to_add = (60 - deftime.second) % 60

        # Add a timedelta for the remaining time to get to at least another hour
        time_to_next_hour = datetime.timedelta(hours=1, minutes=minutes_to_add, seconds=seconds_to_add)
        rounded_time = datetime.datetime.now() + time_to_next_hour

        # Zero out minutes, seconds, and microseconds
        rounded_time = rounded_time.replace(minute=0, second=0, microsecond=0)
        return rounded_time

    @classmethod
    def defBookingPeriod(cls):
        return datetime.timedelta(minutes=90) + datetime.datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)

    @classmethod
    def maxBookingTime(cls):
        # maximum table booking time is 8 hours
        return datetime.time(8, 0)

    def __init__(self, table, name, phone, start, period):
        self.table = table
        self.name = name
        self.phone = phone
        self.start = start
        self.period = period
    
    def expired(self, now):
        complete = datetime.timedelta()


#
# Bookings class
#

class Bookings:
    """
    A Bookings object maintains a list of bookings and their group semantics,
    such as ensuring that there are no overlapping reservations for the same
    table, or that a name/phone has not been used for double-booking.
    """

    def __init__(self):
        self.reload()

    def reload(self):
        self.bookings = pytock_data.get("restaurant_bookings")
        if not self.bookings:
            self.bookings = []
            self.save()

    def save(self):
        pytock_data.set("restaurant_bookings", self.bookings)

    def validBooking(self, bk, tables, now):
        """
        Return true iff booking is still valid
        """
        return tables.findTable(bk.table) and not bk.expired(now)

    def tableGC(self):
        """
        Remove bookings that reference missing tables.
        """
        tables = Tables()
        now = datetime.datetime.now()
        self.bookings = [bk for bk in self.bookings if self.validBooking(bk, tables, now)]

    def tableStatus(self):
        """
        Report the booking status by tables.

        Args:
            None.

        Returns:
            Dictionary with table names as keys and array of Booking objects
            as data. Each array of bookings is sorted by start time.

        Raises:
            None.
        """

        self.tableGC()
        output = { }
        for bk in self.bookings:
            if output[bk.table]:
                output[bk.table].append(bk)
            else:
                output[bk.table] = [bk]
        for table, bookings in output:
            bookings.sort(cmp=Booking.compareByStart)
        return output

    def add(self, booking):
        """
        Add a booking.

        Args:
            Booking object.

        Returns:
            True iff successfully booked.

        Raises:
            TableBusyError.
        """
