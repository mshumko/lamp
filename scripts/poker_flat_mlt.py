from datetime import datetime, timedelta
import pytz

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates
import matplotlib.ticker
import IRBEM

m = IRBEM.MagFields(kext='OPQ77')

timeZ_AK = pytz.timezone('US/Alaska')

ut_times = [datetime(2022, 2, 24).replace(tzinfo=pytz.UTC) + timedelta(hours=i) for i in range(24)]
ak_times = [t.astimezone(tz=timeZ_AK) for t in ut_times]

mlt = np.zeros(24)
for i, time in enumerate(ut_times):
    mlt[i] = m.make_lstar(
        X={'time':time, 'x1':100, 'x2':65, 'x3':-147}, 
        maginput=None
        )['MLT'][0]

fig, ax = plt.subplots()
ax.xaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(1))
ax.yaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(1))
# ax.plot(ak_times, mlt, label='AK'); 
ax.scatter([t.hour for t in ut_times], mlt, c='r', label='UTC'); 
ax.scatter([t.hour for t in ak_times], mlt, c='k', label='AKST'); 
ax.axvline(12, c='r')
ax.axvline(3, c='k')
ax.set_xlabel('Hour of the Day')
ax.set_xlim(0, 24)
ax.set_ylabel('MLT')
ax.set_ylim(0, 24)
ax.set_title('MLT at Poker Flat')
plt.legend(); 
plt.show()