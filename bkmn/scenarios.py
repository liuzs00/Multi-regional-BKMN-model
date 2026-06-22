"""
Bayesian SSP/RCP scenario layer (Section 2.2).

  * Prior mixture probabilities over SSP and RCP (Dirichlet-Categorical
    expected values), taken from Eq 18-19.
  * Annual RCP transition matrix Q (Eq 1), exponential in state distance.
  * Mixture evolution  q_T = q_0 Q^T  and expected-output weighting (Eq 20-21).

SSP states do not transition (paper assumption); only RCP states do.  In this
simplified reproduction the climate drivers depend on RCP, so expected outputs
are weighted by the RCP mixture (SSP weighting is carried for completeness).
"""

import numpy as np

from . import assumptions as cfg
from .climate import RCP_STATES, SSP_STATES


def prior_rcp() -> np.ndarray:
    return np.array([cfg.RCP_PRIOR[r] for r in RCP_STATES], dtype=float)


def prior_ssp() -> np.ndarray:
    return np.array([cfg.SSP_PRIOR[s] for s in SSP_STATES], dtype=float)


def transition_matrix(lam: float = cfg.TRANSITION_LAMBDA) -> np.ndarray:
    """
    Annual RCP transition matrix Q (Eq 1):
        q(j,k) = exp(-lam |j-k|) / sum_h exp(-lam |j-h|)
    using the state index (0..4) as the distance measure.
    """
    n = len(RCP_STATES)
    idx = np.arange(n)
    Q = np.zeros((n, n))
    for j in idx:
        w = np.exp(-lam * np.abs(j - idx))
        Q[j] = w / w.sum()
    return Q


def rcp_mixture_at(years: float, lam: float = cfg.TRANSITION_LAMBDA) -> np.ndarray:
    """
    RCP mixture probabilities after `years` (Q applied annually).
    Sub-year horizons use the prior (Q^0 = I).
    """
    Q = transition_matrix(lam)
    n_steps = int(round(years))
    q = prior_rcp()
    if n_steps <= 0:
        return q
    return q @ np.linalg.matrix_power(Q, n_steps)


def expected_over_rcp(value_by_rcp: dict, years: float,
                      lam: float = cfg.TRANSITION_LAMBDA):
    """
    Expectation of an output across the RCP mixture at `years` (Eq 21).
    `value_by_rcp` maps RCP label -> scalar or np.ndarray.
    """
    q = rcp_mixture_at(years, lam)
    vals = [value_by_rcp[r] for r in RCP_STATES]
    acc = q[0] * np.asarray(vals[0], dtype=float)
    for w, v in zip(q[1:], vals[1:]):
        acc = acc + w * np.asarray(v, dtype=float)
    return acc
