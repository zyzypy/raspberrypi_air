import time
def delay(i):
    k=0
    for j in range(i):
        k+=1
n=5000
j=0

a=time.time()
i=1
c=time.time()
d=c-a
print(d)

a=time.time()
for i in range(n):
    j+=1
c=time.time()
d=c-a
print(d)

a=time.time()
delay(n)
c=time.time()
d=c-a
print(d)