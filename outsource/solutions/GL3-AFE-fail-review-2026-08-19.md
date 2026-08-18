已解压并按包内 `_REVIEW_RETURN_TEMPLATE.md` 的标准做了独立核查。**本轮裁决：FAIL（针对当前提交版本）**。这不是否定 GL(_3) AFE 路线本身，而是当前包尚不能支持“rigorous computation / certified nonvanishing / zero-free region”的结论。

## 1. 总体裁决

| 检查项                            | 裁决                            |
| ------------------------------ | ----------------------------- |
| 两项 AFE 的基本结构                   | **PARTIAL / 基本合理**            |
| Gamma 因子及 FE 前提                | **PARTIAL**，关键归一化/根数/导子未在包内闭合 |
| 权函数数值计算                        | **DISCOVERY ONLY**            |
| 显式积分误差界                        | **FAIL / 缺失**                 |
| (N=60) 截断充分性                   | **FAIL**                      |
| 主和、对偶和尾项严格界                    | **FAIL**                      |
| Arb/python-flint 区间算术          | **FAIL / 未实现**                |
| 网格点非零证书                        | **未建立**                       |
| 连续零点自由区域                       | **未建立**                       |
| witness / proof / metadata 一致性 | **FAIL**                      |
| novelty/status 表述              | **有明显 overclaim**             |
| 当前能否作为下游证明前提                   | **不能**                        |

### 最重要的结论

当前版本最多是一个**双和 AFE 的 discovery-tier 数值实验程序**。不能称为 rigorous AFE computation，更不能用于证明零点自由区域。

---

# 2. 最严重的问题：(N=60) 的数值根本没有表现出所宣称的截断稳定性

`proof.md:53–60` 称：

> (X=12,\ N=60)，权函数已经足够衰减，并需要验证其达到 (10^{-4}) 精度。

我用包内当前代码独立重算了最危险的点

[
s=0.6-20i,\qquad X=12.
]

固定同一套 AFE，只改变截断长度，得到：

| N | 独立计算的 (|L_N(0.6-20i)|) |
|---:|---:|
| 60 | **0.334039207** |
| 80 | **0.444337314** |
| 100 | **0.520025511** |
| 120 | **0.374201283** |
| 150 | **0.423924423** |
| 180 | **0.442692537** |
| 240 | **0.430927656** |
| 300 | **0.410742106** |

这些仍然是 mpmath discovery 数值，不能当成真值；但它们已经足以说明一个事实：

**当前没有任何数值依据可以把 (N=60) 宣称为 (10^{-4}) 精度截断。**

尤其是从 (N=60) 到 (N=80) 就改变约 (0.11)，远大于目标误差 (10^{-4})。

因此 `proof.md:54–55` 的

> (V(5,s)\sim0.2) ... “ensuring rapid convergence”

这个判断不能接受。事实上，**0.2 本身甚至都不是一个“小到足以支持 (10^{-4})”的截断权重**。

---

# 3. `statement.md` 的截断尺度推导有数学问题

`statement.md:40–41` 写：

> (N\sim X^{3/2}) ensures (\exp(-cN^{2/3})) small.

但同一文档定义

[
y=n/X,
]

并声称权函数按

[
V(y)\lesssim \exp(-c y^{2/3})
]

衰减。

那么在 (n=N) 处自然得到的是

[
\exp!\left[-c(N/X)^{2/3}\right],
]

而不是

[
\exp(-cN^{2/3}).
]

所以 `statement.md:40–41` 的尺度关系目前**没有从前面的权函数界推出**。

如果确实具有统一的
[
e^{-c y^{2/3}}
]
型界，那么粗略地解决
[
e^{-c(N/X)^{2/3}}\le\varepsilon
]
给出的尺度应类似

[
N\gtrsim
X\left(\frac{\log(1/\varepsilon)}c\right)^{3/2},
]

不是文中未经解释的 (N\sim X^{3/2})。

这是需要正式修正的分析层错误，不只是“缺一个常数”。

---

# 4. proof 中报告的网格最小值是错的

`proof.md:98–103` 和 `witness/README.md:12` 都写：

> Min (|L(s)|=0.532) at ((0.6,0)).

但实际 `witness/grid_values.json` 中已经有

[
|L(0.6-20i)|=0.33403921,
]

显然

[
0.33403921 < 0.53188268.
]

我用当前**双和**代码重新计算：

[
|L(0.6)|=0.531882680306,
]

以及

[
L(0.6-20i)
\approx
0.329542963939+0.054622588307,i,
]

所以

[
|L(0.6-20i)|
\approx0.334039207631.
]

因此这里不是简单的旧 witness 问题：

**正文的“minimum = 0.532”结论本身就是错误的。**

必须重新自动生成统计摘要，禁止人工复制 min/max。

---

# 5. witness 内部也发生了版本漂移

`witness/grid_values.json` 的 notes 仍然写：

> `single-sum AFE only`
> `Missing: dual sum`

但当前 `src/afe_sym2.py:183–224` 明明已经实现了 main + dual 两项。

而且我独立拆开计算 (s=0.6-20i)：

[
\text{main}\approx0.6496594-0.0272118i,
]

[
\text{dual}\approx-0.3201165+0.0818344i,
]

两项相加才得到 witness 中的

[
0.3295430+0.0546226i.
]

也就是说，**witness 数值似乎已经来自双和代码，但 metadata 还是上一版单和说明。**

因此当前 `MANIFEST.sha256` 虽然全部通过，只能证明“这些互相矛盾的文件就是打包时的文件”，不能证明证据链的一致性。

建议新增 machine-checkable coherence gate：

```text
proof summary
   ↓
certificate metadata
   ↓
witness statistics
   ↓
checker expectations
```

任何字段漂移立即 CI FAIL。

---

# 6. Arb 证明层实际上完全没有实现

这一点包内自己也承认。

`src/afe_sym2.py:11–12`：

> discovery-tier (mpmath floats, not Arb intervals)

`proof.md:81–94` 也明确列出：

* 没有 Arb；
* 没有 outward-rounded enclosure；
* 没有 quadrature error；
* 没有 Gamma contour bound。

所以 `_REVIEW_RETURN_TEMPLATE.md` 中：

> Arb interval arithmetic: outward rounding used throughout

答案必须是：

**NO。**

Arb 确实可以用于严格 ball arithmetic 和 rigorous integration，但“库有能力”与“本程序已经完成严格证明”是两回事。([Fredrik Johansson's Website][1])

---

# 7. README 的 rounding 描述甚至有方向错误

`README.md:61–63` 写：

> rigorous rounding (**outward for upper bound, inward for lower**)

若这里指区间端点，这是不安全的。

为了保证 enclosure：

* lower endpoint 应向 (-\infty) 外舍入；
* upper endpoint 应向 (+\infty) 外舍入。

即两端都应当是**outward enclosure**。

对于 Arb 更自然的做法是直接使用 complex ball / real ball API，让库维护 enclosure，而不是设计“lower inward rounding”。

这一句必须删除或改写。

---

# 8. 对复数 (L(s)) 使用 `[L_lo,L_hi]` 的定义也不正确

`statement.md:24–28` 要输出：

> Arb interval `[L_lo,L_hi]` enclosing (L(\sigma+it)).

对于一般 (t\neq0)，(L(s)\in\mathbf C)，没有这样的实数顺序区间。

证明层应改成例如：

[
L(s)\in
[x_0\pm r_x]+i[y_0\pm r_y],
]

或者一个 Arb `acb` complex ball。

非零判据应写成：

[
0\notin B_s,
]

或更清楚地生成严格下界

[
|L(s)|\ge \delta_s>0.
]

这一点对最终 certificate schema 也很重要。

---

# 9. 对偶尾项的说明不足，而且 `limitations.md` 有错误论证

`limitations.md:20–21` 声称：

> (V_{\rm dual}(nX,s)\sim(nX)^{-1}), ensuring convergence.

这个说法至少作为当前论证是不够的。

如果只有

[
V_{\rm dual}(nX,s)=O((nX)^{-1}),
]

则对偶项绝对值按文中的 Deligne 型界至多类似

[
d_3(n)n^{\sigma-1}n^{-1}
========================

d_3(n)n^{\sigma-2}.
]

当 (\sigma=1) 时变成

[
d_3(n)/n,
]

并不绝对收敛。

实际权函数应通过向右移动 Mellin 线得到任意幂衰减，或更强的 stretched-exponential 衰减；**必须证明那个更强的界**，不能用“(\sim y^{-1}) ensuring convergence”结束。

---

# 10. `statement.md` 与实际代码的 contour 方法不一致

`statement.md:36–38` 宣称：

> contour shift to (\Re u=-m), picking up residues from Gamma poles.

但 `src/afe_sym2.py:129–176` 实际做的是：

[
\Re u=1,\qquad -T\le \Im u\le T
]

上的直接 midpoint quadrature。

代码没有实现：

* contour shift；
* residue bookkeeping；
* shifted-contour integral；
* residue interval enclosure。

因此必须二选一：

**A.** 文档改成“直接在 (\Re u=1) 做 rigorous integration”，并证明纵向截断与 quadrature error；

或者

**B.** 真正实现 contour-shift + residues。

不能保留目前这种“证明稿描述了 A，代码运行 B”的状态。

---

# 11. (L(2)) spot-check 的误差说明也不严谨

`witness/README.md:20–21` 写：

> tail error is (O(N^{-1})\sim5\times10^{-3}).

如果使用包内提供的通用绝对界

[
|A(n)|\le d_3(n),
]

则尾部对应

[
\sum_{n>N}\frac{d_3(n)}{n^2},
]

其自然量级带有 ((\log N)^2/N) 因子，不能简单把常数取成 1 后写成 (1/N)。

所以：

> “matches to ~3 digits”

目前也没有严格依据。

作为 sanity check 没问题，但必须标为 heuristic/discovery cross-check。

---

# 12. AFE 本身：核心结构可以保留，但前提必须精确闭合

当前双和公式

[
L(s)=
\sum_n\frac{A(n)}{n^s}V(n/X,s)
+
\sum_n A(n)n^{s-1}\widetilde V(nX,s)
]

以及

[
\widetilde V(y,s)=
\frac1{2\pi i}\int
\frac{G(1-s+v)}{G(s)}
y^{-v}\frac{h(-v)}v,dv
]

在假定

[
\Lambda(s)=G(s)L(s)=\Lambda(1-s)
]

且 self-dual、root number (+1)、conductor (1) 后，和标准 Mellin-shift 推导是相容的。

所以我**没有发现需要推翻“两项 AFE 核心形式”的理由**。

但当前包直接假设：

* conductor (Q=1)；
* root number (+1)；
* self-duality；
* (G(s)=\Gamma_{\mathbb R}(s+1)\Gamma_{\mathbb C}(s+11))；
* 所需 entireness / FE。

这些都应该成为显式 dependency lemma，而不是注释中的默认知识。

Gelbart–Jacquet 的确建立了 GL(2)→GL(3) 的相关 lift；包内 `dependencies.yaml` 写的文章标题 `"A note on the symmetric square L-function"` 不准确，正式文献标题是 **“A relation between automorphic representations of GL(2) and GL(3)”**。([Numdam][2])

另外 Harcos 文献明确表述的主要结果是**central value (L(1/2,\pi))** 的 uniform AFE。([arXiv][3]) 因此若本任务需要任意 (0.5\le\sigma\le1) 的 (s)，最好在本文中直接给出完整 Mellin 推导，而不要只用“standard GL(_3) AFE”一句带过。

---

# 13. novelty.md 必须降级

这是当前最明显的 status overclaim。

`novelty.md:3–5`：

> “What is new is the **RIGOROUS implementation with certified error bounds using Arb**”

然而实际根本没有 Arb 或 certified error bounds。

`novelty.md:7–9` 又说：

> “the rigorous AFE computation provides the zero-free region”

而 `proof.md` 自己又明确承认：

> finite grid cannot establish a continuous zero-free region.

这两处直接冲突。

建议当前版本改为：

> “The current contribution is a discovery-tier prototype implementing a two-term AFE for (L(s,\mathrm{sym}^2\Delta)). Rigorous Arb certification and continuous zero-free verification remain future obligations.”

在真正完成 proof-tier 前不要出现：

* rigorous implementation；
* certified error bounds；
* provides the zero-free region。

---

# 14. continuous zero-free region：当前完全没有

这一点 `proof.md:108–119` 判断是正确的。

即使未来每个 grid point 都得到

[
|L(s_j)|>\delta_j,
]

也**不能**推出网格间没有零点。

必须增加第二层：

### 路线 A：导数覆盖

严格计算

[
M=\sup_R |L'(s)|
]

并令网格覆盖半径 (r) 满足

[
Mr < \min_j |L(s_j)|.
]

然后由

[
|L(s)-L(s_j)|\le M|s-s_j|
]

完成覆盖。

### 路线 B：argument principle

对矩形边界进行 rigorous complex interval evaluation，证明：

1. 边界无零；
2. 计算 winding number；
3. 得到内部零点数。

对于“零点自由区域”任务，我更推荐 **argument principle certificate**，因为它比极细二维网格 + 全局 (L') 界更自然。

---

# 15. 我建议的修复优先级

### P0 — 当前版本立即修

1. 删除 `proof.md` 与 `witness/README.md` 中错误的 `min=0.532`。
2. 从 JSON 自动计算所有 min/max，禁止手填。
3. 修正 witness 的 `single-sum` stale metadata。
4. 删除 novelty 中所有“rigorous implementation 已完成”描述。
5. 修正 Gelbart–Jacquet 引用标题。
6. 删除 `dependencies.yaml` 中不存在的
   `src/zero_free_arb.py` 与 `baseline/zero_free_scan.json`
   引用，或者把这些文件真正放入包。
7. 修正 README 的 inward-rounding 表述。
8. 将 complex output 改成 `acb` ball schema。

### P1 — 先完成“单点 rigorous AFE”

不要立即扫 45 点。

先选一个，例如

[
s=1,\quad\text{或}\quad s=0.6-20i,
]

做完整 proof-tier pipeline：

[
\boxed{
\text{exact }A(n)
+
\text{rigorous }V,\widetilde V
+
\text{main tail}
+
\text{dual tail}
+
\text{quadrature error}
}
]

最终只输出一个：

[
L(s)\in B,\qquad |L(s)|>\delta.
]

这一步真正通过后再扩网格。

### P2 — Arb 实现

系数首先改成精确形式：

[
\lambda(p)^2
============

\frac{\tau(p)^2}{p^{11}},
]

而不是当前

```python
tau(p) / p**5.5
```

浮点平方。

然后所有：

* Gamma；
* powers；
* quadrature；
* sums；
* tail constants

均进入 Arb/Acb enclosure。

### P3 — 正式解析尾界

证明统一于

[
0.6\le\sigma\le1,\quad |t|\le20
]

的

[
|V(y,s)|\le C_A(s)y^{-A},
\qquad
|\widetilde V(y,s)|\le \widetilde C_A(s)y^{-A}
]

或显式 stretched-exponential 版本。

然后用

[
|A(n)|\le d_3(n)
]

导出**可计算的两个尾和上界**。

不要先固定 `N=60` 再寻找理由；应当让程序根据误差预算自动求最小 (N)。

### P4 — 最后才做 zero-free rectangle

只有所有单点都 certified 后，再加入 argument-principle / derivative-cover gate。

---

# 完成版 Review Return Template

**Verdict: FAIL**

### GL(_3) AFE computation method

* **Mathematical verdict on the method:** PARTIAL；双和 AFE 框架可继续，但前提与误差分析未闭合。
* **Weight function computation:** FAIL as rigorous computation；只有 midpoint mpmath quadrature，无严格积分误差。
* **Gamma factor bounds:** NOT PROVIDED。
* **Truncation parameter (N):** FAIL；没有证明 (N=60) 足够，独立数值稳定性检查反而显示显著 (N)-依赖。
* **Tail bound:** FAIL；没有 explicit certified main/dual tail。
* **Arb interval arithmetic:** **NO**。
* **Dual sum handling:** FORMULA IMPLEMENTED，但 tail 未证明。
* **Error analysis completeness:** INCOMPLETE。

### Computational results

* Grid: (\sigma\in[0.6,1.0]), (|t|\le20)
* Resolution: (5\times9)
* Minimum **certified** (|L(s)|): **NONE**
* Minimum discovery value in supplied JSON: **0.33403921 at ((0.6,-20))**，不是正文所称 0.532。
* Zero-free region established: **NONE**
* python-flint / Arb: **NO**

### Cross-cutting

* **Dependency above evidence level:** yes；一些“standard AFE / zero-free”依赖没有精确闭合。
* **Status/novelty overclaim:** **YES，严重。**
* **Gap in error analysis:** quadrature + main tail + dual tail + exact coefficient enclosure + continuous-region certificate。
* **Required revision:** **major revision / proof-tier rewrite**。

**建议不要继续扩大网格。当前最有效的下一步是把整个 Batch 04 收缩成“一个点的完整 Arb 证书”，先把 analytic error budget 真正闭环；完成后再恢复网格和零点自由区域任务。**

[1]: https://fredrikj.net/arb/ "Welcome to Arb’s documentation! — Arb 2.9.0-git documentation"
[2]: https://www.numdam.org/item/10.24033/asens.1355.pdf "A relation between automorphic representations of GL(2) and GL(3)"
[3]: https://arxiv.org/pdf/math/0111312 "arXiv:math/0111312v3  [math.NT]  12 Feb 2002"
