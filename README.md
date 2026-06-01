# DFT Fundamentals

A hands-on, build-it-to-understand-it project working through core
**Design-for-Test (DFT)** concepts — from digital logic foundations up to
scan chains, fault models and ATPG. Each topic is implemented in runnable
Python and/or Verilog rather than just summarised in notes.

## What's here

```
foundations/   Digital-logic building blocks (gates → flip-flops → FSMs)
scan/          Scan-chain simulator (shift-in / capture / shift-out)
atpg/          Stuck-at fault simulator + fault-coverage / test-set finder
rtl/           Synthesizable Verilog: D-FF, scan-FF, 4-bit scan chain
testbench/     Verilog testbench for the scan chain (verified PASS)
```

### `foundations/`
| File | What it does |
|------|--------------|
| `step1_truth_tables.py` | Truth tables for NOT/AND/OR/NAND/NOR |
| `logicGates.py` | Interactive logic-gate calculator |
| `universal_gates.py` | NAND & NOR shown as universal gates |
| `boolean_simplify.py` | K-maps (2/3/4-var), canonical SOP, De Morgan checks |
| `latch_sim.py` | SR (NOR/NAND) and D latches via an iterative settle loop |
| `flip_flop.py` | D-FF and JK-FF with edge detection + waveform demos |
| `fsm.py` | Moore traffic-light FSM and an overlap-aware `101` detector |

### `scan/` — scan-chain simulator
Models a chain of N scan flip-flops with the three classic operations:
`shift_in(pattern)`, `capture()` (one functional clock), and `shift_out()`.
Each `ScanFF` selects between functional data `D` and serial-in `SI` based on
the scan-enable `SE`. Run `python scan/scan_chain_simulator.py` for a self-test.

### `atpg/` — fault simulator
Implements the **stuck-at-0 / stuck-at-1** fault model on a small AND→OR
circuit, detects each fault by propagating its effect to a primary output,
computes **fault coverage**, and derives a minimal detecting test set.
Run `python atpg/fault_simulator.py`.

### `rtl/` + `testbench/` — Verilog
- `dff.v` — D flip-flop, async reset
- `scan_dff.v` — scan flip-flop: `Q <= SE ? SI : D`
- `scan_chain.v` — structural 4-FF scan chain
- `tb_scan_chain.v` — shifts a pattern in, captures, shifts out; **PASS** verified

```bash
# Simulate (Icarus Verilog)
iverilog -o sim rtl/*.v testbench/tb_scan_chain.v && vvp sim
```
The Verilog scan-chain behaviour matches the Python `scan/` model.

## Topic coverage
| # | Topic | Status |
|---|-------|--------|
| 1 | Digital logic: gates, Boolean algebra, K-maps | ✅ `foundations/` |
| 2 | Sequential logic: latches, flip-flops, FSMs | ✅ `foundations/` |
| 3 | Scan flip-flop & scan-chain operation | ✅ `scan/`, `rtl/` |
| 4 | Stuck-at fault model & fault coverage | ✅ `atpg/` |
| 5 | ATPG pattern generation (D-algorithm/PODEM) | ⬜ planned |
| 6 | Test compression (EDT) | ⬜ planned |
| 7 | Boundary scan / JTAG TAP controller | ⬜ planned |
| 8 | MBIST | ⬜ planned |

## Tools
Python 3 · Icarus Verilog (`iverilog`/`vvp`) · GTKWave · Yosys
