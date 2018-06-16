import time

from math import sin, cos, sqrt 

G = 9.81
h2 = 0.827-0.11
theta = 0.314159

def get_t1(theta, h1):
    return sqrt(70*G*h1) / (5*G*sin(theta))

def get_t2(theta, h1, h2):
    v1 = sqrt(10*G*h1/7)
    return (-v1*sin(theta) + sqrt(v1*v1*sin(theta)*sin(theta) + 2*G*h2))/G

def get_d(theta, h1, h2):
    v1 = sqrt(10*G*h1/7)
    t2 = (-v1*sin(theta) + sqrt(v1*v1*sin(theta)*sin(theta) + 2*G*h2))/G
    return v1*cos(theta)*t2

preset = input("DROP LOCATION: ")

preset = int(preset)

if preset == 1:
	h1 = 0.241
else:
	if preset == 2:
		h1 = 0.145
	else:
		if preset == 3:
			h1 = 0.057 

theta = float(theta)
h2 = float(h2)
h1 = float(h1)
G = float(G)

t1 = get_t1(theta, h1)
t2 = get_t2(theta, h1, h2)
d = get_d(theta, h1, h2)

print "t1: "+ str(t1) + "sec"
print "t2: "+ str(t2) + "sec"
print "d: "+ str(d) + "m"


time.sleep(t1)
print "Turn LED 1 on!"

time.sleep(t2)
print "Turn LED 2 on!"

