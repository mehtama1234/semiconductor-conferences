# ISCA 2026 primary evidence batch 4

## PuDGhost: hidden interference in processing-using-DRAM

PuDGhost tests a basic assumption behind processing-using-DRAM (PuD): that a
column’s computation depends only on its selected operands. PuD uses simultaneous
multiple-row activation to make DRAM columns act as computation engines, but
density scaling brings cells and neighboring structures closer together. The
result is that non-participating data can influence a computation.

The study characterizes two interference paths. Data in adjacent, non-activated
rows can affect the output, and other columns computing concurrently under the
same activation can also interfere. The author preprint reports experiments on 96
real DDR4 chips from 12 modules, with up to 10% output impact from adjacent rows
and up to 48% from concurrently computing columns for random inputs. It evaluates
robust column screening and a compute-row layout that inserts dedicated rows
between compute rows. [Primary preprint](https://arxiv.org/abs/2606.19119)

The detailed capability is reliability characterization at the physical-to-
architecture boundary. Before PuD can be treated as a dependable accelerator,
the system must account for interference from data that the programmer did not
intend to participate. The proposed response spans device measurement, column
selection, and layout policy rather than relying on an abstract fault rate.

The current evidence does not establish cost, behavior across DRAM generations,
or end-to-end accuracy across broad workloads. The full paper is needed for chip
identities, environmental sweeps, screening overhead, layout capacity loss, and
the complete matrix-vector multiplication results.
