"""Write conceptual direction articles using the existing evidence references."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Each direction: (title, [(heading that states the point, Markdown body), ...4 sections]).
# Written for a newcomer: short sentences, lists where there are parts, numbered steps where order matters.
SECTIONS = {
 'constraints-become-executable': (
 'Using design requirements to choose the next design',
 [('The problem: a requirement checked only at the end can fail an expensive design', """A design requirement is a condition the result must meet. A circuit must:

- compute the required function;
- fit within an area budget;
- deliver signals within a specified time.

A design process considers many candidates. If a requirement is checked only after a candidate is chosen, an expensive implementation can fail at the end."""),
  ('The change: run the checks while building, and let the result steer the next attempt', """1. A tool measures or tests a candidate.
2. It reports a failure or a cost.
3. The next design decision uses that report.

The check must return something useful: which property failed, where, or which resource went over its limit. A bare pass or fail may rule a candidate out without saying how to improve it."""),
  ('Different checks prove different things, so keep them apart', """Three kinds of tool can use this loop: a language model writing circuit code, a compiler ordering operations, and a placement tool choosing locations. Their checks differ:

- **Compiling** shows a tool accepts the code's syntax and structure.
- **Simulating** selected inputs checks those runs only.
- **Proving equivalence** is a stronger claim, within the proof's model.

An evaluation must keep these outcomes separate."""),
  ('The test: same unseen tasks, same total budget, count every outcome', """1. Compare methods on the same unseen design tasks, with the same total time and computing resources.
2. Count valid completed designs, failures, unresolved checks, and final area, timing and power.
3. If feedback helps on development examples but fails on new designs, the evidence supports only a narrower method.
4. To show a trend over time, compare like-for-like sets of papers across years. Then record which checks actually change design decisions.""")]),
 'data-movement-as-contract': (
 'Designing computation around the cost of moving data',
 [('The problem: a job can spend most of its time waiting for data', """Every operation needs its inputs where the hardware can reach them. If they are elsewhere, they must move.

Moving them uses bandwidth, takes time and costs energy. So a job can spend most of its time waiting for values, even when its arithmetic is simple."""),
  ('The change: choose the algorithm, the data placement and the schedule together', """- Keep intermediate values near the operations that use them next, to cut repeated transfers.
- Move a computation near the stored data, to cut the bytes sent over a connection.
- Recompute a cheap value, sometimes, instead of storing and fetching it.

Each change brings new costs, such as local traffic and extra computation. Count them."""),
  ('Memory, architecture and scheduling overlap, so fixing one can shift the delay', """- A **memory** method decides where values can live.
- An **architecture** decides where operations can run.
- A **scheduler** decides when workers compete for data.

A method that changes only one layer may just move the delay elsewhere. A full comparison includes the first loading of data and any later migration."""),
  ('The test: fixed output quality, varied data sizes, every transfer counted', """1. Measure completion time and energy at fixed output quality.
2. Vary input size, memory capacity and competing requests. Include data that fits, and data that does not fit, in fast memory.
3. For approximate search, compare at the same rate of correct answers. For services, include slow requests and data migration.

The hypothesis weakens if the advantage disappears once capacity is matched or all transfer costs are counted. Seeing it recur in today's cases cannot show growth over time.""")]),
 'closed-loop-design': (
 'Improving design choices using measured feedback',
 [('The problem: detailed checks are too slow to run on every candidate', """Choosing a design means estimating what it will do.

- A detailed simulation can take too long to run on every candidate.
- A simpler model is faster but less accurate.

So design is partly a measurement problem: how much evaluation effort to spend before choosing the next candidate?"""),
  ('The change: evaluate, update the estimate, choose again', """1. Evaluate a candidate.
2. Update the estimate.
3. Use the new estimate to choose the next candidate.

Some methods use many cheap predictions and fewer detailed checks. That saves search time when the cheap predictions find good candidates. It can also exclude the best candidates if the prediction error is systematic."""),
  ('What matters is the decision a prediction causes, not its average error', """A model with low average error can still rank the best candidates wrongly.

Errors near a hard limit matter most. A small error in predicted timing or temperature can turn an apparently valid design into a failing one.

So the search should record rejected candidates, and check whether its confidence matches later measurements."""),
  ('The test: equal total evaluation time, with every hidden cost charged', """1. Compare the final valid designs under equal total evaluation time.
2. Include model training, calibration, failed simulations and final checks.
3. Try unfamiliar designs or operating conditions, to see whether the model stays useful.

A gain that disappears once these costs are charged does not show a more efficient design process. A claim about change over time needs comparable descriptions of feedback and evaluation budgets across editions.""")]),
 'reliability-security-upstream': (
 'Choosing system designs with faults and attacks in view',
 [('The problem: a result is useful only if it stays valid under faults and attacks', """A corrupted memory value, a failed component or an attacker can change a result.

Protection uses resources. It may also limit how the system shares data or runs work."""),
  ('The change: weigh faults and attacks while choosing the architecture and software', """- Where data is stored decides which errors must be detected and corrected.
- Sharing a resource can raise utilization, but may let one user see timing changes caused by another.
- Recovery can need spare capacity or saved copies of state.

These choices affect normal operation, not only failure handling."""),
  ('Reliability and security rest on different assumptions', """- A **random fault** experiment asks how the system behaves under an injected error pattern.
- An **adversarial** experiment asks what a person with stated access and knowledge can cause or observe.

Success under one set of assumptions does not prove protection against another. A paper must state its assumptions before its protection result can be read."""),
  ('The test: useful correct work with protection on, under a fixed threat', """1. Compare correct useful work, energy, missed detections and recovery time, with protection switched on.
2. Keep the fault model or attacker capability fixed.
3. Vary realistic fault rates or attack conditions, and record cases not covered.

The direction gains support when several independent cases show early design choices improve this combined outcome. A fix for one attack is a narrower result. Today's evidence does not show adoption rates or growth.""")]),
 'physical-reality-in-the-loop': (
 'Using physical limits while selecting a design',
 [('The problem: a design chosen on paper can break physical limits once built', """A logical design lists operations and connections. Real circuits take up space, draw current and produce heat. Wires have electrical behavior. Manufacturing adds variation.

So a design picked with an abstract performance estimate can break timing, temperature or manufacturing rules once implemented."""),
  ('The change: use physical estimates while choosing, not only to describe the result', """- A **temperature** estimate can change where computation is placed.
- A **wire-delay** estimate can change which components sit near each other.
- A **variation** model can change the safety margin a circuit needs to work reliably.

The estimate shapes the construction rather than just describing the final output."""),
  ('More physical detail costs time, so check the final design accurately', """A detailed model can be too expensive to run for every choice. A cheaper model can miss interactions.

The key comparison: does the chosen design stay valid under a more accurate evaluation? Agreeing on easy examples is not enough if errors cluster near limits or on new structures."""),
  ('The test: same physical setup, violations recorded, an independent accurate check', """1. Use the same process data, circuit inputs, package assumptions and physical constraints.
2. Record final violations, completed designs, search time and any calibration cost.
3. Check both selected and rejected candidates with an independent, more accurate evaluator when one exists.

A simulation result keeps its simulation assumptions. Readiness for manufacturing needs evidence from fabricated parts, not only a favorable model.""")]),
 'evaluation-as-research': (
 'Designing measurements that make research results comparable',
 [('The problem: the same method can score differently under a different test', """A reported result answers one question under one experiment.

- A **speedup** is the ratio of two completion times.
- A **correctness rate** is the fraction of stated tasks that passed a stated check.

Change the input set, the comparison or the rule for success, and the number can change. The method itself may be the same."""),
  ('The change: treat the measurement procedure as a research contribution', """- Better tests can expose failures earlier tests missed.
- Reproducible software and input data let another researcher check a claim.
- Clearly defined timeouts stop unfinished runs from counting as success.
- Keeping development examples apart from evaluation examples tests whether a method works beyond the cases used to build it."""),
  ('Available, reproduced and independently reviewed are three different steps', """1. An **available artifact** shows some materials can be inspected or run.
2. **Reproducing** a result also needs the matching inputs, versions, settings, hardware and measurement procedure.
3. **Independent review** asks whether another reviewer accepts the interpretation.

This repository has evidence and review preparation, but no independent acceptance verdicts yet."""),
  ('The test: do rankings survive harder tasks, bigger inputs and other budgets?', """1. Compare the same methods under documented evaluation rules.
2. Check whether rankings survive changes in task difficulty, input size and resource budget.
3. Record failed and unresolved runs.

A stronger evaluation can lower a previously reported score by exposing a missing condition. That correction is useful scientific information. The hypothesis is about better comparability and error detection. It does not claim that the number of evaluation papers is rising.""")]),
}

def build(root=ROOT):
    atlas = json.loads((root / 'data/long-term-direction-atlas-v1.json').read_text())
    for direction in atlas['directions']:
        did = direction['direction_id']
        title, sections = SECTIONS[did]
        path = root / direction['page']
        evidence_page = f'evidence/{path.stem}-evidence.md'
        challenge = direction['challenge']
        lines = ['# ' + title, '',
                 'Status: a research hypothesis supported by selected cases. A measured increase across comparable years has not been established.', '']
        for heading, body in sections:
            lines += ['## ' + heading, '', body.strip(), '']
        lines += [
                 '## Counterpressure and falsification boundary', '',
                 f"Challenge paper: `{challenge['paper_id']}` ({challenge['relation']}; source tier `{challenge['evidence_tier']}`). [Open the recorded source]({challenge['source_url']}).", '',
                 challenge['qualification'], '',
                 f"**What would weaken the direction:** {challenge['failure_condition']}", '',
                 f"**Next evidence:** {challenge['next_evidence']}", '',
                 '## Paper evidence and open conditions', '',
                 f'[Read the paper evidence dossier]({evidence_page}). It connects this discussion to the recorded sources and unresolved conditions.', '',
                 f'[Read the cross-conference comparison](../comparisons/{did}.md). Different conferences can examine different parts of the problem; their reported numbers are not automatically comparable.', '',
                 '[Check the condition register](../direction-condition-register-v1.md) for unresolved experimental details and [the review gate](../direction-review-gate-v1.md) for the current review status.', '',
                 '## Establishing a long-term trend', '',
                 'A trend needs the same rules applied to comparable years:\n\n1. Select comparable editions.\n2. Apply the same inclusion and coding rules.\n3. Measure source coverage in each edition.\n4. Tell apart how many papers discuss a method from evidence that the method improves results.\n\nThe current sample combines DAC and ISCA 2026 with ICCAD 2025 fallback material, and coverage is uneven. That supports comparing cases with stated limits.', '',
                 '[Read the longitudinal protocol](../longitudinal-protocol-v1.md) · [Return to research directions](README.md)', '']
        path.write_text('\n'.join(lines))

if __name__ == '__main__':
    build()
