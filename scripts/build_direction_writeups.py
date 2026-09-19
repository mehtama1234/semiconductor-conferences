"""Write conceptual direction articles using the existing evidence references."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SECTIONS = {
 'constraints-become-executable': (
 'Using design requirements to choose the next design',
 'A design requirement states a condition that the result must satisfy. A circuit must compute the required function, fit within an area budget, and deliver signals within a specified time. A design process considers many candidates. If a requirement is checked only after choosing a candidate, an expensive implementation can fail at the end.',
 'The proposed direction is to use checks while constructing or revising a design. A tool measures or tests a candidate, reports a failure or a cost, and the next design decision uses that information. The check must return something useful: which property failed, where the failure occurred, or which resource exceeded its limit. A simple pass or fail may eliminate a candidate without explaining how to improve it.',
 'A language model generating circuit code, a compiler arranging operations, and a placement tool choosing component locations can all use this procedure. Their checks differ. Compiling code establishes that a tool accepts its syntax and structure. Simulating selected inputs checks those executions. Proving equivalence establishes a stronger claim within the proof model. These outcomes must remain distinct in an evaluation.',
 'Compare methods on the same unseen design tasks with the same total time and computing resources. Count valid completed designs, failures, unresolved checks, and final area, timing, and power. If feedback improves development examples but fails on new designs, the evidence supports a narrower method. To establish a time trend, compare equivalent paper populations across years and code which checks actually influence design decisions.'),
 'data-movement-as-contract': (
 'Designing computation around the cost of moving data',
 'Every operation needs inputs in a place the executing hardware can access. If those inputs are elsewhere, they must move. The transfer uses bandwidth, takes time, and consumes energy. A job can therefore spend most of its time waiting for values even when its arithmetic is simple.',
 'The proposed direction is to choose the algorithm, placement of data, and execution schedule together. Keeping intermediate values near later operations can reduce repeated transfers. Moving a computation near stored data can reduce the bytes sent over a connection. Recomputing a cheap value can sometimes avoid storing and retrieving it. Each change needs an account of its new costs, including local traffic and extra computation.',
 'These choices explain why memory systems, accelerator designs, and distributed applications overlap. A memory method determines where values can reside; an architecture determines where operations can run; a scheduler determines when workers compete for data. A method that changes only one layer may shift the delay elsewhere. A full comparison must include the initial loading of data and any later migration.',
 'Measure completion time and energy at fixed output quality while varying input size, memory capacity, and competing requests. Include cases where data fits and does not fit in fast memory. For approximate search, compare at the same rate of correct answers. For services, include slow requests and data migration. The hypothesis weakens if an advantage disappears after matching capacity or including all transfer costs. Recurrence across the current cases alone cannot establish growth over time.'),
 'closed-loop-design': (
 'Improving design choices using measured feedback',
 'Choosing a design requires estimating what it will do. A detailed simulation can take too long to run for every candidate. A simpler model can be faster but less accurate. The design problem is therefore partly a measurement problem: how much evaluation effort should be spent before choosing the next candidate?',
 'A feedback process evaluates a candidate, updates its estimate, and uses the revised estimate to choose another candidate. Some methods use many inexpensive predictions and a smaller number of detailed checks. This can reduce search time when the inexpensive predictions identify useful candidates. It can also exclude the best candidates if the prediction error is systematic.',
 'The essential issue is the decision caused by the prediction. A model with a low average error can still rank the best candidates incorrectly. Errors near a hard limit are especially consequential: a small error in predicted timing or temperature can turn an apparently valid design into a failing one. The search should record rejected candidates and test whether its confidence matches later measurements.',
 'Compare the final valid designs under equal total evaluation time. Include model training, calibration, failed simulations, and final checks. Evaluate unfamiliar designs or operating conditions to see whether the model remains useful. An improvement that disappears after charging these costs does not establish a more efficient design process. A longitudinal claim requires comparable descriptions of feedback and evaluation budgets across editions.'),
 'reliability-security-upstream': (
 'Choosing system designs with faults and attacks in view',
 'A system is useful only when its results remain valid under the conditions it must face. A corrupted memory value, failed component, or attacker can change the result. Protection consumes resources and may constrain how the system shares data or executes work.',
 'The proposed direction is to consider those conditions while choosing the architecture and software. For example, where data is stored affects which errors must be detected and corrected. Sharing a resource can improve utilization while allowing one user to observe timing changes caused by another. Recovery can require spare capacity or retained copies of state. These choices affect normal operation as well as failure handling.',
 'Reliability and security need different assumptions. A random fault experiment asks how the system behaves under an injected error distribution. An adversarial experiment asks what a person with specified access and knowledge can cause or observe. Success under one set of assumptions cannot establish protection against another. The paper must state the assumptions before its protection result can be interpreted.',
 'Compare correct useful work, energy, detection failures, and recovery time with protection enabled. Keep the fault model or attacker capability fixed. Vary realistic fault rates or attack conditions and record uncovered cases. A direction gains support when multiple independent cases show that early design choices improve this combined outcome; an attack-specific improvement is a narrower result. The current evidence does not establish adoption rates or growth.'),
 'physical-reality-in-the-loop': (
 'Using physical limits while selecting a design',
 'A logical design specifies operations and connections, but actual circuits occupy space, consume current, and produce heat. Wires have electrical behavior. Manufacturing introduces variation. A design chosen using an abstract performance estimate can violate timing, temperature, or manufacturing rules after implementation.',
 'The proposed direction is to evaluate these physical effects while choosing circuit structure, placement, packaging, or operation. A temperature estimate can change where computation is placed. A wire-delay estimate can change which components should be near one another. A variation model can change the margin required for a circuit to operate reliably. The estimate influences construction rather than merely describing the final output.',
 'Using more physical information also costs time. A detailed model can be too expensive to run for every choice; a cheaper model can miss interactions. The important comparison is whether the resulting design remains valid under a more accurate evaluation. Agreement on easy examples is insufficient if errors concentrate near limits or on new structures.',
 'Use the same process data, circuit inputs, package assumptions, and physical constraints. Record final violations, completed designs, search time, and any calibration cost. Test selected and rejected candidates with an independent, more accurate evaluator when available. A simulation result should retain its simulation assumptions. Manufacturing readiness requires evidence about fabricated behavior and cannot be inferred solely from a favorable model.'),
 'evaluation-as-research': (
 'Designing measurements that make research results comparable',
 'A reported result answers a particular question under a particular experiment. A speedup is the ratio of two completion times. A correctness rate is the fraction of stated tasks that passed a stated check. Changing the input set, comparison method, or rule for success can change the number even if the proposed method stays the same.',
 'The proposed direction treats the measurement procedure as a research contribution. Better tests can expose failures that earlier tests missed. Reproducible software and input data can let another researcher check a claim. Clearly defined timeouts prevent unfinished runs from being counted as success. Separating development examples from evaluation examples helps test whether a method works beyond the cases used to build it.',
 'An available artifact establishes that some materials can be inspected or run. Reproducing a paper result additionally requires the corresponding inputs, versions, settings, hardware, and measurement procedure. Independent review asks whether another reviewer accepts the interpretation. These are distinct achievements. The current repository has evidence and review preparation, but no independent acceptance verdicts.',
 'Compare the same methods under documented evaluation rules and examine whether rankings survive changes in task difficulty, input size, and resource budget. Record failed and unresolved runs. A stronger evaluation can reduce a previously reported score by exposing a missing condition. That correction is useful scientific information. The research hypothesis concerns improved comparability and error detection; it does not imply that the count of evaluation papers is increasing.'),
}

def build(root=ROOT):
    atlas = json.loads((root / 'data/long-term-direction-atlas-v1.json').read_text())
    for direction in atlas['directions']:
        did = direction['direction_id']
        title, basic, change, detail, test = SECTIONS[did]
        path = root / direction['page']
        evidence_page = f'evidence/{path.stem}-evidence.md'
        challenge = direction['challenge']
        lines = ['# ' + title, '',
                 'Status: a research hypothesis supported by selected cases. A measured increase across comparable years has not been established.', '',
                 '## The basic technical problem', '', basic, '',
                 '## What would change in the design process', '', change, '',
                 '## Why the details matter', '', detail, '',
                 '## What would support or weaken the claim', '', test, '',
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
                 'To test change over time, select comparable editions, apply the same inclusion and coding rules, and measure source coverage in each edition. Distinguish the number of papers discussing a method from evidence that the method improves results. The current sample combines DAC and ISCA 2026 with ICCAD 2025 fallback material, and coverage is uneven. That supports comparison of cases with stated limits.', '',
                 '[Read the longitudinal protocol](../longitudinal-protocol-v1.md) · [Return to research directions](README.md)', '']
        path.write_text('\n'.join(lines))

if __name__ == '__main__':
    build()
