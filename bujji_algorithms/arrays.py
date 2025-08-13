import sys
import time
from array import array


class StaticArray:
    """
    A fixed-size collection of elements stored in contiguous memory.

    This implementation uses Python's built-in ``array`` module for memory efficiency,
    storing elements of the same type in contiguous memory.

    Parameters
    ----------
    size : int
        The fixed size (number of elements).
    typecode : str, optional
        Typecode for elements (default is 'i' for signed integers).
        Example typecodes:
            'i' - signed int
            'f' - float
            'u' - unicode character
    fill_value : Any, optional
        Value used to initialize all elements (default is 0).
        Must be compatible with the chosen `typecode`.

    Notes
    -----
    - "Static" here means the *size* is fixed after creation. The element values
      at existing indices are mutable (you can overwrite them).
    - Assignments are type-checked and will raise a clear TypeError if the value
      is incompatible with the array's typecode.

    Example
    -------
    >>> arr = StaticArray(5, typecode='i', fill_value=1)
    >>> arr
    StaticArray([1, 1, 1, 1, 1])

    Valid assignment:
    >>> arr[2] = 10
    >>> arr[2]
    10

    Negative indexing:
    >>> arr[-1] = 9
    >>> arr[-1]
    9

    Wrong-type assignment (raises clear error):
    >>> arr[0] = "hello"
    TypeError: StaticArray: invalid value type; expected value compatible with typecode 'i'

    Useful methods:
      - len(arr) -> 5
      - for x in arr: ...
      - 10 in arr
      - arr.fill(0)
      - arr.to_list()
      - arr.count(0)
      - arr.copy()
    """

    __slots__ = ['_data', '_size']

    def __init__(self, size, typecode='i', fill_value=0):
        if size < 0:
            raise ValueError("size must be non-negative")
        # Construct using the array module; this will raise a TypeError if fill_value is incompatible.
        self._size = size
        self._data = array(typecode, [fill_value] * size)

    def _normalize_index(self, index):
        """Normalize negative indices to positive and validate range."""
        if not -self._size <= index < self._size:
            raise IndexError("Index out of range")
        if index < 0:
            index += self._size
        return index

    def __getitem__(self, index):
        idx = self._normalize_index(index)
        return self._data[idx]

    def __setitem__(self, index, value):
        idx = self._normalize_index(index)
        # Attempt assignment; if underlying array rejects the type, raise a clearer error.
        try:
            self._data[idx] = value
        except TypeError:
            raise TypeError(
                f"StaticArray: invalid value type; expected value compatible with typecode '{self._data.typecode}'"
            )

    def __len__(self):
        return self._size

    def __iter__(self):
        return iter(self._data)

    def __repr__(self):
        return f"StaticArray({list(self._data)})"

    def __contains__(self, value):
        return value in self._data

    def fill(self, value):
        """Fill the entire array with a given value (must be compatible with typecode)."""
        # Assign via indexed writes to get consistent error messages on invalid types.
        for i in range(self._size):
            try:
                self._data[i] = value
            except TypeError:
                raise TypeError(
                    f"StaticArray: invalid value type for fill; expected value compatible with typecode '{self._data.typecode}'"
                )

    def to_list(self):
        """Return a Python list copy of the array."""
        return list(self._data)

    def count(self, value):
        """Count occurrences of a value."""
        return sum(1 for v in self._data if v == value)

    def copy(self):
        """Return a copy of this StaticArray (preserves typecode)."""
        # Create a shallow copy of the underlying array (works for all typecodes).
        new_arr = object.__new__(StaticArray)
        new_arr._size = self._size
        new_arr._data = array(self._data.typecode, self._data)  # copy underlying buffer
        return new_arr


class DynamicArray:
    """
    A resizable array that grows as elements are added.

    Internally uses Python's built-in ``array`` module for contiguous
    memory storage, doubling capacity when full (amortized O(1) append).

    Parameters
    ----------
    typecode : str, optional
        Typecode for elements (default is 'i' for signed integers).
    initial_capacity : int, optional
        Starting capacity of the array (default is 1).

    Example
    -------
    >>> arr = DynamicArray(typecode='i')
    >>> arr.append(1)
    >>> arr.append(2)
    >>> arr
    DynamicArray([1, 2], size=2, capacity=2)

    Access elements:
    >>> arr[1]
    2

    Insert at index:
    >>> arr.insert(1, 5)
    >>> arr
    DynamicArray([1, 5, 2], size=3, capacity=4)

    Remove an element:
    >>> arr.remove(5)
    >>> arr
    DynamicArray([1, 2], size=2, capacity=4)

    Convert to Python list:
    >>> arr.to_list()
    [1, 2]
    """

    __slots__ = ['_data', '_size', '_capacity', '_typecode']

    def __init__(self, typecode='i', initial_capacity=1):
        if initial_capacity <= 0:
            raise ValueError("initial_capacity must be > 0")
        self._typecode = typecode
        self._capacity = initial_capacity
        self._size = 0
        self._data = array(typecode, [0] * initial_capacity)

    def _resize(self, new_capacity):
        """Resize the internal array to new_capacity."""
        new_data = array(self._typecode, [0] * new_capacity)
        for i in range(self._size):
            new_data[i] = self._data[i]
        self._data = new_data
        self._capacity = new_capacity

    def append(self, value):
        """Add a value to the end of the array."""
        try:
            if self._size == self._capacity:
                self._resize(self._capacity * 2)
            self._data[self._size] = value
            self._size += 1
        except TypeError:
            raise TypeError(
                f"DynamicArray: invalid value type; expected value compatible with typecode '{self._typecode}'"
            )

    def insert(self, index, value):
        """Insert value at a given index (shifts elements right)."""
        if not 0 <= index <= self._size:
            raise IndexError("Index out of range")
        if self._size == self._capacity:
            self._resize(self._capacity * 2)
        for i in range(self._size, index, -1):
            self._data[i] = self._data[i - 1]
        try:
            self._data[index] = value
        except TypeError:
            raise TypeError(
                f"DynamicArray: invalid value type; expected value compatible with typecode '{self._typecode}'"
            )
        self._size += 1

    def remove(self, value):
        """Remove first occurrence of value (shifts elements left)."""
        for i in range(self._size):
            if self._data[i] == value:
                for j in range(i, self._size - 1):
                    self._data[j] = self._data[j + 1]
                self._size -= 1
                return
        raise ValueError(f"{value} not found in DynamicArray")

    def __getitem__(self, index):
        if not -self._size <= index < self._size:
            raise IndexError("Index out of range")
        if index < 0:
            index += self._size
        return self._data[index]

    def __setitem__(self, index, value):
        if not -self._size <= index < self._size:
            raise IndexError("Index out of range")
        if index < 0:
            index += self._size
        try:
            self._data[index] = value
        except TypeError:
            raise TypeError(
                f"DynamicArray: invalid value type; expected value compatible with typecode '{self._typecode}'"
            )

    def __len__(self):
        return self._size

    def __iter__(self):
        for i in range(self._size):
            yield self._data[i]

    def __repr__(self):
        return f"DynamicArray({[self._data[i] for i in range(self._size)]}, size={self._size}, capacity={self._capacity})"

    def to_list(self):
        """Return a Python list copy of the array's contents."""
        return [self._data[i] for i in range(self._size)]


class TwoDArray:
    """
    A 2D matrix-like grid of rows and columns stored in contiguous memory.

    Uses row-major order with Python's built-in ``array`` for memory efficiency.
    The size (rows × cols) is fixed at creation.

    Parameters
    ----------
    rows : int
        Number of rows in the array.
    cols : int
        Number of columns in the array.
    typecode : str, optional
        Typecode for elements (default is 'i' for signed integers).
    fill_value : Any, optional
        Value to initialize all cells with (default is 0).

    Example
    -------
    >>> mat = TwoDArray(2, 3, typecode='i', fill_value=1)
    >>> print(mat)
    TwoDArray(2x3):
    [1, 1, 1]
    [1, 1, 1]

    Access elements:
    >>> mat.get(0, 1)
    1
    >>> mat[0][1]
    1

    Modify elements:
    >>> mat.set(0, 1, 9)
    >>> print(mat)
    TwoDArray(2x3):
    [1, 9, 1]
    [1, 1, 1]

    Get dimensions:
    >>> mat.shape
    (2, 3)
    """

    __slots__ = ['_data', '_rows', '_cols', '_typecode']

    def __init__(self, rows, cols, typecode='i', fill_value=0):
        if rows <= 0 or cols <= 0:
            raise ValueError("rows and cols must be positive integers")
        self._rows = rows
        self._cols = cols
        self._typecode = typecode
        self._data = array(typecode, [fill_value] * (rows * cols))

    @property
    def shape(self):
        """Return (rows, cols) tuple."""
        return (self._rows, self._cols)

    def _index(self, row, col):
        """Convert 2D coordinates to 1D index."""
        if not (0 <= row < self._rows and 0 <= col < self._cols):
            raise IndexError("row or column index out of range")
        return row * self._cols + col

    def get(self, row, col):
        """Get value at (row, col)."""
        return self._data[self._index(row, col)]

    def set(self, row, col, value):
        """Set value at (row, col)."""
        try:
            self._data[self._index(row, col)] = value
        except TypeError:
            raise TypeError(
                f"TwoDArray: invalid value type; expected type compatible with '{self._typecode}'"
            )

    def __getitem__(self, row):
        """Return a list-like view of a row."""
        if not 0 <= row < self._rows:
            raise IndexError("row index out of range")
        start = row * self._cols
        end = start + self._cols
        return self._data[start:end]

    def __len__(self):
        """Number of rows."""
        return self._rows

    def __repr__(self):
        rows_str = "\n".join(
            str(list(self._data[r * self._cols:(r + 1) * self._cols]))
            for r in range(self._rows)
        )
        return f"TwoDArray({self._rows}x{self._cols}):\n{rows_str}"


class SparseMatrix:
    """
    A memory-efficient matrix with mostly zero or empty values.

    Stores only non-default values internally in a dictionary, with
    (row, col) tuples as keys.

    Parameters
    ----------
    rows : int
        Number of rows.
    cols : int
        Number of columns.
    default_value : Any, optional
        Value to treat as "empty" (default is 0).

    Example
    -------
    >>> sm = SparseMatrix(3, 3)
    >>> sm.set(0, 1, 5)
    >>> sm.set(2, 2, 8)
    >>> print(sm)
    SparseMatrix(3x3):
    [0, 5, 0]
    [0, 0, 0]
    [0, 0, 8]

    Access elements:
    >>> sm.get(0, 1)
    5
    >>> sm.get(1, 1)
    0

    Remove a value (set to default):
    >>> sm.set(0, 1, 0)
    >>> sm.get(0, 1)
    0
    """

    __slots__ = ['_rows', '_cols', '_default', '_data']

    def __init__(self, rows, cols, default_value=0):
        if rows <= 0 or cols <= 0:
            raise ValueError("rows and cols must be positive integers")
        self._rows = rows
        self._cols = cols
        self._default = default_value
        self._data = {}  # {(row, col): value}

    @property
    def shape(self):
        """Return (rows, cols)."""
        return (self._rows, self._cols)

    def _check_index(self, row, col):
        if not (0 <= row < self._rows and 0 <= col < self._cols):
            raise IndexError("row or column index out of range")

    def get(self, row, col):
        """Get the value at (row, col)."""
        self._check_index(row, col)
        return self._data.get((row, col), self._default)

    def set(self, row, col, value):
        """Set the value at (row, col). If value == default, remove the entry."""
        self._check_index(row, col)
        if value == self._default:
            self._data.pop((row, col), None)
        else:
            self._data[(row, col)] = value

    def __getitem__(self, row):
        """Return a full row as a list."""
        if not 0 <= row < self._rows:
            raise IndexError("row index out of range")
        return [self._data.get((row, c), self._default) for c in range(self._cols)]

    def __len__(self):
        """Number of rows."""
        return self._rows

    def __repr__(self):
        rows_str = "\n".join(
            str([self._data.get((r, c), self._default) for c in range(self._cols)])
            for r in range(self._rows)
        )
        return f"SparseMatrix({self._rows}x{self._cols}):\n{rows_str}"


class CircularArray:
    """
    Circular Array (Ring Buffer) with fixed capacity.

    Stores elements in a fixed-size buffer and overwrites the oldest element
    when full (optional behavior). Supports push/pop at both ends in O(1) time.

    Parameters
    ----------
    capacity : int
        Maximum number of elements in the buffer.
    typecode : str, optional
        Typecode for the array elements (default is 'i' for integers).
    overwrite : bool, optional
        If True, overwrite oldest values when buffer is full (default False).

    Example
    -------
    >>> buf = CircularArray(3, typecode='i', overwrite=True)
    >>> buf.push_back(1)
    >>> buf.push_back(2)
    >>> buf.push_back(3)
    >>> buf.push_back(4)  # overwrites oldest
    >>> list(buf)
    [2, 3, 4]

    >>> buf.push_front(10)
    >>> list(buf)
    [10, 2, 3]
    """

    __slots__ = ['_data', '_capacity', '_typecode', '_size', '_front', '_rear', '_overwrite']

    def __init__(self, capacity, typecode='i', overwrite=False):
        if capacity <= 0:
            raise ValueError("capacity must be > 0")
        self._capacity = capacity
        self._typecode = typecode
        self._overwrite = overwrite
        self._data = array(typecode, [0] * capacity)
        self._size = 0
        self._front = 0
        self._rear = -1

    def _advance(self, index):
        """Move index forward by 1 with wrap-around."""
        return (index + 1) % self._capacity

    def _retreat(self, index):
        """Move index backward by 1 with wrap-around."""
        return (index - 1 + self._capacity) % self._capacity

    def push_back(self, value):
        """Insert value at the rear."""
        if self._size == self._capacity:
            if not self._overwrite:
                raise OverflowError("CircularArray is full")
            self._front = self._advance(self._front)
        else:
            self._size += 1
        self._rear = self._advance(self._rear)
        try:
            self._data[self._rear] = value
        except TypeError:
            raise TypeError(
                f"CircularArray: invalid value type; expected type compatible with '{self._typecode}'"
            )

    def push_front(self, value):
        """Insert value at the front."""
        if self._size == self._capacity:
            if not self._overwrite:
                raise OverflowError("CircularArray is full")
            self._rear = self._retreat(self._rear)
        else:
            self._size += 1
        self._front = self._retreat(self._front)
        try:
            self._data[self._front] = value
        except TypeError:
            raise TypeError(
                f"CircularArray: invalid value type; expected type compatible with '{self._typecode}'"
            )

    def pop_front(self):
        """Remove and return value from the front."""
        if self._size == 0:
            raise IndexError("CircularArray is empty")
        value = self._data[self._front]
        self._front = self._advance(self._front)
        self._size -= 1
        return value

    def pop_back(self):
        """Remove and return value from the rear."""
        if self._size == 0:
            raise IndexError("CircularArray is empty")
        value = self._data[self._rear]
        self._rear = self._retreat(self._rear)
        self._size -= 1
        return value

    def __len__(self):
        return self._size

    def __iter__(self):
        idx = self._front
        for _ in range(self._size):
            yield self._data[idx]
            idx = self._advance(idx)

    def __repr__(self):
        return f"CircularArray({list(self)}, size={self._size}, capacity={self._capacity})"


class BitArray:
    """
    BitArray (Bit Vector) — compact storage for boolean values.

    Stores bits in a byte array for memory efficiency.

    Parameters
    ----------
    size : int
        Number of bits in the array.
    fill : bool, optional
        Initial value for all bits (default False).

    Example
    -------
    >>> bits = BitArray(10)
    >>> bits.set(3, True)
    >>> bits.get(3)
    True
    >>> bits[3]
    True
    >>> bits.count()
    1
    """

    __slots__ = ['_size', '_data']

    def __init__(self, size, fill=False):
        if size <= 0:
            raise ValueError("size must be > 0")
        self._size = size
        byte_count = (size + 7) // 8
        init_byte = 0xFF if fill else 0x00
        self._data = array('B', [init_byte] * byte_count)

    def _check_index(self, index):
        if not 0 <= index < self._size:
            raise IndexError("bit index out of range")

    def set(self, index, value: bool):
        """Set the bit at index to True or False."""
        self._check_index(index)
        byte_index, bit_pos = divmod(index, 8)
        if value:
            self._data[byte_index] |= (1 << bit_pos)
        else:
            self._data[byte_index] &= ~(1 << bit_pos)

    def get(self, index):
        """Get the boolean value of the bit at index."""
        self._check_index(index)
        byte_index, bit_pos = divmod(index, 8)
        return bool(self._data[byte_index] & (1 << bit_pos))

    def __getitem__(self, index):
        return self.get(index)

    def __setitem__(self, index, value):
        self.set(index, value)

    def toggle(self, index):
        """Flip the bit at index."""
        self._check_index(index)
        byte_index, bit_pos = divmod(index, 8)
        self._data[byte_index] ^= (1 << bit_pos)

    def count(self):
        """Return the number of bits set to True."""
        return sum(bin(byte).count('1') for byte in self._data)

    def __len__(self):
        return self._size

    def __repr__(self):
        bits_str = ''.join(
            '1' if self.get(i) else '0' for i in range(self._size)
        )
        return f"BitArray({bits_str})"


class ColumnMajor2DArray:
    """
    Column-Major 2D Array (Fortran-style memory layout).

    Stores elements in a single 1D array in column-major order:
    all elements of column 0, then column 1, etc.

    Parameters
    ----------
    rows : int
        Number of rows.
    cols : int
        Number of columns.
    typecode : str, optional
        Typecode for the array elements (default 'i').
    fill_value : optional
        Initial value for all elements (default 0).

    Example
    -------
    >>> mat = ColumnMajor2DArray(2, 3, fill_value=0)
    >>> mat.set(0, 1, 5)
    >>> mat.get(0, 1)
    5
    >>> print(mat)
    ColumnMajor2DArray(2x3):
    [0, 5, 0]
    [0, 0, 0]
    """

    __slots__ = ['_rows', '_cols', '_data', '_typecode']

    def __init__(self, rows, cols, typecode='i', fill_value=0):
        if rows <= 0 or cols <= 0:
            raise ValueError("rows and cols must be > 0")
        self._rows = rows
        self._cols = cols
        self._typecode = typecode
        self._data = array(typecode, [fill_value] * (rows * cols))

    @property
    def shape(self):
        return (self._rows, self._cols)

    def _check_index(self, row, col):
        if not (0 <= row < self._rows and 0 <= col < self._cols):
            raise IndexError("row or column index out of range")

    def _index(self, row, col):
        # Column-major index calculation
        return col * self._rows + row

    def set(self, row, col, value):
        """Set value at (row, col)."""
        self._check_index(row, col)
        try:
            self._data[self._index(row, col)] = value
        except TypeError:
            raise TypeError(
                f"ColumnMajor2DArray: invalid value type; expected type compatible with '{self._typecode}'"
            )

    def get(self, row, col):
        """Get value at (row, col)."""
        self._check_index(row, col)
        return self._data[self._index(row, col)]

    def __getitem__(self, row):
        """Get full row as a list."""
        if not 0 <= row < self._rows:
            raise IndexError("row index out of range")
        return [self.get(row, c) for c in range(self._cols)]

    def __len__(self):
        return self._rows

    def __repr__(self):
        rows_str = "\n".join(
            str([self.get(r, c) for c in range(self._cols)])
            for r in range(self._rows)
        )
        return f"ColumnMajor2DArray({self._rows}x{self._cols}):\n{rows_str}"


class ImmutableArray:
    """
    ImmutableArray — a fixed-size, read-only array.

    Once created, values cannot be changed.
    Useful for lookup tables and thread-safe constant data.

    Parameters
    ----------
    iterable : iterable
        Initial data to store in the array.
    typecode : str, optional
        Typecode for the array elements (default 'i').

    Example
    -------
    >>> arr = ImmutableArray([1, 2, 3])
    >>> arr[1]
    2
    >>> len(arr)
    3
    >>> arr[1] = 5
    Traceback (most recent call last):
        ...
    TypeError: ImmutableArray does not support item assignment
    """

    __slots__ = ['_data', '_typecode']

    def __init__(self, iterable, typecode='i'):
        self._typecode = typecode
        try:
            self._data = array(typecode, iterable)
        except TypeError:
            raise TypeError(
                f"ImmutableArray: invalid value type; expected type compatible with '{typecode}'"
            )

    def __getitem__(self, index):
        return self._data[index]

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)

    def __repr__(self):
        return f"ImmutableArray({list(self._data)})"

    def __setitem__(self, index, value):
        raise TypeError("ImmutableArray does not support item assignment")

    def append(self, value):
        raise TypeError("ImmutableArray does not support append")

    def extend(self, iterable):
        raise TypeError("ImmutableArray does not support extend")

    def insert(self, index, value):
        raise TypeError("ImmutableArray does not support insert")

    def remove(self, value):
        raise TypeError("ImmutableArray does not support remove")

    def pop(self, index=-1):
        raise TypeError("ImmutableArray does not support pop")


def real_world_examples():
    """
    Arrays Module — Real World Usage Examples
    =========================================

    1. StaticArray
       Scenario:
           A spacecraft's onboard computer logs exactly 1,000 temperature readings
           from sensors during its trip to Mars.
       If Using Built-in List:
           - Stores extra metadata for each element → higher memory usage.
           - Possible accidental resizing → memory fragmentation.
       If Using StaticArray:
           - Fixed contiguous block of memory → minimal overhead.
           - No accidental resizing → predictable performance.
       Production Benefit:
           Ideal when data size is fixed & performance predictability is critical.

    2. DynamicArray
       Scenario:
           A social media feed storing posts in real-time as users post.
       If Using Built-in List:
           - Works fine but internal resizing may cause unpredictable spikes.
       If Using DynamicArray:
           - Resizes in controlled way → avoids performance hiccups.
       Production Benefit:
           Good for workloads with frequent appends but occasional reads.

    3. TwoDArray
       Scenario:
           A chess game board storing piece positions.
       If Using Built-in List of Lists:
           - Memory scattered → slower cache performance.
           - Row/column access may involve extra indirection.
       If Using TwoDArray:
           - Single contiguous memory block → faster access.
       Production Benefit:
           Best for grid-like structures with frequent row/column access.

    4. SparseMatrix
       Scenario:
           Representing a road network with thousands of cities but only a few
           direct roads between them.
       If Using Built-in 2D List:
           - Stores a huge number of zeros → massive wasted memory.
       If Using SparseMatrix:
           - Stores only non-zero connections → huge memory savings.
       Production Benefit:
           Ideal for very sparse datasets like maps, graphs, or NLP term matrices.

    5. CircularArray
       Scenario:
           A system log storing only the last 1,000 events on a web server.
       If Using Built-in List:
           - Must manually pop from front (O(n)) or slice arrays.
       If Using CircularArray:
           - Automatically overwrites oldest entries in O(1) time.
       Production Benefit:
           Perfect for fixed-size queues, rolling buffers, and streaming windows.

    6. BitArray
       Scenario:
           Feature flags for 10 million users (boolean values).
       If Using Built-in List of Booleans:
           - Each bool may take up to 28 bytes in CPython → huge waste.
       If Using BitArray:
           - Packs bits densely → ~1.25 MB instead of ~280 MB.
       Production Benefit:
           Extreme memory savings for large boolean datasets.

    7. ColumnMajor2DArray
       Scenario:
           Data analytics where each column is processed separately
           (e.g., a DataFrame-like structure for machine learning).
       If Using Row-Major (like list of lists):
           - Column operations require non-contiguous memory access → slower.
       If Using ColumnMajor2DArray:
           - Columns stored contiguously → faster column operations.
       Production Benefit:
           Ideal for ML preprocessing and scientific computing.

    8. ImmutableArray
       Scenario:
           A lookup table of ASCII values that should never change.
       If Using Built-in List or Array:
           - Can be accidentally modified, leading to hard-to-find bugs.
       If Using ImmutableArray:
           - Completely read-only → thread-safe & bug-proof.
       Production Benefit:
           Safest option for constants & read-heavy datasets.
    """
    print(real_world_examples.__doc__)


def list_classes():
    """
    List all available array classes in the arrays module.
    """
    print(", ".join(__all__[:-1]))  


__all__ = [
    "StaticArray", "DynamicArray", "TwoDArray", "SparseMatrix",
    "CircularArray", "BitArray", "ColumnMajor2DArray", "ImmutableArray",
    "real_world_examples", "list_classes"
]
