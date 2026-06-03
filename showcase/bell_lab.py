"""Reusable CHSH experiments for classifying functional information flow.

Each model is intentionally represented as ordinary Python functions.  The
diagnostics are not a proof of quantum behavior; they are a measurement tool
for the internal anatomy of a black-box response function.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
import random
from typing import Callable, Dict, Iterable, Mapping, Sequence, Tuple

Outcome = int
Setting = int
Settings = Tuple[Setting, Setting]
ExpectationTable = Dict[Settings, float]

SETTINGS: Tuple[Settings, ...] = ((0, 0), (0, 1), (1, 0), (1, 1))


@dataclass(frozen=True)
class TrialContext:
    """Information available to a measurement function during one trial."""

    trial: int
    hidden: float
    alice_setting: Setting
    bob_setting: Setting
    rng: random.Random


ResponseFunction = Callable[[Setting, TrialContext], Outcome]
JointModel = Callable[[Settings, TrialContext], Tuple[Outcome, Outcome]]


@dataclass(frozen=True)
class ModelSpec:
    name: str
    family: str
    description: str
    alice: ResponseFunction | None = None
    bob: ResponseFunction | None = None
    joint: JointModel | None = None


@dataclass(frozen=True)
class CHSHResult:
    name: str
    family: str
    description: str
    s_value: float
    expectations: ExpectationTable
    classification: str
    anatomy: Mapping[str, float | str]


def sign(value: bool) -> Outcome:
    return 1 if value else -1


def quantum_expectation(a_angle: float, b_angle: float) -> float:
    """Spin-singlet expectation for two analyzer angles."""

    return -math.cos(a_angle - b_angle)


def quantum_like_joint(settings: Settings, ctx: TrialContext) -> Tuple[Outcome, Outcome]:
    """Sample a no-signalling quantum-like pair from the CHSH optimum angles."""

    alice_angles = (0.0, math.pi / 2.0)
    bob_angles = (math.pi / 4.0, -math.pi / 4.0)
    expected_product = quantum_expectation(
        alice_angles[settings[0]], bob_angles[settings[1]]
    )
    same_probability = (1.0 + expected_product) / 2.0
    product = 1 if ctx.rng.random() < same_probability else -1
    alice_outcome = 1 if ctx.rng.random() < 0.5 else -1
    return alice_outcome, alice_outcome * product


def pr_box_joint(settings: Settings, ctx: TrialContext) -> Tuple[Outcome, Outcome]:
    """Super-quantum no-signalling box with algebraic CHSH value 4."""

    alice_bit = 1 if ctx.rng.random() < 0.5 else 0
    bob_bit = alice_bit ^ (settings[0] & settings[1])
    return bit_to_outcome(alice_bit), bit_to_outcome(bob_bit)


def bit_to_outcome(bit: int) -> Outcome:
    return 1 if bit == 0 else -1


def deterministic_table(table: Sequence[Outcome]) -> ResponseFunction:
    return lambda setting, ctx: table[setting]


def threshold_response(low: float, high: float) -> ResponseFunction:
    def response(setting: Setting, ctx: TrialContext) -> Outcome:
        threshold = low if setting == 0 else high
        return sign(ctx.hidden >= threshold)

    return response


def remote_leak_bob(setting: Setting, ctx: TrialContext) -> Outcome:
    """Bob can read Alice's setting: a one-bit locality violation."""

    if setting == 0:
        return 1
    return -1 if ctx.alice_setting == 1 else 1


def independent_noise(setting: Setting, ctx: TrialContext) -> Outcome:
    return 1 if ctx.rng.random() < 0.5 else -1


MODELS: Tuple[ModelSpec, ...] = (
    ModelSpec(
        name="constant_local",
        family="local_deterministic",
        description="Both observers return fixed local values.",
        alice=deterministic_table((1, 1)),
        bob=deterministic_table((1, 1)),
    ),
    ModelSpec(
        name="shared_thresholds",
        family="local_hidden_variable",
        description="Both observers see the same lambda but only their own setting.",
        alice=threshold_response(0.25, 0.70),
        bob=threshold_response(0.40, 0.60),
    ),
    ModelSpec(
        name="independent_noise",
        family="uncorrelated",
        description="Responses are local and random with no stable correlation.",
        alice=independent_noise,
        bob=independent_noise,
    ),
    ModelSpec(
        name="one_bit_remote_leak",
        family="non_local_leak",
        description="Bob's second setting reads Alice's setting.",
        alice=deterministic_table((1, 1)),
        bob=remote_leak_bob,
    ),
    ModelSpec(
        name="quantum_singlet_sampler",
        family="quantum_like_no_signalling",
        description="Joint sampler with singlet correlations at CHSH-optimal angles.",
        joint=quantum_like_joint,
    ),
    ModelSpec(
        name="pr_box",
        family="super_quantum_no_signalling",
        description="Popescu-Rohrlich box: perfect algebraic CHSH violation.",
        joint=pr_box_joint,
    ),
)


def run_model(
    model: ModelSpec,
    trials: int = 20_000,
    seed: int = 7,
) -> CHSHResult:
    rng = random.Random(seed)
    products: Dict[Settings, list[int]] = {setting: [] for setting in SETTINGS}
    alice_marginals: Dict[Settings, list[int]] = {setting: [] for setting in SETTINGS}
    bob_marginals: Dict[Settings, list[int]] = {setting: [] for setting in SETTINGS}

    for trial in range(trials):
        hidden = rng.random()
        for settings in SETTINGS:
            ctx = TrialContext(
                trial=trial,
                hidden=hidden,
                alice_setting=settings[0],
                bob_setting=settings[1],
                rng=rng,
            )
            if model.joint is not None:
                alice_outcome, bob_outcome = model.joint(settings, ctx)
            else:
                if model.alice is None or model.bob is None:
                    raise ValueError(f"model {model.name} has no runnable functions")
                alice_outcome = model.alice(settings[0], ctx)
                bob_outcome = model.bob(settings[1], ctx)
            products[settings].append(alice_outcome * bob_outcome)
            alice_marginals[settings].append(alice_outcome)
            bob_marginals[settings].append(bob_outcome)

    expectations = {
        settings: sum(values) / len(values) for settings, values in products.items()
    }
    s_value = chsh_value(expectations)
    anatomy = anatomy_signature(expectations, alice_marginals, bob_marginals)
    return CHSHResult(
        name=model.name,
        family=model.family,
        description=model.description,
        s_value=s_value,
        expectations=expectations,
        classification=classify_s_value(s_value),
        anatomy=anatomy,
    )


def chsh_value(expectations: Mapping[Settings, float]) -> float:
    return abs(
        expectations[(0, 0)]
        + expectations[(0, 1)]
        + expectations[(1, 0)]
        - expectations[(1, 1)]
    )


def classify_s_value(s_value: float) -> str:
    if s_value <= 2.0 + 0.03:
        return "classical_or_local"
    if s_value <= 2.0 * math.sqrt(2.0) + 0.05:
        return "quantum_range"
    return "post_quantum_or_leaky"


def anatomy_signature(
    expectations: Mapping[Settings, float],
    alice_marginals: Mapping[Settings, Sequence[int]],
    bob_marginals: Mapping[Settings, Sequence[int]],
) -> Mapping[str, float | str]:
    """Summarize a function by the information-flow traces visible at CHSH level."""

    alice_signal = max(
        abs(mean(alice_marginals[(a, 0)]) - mean(alice_marginals[(a, 1)]))
        for a in (0, 1)
    )
    bob_signal = max(
        abs(mean(bob_marginals[(0, b)]) - mean(bob_marginals[(1, b)]))
        for b in (0, 1)
    )
    curvature = (
        expectations[(0, 0)]
        - expectations[(0, 1)]
        - expectations[(1, 0)]
        + expectations[(1, 1)]
    )
    contrast = max(expectations.values()) - min(expectations.values())
    signalling = max(alice_signal, bob_signal)
    return {
        "signalling": signalling,
        "correlation_curvature": curvature,
        "correlation_contrast": contrast,
        "diagnostic_label": diagnostic_label(signalling, contrast),
    }


def diagnostic_label(signalling: float, contrast: float) -> str:
    if signalling > 0.15:
        return "remote_setting_leak_visible"
    if contrast > 1.3:
        return "strong_joint_correlation"
    if contrast > 0.35:
        return "structured_local_or_quantum_like"
    return "weak_or_no_structure"


def mean(values: Sequence[int]) -> float:
    return sum(values) / len(values)


def format_expectations(expectations: Mapping[Settings, float]) -> str:
    return " ".join(
        f"E{settings}={expectations[settings]:+.3f}" for settings in SETTINGS
    )


def iter_results(trials: int = 20_000, seed: int = 7) -> Iterable[CHSHResult]:
    for index, model in enumerate(MODELS):
        yield run_model(model, trials=trials, seed=seed + index)
