"""Scan-chain simulator.

Models a chain of N scan flip-flops with the three classic scan ops:
    shift_in(pattern)  -- serially load a test pattern via SI
    capture()          -- one functional clock; each FF captures its D
    shift_out()        -- serially read the captured state out of SO

Each scan FF has:
    D   functional data input
    SI  scan data input (serial)
    SE  scan enable  (1 = shift mode, 0 = capture mode)
    Q   output (also drives SO of the next FF in the chain)

Run as a script for a self-test:
    python scan_chain_simulator.py
"""

from dataclasses import dataclass, field
from typing import Callable, List, Optional


@dataclass
class ScanFF:
    q: int = 0

    def tick(self, d: int, si: int, se: int) -> int:
        self.q = (si if se else d) & 1
        return self.q


@dataclass
class ScanChain:
    length: int
    d_inputs: Callable[[int], int] = field(default=lambda i: 0)
    cells: List[ScanFF] = field(init=False)

    def __post_init__(self) -> None:
        self.cells = [ScanFF() for _ in range(self.length)]

    def state(self) -> List[int]:
        return [c.q for c in self.cells]

    def _shift_once(self, si_bit: int, se: int) -> int:
        prev_q = [c.q for c in self.cells]
        d_vals = [self.d_inputs(i) for i in range(self.length)]
        self.cells[0].tick(d_vals[0], si_bit, se)
        for i in range(1, self.length):
            self.cells[i].tick(d_vals[i], prev_q[i - 1], se)
        return prev_q[-1]

    def shift_in(self, pattern: str, verbose: bool = False) -> None:
        if len(pattern) != self.length:
            raise ValueError(
                f"pattern length {len(pattern)} != chain length {self.length}"
            )
        if verbose:
            print(f"  shift_in {pattern!r}:")
        for bit in pattern:
            self._shift_once(int(bit), se=1)
            if verbose:
                print(f"    state = {self._fmt(self.state())}")

    def capture(self, verbose: bool = False) -> None:
        for i, cell in enumerate(self.cells):
            cell.tick(self.d_inputs(i), si=0, se=0)
        if verbose:
            print(f"  capture -> state = {self._fmt(self.state())}")

    def shift_out(self, verbose: bool = False) -> str:
        bits = []
        for _ in range(self.length):
            so = self._shift_once(si_bit=0, se=1)
            bits.append(str(so))
            if verbose:
                print(f"    state = {self._fmt(self.state())}  SO={so}")
        return "".join(reversed(bits))

    @staticmethod
    def _fmt(state: List[int]) -> str:
        return "[" + " ".join(str(b) for b in state) + "]"


def demo() -> None:
    print("Scan chain demo (length=4)")
    print("-" * 40)

    chain = ScanChain(length=4, d_inputs=lambda i: [1, 0, 1, 1][i])

    pattern = "1010"
    chain.shift_in(pattern, verbose=True)
    assert chain.state() == [0, 1, 0, 1], chain.state()

    chain.capture(verbose=True)
    assert chain.state() == [1, 0, 1, 1], chain.state()

    captured = chain.shift_out(verbose=True)
    print(f"\n  captured pattern (shifted out) = {captured}")
    assert captured == "1011", captured

    print("\nOK — shift_in / capture / shift_out behave correctly.")


if __name__ == "__main__":
    demo()
