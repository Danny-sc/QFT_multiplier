from qiskit import(QuantumCircuit)
from numpy import pi
from qft import(qft, inverse_qft)
from qft_multiplier import qft_multiplier
import random
import matplotlib.pyplot as plt


"""
 The code below 
 1. calculates the minimum and maximum depth and minimum and 
 maximum length of the `qft_multiplier` circuit as a function of the number 
 of bits needed to represent a and b.
 2. calculates the depth and length of the `qft_multiplier` circuit for random 
 pairs of integers.
 3. produces a plot that shows the minimum and maximum depth (length) of the 
 `qft_multiplier` circuit, together with the depth (length) of the 
 `qft_multiplier` circuit for random pairs of integers.  
"""

# Define the maximum number of bits a and b can have in their binary 
# representation                                                                   
n = 11

# lb is a list of the powers of 2 up to 2^(n-1)
lb = [2**i for i in range(n)]
# depths_lb and lengths_lb will contain the minimum depth and length of the 
# `qft_multiplier` circuit for a and b with 1,2,...,n bits 
depths_lb = [0 for i in range(n)]
lengths_lb = [0 for i in range(n)]
for i in range(len(lb)): 
    x =qft_multiplier(lb[i],lb[i])
    depths_lb[i] = x[0].depth()
    lengths_lb[i] = len(x[0])

# ub is a list of the powers of 2 minus 1, up to 2^n-1
ub = [2**(i+1)-1 for i in range(n)]
# depths_ub and lengths_ub will contain the maximum depth and length of the 
# `qft_multiplier` circuit for a and b with 1,2,...,n bits 
depths_ub = [0 for i in range(n)]
lengths_ub = [0 for i in range(n)]
for i in range(len(ub)): 
    x =qft_multiplier(ub[i],ub[i])
    depths_ub[i] = x[0].depth()
    lengths_ub[i] = len(x[0])

# depths_rand[i] will contain the depth of the `qft_multiplier` circuit for 
# 2*(i-1)+1 random pairs of integers between 2**(i+1) and 2**(i+2)-1.
depths_rand = []
# lengths_rand[i] will contain the length of the `qft_multiplier` circuit for 
# 2*(i-1)+1 random pairs of integers between 2**(i+1) and 2**(i+2)-1.
lengths_rand = []
for i in range(1,n-1):
    a = random.sample(range(2**(i+1), 2**(i+2)), 2*(i-1)+1)
    b = random.sample(range(2**(i+1), 2**(i+2)), 2*(i-1)+1)
    depths = [0 for t in range(2*(i-1)+1)]
    lengths = [0 for t in range(2*(i-1)+1)]
    for j in range(2*(i-1)+1):
        x = qft_multiplier(a[j],b[j])
        depths[j] = x[0].depth()
        lengths[j] = len(x[0])
    depths_rand.append(depths)
    lengths_rand.append(lengths)

# Make a plot with points for the length of the circuit for each random pair 
# and with lines for the minimum and maximum length.    
for i in range(1,n-1):
    plt.scatter([i+2 for t in range(2*(i-1)+1)], lengths_rand[i-1], s=25)
plt.plot(range(1,n+1), lengths_lb, label = "Estimated minimum number of operations")
plt.plot(range(1,n+1), lengths_ub, label = "Estimated maximum number of operations")
plt.xlabel("Number of bits in a (and b)")
plt.ylabel("Number of operations")
plt.title("Number of operations in the qft_multiplier circuit")
plt.legend()
#plt.savefig('Length_analysis.png', dpi=200)
plt.show()

# Make a plot with points for the depth of the circuit for each random pair 
# and with lines for the minimum and maximum depth. 
for i in range(1,n-1):
    plt.scatter([i+2 for t in range(2*(i-1)+1)], depths_rand[i-1], s=25)
plt.plot(range(1,n+1), depths_lb, label = "Estimated minimum depth of circuit")
plt.plot(range(1,n+1), depths_ub, label = "Estimated maximum depth of circuit")
plt.xlabel("Number of bits in a (and b)")
plt.ylabel("Depth of the circuit")
plt.title("Depth of the qft_multiplier circuit")
plt.legend()
#plt.savefig('Depth_analysis.png', dpi=200)
plt.show()