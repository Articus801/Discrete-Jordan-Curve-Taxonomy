# deval.py - PVA with real phi_n reduction

EAGER_THRESHOLD = 50

def phi_n(p, k):
    # Euler's totient for prime power p^k = p^k - p^(k-1) = p^(k-1)*(p-1)
    # For k=1, phi(p) = p-1. This is the core of PVA reduction
    return (p ** (k-1)) * (p - 1)

class PVA:
    def __init__(self, prime, exp=1):
        self.tuple = [(prime, exp)]

    def _reduce_phi_n(self):
        # Real reduction: merge same primes and apply phi_n when exp > 1
        d = {}
        for item in self.tuple: # loop the item first
            p, e = item[0], item[1] # then unpack
            d[p] = d.get(p, 0) + e

        # Apply phi_n reduction for exponents > 1
        new_tuple = []
        for p, e in d.items():
            if e == 1:
                new_tuple.append((p, 1))
            else:
                # Reduce p^e using phi_n: store as phi(p^e)
                reduced_val = phi_n(p, e)
                new_tuple.append((p, e, reduced_val)) # tuple of 3 for tracking
        self.tuple = new_tuple

    def __mul__(self, other):
        new = PVA(2, 0)
        new.tuple = self.tuple + other.tuple

        if len(new.tuple) > EAGER_THRESHOLD:
            new._reduce_phi_n() # now with real math!

        return new

    def __len__(self):
        return len(self.tuple)

    def __repr__(self):
        return "PVA" + str(self. tuple) #


