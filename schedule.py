# %%
import os
import signal

from sqlalchemy import false

command = 'streamlit run app.py'

from time import time, sleep
PID = '9352'

timer = sleep(60 -time() % 60)
if timer:    
    os.system(command)
else: os.kill(PID,signal.SIGINT) & os.system(command)
    
# %%    
os.kill(PID,signal.SIGINT)

# else:
#     os.kill(p.PID,signal.SIGINT)

# %%
