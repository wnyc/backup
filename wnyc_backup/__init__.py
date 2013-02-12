from datetime import * 

def count_right_zero_bits(v):
    """Count the number of zero bits to the right of an integer.

    Pretty much copied from 
    http://graphics.stanford.edu/~seander/bithacks.html#ZerosOnRightLinear
    
    Args:
      v: The integer whose bits will be inspected

    Returns:
      integer indicating the number of bits set to the right

    Example:
      count_right_zero_bits(24) => 3
      count_right_zero_bits(32) => 5
    """

    if v<=0:
        raise ValueError("count_right_zero_bits only works on positive numbers")

    v = int(v)
    c = 0;
    v = (v ^ (v-1)) >> 1
    while v:
        v = v >> 1;
        c += 1
    return c

def kill_date(i):
    """Compute the backup kill date for a given date.
    
    Args:
      d: Either a datetime object or the value form datetime.toordinal
    
    Returns:
      date object indicating when a backup recorded at d should be
      deleted.
    """
    if isinstance(i, (datetime, date)):
        i = i.toordinal()
    return date.fromordinal(i + 2**count_right_zero_bits(i))

def kill_now(i, now=None, now_func=lambda :None):
    now = now or now_func() or datetime.now()
    if isinstance(now, datetime):
        now = now.date()
    return kill_date(i) < now
        

    
