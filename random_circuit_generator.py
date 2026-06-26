import random

from qiskit.primitives import StatevectorSampler
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

def gen_circuit_set(circuit_count: int, qubit_count: int, gate_count: int, gate_set: list[Gate]) -> list[QuantumCircuit]:
    qcs = []
    for _ in range(circuit_count):
        qcs.append(gen_circuit(qubit_count, gate_count, gate_set))
    return qcs

def gen_results(circuit_count: int, qubit_count: int, gate_count: int, gate_set: list[Gate]) -> list[dict]:
    sampler = StatevectorSampler()
    pm = generate_preset_pass_manager(optimization_level=2)
    qcs = gen_circuit_set(circuit_count, qubit_count, gate_count, gate_set)
    isa_qcs = pm.run(qcs)
    
    output = []
    results = sampler.run(isa_qcs).result()
    for i in range(circuit_count):
        output.append(results[i].data.meas.get_counts())
    return output