
import datetime as dt
import time
import RPi.GPIO as GPIO
import requests
from bs4 import BeautifulSoup
import cvxopt
from functools import partial
import numpy as np
from functools import partial
from scipy.optimize import minimize

url = "https://transparency.entsoe.eu/transmission-domain/r2/dayAheadPrices/show?name=&defaultValue=false&viewType=TABLE&areaType=BZN&atch=false&dateTime.dateTime=22.06.2020+00:00|CET|DAY&biddingZone.values=CTY|10Y1001A1001A83F!BZN|10Y1001A1001A82H&dateTime.timezone=CET_CEST&dateTime.timezone_input=CET+(UTC+1)+/+CEST+(UTC+2)
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
table=soup.find('table')
tablerows=table.find_all('tr')
price=[]
pricee=[]
for tr in tablerows:
    td=tr.find_all('td')
    row=[i.text for i in td]
    price.append(row)
for i in price:
    print(i)
    x =len(i)
    if len(i)==2:
     y=i[1]
     x=float(y)
     pricee.append(x)
print(pricee)

DAP = [
    29,
    22.0700000000000,
    20.7500000000000,
    17.6100000000000,
    18.2900000000000,
    21.3900000000000,
    23.4700000000000,
    26.7500000000000,
    34.0900000000000,
    35.8000000000000,
    35.3900000000000,
    45.5600000000000,
    43.5200000000000,
    58.0300000000000,
    70.5700000000000,
    88.5700000000000,
    99.0200000000000,
    91.2300000000000,
    71.4600000000000,
    43.5300000000000,
    49.4500000000000,
    35.3200000000000,
    34.5700000000000,
    31.3800000000000,
]

DAP = np.array(DAP) * 0.001

E_a = [1.2282, 0.3, 0.1577, 0.846]  # energy consumption per device
a_a = [7, 10, 17, 9]  # starting time of each appliance
b_a = [23, 11, 19, 13]  # ending time of each appliance
x_a = [0, 0, 0, 0]  # min allowed power
y_a = [0.14, 0.3, 0.1, 0.3]  # max allowed power per appliance
D_a = [1, 2, 2, 1]  # duration of each device

ROW = len(E_a) 
COL = len(DAP)  

def objective(x):
    s_a = x.reshape(ROW, COL)
    col_sum = np.sum(s_a, axis=0)
    return np.sum(DAP * col_sum)

def E_constraint(x, i):
    s_a = x.reshape(ROW, COL)
    return sum(s_a[i, a_a[i] : (b_a[i] + 1)]) - E_a[i]

def sum_constraint(x, i):
    s_a = x.reshape(ROW, COL)
    col_sum = sum(s_a[:, i])
    return 1.0 - col_sum

s_a = np.zeros(ROW * COL) 
bnds = []
ind = 0 
for i in range(ROW):
    for j in range(COL):
        if a_a[i] <= j and j <= b_a[i]:
            bnds.append((x_a[i], y_a[i]))
        else:
            bnds.append((0.0, 0.0))
        s_a[ind] = sum(bnds[ind]) / len(bnds[ind])
        ind += 1

cons = []
for ind in range(ROW):
    cons.append({"type": "eq", "fun": partial(E_constraint, i=ind)})

for ind in range(COL):
    cons.append({"type": "ineq", "fun": partial(sum_constraint, i=ind)})

solution = minimize(objective, s_a, method="SLSQP", bounds=bnds, constraints=cons)
print(solution)

s_a = solution.x.reshape(ROW, COL)

np.set_printoptions(suppress=True)


print("optimal function value", solution.fun, "\n\n")
print("schedule matrix\n\n", s_a)


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
pins = [18,17,15,14]
x=0
ind=0
t=0
time=dt.datetime.now().hour
print(time)
d1=[]
d2=[]
d3=[]
d4=[]
relay=[]
state=[0,0,0,0]
ROW = 4  
COL = 24  
for i in range(ROW):
     for j in range(COL):
         if(s_a[i][j]>0):
          #print(s_a[i][j])
          #print(i,j)
          if(i==0):
              d1.append(j)
          if(i==1):
              d2.append(j)
          if(i==2):
              d3.append(j)
          if(i==3):
              d4.append(j)
while 1:
  GPIO.setmode(GPIO.BCM)
  if(x<25):
   for a in d1:
    if(a==x):
        r1=1
        relay.append(r1)
   for a in d2:
    if(a==x):
        r2=2
        relay.append(r2)
   for a in d3:
    if(a==x):
        r3=3
        relay.append(r3)
   for a in d4:
    if(a==x):
        r4=4
        relay.append(r4)
   print(relay)
   for y in relay:
    print(y)
    if(y>0):
      state[y-1]=1
   print(state)
   for q in state:
         GPIO.setmode(GPIO.BCM)
         GPIO.setup(pins, GPIO.OUT)
         print(q)
         t=t+1
         print(state.index(q))
         if(q==1) & (t==1):
              print("device1")
              GPIO.output(15,GPIO.LOW)
         if(q==0) & (t==1):
              print("device1no")
              GPIO.output(15,GPIO.HIGH)
         if(q==1) & (t==2):
              print("device2")
              GPIO.output(18,GPIO.LOW)
         if(q==0) & (t==2):
              print("device2no")
              GPIO.output(18,GPIO.HIGH)     	
         if(q==1) & (t==3):
              print("device3")
              GPIO.output(17,GPIO.LOW)
         if(q==0) & (t==3):
              print("device3no")
              GPIO.output(17,GPIO.HIGH)
         if(q==1) & (t==4):
              print("device4")
              GPIO.output(14,GPIO.LOW)
         if(q==0) & (t==4):
              print("device4no")
              GPIO.output(14,GPIO.HIGH)
         print(t)
         #time.sleep(1)
   print(x)
   t=0
   x=x+1
   time.sleep(5)