# DFT Fundamentals

> Learning **Design-for-Test** the only way it really sticks — by building each
> piece in runnable code. Gates to flip-flops to scan chains to ATPG, in Python
> and synthesizable Verilog.

![Focus](https://img.shields.io/badge/focus-Design%20for%20Test-1f6feb)
![Python](https://img.shields.io/badge/Python-3-3776ab?logo=python&logoColor=white)
![Verilog](https://img.shields.io/badge/HDL-Verilog-orange)
![Sim](https://img.shields.io/badge/sim-Icarus%20Verilog-555)
![Coverage](https://img.shields.io/badge/ATPG%20demo-100%25%20fault%20coverage-2ea043)
![Testbench](https://img.shields.io/badge/testbench-PASS-2ea043)

A hands-on study repo that works up the DFT stack — digital-logic foundations,
scan-chain insertion, the stuck-at fault model, and fault simulation — with every
concept implemented and runnable, not just summarised in notes.

---

## Why I Built This

I'm targeting a **DFT engineering** role, and I learn hardware best by making it
run. Reading about scan chains is one thing; writing a scan flip-flop, stitching
four of them into a chain, shifting a pattern through, and watching the captured
value come back out the other end is what makes it *click*. Same for the fault
model — it's abstract until you actually inject a stuck-at fault, propagate it to
an output, and compute the coverage yourself.

So this repo is my DFT coursework done in code: each topic earns its place by
working.

---

## What's Here

```
foundations/   Digital logic: gates, Boolean algebra, latches, flip-flops, FSMs
scan/          Scan-chain simulator (shift-in / capture / shift-out)
atpg/          Stuck-at fault simulator + coverage + minimal test-set finder
rtl/           Synthesizable Verilog: D-FF, scan-FF, 4-bit scan chain
testbench/     Verilog testbench for the scan chain (verified PASS)
```

---

## Scan Chain — the core idea

A scan chain turns hard-to-reach internal flip-flops into a shift register you can
load and read from two pins. Each flop gets a 2:1 mux on its input, picked by the
**scan-enable** (`SE`):

```
                SE=0  capture  (Q <= D, functional data)
                SE=1  shift    (Q <= SI, from previous flop)

  SI ─▶┌──────┐   ┌──────┐   ┌──────┐   ┌──────┐
       │ FF0  │──▶│ FF1  │──▶│ FF2  │──▶│ FF3  │──▶ SO
       └──▲───┘   └──▲───┘   └──▲───┘   └──▲───┘
         D0         D1         D2         D3      (functional inputs)
          ▲ shared CLK · SE · RST to all flops ▲
```

- **Shift** in a known test pattern (`SE=1`), **capture** the circuit's response
  in one functional clock (`SE=0`), then **shift** the captured state out to
  compare against the expected result.
- Implemented twice and cross-checked: a Python model (`scan/`) and structural
  Verilog (`rtl/`) that produce the same output.

---

## Modules

### `foundations/` — digital logic
| File | What it does |
|------|--------------|
| `step1_truth_tables.py` | Truth tables for NOT/AND/OR/NAND/NOR |
| `logicGates.py` | Interactive logic-gate calculator |
| `universal_gates.py` | NAND & NOR shown as universal gates |
| `boolean_simplify.py` | K-maps (2/3/4-var), canonical SOP, De Morgan checks |
| `latch_sim.py` | SR (NOR/NAND) and D latches via an iterative settle loop |
| `flip_flop.py` | D-FF and JK-FF with edge detection + waveform demos |
| `fsm.py` | Moore traffic-light FSM + an overlap-aware `101` sequence detector |

### `scan/` — scan-chain simulator
Models N scan flip-flops with `shift_in(pattern)`, `capture()` (one functional
clock), and `shift_out()`. Each `ScanFF` picks between functional `D` and serial
`SI` by the scan-enable.

```bash
python scan/scan_chain_simulator.py
```

### `atpg/` — fault simulator
Stuck-at-0 / stuck-at-1 fault model on a small AND→OR circuit. Detects each fault
by driving the node to the opposite value and propagating the difference to a
primary output, then computes **fault coverage** and a minimal detecting test set.

```bash
python atpg/fault_simulator.py
```

Current demo circuit: **10 faults (SA0+SA1 per node), 100% coverage** from the
derived test set.

### `rtl/` + `testbench/` — Verilog
| File | What it is |
|------|------------|
| `dff.v` | D flip-flop, async reset |
| `scan_dff.v` | scan flip-flop — `Q <= SE ? SI : D` |
| `scan_chain.v` | structural 4-FF scan chain (`SI → FF0…FF3 → SO`) |
| `tb_scan_chain.v` | shift-in → capture → shift-out; self-checking |

```bash
iverilog -o sim rtl/*.v testbench/tb_scan_chain.v && vvp sim
```
The testbench is **self-checking and passes** — the Verilog scan chain reproduces
the Python model's shift/capture/shift-out result.

---

## Topic Coverage

| # | Topic | Status |
|---|-------|--------|
| 1 | Digital logic: gates, Boolean algebra, K-maps | ✅ `foundations/` |
| 2 | Sequential logic: latches, flip-flops, FSMs | ✅ `foundations/` |
| 3 | Scan flip-flop & scan-chain operation | ✅ `scan/`, `rtl/` |
| 4 | Stuck-at fault model & fault coverage | ✅ `atpg/` |
| 5 | ATPG pattern generation (D-algorithm / PODEM) | ⬜ planned |
| 6 | Test compression (EDT) | ⬜ planned |
| 7 | Boundary scan / JTAG TAP controller | ⬜ planned |
| 8 | MBIST | ⬜ planned |

---

## What I Learned

- **Scan turns sequential test into combinational test.** Once every flop is on
  the chain, you control and observe internal state directly — the hard part of
  testing a real chip becomes "shift, clock once, shift out."
- **A fault is only "detected" if you can both sensitise it and propagate it** to
  an output. Writing the propagation logic is what makes fault coverage stop being
  a number on a slide.
- **Two models beat one.** Building the scan chain in both Python and Verilog and
  diffing their outputs caught my own bugs faster than either alone.

---

## Roadmap

- [ ] ATPG pattern generation (PODEM) instead of the current exhaustive search
- [ ] Run Yosys synthesis on the RTL → gate-level netlist
- [ ] Boundary-scan / JTAG TAP controller (see [`bsr-cell`](https://github.com/ChargeInMotion/bsr-cell))
- [ ] Scale the fault simulator to a parsed netlist (see [`dft-readiness-checker`](https://github.com/ChargeInMotion/dft-readiness-checker))

## Tools

Python 3 · Icarus Verilog (`iverilog` / `vvp`) · GTKWave · Yosys

## Author

**Sarosh (KJ)** · [github.com/ChargeInMotion](https://github.com/ChargeInMotion) · sarosh@chargeinmotion.dev
