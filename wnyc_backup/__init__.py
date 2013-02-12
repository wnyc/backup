from cloudfiles import get_connection
import cloudfiles.errors 
from datetime import * 
import os.path 
import gflags
FLAGS = gflags.FLAGS
gflags.DEFINE_string('key', None, 'Your cloud provider key')
gflags.DEFINE_string('account', None,' Your cloud provider account name')
gflags.DEFINE_string('container', None, 'The cloud provider container you should backup into')



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

class FilenameRewriter:
    def __init__(self):
        self.now = "%06x" % date.today().toordinal()

    def __call__(self, s):
        return os.path.join(self.now, os.path.basename(s))

    
def upload():
    import sys
    
    try:
        argv = FLAGS(sys.argv)[1:]
    except gflags.FlagsError, e:
        print e 
        print __doc__
        sys.exit(1)

    if not FLAGS.account:
        print >>sys.stderr, "Missing --account flag"
    if not FLAGS.key:
        print >>sys.stderr, "Missing --key flags"
    if not FLAGS.container:
        print >>sys.stderr, "Missing --container flags" 

    rewrite_name = FilenameRewriter()

    connection = get_connection(FLAGS.account, FLAGS.key)
    try:
        container = connection.get_container(FLAGS.container)
    except cloudfiles.errors.NoSuchContainer:
        container = connection.create_container(FLAGS.container)
        

    for source in argv:
        target = rewrite_name(source)
        print >>sys.stderr, "Uploading", source, "to", target
        try:
            container.create_object(target).load_from_filename(source)
        except IOError, e:
            print >>sys.stderr,  e
    
        
