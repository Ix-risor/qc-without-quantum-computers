import random
import matplotlib.pyplot as plt
import numpy as np

from qiskit.primitives import StatevectorSampler
from qiskit.visualization import plot_histogram
from qiskit.circuit.library import CXGate, HGate, SGate, TGate
from qiskit import QuantumCircuit, generate_preset_pass_manager
from qiskit.circuit import Gate

def gen_circuit(qubit_count: int, gate_count: int, gate_set: list[Gate]) -> QuantumCircuit:
    qc = QuantumCircuit(qubit_count)
    for _ in range(gate_count):
        chosen_gate = random.choice(gate_set)
        chosen_qubits = random.sample(range(qubit_count), chosen_gate.num_qubits)
        qc.append(chosen_gate, chosen_qubits)
    qc.measure_all()
    return qc


def gen_dataset(circuit_count: int, qubit_count: int, gate_count: int, gate_set: list[Gate]) -> list[dict]:
    sampler = StatevectorSampler()
    pm = generate_preset_pass_manager(optimization_level=1)
    qcs = []
    output = []
    for _ in range(circuit_count):
        qc = gen_circuit(qubit_count, gate_count, gate_set)
        new_qc = pm.run(qc)
        qcs.append(new_qc)
    results = sampler.run(qcs).result()
    for i in range(circuit_count):
        output.append(results[i].data.meas.get_counts())
    return output

data = gen_dataset(10, 5, 12, [HGate(), SGate(), TGate(), CXGate()])

plot_histogram(data)
plt.show()