# Appendix A — Existence and Convergence of the Leontief Inverse

*Proof of the result used in §2.2 of the multi-regional input–output chapter.*

Throughout, $\mathbf{A}\in\mathbb{R}^{N\times N}$ is the matrix of technical
coefficients, $N = R\,n = 1000$. Inequalities between matrices and vectors are
**entrywise**, and $\rho(\mathbf{A}) = \max\{|\lambda| : \lambda\in\sigma(\mathbf{A})\}$
is the spectral radius.

---

## A.1 Statement

> **Theorem A.1.** Let $\rho(\mathbf{A}) < 1$ and put
> $\mathbf{S}_m = \sum_{k=0}^{m}\mathbf{A}^{k}$. Then
>
> 1. $\mathbf{I}-\mathbf{A}$ is invertible;
> 2. $\displaystyle\mathcal{L} := (\mathbf{I}-\mathbf{A})^{-1} = \sum_{k=0}^{\infty}\mathbf{A}^{k}$, the series converging absolutely;
> 3. $\mathcal{L}-\mathbf{S}_m = \mathbf{A}^{m+1}\mathcal{L}$, so the truncation error decays geometrically at asymptotic rate $\rho(\mathbf{A})$;
> 4. if moreover $\mathbf{A}\ge0$, then $\mathcal{L}\ge\mathbf{I}\ge0$.

Part 4 carries the economic content: output requirements are non-negative, and
delivering one unit of final demand for good $j$ needs at least one unit of gross
output of $j$.

---

## A.2 Preliminaries

The hypothesis constrains eigenvalues, but the argument needs norms. The bridge is
standard.

> **Lemma A.2.** For every $\varepsilon>0$ there is a submultiplicative matrix norm
> with $\lVert\mathbf{A}\rVert_{\varepsilon}\le\rho(\mathbf{A})+\varepsilon$.

*Proof.* Write $\mathbf{A}=\mathbf{P}\mathbf{J}\mathbf{P}^{-1}$ with
$\mathbf{J}=\mathbf{D}+\mathbf{N}$, $\mathbf{D}$ diagonal and $\mathbf{N}$ the
nilpotent superdiagonal. For $\delta>0$ and
$\mathbf{D}_{\delta}=\operatorname{diag}(1,\delta,\dots,\delta^{N-1})$ one has
$\mathbf{D}_{\delta}^{-1}\mathbf{J}\mathbf{D}_{\delta}=\mathbf{D}+\delta\mathbf{N}$.
Then $\lVert\mathbf{M}\rVert_{\varepsilon}:=\lVert(\mathbf{P}\mathbf{D}_{\delta})^{-1}\mathbf{M}(\mathbf{P}\mathbf{D}_{\delta})\rVert_{\infty}$
is submultiplicative, being a similarity transform of an induced operator norm, and
$\lVert\mathbf{A}\rVert_{\varepsilon}=\lVert\mathbf{D}+\delta\mathbf{N}\rVert_{\infty}\le\rho(\mathbf{A})+\delta$;
take $\delta=\varepsilon$. See Horn and Johnson (2013, §5.6). $\blacksquare$

> **Corollary A.3.** If $\rho(\mathbf{A})<1$ then $\mathbf{A}^{k}\to\mathbf{0}$ and
> $\sum_{k}\lVert\mathbf{A}^{k}\rVert<\infty$ in every norm.

*Proof.* Choose $\varepsilon$ with $r:=\rho(\mathbf{A})+\varepsilon<1$. Submultiplicativity
gives $\lVert\mathbf{A}^{k}\rVert_{\varepsilon}\le\lVert\mathbf{A}\rVert_{\varepsilon}^{k}\le r^{k}$,
so $\lVert\mathbf{A}^{k}\rVert_{\varepsilon}\to0$ and
$\sum_{k}\lVert\mathbf{A}^{k}\rVert_{\varepsilon}\le(1-r)^{-1}<\infty$. Norms on
$\mathbb{R}^{N\times N}$ are equivalent. $\blacksquare$

Note that $\rho(\mathbf{A})<1$ is the sharp threshold: $\lVert\mathbf{A}\rVert<1$ in
some given norm is sufficient but not necessary.

---

## A.3 Proof of Theorem A.1

**(1)** If $\mathbf{I}-\mathbf{A}$ were singular there would exist
$\mathbf{v}\ne\mathbf{0}$ with $\mathbf{A}\mathbf{v}=\mathbf{v}$, giving
$1\in\sigma(\mathbf{A})$ and $\rho(\mathbf{A})\ge1$.

**(2)** *Algebra.* For every finite $m$, telescoping gives

$$(\mathbf{I}-\mathbf{A})\mathbf{S}_m=\sum_{k=0}^{m}\mathbf{A}^{k}-\sum_{k=0}^{m}\mathbf{A}^{k+1}=\mathbf{I}-\mathbf{A}^{m+1},$$

and $\mathbf{S}_m$, a polynomial in $\mathbf{A}$, commutes with $\mathbf{A}$, so
$\mathbf{S}_m(\mathbf{I}-\mathbf{A})=\mathbf{I}-\mathbf{A}^{m+1}$ as well. No
convergence hypothesis has been used.

*Analysis.* By Corollary A.3, $\sum_k\lVert\mathbf{A}^k\rVert<\infty$, so
$(\mathbf{S}_m)$ is Cauchy in the complete space $\mathbb{R}^{N\times N}$; let
$\mathbf{S}=\lim\mathbf{S}_m$. Multiplication is continuous and
$\mathbf{A}^{m+1}\to\mathbf{0}$, so letting $m\to\infty$ above yields
$(\mathbf{I}-\mathbf{A})\mathbf{S}=\mathbf{S}(\mathbf{I}-\mathbf{A})=\mathbf{I}$.
Inverses are unique, so $\mathcal{L}=\mathbf{S}$.

**(3)** Factoring the tail,
$\mathcal{L}-\mathbf{S}_m=\sum_{k>m}\mathbf{A}^{k}=\mathbf{A}^{m+1}\sum_{j\ge0}\mathbf{A}^{j}=\mathbf{A}^{m+1}\mathcal{L}$,
exactly; hence $\lVert\mathcal{L}-\mathbf{S}_m\rVert\le r^{m+1}\lVert\mathcal{L}\rVert$
with $r=\rho(\mathbf{A})+\varepsilon$ and $\varepsilon>0$ arbitrary.

**(4)** If $\mathbf{A}\ge0$ then $\mathbf{A}^{k}\ge0$ and $\mathbf{S}_m\ge0$ for every
$m$; the non-negative orthant is closed, so $\mathcal{L}\ge0$. Isolating the $k=0$
term, $\mathcal{L}=\mathbf{I}+\sum_{k\ge1}\mathbf{A}^{k}\ge\mathbf{I}$. $\blacksquare$

---

## A.4 The hypothesis is the economics

> **Definition A.4.** $\mathbf{A}\ge0$ is **productive** if there exists
> $\mathbf{x}\ge\mathbf{0}$ with $(\mathbf{I}-\mathbf{A})\mathbf{x}>\mathbf{0}$ — some
> gross output leaves a strictly positive surplus of every good.

> **Theorem A.5.** For $\mathbf{A}\ge0$ the following are equivalent:
> (1) $\rho(\mathbf{A})<1$; (2) $(\mathbf{I}-\mathbf{A})^{-1}$ exists and is
> non-negative; (3) $\mathbf{A}$ is productive; (4) every leading principal minor of
> $\mathbf{I}-\mathbf{A}$ is positive (**Hawkins–Simon**).

*Proof.* (1)$\Rightarrow$(2) is Theorem A.1.

(2)$\Rightarrow$(3): take $\mathbf{x}=\mathcal{L}\mathbf{1}\ge\mathbf{0}$; then
$(\mathbf{I}-\mathbf{A})\mathbf{x}=\mathbf{1}>\mathbf{0}$.

(3)$\Rightarrow$(1): Perron–Frobenius supplies $\mathbf{w}\ge\mathbf{0}$,
$\mathbf{w}\ne\mathbf{0}$, with
$\mathbf{w}^{\!\top}\mathbf{A}=\rho(\mathbf{A})\mathbf{w}^{\!\top}$. For $\mathbf{x}$
as in Definition A.4,

$$\mathbf{w}^{\!\top}(\mathbf{I}-\mathbf{A})\mathbf{x}=\big(1-\rho(\mathbf{A})\big)\,\mathbf{w}^{\!\top}\mathbf{x}.$$

The left side is strictly positive, since $(\mathbf{I}-\mathbf{A})\mathbf{x}>\mathbf{0}$
componentwise and $\mathbf{w}\ge\mathbf{0}$ is non-zero. Hence
$\mathbf{w}^{\!\top}\mathbf{x}\ne0$, and being non-negative it is positive; dividing
gives $\rho(\mathbf{A})<1$.

(4) is classical (Nikaido, 1968). It avoids an eigenvalue computation but is the more
expensive test at $N=1000$. $\blacksquare$

An economy with $\rho(\mathbf{A})\ge1$ consumes at least as much as it produces: the
regress "inputs to make the inputs to make the inputs…" diverges and no positive final
demand is attainable from finite output. The hypothesis of Theorem A.1 is therefore not
a regularity condition but the viability of the economy — an empirical property of the
estimated table.

---

## A.5 Verification in the twenty-region system

The matrix satisfies $\mathbf{A}\ge0$ and $\rho(\mathbf{A})=0.586466<1$, so Theorem A.1
applies. Productiveness holds constructively as in (2)$\Rightarrow$(3): with
$\mathbf{x}=\mathcal{L}\mathbf{1}$, $\min_i[(\mathbf{I}-\mathbf{A})\mathbf{x}]_i=1.000000$.
Non-negativity holds with $\min_j\mathcal{L}_{jj}=1.0000$ exactly, attained by sectors
purchasing no intermediate inputs.

Contribution of each production round as a share of $\sum_{ij}\mathcal{L}_{ij}$:

| Round $k$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| Share (%) | 46.88 | 24.07 | 13.11 | 7.14 | 3.91 | 2.16 | 1.20 | 0.67 |
| Cumulative (%) | 46.88 | 70.95 | 84.06 | 91.19 | 95.11 | 97.27 | 98.47 | 99.13 |
| Ratio to previous | — | 0.513 | 0.545 | 0.544 | 0.548 | 0.552 | 0.555 | 0.558 |

The last row is an independent estimate of the spectral radius. Since
$\mathbf{A}^{k}\sim\rho(\mathbf{A})^{k}\mathbf{v}\mathbf{w}^{\!\top}$ asymptotically,
successive round contributions must have ratio tending to $\rho(\mathbf{A})$; the
observed ratios rise monotonically, reaching $0.568$ by $k=11$ (cumulative $99.91\%$)
against the computed $0.5865$. The decay rate of the economic decomposition and the
dominant eigenvalue of the matrix are the same number, obtained two different ways.

Part 3 is confirmed at $m=30$:
$\lVert(\mathbf{I}-\mathbf{A})\mathbf{S}_{30}-(\mathbf{I}-\mathbf{A}^{31})\rVert_{\max}=3.0\times10^{-8}$
verifies the algebraic identity to machine precision, and
$\lVert\mathcal{L}-\mathbf{S}_{30}\rVert_{\max}=1.0\times10^{-7}$ matches
$\lVert\mathbf{A}^{31}\rVert_{\max}=7.3\times10^{-8}$ in order of magnitude, as
$\mathcal{L}-\mathbf{S}_m=\mathbf{A}^{m+1}\mathcal{L}$ requires.

Output multipliers, the column sums of $\mathcal{L}$, average $2.1331$ over the $1000$
region–industry pairs, ranging from $1.0000$ to $3.7443$. The aggregate scale implied
by the spectral radius alone, $1/(1-\rho)=2.418$, is of the same order but is not equal
to the mean and should not be expected to be: it governs the decay of successive rounds
in aggregate, whereas a column sum reflects one sector's particular position in the
production network.

---

### References

Horn, R. A. and C. R. Johnson (2013). *Matrix Analysis*, 2nd edn. Cambridge University
Press.

Miller, R. E. and P. D. Blair (2022). *Input–Output Analysis: Foundations and
Extensions*, 3rd edn. Cambridge University Press.

Nikaido, H. (1968). *Convex Structures and Economic Theory.* Academic Press.
