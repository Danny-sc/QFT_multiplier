from qiskit import(QuantumCircuit, execute, Aer)
from numpy import pi
from qft import(qft, inverse_qft)


def qft_multiplier(a, b):
    """
    This function takes two non-negative integers and calculates their product
    using the Quantum Fourier Transform. It prints out the found product and 
    the correct answer too, for comparison.

    Parameters
    ----------
    a : int
        A non-negative integer to be multiplied by the second parameter, b.
    b : int
        A non-negative integer to be multiplied by the first parameter, a.

    Returns
    -------
    circuit :  QuantumCircuit object
        A quantum circuit containing the product of a and b in the first 2n 
        qubits, where n is the maximum length of a and b when written in base 2.
    result : Result
        A class that stores the counts result from the execution of the Quantum
        Fourier Transform multiplier on `qasm_simulator` with 1000 shots.

    """
    n_bit = max(a.bit_length(), b.bit_length())
    binary_format = '0'+str(n_bit)+'b'
    a_bin = format(a, binary_format) 
    b_bin = format(b, binary_format) 
    circuit = QuantumCircuit(4*n_bit, 2*n_bit) 
    # a is encoded in qubits indexed 2n to 3n-1, with the least significant bit 
    # encoded in the qubit of index 2n 
    # b is encoded in the last n qubits of the circuit, with the least 
    # significant bit encoded in the qubit of index 3n
    for i in range(n_bit):
        if a_bin[i]=='1': 
            circuit.x(3*n_bit-1-i) 
        if b_bin[i]=='1': 
            circuit.x(4*n_bit-1-i) 
    # Apply `qft` to the first 2n qubits, containing all zeroes 
    circuit =  qft(circuit, 2*n_bit) 
    for j in range(1, n_bit+1):
        # Apply all necessary rotation gates to add b_{j} 2^{n-j} a 
        if b_bin[j-1]=='1': 
            for s in range(1, 2*n_bit+1):
                if n_bit>(2*n_bit-j-s):
                    i_min = max(1, 2*n_bit-j-s+1)
                    for i in range(i_min, n_bit+1):
                        circuit.cp(pi/(2**(j+s-2*n_bit+i-1)), 3*n_bit-i, s-1) 
    # Apply the inverse QFT to the first 2n qubits
    circuit = inverse_qft(circuit, 2*n_bit) 
    # Measure the first 2n qubits
    circuit.measure(range(2*n_bit), range(2*n_bit)) 
    simulator = Aer.get_backend('qasm_simulator')
    job = execute(circuit, simulator, shots=1) 
    result = job.result()
    counts = result.get_counts(circuit)
    # Get the product of a and b (according to the circuit) as a decimal number
    product = int(list(counts.keys())[0], 2) 
    print('QFT multiplier output:', product, '\nCorrect answer:', a*b)
    return (circuit, result)
