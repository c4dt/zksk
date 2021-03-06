"""
And-composition of two discrete-logarithm knowledge proofs:
PK{ (x0, x1, x2): (Y0 = x0 * G0 + x1 * G1) &
                  (Y1 = x1 * G1 + x2 * G2) }

WARNING: if you update this file, update the line numbers in the documentation.
"""

from petlib.ec import EcGroup

from zksk import Secret, DLRep
from zksk.composition import AndProofStmt

group = EcGroup()

# Create the base points on the curve.
g0 = group.generator()
g1 = group.hash_to_point(b"one")
g2 = group.hash_to_point(b"two")
g3 = group.hash_to_point(b"three")

# Preparing the secrets.
# In practice, they probably should be big integers (petlib.bn.Bn)
x0 = Secret()
x1 = Secret()
x2 = Secret()

# Set up the proof statement.

# First, compute the values, "left-hand side".
y1 = 4 * g0 + 5 * g1
y2 = 4 * g2 + 7 * g3

# Next, create the proof statement.
stmt = DLRep(y1, x0 * g0 + x1 * g1) \
     & DLRep(y2, x0 * g2 + x2 * g3)

# This is an equivalent way to create the proof statement above.
stmt_1 = DLRep(y1, x0 * g0 + x1 * g1)
stmt_2 = DLRep(y2, x0 * g2 + x2 * g3)

equivalent_stmt = AndProofStmt(stmt_1, stmt_2)

assert stmt.get_proof_id() == equivalent_stmt.get_proof_id()

# Simulate the prover and verifier interacting.

prover = stmt.get_prover({x0: 4, x1: 5, x2: 7})
verifier = stmt.get_verifier()

commitment = prover.commit()
challenge = verifier.send_challenge(commitment)
response = prover.compute_response(challenge)
assert verifier.verify(response)

# Composition takes into account re-occuring secrets.

x0 = Secret(4)
x1 = Secret(4)
stmt = DLRep(4 * g0, x0 * g0) & DLRep(4 * g1, x1 * g1)

# NOT the same as above. Note that x1_prime is used for both clauses.
x1_prime = Secret(4)
another_stmt = DLRep(4 * g0, x1_prime * g0) & DLRep(4 * g1, x1_prime * g1)

assert stmt.get_proof_id() != another_stmt.get_proof_id()
