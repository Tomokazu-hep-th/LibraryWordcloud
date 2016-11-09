import pandas as pd
import subprocess
import sys
import codecs
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import numpy as np
from joblib import Parallel, delayed
from time import time

df=pd.DataFrame(pd.read_csv('data/takeout201410-201609UTF-8.csv',encoding='utf-8'))
#dfdup=df['所属名称'].duplicated()
dfdup=df[~df['所属名称'].duplicated(keep='last')]
dfdup=dfdup.reset_index(drop=True)

start=time()
def main(i):
    x=dfdup.ix[i,'所属名称']
    subprocess.call(['python','keywords3.py','--sday','20141001','--eday','20141031','--mjr',x,'--lan','ja'])
    subprocess.call(['python','keywords3.py','--sday','20141101','--eday','20141131','--mjr',x,'--lan','ja'])
    subprocess.call(['python','keywords3.py','--sday','20141201','--eday','20141231','--mjr',x,'--lan','ja'])
    subprocess.call(['python','keywords3.py','--sday','20150101','--eday','20150131','--mjr',x,'--lan','ja'])
    subprocess.call(['python','keywords3.py','--sday','20150201','--eday','20150231','--mjr',x,'--lan','ja'])
    subprocess.call(['python','keywords3.py','--sday','20150301','--eday','20150331','--mjr',x,'--lan','ja'])
    subprocess.call(['python','keywords3.py','--sday','20150401','--eday','20150431','--mjr',x,'--lan','ja'])
    subprocess.call(['python','keywords3.py','--sday','20150501','--eday','20150531','--mjr',x,'--lan','ja'])
    subprocess.call(['python','keywords3.py','--sday','20150601','--eday','20150631','--mjr',x,'--lan','ja'])
    subprocess.call(['python','keywords3.py','--sday','20150701','--eday','20150731','--mjr',x,'--lan','ja'])
    subprocess.call(['python','keywords3.py','--sday','20150801','--eday','20150831','--mjr',x,'--lan','ja'])
    subprocess.call(['python','keywords3.py','--sday','20150901','--eday','20150931','--mjr',x,'--lan','ja'])
    
l=len(dfdup['所属名称'])
Parallel(n_jobs=16)([delayed(main)(i) for i in range(l)])
print('{}秒かかりました'.format(time() - start))


#for x in dfdup['所属名称']:
#    subprocess.call(['python','keywords3.py','--sday','20141001','--eday','20141031','--mjr',x,'--lan','en'])


#subprocess.call(['python','keywords3.py','--sday','20141001','--eday','20141031','--mjr',mjrarg])

#mjrarg='理学部'
#subprocess.call(['python','keywords3.py','--sday','20141001','--eday','20141031','--mjr',mjrarg])
#subprocess.call(['python','keywords3.py','--sday','20141101','--eday','20141131','--mjr',mjrarg])
#subprocess.call(['python','keywords3.py','--sday','20141201','--eday','20141231','--mjr',mjrarg])
#subprocess.call(['python','keywords3.py','--sday','20150101','--eday','20150131','--mjr',mjrarg])
#subprocess.call(['python','keywords3.py','--sday','20150201','--eday','20150231','--mjr',mjrarg])
#subprocess.call(['python','keywords3.py','--sday','20150301','--eday','20150331','--mjr',mjrarg])
#subprocess.call(['python','keywords3.py','--sday','20150401','--eday','20150431','--mjr',mjrarg])
#subprocess.call(['python','keywords3.py','--sday','20150501','--eday','20150531','--mjr',mjrarg])
#subprocess.call(['python','keywords3.py','--sday','20150601','--eday','20150631','--mjr',mjrarg])
#subprocess.call(['python','keywords3.py','--sday','20150701','--eday','20150731','--mjr',mjrarg])
#subprocess.call(['python','keywords3.py','--sday','20150801','--eday','20150831','--mjr',mjrarg])
#subprocess.call(['python','keywords3.py','--sday','20150901','--eday','20150931','--mjr',mjrarg])
#subprocess.call(['python','keywords3.py','--sday','20151001','--eday','20151031','--mjr',mjrarg])
#subprocess.call(['python','keywords3.py','--sday','20151101','--eday','20151131','--mjr',mjrarg])
#subprocess.call(['python','keywords3.py','--sday','20151201','--eday','20151231','--mjr',mjrarg])
#subprocess.call(['python','keywords3.py','--sday','20160101','--eday','20160131','--mjr',mjrarg])
#subprocess.call(['python','keywords3.py','--sday','20160201','--eday','20160231','--mjr',mjrarg])
#subprocess.call(['python','keywords3.py','--sday','20160301','--eday','20160331','--mjr',mjrarg])
#subprocess.call(['python','keywords3.py','--sday','20160401','--eday','20160431','--mjr',mjrarg])
#subprocess.call(['python','keywords3.py','--sday','20160501','--eday','20160531','--mjr',mjrarg])
#subprocess.call(['python','keywords3.py','--sday','20160601','--eday','20160631','--mjr',mjrarg])
#subprocess.call(['python','keywords3.py','--sday','20160701','--eday','20160731','--mjr',mjrarg])
#subprocess.call(['python','keywords3.py','--sday','20160801','--eday','20160831','--mjr',mjrarg])
#subprocess.call(['python','keywords3.py','--sday','20160901','--eday','20160931','--mjr',mjrarg])

#mjrarg='農学部'
#subprocess.call(['python','keywords3.py','--sday','20141001','--eday','20141031','--mjr',mjrarg])
#subprocess.call(['python','keywords3.py','--sday','20141101','--eday','20141131','--mjr',mjrarg])
#subprocess.call(['python','keywords3.py','--sday','20141201','--eday','20141231','--mjr',mjrarg])
#subprocess.call(['python','keywords3.py','--sday','20150101','--eday','20150131','--mjr',mjrarg])
#subprocess.call(['python','keywords3.py','--sday','20150201','--eday','20150231','--mjr',mjrarg])
#subprocess.call(['python','keywords3.py','--sday','20150301','--eday','20150331','--mjr',mjrarg])
#subprocess.call(['python','keywords3.py','--sday','20150401','--eday','20150431','--mjr',mjrarg])
#subprocess.call(['python','keywords3.py','--sday','20150501','--eday','20150531','--mjr',mjrarg])
#subprocess.call(['python','keywords3.py','--sday','20150601','--eday','20150631','--mjr',mjrarg])
#subprocess.call(['python','keywords3.py','--sday','20150701','--eday','20150731','--mjr',mjrarg])
#subprocess.call(['python','keywords3.py','--sday','20150801','--eday','20150831','--mjr',mjrarg])
#subprocess.call(['python','keywords3.py','--sday','20150901','--eday','20150931','--mjr',mjrarg])
#subprocess.call(['python','keywords3.py','--sday','20151001','--eday','20151031','--mjr',mjrarg])
#subprocess.call(['python','keywords3.py','--sday','20151101','--eday','20151131','--mjr',mjrarg])
#subprocess.call(['python','keywords3.py','--sday','20151201','--eday','20151231','--mjr',mjrarg])
#subprocess.call(['python','keywords3.py','--sday','20160101','--eday','20160131','--mjr',mjrarg])
#subprocess.call(['python','keywords3.py','--sday','20160201','--eday','20160231','--mjr',mjrarg])
#subprocess.call(['python','keywords3.py','--sday','20160301','--eday','20160331','--mjr',mjrarg])
#subprocess.call(['python','keywords3.py','--sday','20160401','--eday','20160431','--mjr',mjrarg])
#subprocess.call(['python','keywords3.py','--sday','20160501','--eday','20160531','--mjr',mjrarg])
#subprocess.call(['python','keywords3.py','--sday','20160601','--eday','20160631','--mjr',mjrarg])
#subprocess.call(['python','keywords3.py','--sday','20160701','--eday','20160731','--mjr',mjrarg])
#subprocess.call(['python','keywords3.py','--sday','20160801','--eday','20160831','--mjr',mjrarg])
#subprocess.call(['python','keywords3.py','--sday','20160901','--eday','20160931','--mjr',mjrarg])
