#
# restaurant.py
#
# Restaurant-oriented class definitions. Class defintions here are:
#
#   Table  - an object representing a specific table that can be booked
#   Tables - an object representing a collection of tables having unique names.
#   Booking - a specific booking with name/phone/start/period/table
#   Bookings - a collection of bookings
#
# These are POD objects to make it easy to manage them in streamlit. Backend
# storage is just the streamlit shared cache resource, so callers may freely
# instantiate the collections, which are read from the cache. This simplifies
# change detection and notification to other browsers and tabs sharing our
# backend, so that UI updates can occur in real time.
#

import exceptions
import datetime
import pytock_data


#
# Table class
#
# Just POD with some additional semantics important to tables.
#

class Table:
    """
    A Table object maintains the information about a specific table, which is
    the number of seats and the name of the table. Table objects are created 
    and deleted by a Tables object.
    """

    # class constants
    MAX_SEATS = 12

    @classmethod
    def compareByStartKey(cls, table: 'Table') -> str:
        return table.name

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
        
        self._name = name
        self._seats = seats

    @property
    def name(self):
        """Name of the table."""
        return self._name

    @property
    def seats(self):
        """Number of seats at the table."""
        return self._seats

    def description(self):
        """
        Display a short description: string <name> - <N> seats.

        Args:
            None.

        Returns:
            string.

        Raises:
            None.
        """

        return f"{self.name} - {self.seats} seats"


#
# Tables class
#
# A Tables object is a collection of Table objects, where the "source of truth"
# and backing data storage is the shared streamlit backend resource cache.
# Callers may instantiate a new Tables() object at any time and it will have the
# latest data.
#
# The Tables class enforces unique names among the Table objects, and offers
# demographics like total tables and seats as well as the usual CRUD operations.
#
# To avoid being annoying during testing, this creates 3 default tables when it
# is first initializes, but allows all tables to be deleted.
#

class Tables:
    """
    A Tables object maintains a list of tables and their group semantics, such as
    ensuring a unique name.
    """

    # class constants
    MAX_SEATS = 12
    DEF_SEATS = 4

    def __init__(self):
        """
        Read latest state
        """
        self.__reload()

    def __reload(self):
        self.tables = pytock_data.get("restaurant_tables")
        if not isinstance(self.tables, list):       # allow tables list to be empty
            self.tables = [Table("Table 1", 4), Table("Table 2", 4), Table("Table 3", 6)]
            self.__save()

    def __save(self):
        """
        Save our state
        """
        pytock_data.set("restaurant_tables", self.tables)

    def defName(self) -> str:
        """
        Return a unique default name for a possible new table.
        """
        counter = 0
        while True:
            counter += 1
            tablename = f"Table {counter}"
            if not self.findTable(tablename):
                return tablename
    
    def capacity(self) -> tuple[int, int]:
        """
        Report the total table and seat capacity.

        Args:
            None.

        Returns:
            tables, seats.

        Raises:
            None.
        """
        tableCount = 0
        seatCount = 0
        for table in self.tables:
            tableCount += 1
            seatCount += table.seats
        return tableCount, seatCount

    def namelist(self) -> list[str]:
        """
        Get the sorted list of table names.

        Args:
            None.

        Returns:
            an array of strings.

        Raises:
            None.
        """
        return [table.name for table in self.tables]

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
        self.tables.sort(key=Table.compareByStartKey)
        self.__save()
        return table

    def findTable(self, tablename: str) -> Table:
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
            if tablename == table.name:
                return table
        return None

    def deleteTable(self, tablename: str) -> None:
        """
        Delete a table by name from our list

        Args:
            tablename string.

        Returns:
            None.

        Raises:
            InternalError if table is not in list.
        """
        table = self.findTable(tablename)
        if not table:
            raise exceptions.InternalError
        self.tables.remove(table)
        self.__save()


#
# Booking class
#
# Just POD with some additional semantics important to bookings. There are two
# types of bookings:
#   - advance bookings with customer name / phone / start time / period
#   - walk-in bookings with none of those parameters, created with the WalkIn
#     class method. The start time is arranged to sort before advance bookings.
#

class Booking:
    """
    A Booking object tracks the state of a specific booking, which includes the
    table, phone, start time, and reservation period.
    """
    
    @classmethod
    def WalkIn(cls, tablename: str):
        booking = cls(tablename, "Walk-In Guest", "", datetime.time(hour=0,minute=0,second=0), datetime.time(hour=23,minute=59,second=59))
        booking.walkInGuest = True
        return booking

    @classmethod
    def compareByStartKey(cls, bk: 'Booking') -> datetime.datetime:
        return bk.start

    @classmethod
    def defBookingTime(cls) -> datetime.datetime:
        """
        Provide a default booking time with no conflict resolution.
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
    def defBookingPeriod(cls) -> datetime.datetime:
        return datetime.timedelta(minutes=90) + datetime.datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)

    @classmethod
    def maxBookingTime(cls) -> datetime.time:
        # maximum table booking time is 8 hours
        return datetime.time(8, 0)

    def __init__(self, tablename, name, phone, start, period):
        self._tablename = tablename
        self._name = name
        self._phone = phone
        todate = datetime.datetime.today().date()
        self._start = datetime.datetime.combine(todate, start)
        self._period = period
        self._walkInGuest = False

    @property
    def tablename(self):
        """Name of the booked table."""
        return self._tablename

    @property
    def name(self):
        """Customer name."""
        return self._name

    @property
    def phone(self):
        """Customer phone."""
        return self._phone

    @property
    def start(self):
        """Start datetime.datetime."""
        return self._start

    @property
    def period(self):
        """Period datetime.time."""
        return self._period

    @property
    def walkInGuest(self):
        """Customer phone."""
        return self._walkInGuest

    @walkInGuest.setter
    def walkInGuest(self, value: bool):
        """Walk-in flag."""
        if self._walkInGuest and not value:
            raise exceptions.InternalError                  # cannot unset this
        self._walkInGuest = value

    def keyString(self) -> str:
        return "-".join([self.tablename, self.name, self.phone, str(self.start), str(self.period)])

    def expired(self, now: datetime.datetime) -> bool:
        # bookings never expire because we live in a timeless world
        False
    
    def overlap(self, booking: 'Booking') -> bool:
        """
        True iff the other booking overlaps us in time.

        Args:
            None.

        Returns:
            bool.

        Raises:
            None.
        """

        our_end = self.start + datetime.timedelta(hours=self.period.hour, minutes=self.period.minute)
        his_end = booking.start + datetime.timedelta(hours=booking.period.hour, minutes=booking.period.minute)
        if booking.start < our_end and his_end >= self.start:
            return True
        if self.start < his_end and our_end >= booking.start:
            return True
        False
    
    def duplicate(self, booking: 'Booking', matchTable: bool = False) -> bool:
        """
        True iff the other booking overlaps us in time and name/phone. 

        Args:
            None.

        Returns:
            bool.

        Raises:
            None.
        """

        if self.name != booking.name or self.phone != booking.phone:
            return False
        if matchTable and booking.tablename != self.tablename:
            return False
        if self.overlap(booking):
            return True
        False

    def equals(self, booking: 'Booking') -> bool:
        """
        True iff the other booking matches us exactly.
            <time> / <period>
            <name> / <phone>

        Args:
            None.

        Returns:
            string.

        Raises:
            None.
        """
        return self.tablename == booking.tablename \
            and self.name == booking.name \
            and self.phone == booking.phone \
            and self.start == booking.start \
            and self.period == booking.period

    def description(self) -> str:
        """
        Display a description string:
            <time> / <period>
            <name> / <phone>

        Args:
            None.

        Returns:
            string.

        Raises:
            None.
        """

        if self.walkInGuest:
            return \
            """
            Walk-In Guest  
            """
        else:
            return \
                """
                **{0}** / *{1}*  
                **{2}** / *{3}*  
                """.format(self.start.strftime("%H:%M"), self.period.strftime("%H:%M"), self.name, self.phone)


#
# Bookings class
#
# A Bookings object is a collection of Booking objects, where the "source of
# truth" and backing data storage is the shared streamlit backend resource
# cache. Callers may instantiate a new Bookings() object at any time and it will
# have the latest data.
#
# Bookings references tables, but the reverse is carefully avoided. A Table is
# created or deleted without any notice to Bookings, so it is necessary to check
# that all referenced tables exist when performing booking operations. Bookings
# with missing tables are culled when identified by the self.__tableGC() method.
# Design alternatives would require more coupling between tables and bookings,
# which is better avoided where possible.
#
# Conflict management is quite simplified from the real world. Customers are the
# same if their name and phone number match exactly. Customers may have as many
# bookings as they like that do not overlap, but they may not book more than one
# table at any given time.
#
# Because this is a classroom project it does not actually track real time. The
# date/time model used here is a single day where the period of a booking can
# overflow to the next day. Obviously in a real system bookings would be used or
# expired, but here we are apart from time and tables are considered "free" only
# when they have no bookings at any time.
#
# WalkIns are just another booking, except that they are in addition to any
# existing advance booking for the table involved. At most one walkIn is allowed
# for each table.
#

class Bookings:
    """
    A Bookings object maintains a list of bookings and their group semantics,
    such as ensuring that there are no overlapping reservations for the same
    table, or that a name/phone has not been used for double-booking.
    """

    def __init__(self):
        self.__reload()

    def __reload(self):
        """
        Read latest state
        """
        self.bookings = pytock_data.get("restaurant_bookings")
        if not self.bookings:
            self.bookings = []
            self.__save()

    def __save(self):
        """
        Save our state
        """
        pytock_data.set("restaurant_bookings", self.bookings)

    def __tableGC(self):
        """
        Remove bookings that reference missing tables.
        """
        tables = Tables()
        now = datetime.datetime.now()
        self.bookings = [bk for bk in self.bookings if self.__validBooking(bk, tables, now)]
        self.__save()
        return tables

    def __validBooking(self, bk: Booking, tables: Tables, now: datetime.datetime) -> bool:
        """
        Return true iff booking is still valid
        """
        return tables.findTable(bk.tablename) and not bk.expired(now)

    def utilization(self) -> tuple[int, int]:
        """
        Report the utilized (non-free) tables and seats.

        Args:
            None.

        Returns:
            tables, seats.

        Raises:
            None.
        """
        tables = self.__tableGC()
        utilized = { }
        tableCount = 0
        seatCount = 0
        for bk in self.bookings:
            table = tables.findTable(bk.tablename)
            if not bk.tablename in utilized:
                utilized[bk.tablename] = True
                tableCount += 1
                seatCount += table.seats
        return tableCount, seatCount

    def tableStatus(self) -> dict:
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

        self.__tableGC()
        output = { }
        for bk in self.bookings:
            if bk.tablename in output:
                output[bk.tablename].append(bk)
            else:
                output[bk.tablename] = [bk]
        for tablename, bookings in output.items():
            bookings.sort(key=Booking.compareByStartKey)
        return output

    def bookingAvailable(self, booking: Booking) -> bool:
        """
        Check if a new booking would conflict in time and table. This ignores
        the name and phone.

        Args:
            Booking object.

        Returns:
            True if available, otherwise False.

        Raises:
            None.
        """
        self.__tableGC()
        for bk in self.bookings:
            if bk.tablename == booking.tablename and bk.overlap(booking):
                return False
        return True

    def bookingDuplicate(self, booking: Booking, matchTable: bool = False) -> bool:
        """
        Check if a new booking would conflict in time and name/phone. This is
        useful for checking if the customer has an existing booking during the
        same time range.

        Args:
            Booking object.

        Returns:
            True if duplicated, otherwise False.

        Raises:
            None.
        """
        self.__tableGC()
        for bk in self.bookings:
            if bk.duplicate(booking, matchTable):
                return True
        return False

    def add(self, booking: Booking) -> bool:
        """
        Add a booking if the time and table are available.

        Args:
            Booking object.

        Returns:
            True iff successfully booked.

        Raises:
            TableBusyError.
        """
        if self.bookingDuplicate(booking):
            raise exceptions.DuplicateBookingError
        if not self.bookingAvailable(booking):
            raise exceptions.TableBusyError
        self.bookings.append(booking)
        self.__save()
        return True

    def delete(self, booking: Booking) -> None:
        """
        Delete a matching booking if it exists.

        Args:
            Booking object.

        Returns:
            None.

        Raises:
            None.
        """
        self.__tableGC()
        self.bookings = [bk for bk in self.bookings if not bk.equals(booking)]
        self.__save()
    
    def walkInAvailable(self, tablename: str) -> bool:
        """
        True if table available for a walkIn customer, or False otherwise.

        Args:
            tablename.

        Returns:
            None.

        Raises:
            None.
        """
        if not tablename:
            return False
        booking = Booking.WalkIn(tablename)
        return not self.bookingDuplicate(booking, True)

    def walkIn(self, tablename: str) -> None:
        """
        Take the table for a walkIn customer, overriding any booking.

        Args:
            tablename.

        Returns:
            None.

        Raises:
            TableBusyError if already taken for a walkIn.
        """
        booking = Booking.WalkIn(tablename)
        if self.bookingDuplicate(booking, True):
            raise exceptions.TableBusyError
        self.bookings.append(booking)
        self.__save()

    def walkOut(self, tablename: str) -> None:
        """
        Release the table from a walkIn customer.

        Args:
            tablename.

        Returns:
            None.

        Raises:
            TableFreeError if not already taken for a walkIn.
        """
        booking = Booking.WalkIn(tablename)
        if not self.bookingDuplicate(booking, True):
            raise exceptions.TableFreeError
        self.delete(booking)
