from datetime import datetime, timedelta
from pytz import timezone
import pytz

utc = pytz.utc

monterrey = timezone('America/Monterrey')

fmt = '%Y-%m-%d %H:%M:%S %Z%z'

utc_dt = datetime.now(tz=utc)
loc_dt = utc_dt.astimezone(monterrey)
a = loc_dt.strftime(fmt)
print(a)
