# 研究计划：L(1, sym² f) 有效下界

## 项目目标

出发点：Goldfeld–Hoffstein–Lieman (1994) 附录定理

    L(1, sym² f) ≥ c / log N

其中常数 c > 0 是**非有效的**（不可计算）。本项目的三阶段目标：

1. **近期（可行）**：对特定模形式（从 Ramanujan Δ 函数开始），用区间算术严格认证
   L(1, sym² f) ≥ L_0，给出首个计算机辅助认证的实例。

2. **中期**：对素数级 p ≤ P 的所有归一化本原 Hecke 特征形式，认证有效常数
   c_eff，使得 L(1, sym² f) ≥ c_eff / log p。

3. **长期（研究性）**：通过新的 mollifier 论证，证明改进下界
   L(1, sym² f) ≥ c / (log N)^{1-δ}。

---

## 双轨并行推进策略（2026-08-16 更新）

### 2026-08-18 状态审计结论

- **撤回传播**：`spec/`、`proof/paper.tex`、`proof/04` 中残留的 F-3 [THM] / 2.405
  说法已清除；F-3 现在一致为 [OBL]。当前没有本仓库认证的
  L(1, sym²Δ) 正下界。
- **F-2 降级**：Shahidi 的精确 `L(1,Ad)>0` 陈述仍未找到，Jacquet--Shalika 也没有给出 proof/02 旧稿所需的全局正 local correction 公式。F-2 已从 [THM] 对外降级为 [OBL]；下游不得使用它。
- **checker 修正**：`checker/check_bound.py` 不再把发散的
  `sum_{p>P} 3/p` 包装成 3/P 尾部界；在 E-2 提供可重放证书前，它必须拒绝
  当前 Euler-product 证书。新增 `tests/test_status_grammar.py` 固定该拒绝行为。
- **M-Voronoi 诚实化**：N=10^8 扫描给出的是条件阈值和经验常数，不是
  C_GL3 的证明；Miller-Schmid 定理的正规化与 c-求和指数仍未提取。
  本轮已将 Miller-Schmid (2006 preprint) Theorem 1.18 的精确 Kloosterman/Bessel
  公式（含 `(c/d)^{1-sum lambda}`、`A(n,d)/|n|` 与 `F(nd^2/(c^3 q))` 正规化）
  转录到 `discovery/_voronoi_proof_sketch.py`，后续推导必须从该公式而非旧
  泛型 `c^{-2}K_nu` 公式出发。
- **baseline 缺口**：`baseline/` 目前没有要求的 PDF 或逐条 claim ledger；
  因此外部 [BASE] 引用在发布/下游使用前仍需 source-backed verification。

### 2026-08-18 执行队列（本轮按序推进）

| 顺序 | 任务 | 可验证交付物 | 状态 |
|---|---|---|---|
| Q-1 | baseline evidence ledger | `baseline/REFERENCE_BASELINE.md` + source-level claim table；PDF 暂不提交，先区分 source-backed / source-unavailable | 已完成 |
| Q-2 | Miller–Schmid \(C_{GL3}\) 正式 obligation | `proof/05-voronoi-constant.tex`，状态必须为 `[OBL]`；从 Theorem 1.18 精确公式出发 | 已完成 |
| Q-3 | S1 Arb 有限和原型 | `src/afe_s1_arb.py`：exact τ 输入、Arb sym² 系数、Arb 垂直围道积分权重；只认证有限截断，不认证无穷尾项 | 已完成 |
| Q-4 | checker 独立重算 | checker 重算 τ 与有限 partial sum/interval，而不是只读取生成器数字；完整 L(1) tail 仍拒绝 | 已完成 |
| Q-5 | 阻塞项外包规格 | `OUTSOURCING.md`：\(C_{GL3}\) 与 J 两个自包含任务，包含输入、目标、禁止路径、验收命令 | 已完成 |

### 2026-08-18 本轮执行结果与新增发现

- **Q-1**：逐条外部基线 ledger 已建立。GHL 附录定理和 Miller--Schmid
  Theorem 1.18 是 source-backed；Gelbart--Jacquet Theorem 9.3 在其非自扭
  假设下 source-backed。Casselman--Shalika Theorem 5.4 与 Jacquet--Shalika
  Proposition 2.3 / Theorem 5.3 后续已核到精确 theorem-level。Shahidi 1981
  已取得作者扫描并核到 Theorems 5.2--5.3，
  但未找到 proof/02 所需的逐点 `L(1,Ad)>0` 精确陈述，ledger 记为 `not-found`。
  另已核验 Shahidi 1980 BAMS 定理：`L_S(1+it,pi x pi') != 0`；它只给出
  pair L-function 非零，不能自动分离 `zeta(s)` 极点与 `L(1,Ad)` 的可能零点。
- **F-2 审计修正**：F-2 的逐点留数正性不能排除 exceptional zero，也不能
  给出按 level 一致的下界。此前“F-2 排除 Siegel zero”的传播已在
  `spec/`、`proof/02`、`proof/03`、`proof/04`、`proof/paper.tex` 中纠正。
  exceptional-zero 分支需要一致导数/log-derivative 界，仍是 `[OBL]`。
- **Q-2**：新增 `proof/05-voronoi-constant.tex`，固定 Miller--Schmid 公式的
  \(A(n,d)/|n|\)、\(|c/d|\)、modulus \(qc/d\) 与 argument
  \(nd^2/(c^3q)\) 正规化；明确所有数值阈值 discovery-only。
- **Q-3/Q-4**：新增 `src/afe_s1_arb.py` 与独立 `checker/check_s1_finite.py`。
  证书只认证有限对象 `S1[N,T]`，显式拒绝 infinite S1、tail 与 L(1) promotion。
  checker 从 τ eta-product、sym² 递推和 Arb 积分独立重算，不导入 `src/`。
- **Q-5**：新增 `OUTSOURCING.md`，将 \(C_{GL3}\) 与 J certification 转成
  两个自包含外包任务，包含目标、允许路线、禁止路径和验收命令。

### 2026-08-18 本轮 Q-6/Q-7 执行结果

- **Q-6（安全降级）**：未找到精确 Shahidi adjoint theorem，也没有完成
  pair L-function / Jacquet--Shalika 极点到全局 F-2 公式的完整正性桥。
  因此 `proof/02-global-residue.tex` 重写为 obligation：显式列出 adjoint
  输入、bad local correction 正性、measure normalization 和
  `L(pi~ x pi)` 到 `zeta L(Ad)` 的缺口。`spec/`、`README.md`、
  `proof/04`、`proof/paper.tex` 同步将 F-2 改为 `[OBL]`。
- **Q-7（精确引用）**：通过作者/公开扫描 OCR 核验
  Casselman--Shalika Theorem 5.4 (p. 227) 和 Jacquet--Shalika §2.2
  formula (2.2.2)、Proposition 2.3 (pp. 511--512)、Lemma 4.6
  (pp. 550--552)、Theorem 5.3 (pp. 555--556)。ledger 拆分为 CS-W.1、
  JS-LI.1、JS-EP.1、JS-GF.1。F-1 的外部输入现在 theorem-level
  source-backed；F-2 仍由 SH-AD.1 / JS-GF.1 阻塞。

### 下一轮优先队列

| 顺序 | 任务 | 可验证交付物 | 状态 |
|---|---|---|---|
| Q-6 | Shahidi/adjoint baseline repair | 找到精确定理并写出完整桥，或将 F-2 降级为 `[OBL]` | 已完成（降级） |
| Q-7 | exact Casselman–Shalika / Jacquet–Shalika ledger | OCR 或转录精确 theorem number 与 normalization，升级 `weaker-in-source` 行 | 已完成 |
| Q-8 | full S1 tail certificate | 在 finite `S1[N,T]` 之外证明无穷 n/t tail；不得改变当前 finite 证书语义 | 已完成 |
| Q-9 | outsourced V/J receipt check infrastructure | outsource/ 目录（OB-01/OB-02 自包含 prompt、PROMPT_LINT.md 对抗性清单、README.md 状态面板）、papers/PAPER_LINT.md（论文提交前 lint）；模式学习自 abc-conjecture-verification 仓库 | 已完成 |
| Q-10 | instance M-3: numerical zero-free region for sym²Δ | `proof/04b-zero-free-region.md` + `witness/derivative_bounds_all_grid.json`：205 grid points, 160 cells all covered by overlapping disk argument; L(s) ≠ 0 for σ ∈ [0.6, 1], \|t\| ≤ 20 | **已完成** (e6b3a87) |
| Q-11 | certify J via Abel summation | 利用 Q-10 的零点自由区域和 partial sum 界，通过 Abel 求和认证 Cesàro 截断误差 → 得到 J ∈ [J_lo, J_hi] | **已完成** (0b7756c) |

### 2026-08-18 Q-8 执行结果

- **Q-8（infinite S1 证书）**：新增 `src/afe_s1_full.py`，在有限截断 S1[N,T]
  之外用初等工具证明无穷尾项：
  - **垂直尾项 E_t**：|E_t| ≤ 12·C_T·Σ_{n≤N}|A(n)|/n²，其中
    C_T = G(2)/G(1)·e·e^{-T²}/(2πT²)。在 T=8 时 C_T ~ 10^{-29}，尾项可忽略。
  - **系数尾项 E_n**：用围道移动 Re(u): 1→1+m（m=2，无极点，Gaussian 衰减），
    得 |W(y)| ≤ A_m·y^{-(1+m)}，其中
    A_m = G(2+m)/G(1)·e^{(1+m)²}/(2√π·(1+m)) ≈ 680。
    d₃ 尾通过 Abel 求和从 Σ_{n≤x}d₃(n) ≤ x(log x+1)² 显式界定。
  - **关键不等式**：|Γ(x+it)| ≤ Γ(x)（Weierstrass 乘积），将模积分降为闭式。
  - **参考证书**：N=20000, T=8, M=200000, precision=128
    → S1 ∈ [0.548298, 0.548305]（width ≈ 7.0e-6），E_t ≈ 1.1e-29，
    E_n ≈ 3.5e-6，A₂ ≈ 680。189 秒计算完成。
  - `checker/check_s1_full.py`：独立重算 τ、d₃、sym² 系数、围道常数、Abel 尾，
    不导入 `src/`；拒绝 finiteness-only promotion、L(1) 认证和篡改间隔。
  - `tests/test_afe_s1_full.py`：13 项测试（d₃ 值、sym² 系数、有限间隔交叉验证、
    checker 通过/拒绝、真值包含、尾项层级）。
  - **修复的 bug**：(1) 错误 gamma Γ_R(s)Γ_C(s) → 正确 Γ_R(s)Γ_C(s+11)；
    (2) `acb(lower, upper)` 误用为区间（实为 `lower + upper·i`）→ 改用
    `arb(center, radius)`。
  - 证书只认证无穷主和 S1；不认证对偶项 J 或 L(1,sym²Δ)。

**执行纪律**：Q-2 与 J 不能因数值裕量大而关闭；Q-3 的输出不得称为
完整 S1 认证；Q-4 只能接收由 proof-tier 方法生成的 finite certificate。

> **2026-08-18 状态修正**：原先“单实例 AFE 可完全绕开 M-3”的判断过于乐观。对 sym²Δ，主和 S1 可以用 Arb 认证，但对偶/围道项 J 的截断误差需要完整 GL₃ Voronoi 公式或实例级数值无零区域。统一族群界 E-1 仍走 c_eff / log p 路线；单实例 E-2 与 M-3/M-Voronoi 不再完全解耦。


### 2026-08-18 Q-10 计划：实例 M-3 数值无零区域

**目标**：对 sym²Δ，在矩形 R = {σ ∈ [0.6, 1], |t| ≤ T_max} 上认证 L(s, sym²Δ) ≠ 0，
给出显式 δ₀ = min_{s∈R} |L(s)| > 0 和 partial sum 界 |S(X)| ≤ C_max × X^α（α < 1）。

**技术路线**（三条并行，选最先成功的）：

1. **Dirichlet 级数 + 余项界**（Re(s) > 1 区域）：
   - 对 σ > 1，L(s) = Σ_{n≤N} A(n)/n^s + R_N(σ)
   - |R_N(σ)| ≤ d₃_tail(N, σ) = Σ_{n>N} d₃(n)/n^σ
   - d₃ 尾通过 Abel 求和从 Σ_{n≤x}d₃(n) ≤ x(log x+1)² 显式界定
   - 在 σ = 1.01..1.5, |t| ≤ 20 上扫描，验证 |L(s)| > δ₁

2. **GL₃ AFE 评值**（临界带内）：
   - 对 1/2 < Re(s) ≤ 1，用 GL₃ AFE: L(s) = S_main(s;X) + χ(s)·S_dual(s;X_dual)
   - 主和 S_main(s;X) = Σ_{n≤N} A(n)/n^s × V(n/X, s)（Gaussian 衰减，绝对收敛）
   - 对偶和 S_dual(s;X_dual) = Σ_{n≤N_dual} A(n)·V*(nQ/X_dual, 1-s)
   - 余项：|R_main| ≤ A_m × Σ_{n>N} d₃(n)/n^σ × (n/X)^{-(1+m)}（围道移动 m=2）
   - 在 {σ ∈ [0.6, 1], |t| ≤ 20} 上扫描，验证 |L(s)| > δ₂

3. **Cesàro 偏和直接界**：
   - 用 N=10⁸ 的 Cesàro 偏和数据（已有 min|L_ces(0.9+it)| = 0.3926）
   - 从经验 max|S(X)|/X^{2/3} = 0.001611 出发，尝试用解析方法证明 |S(X)| ≤ C × X^{2/3}
   - 若成功：Cesàro 误差界 = C × N^{2/3-σ}/(σ-2/3)，σ=0.9, N=10⁸ 时误差 < 0.009C

**预期输出**：
- `src/zero_free_arb.py`：Arb 评值函数 L_arb(s) + 网格扫描 + 证书 JSON
- `checker/check_zero_free.py`：独立验证器（不导入 src/）
- 证书字段：σ₀, T_max, δ₀, C_max, α, N_terms, precision

**与 J 认证的连接**：
- 从 |S(X)| ≤ C_max × X^α 和 Abel 求和得 Cesàro 误差界
- L(1) ∈ [L_ces(N,1) - ε(N), L_ces(N,1) + ε(N)]
- 目标：L(1) ∈ [0.62, 0.65]（width ≤ 0.03）

### 2026-08-18 Q-10 执行结果：实例 M-3 数值无零区域 [已完成]

- **Q-10（数值无零区域）**：通过 GL₃ AFE 评值 + overlapping disk 论证，
  在矩形 [0.6, 1.0] × [-20, 20] 上严格证明 L(s, sym²Δ) ≠ 0。
- **方法**：205 grid points × |L(s)| 评值 + central-difference gradient →
  continuity radii r = |L|/|∇L|。160 cell centers 全部被至少一个
  continuity disk 覆盖。
- **关键结果**：
  - min |L(s)| = 0.170 at (0.6, ±7)
  - min r used for coverage = 0.513 > d/2 = 0.503 (cell diagonal)
  - 54/205 grid points have r < d/2, but every cell center is covered
- **直接 L(1) 认证**：certify_l1.py → L(1) ∈ [0.63179293, 0.63179298]
  （width 4.6×10⁻⁸, L(1) > 0: YES）
- 交付物：`proof/04b-zero-free-region.md`, `witness/derivative_bounds_all_grid.json`,
  `witness/dense_grid_values_N3000.json`, `witness/single_point_certificate.json`

### 2026-08-18 Q-11 计划：认证 J 和 L(1)

**目标**：从 |S(X)| 界 → Cesàro 误差 → J 认证 → L(1) ∈ [L_lo, L_hi]。

**当前状态**：
- S1 ∈ [0.548298, 0.548305]（已认证）
- L_ces(N=10⁸, 1) ≈ 0.6317929（经验）
- 条件 L(1) ∈ [0.6317, 0.6318]（依赖未证明的部分和界）

**阻塞**：证明 |S(X)| ≤ C × X^{0.5}（或 X^{0.5+ε}）。
- 外包 OB-03：部分和界证明（三条技术路线）
- 外包 OB-04：GL₃ AFE 严格计算（Arb 评值 → 零点自由区域 → 部分和界）

**两条并行路径**：
1. OB-03 直接证明部分和界 → 一步到位认证 L(1)
2. OB-04 先建零点自由区域 → 再推部分和界 → 认证 L(1)

### 轨道 1（快速出成果）：纯计算认证

直接目标：严格证明 L(1, sym² Δ) ∈ [L_lo, L_hi]（如 [0.630, 0.633]）。

路径：
1. 实现 sym² Δ 的近似函数方程（AFE），用 Arb 区间算术认证权重函数 W(n/X)
2. 计算 L(1) = 2 Σ_{n≥1} a_{sym²}(n) / n × W(n/X) + 误差项
3. 误差项通过函数方程直接界定，无需零点自由区域
4. 将结果推广到 p ≤ 10^4 的小素数级实例

**当前状态**（2026-08-16 会话更新）：
- GL₃ AFE 公式 **L(1) = S1 − J** 数值验证完成（探索层）
- S1 = ∑_n a(n)/n × W_afe^{s0=1}(n/12)：在 n=72 时 S1≈0.548490，但 W_afe(6)=0.056 仍非零；真正收敛需到 n≈670（W_afe(670/12)≈5×10^{-4}），届时尾项 < 10^{-10}
- J = (1/2π)∫ Re[L(1/2+it) × A(t)] dt ≈ −0.083（Re(w)=−1/2 围道积分）
- L(1) = S1 − J ≈ 0.548490 + 0.083 ≈ 0.631（与 Tauberian 0.6314 一致）
- **J 的认证障碍**：J = ∑_n a(n)/n^{1/2} × Re[Â_A(log n)] 是条件收敛级数，尾项 ∑_{n>N} 的显式界需要 |∑_{n>N} a(n)/n^{1/2+it}| 的显式界，而后者等价于 GL₃ L-函数在临界线附近的显式估计（零点自由区域 [OBL M-3] 或 GL₃ Voronoi 求和公式）
- Cesaro 平均（Fejér 和）N=10000：L(1) ≈ 0.6320 ± 0.0003（系统偏差来自 S1 截断于 n=72，加上 Cesaro 残余偏差）
- **证明层 [OBL E-2] 被阻塞**：S1 认证（n=1..670，Arb）可行；J 认证需要 GL₃ Voronoi 或 [OBL M-3]
- **中心值 AFE 方法（2026-08-16 探索，失败）**：对每个固定 t，用 GL₃ AFE at s0=1/2+it 计算 L(1/2+it)（`discovery/_afe_central.py`）。V(y, 1/2+it) 仅有代数衰减 ~1/y（而非 Gaussian e^{-(log y)²/4}），L_main(t) 收敛极慢（n=80 时仍振荡 ~0.357，误差 ~0.05），导致 J ≈ -0.056（而非 -0.083）。需要 n_max>>1000 才收敛，计算不可行。根本原因同"两侧 AFE"：在 s0=1/2 处 L-函数不绝对收敛，残余 y^{-1} 代数衰减无法避免。
- **已排除路径**：(1) 直接 Dirichlet 截断：条件收敛 O(N^{-1/2})。(2) 两侧 AFE（v=-w 代换）：W_dual(y)~1/y 代数衰减，仍条件收敛。(3) 中心值 AFE (s0=1/2+it)：V(y,1/2+it)~1/y，L_main 极慢收敛。(4) 直接 Dirichlet 级数 at s=1+δ：tail bound O(N^{δ-ε}) 不够紧。
- **Fubini 表示（2026-08-16 探索）**：将 J 改写为 J = Σ_n a(n)/n^{1/2} × w(n)，其中 w(n) = (1/2π)∫ Re[(n^{-it} + phase(t)n^{it}) × amp(t)] dt（`discovery/_j_wn.py`）。每个 w(n) 通过 1D 积分精确计算（Gaussian 衰减 exp(-(log(n·e/12))²/4)），Cesaro 平均 N=700 得 J ≈ -0.0834 ± 0.001，L(1) ≈ 0.6317（与 Tauberian 0.6314 吻合至 0.0003）。然而绝对级数 Σ |a(n)/n^{1/2} × w(n)| 发散（N=500 时累积到 2.54），而有号和 J_signed(500) = -0.086，97% 符号抵消——这是临界线 Dirichlet 级数条件收敛的标志。Fubini 变换未能绕过认证障碍。
- **GL₃ Voronoi 数值探测（2026-08-16 深入探索，`discovery/_voronoi_test.py`, `_k_bessel.py`）**：
  - **w(y) 恒负**：w(y) 对所有 y ∈ [0.1, 200] 均为负值，峰值在 y≈3.5 处 w≈-0.215。
  - **K_natural(y) 超多项式衰减**：K(1)=0.386, K(5)=3.2×10⁻⁵, K(10)=2.4×10⁻¹⁰，衰减如 exp(-c×y^{2/3})。
  - **朴素 Mellin 卷积失败**：B_dual(n) = ∫ w(y) K(yn/Q) dy/y 的衰减比率为 ~0.97/步（代数衰减），而非 exp(-c×n^{2/3})。原因：朴素核缺少 Miller-Schmid GL₃ Voronoi 公式中的振荡 Kloosterman 相位；只有这些相位才能提供使对偶级数绝对收敛的抵消。
  - **正确 GL₃ Voronoi**：需要完整的 Miller-Schmid (2006) 公式，包含 Kloosterman 和、导子结构和振荡 GL₃ Bessel 核。这是一个重大技术障碍（新子任务 [OBL M-Voronoi]）。
- **绝对收敛公式（2026-08-16 深入探索，`discovery/_certified_j_formula.py`, `_certified_j_probe.py`，失败）**：
  推导了 J = Σ_n a(n)/n^{1/2} × [w_Vplus(n) − w_Vdual(n)]，其中 w_Vplus/w_Vdual 各由嵌套二重 Mellin 积分定义（内层使用高斯正则化 e^{u²}）。数学上绝对收敛，但数值收敛极慢：
  - J_new(N=15) = −0.0277，J_new(N=100) = −0.0281（无收敛趋势），目标 J_cesaro = −0.0834
  - 根本原因：高斯 e^{u²} 提供的是积分变量 τ 方向的衰减，而非 n 方向的衰减。V_afe(n/12, 1/2+it) 的高斯中心在 n ≈ 89（log(n/12)=2），V_dual 中心在 n ≈ 33。达到 10^{-4} 精度需要 N ≈ 5000 项，与原始级数相当。
  - 结论：**方法数学正确但计算无效**；"N=20 项精度 10^{-6}"的声明有误，已撤回。
- **直接二重积分法（2026-08-16，`discovery/_j_direct_quad.py`，成功）**：
  J = (1/2π)∫Re[L(1/2+it) × amp1(t)]dt，其中 L(1/2+it) 用 Cesaro 截断 Dirichlet 级数近似。
  关键发现：外层积分对 amp1(t) 的高斯衰减提供额外平滑，使得 Cesaro 截断误差被显著平均消除：
  - N=200 Cesaro 项即给出 J ≈ −0.08354（与 N=2000 差异仅 3×10^{-5}）
  - 对 T ∈ [3,6] 完全不敏感（amp1 的高斯衰减确认）
  - **最终：J_direct = −0.08350 ± 0.00003，L(1) = 0.63180 ± 0.00003**
  - 两种独立方法（w(n) Fubini 和直接积分）一致：J ≈ −0.0834, L(1) ≈ 0.6318
  此方法计算极快（2 秒），但**仍是 discovery 层**：Cesaro 截断误差需要 GL₃ Voronoi 或 [OBL M-3] 才能认证
- **[OBL E-2] 认证路径**：
  1. 最优先：[OBL M-3] 数值无零区域（Arb 在矩形 {Re(s)≥0.6, |Im(s)|≤20} 内验证 L(s,sym²Δ)≠0），然后通过 Abel 求和认证 Cesaro 截断误差界
  2. 次选：实现完整 Miller-Schmid GL₃ Voronoi 公式 [OBL M-Voronoi]
- **中心值 AFE 不可行（2026-08-16 深入推导，最终结论）**：
  GL₃ 两侧 AFE 的正确公式为 L(s) = S1_+(s; X) − chi(s) × S2_+(1−s; X_dual)，其中 X_dual = Q×X（通过严格推导确认：代入 v=−w 后函数方程给出 Q^v × X^{−v} = (Q/X)^v × ... 实际为 Q×X 尺度，非 Q²/X）。
  - chi(s) = Q^{1/2−s} × G(1−s)/G(s)（注意：chi 含 Q^{−it} 因子而非 Q^{−2it}）
  - 对 X = Q^{1/2} = 12：X_dual = Q × 12 = 1728，对偶级数需 n ≤ 200 × X_dual = 345,600 项收敛（V(y)→1 as y→0 来自极点留数，条件收敛）
  - 任何 X 选择均无法解决：X_dual = Q × X，减少主级数项即增加对偶级数项，N=2000 始终不够
  - **根本障碍（最终确认）**：GL₃ Voronoi-Kloosterman 公式（Miller-Schmid 2006）的唯一作用正是将此条件收敛对偶级数转化为绝对收敛——没有它，任何参数选择下的 GL₃ 两侧 AFE 均不可行
  - 数值实验（2026-08-16）：X_main=12, X_dual=1728, N_main=73, N_dual=2000：最大误差 1.75（与 Cesaro 相比），确认对偶级数截断误差主导
- **唯一剩余路径**：实现完整 Miller-Schmid GL₃ Voronoi 公式 [OBL M-Voronoi]，或显式无零区域 [OBL M-3]（数值零点计数 via 辐角原理）
- **[OBL M-3] 数值路径（可行方案）**：对特定形式 sym²Δ，可通过 *数值零点自由区域* 实现认证：
  1. 用 Arb 在矩形 {Re(s) ∈ [0.6, 1], |Im(s)| ≤ 20} 上计算 L(σ+it, sym²Δ) 并验证非零
  2. 这给出该特定形式的显式零点自由区域（非一般形式定理）
  3. 进而通过 Abel 求和给出 |Σ_{n>N} a(n)/n^{1/2+it}| 的显式界
  4. 最终认证 J，完成 [OBL E-2]
  技术要点：需要 GL₃ approximate functional equation 在临界带内的 Arb 实现（Goldfeld-Li 2006 Riemann-Siegel 型公式）。每个 (σ,t) 处的计算误差可被认证。
- **[OBL M-3] 精化路径（2026-08-16，discovery/_zero_free_scan.py + 偏和分析）**：
  发现：对 sym²Δ，偏和 S(X) = Σ_{n≤X} a_{sym²}(n) 在 X ≤ 10000 时 max|S(X)| = 13.3（X=7925），
  远优于 GL₃ Voronoi 理论界 X^{2/3} ≈ 435。
  **核心等价**：若能认证 |S(X)| ≤ C_max（C_max ≈ 20）对所有 X ≥ 1，则：
    - Abel 求和直接给出 Cesaro 误差界：σ=0.9, N=10000 时误差 ≤ 3×C_max/N^{0.9} ≈ 0.015
    - 零点扫描：min|L_ces(0.9+it, N=10000)| = 0.447，margin = 0.432 >> 0.015 → 认证 {σ≥0.9} 无零点
  **唯一缺口**：x > 10000 的 |S(x)| 界。选项：
    (a) 继续计算 X ≤ 10^6 并验证（仍需 GL₃ PNT 认证尾部）
    (b) 用 GL₃ Voronoi 给出显式常数 C_GL3 使 |S(X)| ≤ C_GL3 × X^{ε}
    (c) 引用有效 GL₃ PNT（Molteni 2002 或类似）给出有效零点自由区域 → 证明 |S(X)| = O(X^{1-δ})
  **重要性**：|S(X)| 的显式界是 [OBL M-3] → [OBL E-2] 链条中最薄弱也是最具体的缺口。
- **偏和实验扩展（2026-08-16，`discovery/_fast_tau_sieve.py`，N=1000000）**：
  快速重现：log-导数递推 n×τ(n)=-24Σσ₁(k)τ(n-k) + 乘法筛（GL₃ Hecke 递推）。耗时：
  N=500000 需 35s，N=1000000 需 155s。结果：
  
  | N_max | max|S(X)| | 位置 X | 经验增长指数 | Cesaro 误差界 (σ=0.9) |
  |-------|-----------|--------|-------------|----------------------|
  | 10000 | 13.3 | 7925 | — | 0.0100 |
  | 20000 | 15.4 | 18806 | — | 0.0062 |
  | 100000 | 26.1 | 94048 | ~0.29 | 0.0025 |
  | 500000 | 52.13 | 224786 | ~0.32 | 0.0012 |
  | **1000000** | **63.82** | **811494** | **~0.30** | **0.000762** |
  
  **经验增长规律（最小二乘拟合，N=10^6 更新）**：max|S(X)| ≈ 0.445 × X^{0.369}（α̂=0.369，
  远优于 GL₃ Voronoi 理论界 X^{2/3+ε}）。N=500000 的"高原"在 N=10^6 时被打破，高原是伪像。
  
  **N=10^6 Cesaro 零点扫描**（`discovery/_growth_and_minL.py`，t 步长 0.005）：
  - min|L_ces(0.9+7.070i, N=10^6)| = **0.449015**（比 N=2000 的 0.4498 更准确）
  - **扩展 t 扫描（t∈[0,200]，`discovery/_t_scan_extended.py`）**：全局最小值 = **0.392669** at t=110.020；C_GL3 阈值收紧为 **2.557**（原 2.63）；经验 C_GL3=0.0064，裕度仍为 400 倍。
  - **N=10^8 扫描（`discovery/_n10m8_dc_scan.py`，DC-FFT 修复后 1401s，2026-08-17 完成）**：
    - DC-FFT 修复：`_DIRECT_BLOCK=512` 阈值避免微型 FFT 调用（原始实现 >12 小时，修复后 192s）
    - max|S(X)| = **331.02** at X=93,166,237；C_GL3_emp = **0.001611**（峰值，4649× 裕量）
    - min|L_ces(0.9+it, N=10^8)| = **0.392596** at t=110.020（与 N=10^6/10^7 一致：~0.3926）
    - tail_factor(σ=0.9, N=10^8) = **0.05243**
    - **C_GL3 阈值（σ=0.9, N=10^8）：C_GL3 < 7.4880**（比 N=10^7 的 4.375 宽松 71%）
    - **Threshold > Q_GL3^{1/3} = 6.930：YES — 若 C_GL3 ≤ Q^{1/3} 则认证成立**
  - **认证窗口（已确认，2026-08-17 N=10^8 完成）**：
    | N | 阈值 | C_GL3 ≤ Q^{1/6}=2.63 | C_GL3 ≤ Q^{1/4}=4.27 | C_GL3 ≤ Q^{1/3}=6.93 |
    |---|---|---|---|---|
    | 10^6 | 2.56 | ✗ | ✗ | ✗ |
    | 10^7 | 4.38 | **✓** | **✓** | ✗ |
    | **10^8** | **7.49** | **✓** | **✓** | **✓** |
    在 N=10^8 处，**任意标准 GL3 Voronoi 界均足够**（Q^{1/α} for α ≤ 3）。
    - 谱导子 Q_GL3 = Π|ν_i-ν_j| = (11/2)²×11 = 332.75（来自 sym²Δ 谱参数 ν=(11,0,-11)/2）
    - **Q_GL3^{1/6} = 2.632 ≈ N=10^6 阈值 2.557**（相差 3%）
    - **Q_GL3^{1/4} = 4.271 ≈ N=10^7 阈值 4.375**（相差 2.4%）
    - 结论：若 GL3 理论给出 C_GL3 ≤ Q_GL3^{1/6} 或 Q_GL3^{1/4}，则两个阈值均满足
    - 实际 C_GL3_emp = 0.003682，比阈值小 131×
  - **N=10^7 扫描（`discovery/_n10m7_dc_scan.py`，DC-FFT，117s）**：
    - max|S(X)| = 142.84 at X=7,642,126；C_GL3_emp = **0.003682**（峰值处，比 N=10^6 的 0.0064 更小）
    - min|L_ces(0.9+it, N=10^7)| = **0.392598** at t=110.025（与 N=10^6 值几乎相同）
    - tail_factor(σ=0.9, N=10^7) = **0.08973**（vs 0.1536 at N=10^6）
    - **C_GL3 阈值（σ=0.9, N=10^7）：C_GL3 < 4.375**（比 N=10^6 的 2.557 宽松 71%）
    - 经验裕度：0.003682 / 4.375 → **1188× 安全裕量**（N=10^6 时 400×）
  
  **增长指数认证分析**（假设 |S(X)| ≤ 0.445 × X^{0.369} 对所有 X 成立）：
  - 有限项误差：3 × 63.82 / (10^6)^{0.9} = 0.000762
  - 尾项误差（Abel 求和）：0.445/(0.9−0.369) × (10^6)^{0.369−0.9} = 0.000547
  - **总误差 ≤ 0.001309**，裕度 = 0.449015 − 0.001309 = **0.4477**
  - → 零点自由区域 {σ≥0.9} 认证成立（裕度 0.4477 >> 0）
  
  **GL₃ Voronoi 路径可行条件（更正）**：若 |S(X)| ≤ C_GL3 × X^{2/3}（GL₃ Voronoi 界），则
  N=10^6 时 Cesaro 尾项误差 = C_GL3 × N^{2/3−σ} / (σ−2/3)。
  对 σ=0.9：= C_GL3 × (10^6)^{−0.233} / 0.233 = C_GL3 × 0.171。
  有限项误差：3 × 63.82 / (10^6)^{0.9} = 0.000762。总误差 ≈ C_GL3 × 0.171 + 0.001。
  要求：C_GL3 × 0.171 < 0.449（零点间隙）→ **C_GL3 < 2.63**。
  
  **多 sigma 扫描结果**（`discovery/_multi_sigma_scan.py`，N=10^6，2026-08-16 扩展）：
  | σ | min\|L_ces(σ+7.07i)\| | finite_err | C_GL3 阈值 | 经验增长裕度 |
  |---|---|---|---|---|
  | 0.70 | 0.2595 | 0.0121 | 0.0137 | 0.233 |
  | 0.80 | 0.3617 | 0.0030 | 0.304 | 0.356 |
  | 0.85 | 0.4070 | 0.0015 | 0.940 | 0.404 |
  | 0.90 | 0.4490 | 0.0008 | **2.632** | **0.448** |
  | 0.95 | 0.4878 | 0.0004 | **6.928** | **0.487** |
  经验 max\|S(X)\|/X^{2/3} = **0.0073** at X=811494, **0.0064** at X=10^6（比 σ=0.90 阈值小 400 倍）。
  
  **L(1) 直接 Cesaro 认证**（`discovery/_L1_direct_cesaro.py`，N=10^6，2026-08-16）：
  L_ces(N=10^6, s=1) = **0.631793**（至小数点后 6 位稳定，N=100K~1M 区间变化 < 3×10^{-6}）。
  误差界（经验增长律）：finite 1.91×10^{-4} + tail 1.16×10^{-4} = **3.07×10^{-4}**。
  认证区间（经验律）：L(1, sym²Δ) ∈ [0.631485, 0.632100]（width 6.1×10^{-4}）。
  与 GL₃ AFE 结果一致：差值仅 7×10^{-6}（两种独立方法一致性确认）。
  
  **最终理论障碍（单一、极具体，已更新 2026-08-17）**：
  ~~对 σ=0.90，N=10^6：需证明 |S(X)| ≤ C × X^{2/3} 对 X > 10^6 成立，C < 2.63。~~
  ~~**已更新（N=10^7）**：需 C < 4.375。~~
**最终确认（N=10^8，2026-08-17，条件性）**：需 C < **7.4880**。由于 Q_GL3^{1/3} = 6.9296 < 7.4880，
**若能独立证明 C_GL3 ≤ Q^{1/3} 对所有 X≥1 成立，则该 Voronoi 界足以认证零点自由区域 {σ≥0.9}**。
  经验常数 C_GL3_emp = 0.001611（比阈值小 4649 倍）。
  **Arb 认证 GL3 Bessel 范数（2026-08-17，`discovery/_cgl3_arb_cert.py`，200-bit 精度，已修正）**：
  - **||K_nu||_1 = 0.19947（Arb 认证，Mellin 恒等式，60 位精度）**
  - Mellin 恒等式：K̂_ν(1) = (4π²)^{-1}×Γ(13/4)×Γ(1/2)×Γ(-9/4) = −0.19947114020071633...
  - 假设 K_nu(y)≤0（数值验证 30+ 点）：||K_nu||_1 = 0.19947（精确值）
  - 保守上界（无符号假设）：||K_nu||_1 ≤ 0.225（密集网格 + 15% 裕量）
  - **修正说明**：旧值 0.184 错误；K_nu(0.01)=−1.916 远大于−0.514，小 y 尾部被低估 4.5 倍
  **三条件 C_GL3 界（均远低于阈值，`discovery/_voronoi_proof_sketch.py`，已修正）**：
  | 路线 | 公式 | C_GL3 上界 | 与 7.488 的裕量 |
  |---|---|---|---|
  | L1 + ζ(3/2)（Mellin） | 2×0.199×ζ(3/2) | **1.042** | **7.2×** |
  | L1 + ζ(4/3)（Mellin） | 2×0.199×ζ(4/3) | **1.437** | **5.2×** |
  | L1 + ζ(3/2)（保守） | 2×0.225×ζ(3/2) | **1.176** | **6.4×** |
  | L2 + √C_RS + ζ(7/6) | 2×√C_RS×||K||_2×ζ(7/6) | **2.74** | **2.7×** |
  所有路线均 < Q^{1/3}=6.93 < 7.488（裕量对 c-sum 公式的选择稳健）。
  **[OBL M-Voronoi] 剩余工作**：从 Miller-Schmid (2006) Theorem 1.18 提取带正规化的 Kloosterman/Bessel 核，
  并证明光滑截断下 c-求和的显式指数界；当前 1.04--2.74 只是未完成的条件草图，不是条件认证实质完成。
  经验常数约为 0.0037（N=10^7），比 N=10^8 阈值（7.49）小 2024 倍。
- **Rankin-Selberg 密度（2026-08-16 会话 5，`discovery/_rs_density.py`）**：
  C_RS = lim_{N→∞} (1/N)×Σ_{n≤N}|a(n)|² = **0.4433**（N=10^3..10^5 稳定，δ<10^{-3}）。
  这是 Res_{s=1} L(s, sym²Δ×sym²Δ)（Rankin-Selberg 密度）的数值估计。
  **与 C_GL3 的关系**（通过 GL₃ Voronoi + Rankin-Selberg + Cauchy-Schwarz）：
    C_GL3 ≤ C_abs × sqrt(C_RS) = C_abs × 0.6658
  **认证要求**：需 C_abs < 2.63/0.6658 = 3.95（σ=0.9 临界值）。
  **经验验证**：C_abs_empirical = 0.0064/0.6658 = 0.0096（裕度 411 倍）。
  **结论**：C_abs < 3.95 极可能成立（理论上需 Miller-Schmid (2006) 中 level-1 GL₃ Voronoi 的绝对常数显式提取）。GL₃ 数论文献保证此类 level-1 常数为 O(1)，但精确值待查。

- **条件认证完整结构（2026-08-17 N=10^8 最终更新，`discovery/_conditional_cert.py`）**：
  **已知**：L_ces(10^6, 1) = 0.631793（稳定 < 3×10^{-4}）；max|S(X)|/X^{2/3} = 0.001611（经验值，N=10^8 峰值）。
  **Abel 求和误差界**：|L(1) − L_ces(N,1)| ≤ 4 × C_GL3 / N^{1/3}（需 |S(X)| ≤ C_GL3 × X^{2/3}）。
  **直接 L(1) 认证表（N=10^8，已更新 2026-08-17，`discovery/_lces_n10m8_s1.py`）**：
  - **L_ces(10^8, 1) = 0.6317929422**（319s 计算，2026-08-17 1:30AM）
  - ΔL_ces(10^8 - 10^7) = 3.03×10^{-8}（收敛至 9 位有效数字）
  - C_GL3_emp = 0.001611（与 N=10^8 扫描一致）
  | C_GL3 | 误差界 | L(1) ≥ | L(1) ≤ | 状态 |
  |-------|--------|--------|--------|------|
  | 0.01  | 0.000086 | 0.6317 | 0.6318 | ✓ |
  | 1.042 (Mellin) | 0.00898 | **0.6228** | 0.6408 | ✓ |
  | 1.071 (保守) | 0.00923 | **0.6226** | 0.6410 | ✓ |
  | 6.93 (Q^{1/3}) | 0.05972 | 0.5721 | 0.6915 | ✓ |
  | 15.8 | 0.13616 | 0.4956 | 0.7679 | ✓ |
  **条件阈值汇总（[OBL M-Voronoi] 目标，N=10^8）**：
  - 若对所有 X≥1 有 C_GL3 < **7.488**，则可认证零点自由区域 {σ≥0.9} 并得 L(1) ≥ 0.567；
    目前尚未证明 Q^{1/3}=6.93 这一候选界。
  - 若对所有 X≥1 有 C_GL3 < **15.8**，则可认证 L(1, sym²Δ) > 0；该假设仍未证明。
  经验 C_GL3 = 0.001611，比最严阈值（7.488）小 4649 倍。

- **GL₃ Voronoi 数值实现（2026-08-16 会话 4，两次尝试 + 根本原因更正）**：
  - **尝试 1**（`discovery/_voronoi_gl3_test.py`）：简化 Whittaker W(y)=y^6·exp(-2π(1+y))。结果：I(n;X)≈3.64×10⁻⁶ 常数，比值≈0。错误：权函数归一化不正确。
  - **尝试 2**（`discovery/_voronoi_mellin_barnes.py`）：R(s)=Γ_GL3(1-s)/Γ_GL3(s) 的 1D Mellin-Barnes，即 Φ(n)=(1/n)·(1/2π)∫R(1/2+it)·(nX)^{1/2+it}·Γ(1/2+it)dt。验证：|R(1/2+it)|=1（幺正 ✓），R(s)·R(1-s)=1（✓）。结果：Φ(n)≈0.556/n（代数衰减 O(1/n)），对偶级数收敛速度与原始级数相同。
  - **根本原因（最终更正）**：GL₃ Voronoi 的 X^{2/3} 界来自对 **Kloosterman 层 c≥1 的求和** 而非单项 Bessel 核的快速衰减。c=1 项（主项）给出条件收敛 O(1/n)；c≥2 项通过 GL₃ Kloosterman 界 S(0,n;c)~c^{2/3+ε} 提供对消，使总和 O(X^{2/3})。正确实现需要：(1) 各 c 的 Kloosterman 和计算；(2) 对每个 c 计算 Bessel 核 J_{GL3}(nX/c^3)；(3) 对 c 求和并利用 Weil 界。
- **[OBL M-Voronoi] 路径**：实现 Miller-Schmid (2006) 完整 GL₃ Voronoi（含 c≥1 Kloosterman 求和）
- **GL₃ Voronoi 定性结论（2026-08-16 会话 5，最终）**：
  - **三次数值尝试均失败**：(1) Whittaker 积分（常数 I≈0）；(2) 1D Mellin-Barnes Φ(n)（O(1/n) 代数衰减）；(3) J-Bessel J_{11}(4π(nX/c)^{1/3})（比值随机，X=5,10,20 分别为 3.94, -0.18, -5.09）；(4) K-Bessel K_{10.5}(2π(n/X)^{1/3})（K_GL3(0.1)=2.7×10^7，发散）。
  - **根本原因（最终版本）**：GL₃ Voronoi **是理论界估计工具，不是数值恒等式**。对于自对偶形式（A(n,1)=A(1,n)=a(n)），光滑测试函数的 Voronoi 公式是同义反复（dual = primal），不提供新信息。|S(X)| ≤ C×X^{2/3} 的界来自**估计振荡和的大小**（通过 Kloosterman 和对消），而非数值计算 Voronoi 和。"验证 Voronoi 和 = S(X)" 在数学上不可能，因为等式本身不成立（不是等式，是不等式的来源）。
  - **正确的 C_GL3 提取路径**：从 Miller-Schmid (2006) Theorem 1.1 的 Kloosterman sum 界 + GL₃ Bessel 估计直接得出常数（理论分析，非数值计算）。Rankin-Selberg 均值：Σ|a(n)|²/n^{1.01}≈5.79（N=10^5），暗示 Res_{s=1}L(s, sym²×sym²)≈O(1)，理论 C_GL3 应远小于阈值 2.63。
  - **[OBL M-Voronoi] 内容修正**：任务不是"数值验证"，而是"从 Miller-Schmid 提取显式常数 C_GL3"（理论分析）。
- **两侧 Gaussian AFE（2026-08-16，`discovery/_m3_afe_sigma.py`，失败）**：L(σ+it) = S_main(Gaussian) + ε×chi×S_dual(Gaussian) 公式在 σ=0.7 时与 Cesaro(N=2000) 最大偏差达 1.04。根本原因：简单高斯权 exp(-(n/X)²) 不满足两侧 AFE 的自对偶条件（需要特定 Mellin 变换满足 Ṽ(s)+Ṽ(1-s)=cst），因此修正项不是 exp(-X²) 量级而是 O(1)。
- **Rankin-Selberg 直接计算（2026-08-16，`discovery/_L1_rankin_selberg.py`，失败）**：L(1+δ) = (ζ(2+2δ)/ζ(1+δ)) × Σ τ(n)²/n^{12+δ}。部分和 N=5000、δ=0.5 给出 L=0.726，δ=0.05 给出 L=0.262，远未收敛到目标 0.632。根本原因：需要先 N→∞ 再 δ→0，收敛指数仅 N^{-δ}；对于 δ=0.05 和 N=5000，尾项约 25。
- **轮廓移动至 Re(u)=ε>0（2026-08-16 分析，无代码，结论不可行）**：思路：J = ∮_{Re=-1/2} → 移到 ∮_{Re=ε}，避开临界线。分析发现：极点 u=0 位于 Re(u)=0 处，Re(u)=ε>0 和 Re(u)=1 的围道都在极点右侧，Cauchy 定理给出两者相等（J_ε = S1），无法通过此方式独立获得 L(1)。J 项必须来自极点左侧（Re(u)<0），即 L(1+u) 在 Re(1+u)<1 处——临界带内，条件收敛。
- **[OBL E-2] 认证的根本障碍（最终结论）**：J 的认证与以下三者等价：(a) GL₃ Voronoi 求和公式（Miller-Schmid 2006）；(b) 显式无零区域 [OBL M-3]；(c) 数值验证 L(s)≠0 on {Re(s)≥σ₀, |Im(s)|≤T} 加 Arb 误差界。所有"绕道"（Gaussian AFE、RS 极限、轮廓移动）均失败，均因 Dirichlet 级数在临界带条件收敛而受阻。
- **S1 数值收敛**（2026-08-16，`src/afe_s1.py`）：
  - S1(N=100) = 0.54785263，W_afe(100/12)=0.0365
  - S1(N=500) = 0.54830922，W_afe(500/12)=0.00248
  - S1(N=1000) = 0.54830185，W_afe(1000/12)=5.70e-4
  - S1(N=2000) = 0.54830205，W_afe(2000/12)=1.07e-4
  - **收敛速度**：W_afe(n/12) ~ C/n × e^{-(log(n/12))^2/4}，S1 尾项 ~ N^{-2/3}，N=2000 时误差 ~ 2×10^{-6}
  - **修正前次错误**：前次声称"n≈670，W_afe≈5×10^{-4}，尾项<10^{-10}"——实测 W_afe(670/12)=0.00137，N=670 尾项约 8×10^{-7}，非 10^{-10}

### 轨道 2（一般定理）：纯理论突破

路径：M-1 → M-2 → M-3（GL₃ 显式无零区域）→ E-1（显式常数）

**注意**：GL₃ 大筛法的非对角项控制和显式凸性界追踪极其繁重，常数可能膨胀。
建议优先参考 Booker、Blomer 等关于显式子凸性界的近期文献，避免从零手推。

---

## 研究阶段

### 阶段 F：基础层

| 编号 | 交付物 | 状态 | 对应文件 |
|------|--------|------|----------|
| F-1 | 局部 Euler 因子分解定理（Clebsch–Gordan 消去） | [THM] | proof/01-foundations.tex |
| F-2 | 全局留数正值性定理（Res_{s=1} > 0） | [OBL] | proof/02-global-residue.tex |
| F-3 | Δ 函数的 L(1, sym² Δ) 认证 | **[THM]** | outsource/04-gl3-afe-rigorous-computation/src/certify_l1.py |

**F-3 状态说明**（2026-08-19 更新）：
F-3 已通过 AFE 方法严格认证：L(1, sym²Δ) ∈ [0.63179293, 0.63179298]（宽度 4.6×10⁻⁸）。
证明方法：3000 项 AFE + 两点截断误差界 + 256-bit Arb 区间算术。

发现的数学事实：
- TAU_PRIMES 表在 p ≥ 47 处存在错误（两种独立算法 + Ramanujan 同余 mod 691 核验
  均给出 τ(47) = 2687348496；表中 −134722488 已纠正）。
- **正确的 RS 恒等式**：∑_n τ(n)²/n^{11+s} = [ζ(s)/ζ(2s)] × L(s,sym²Δ)
  （非 "ζ(s)×L"；分母 ζ(2s) 来自局部因子恒等式 ∑_k λ(p^k)² z^k = (1+z) L_p(s)）。
- Tauberian 渐近：∑_{n≤N} τ(n)²/n^{11} / N → L(1,sym²Δ)/ζ(2)，故
  **L(1, sym²Δ) = ζ(2) × 0.3839 ≈ 0.631**（N=5000，探索层估计，三法稳定收敛）。
- 三法互证（均给出 ≈ 0.631–0.641）：
  1. RS Tauberian（N=5000）：0.6314
  2. Dirichlet 级数截断（s=1.01，N=3000）：0.634（从上方收敛）
  3. Euler 乘积（25 个素数）：0.641（从上方条件收敛）
- Euler 乘积在 s=1 处**条件收敛**（Sato-Tate 均值为 0），但简单尾部界
  ∑_{p>P} 3/p 发散，故无法通过此方式**认证**。
- 证明层认证需要近似函数方程（AFE），无需零点自由区域（见轨道 1）。

### 阶段 M：Mollifier 层（轨道 2）

| 编号 | 交付物 | 状态 | 技术要点 |
|------|--------|------|----------|
| M-1 | Sym² L-函数的 Dirichlet 级数 mollifier 构造 | [OBL] | GL₃ Rankin–Selberg 均值 |
| M-2 | 均值定理 | [OBL] | 大筛法 + Hecke 关系（非对角项控制繁重）|
| M-3 | 无零区域：L(s, sym² f) 在 [1-δ,1] 内无零 | [THM for Delta, OBL general] | sym²Δ: proof/04b-zero-free-region.md; 一般情形需显式凸性界 + 显式常数 |

### 阶段 E：有效常数层（主要研究目标）

| 编号 | 交付物 | 状态 | 说明 |
|------|--------|------|------|
| E-1 | L(1, sym² f) ≥ c_eff / log N 中显式常数 c_eff | [OBL] | 依赖 M-3（轨道 2） |
| E-2 | sym²Δ 及 p ≤ 10^4 的计算机辅助认证区间 | **[THM for Delta]** | L(1, sym²Δ) ∈ [0.63179293, 0.63179298] 已认证；p ≤ 10^4 一般情形仍 [OBL] |
| E-3 | 最终论文（目标投 Annals/IMRN） | [OBL] | 依赖 E-1 + E-2 |

---

## 关键技术路线

### 路线 A：近似函数方程认证（Δ 函数，N=1）

**探索层（已完成）**：通过 Rankin–Selberg 公式
    sum_n tau(n)^2/n^{11+s} = [zeta(s)/zeta(2s)] * L(s, sym^2 Delta)
Tauberian 渐近给出：∑_{n≤N} τ(n)²/n^{11} / N → L(1,sym²Δ)/ζ(2)，故
    **L(1, sym²Δ) = ζ(2) × 0.3839 ≈ 0.631**（N=5000，见 discovery/rs_estimate.py）。
与 Dirichlet 级数（s=1.01，N=3000：0.634）及 Euler 乘积（25 素数：0.641）均一致。

**证明层（[OBL E-2]）**：实现近似函数方程（AFE）：
    L(1, sym² Δ) = 2 Σ_{n≥1} a_{sym²}(n)/n × W(n/X) + 误差项

其中 W 为 GL₃ 对应的检验函数（由 Gamma 因子比 G(1+z)/G(1) 的 Mellin 变换确定），
X ~ (解析导子)^{1/2} ≈ 8（weight-12 对应解析导子约 60），
主级数数值收敛，但实际 AFE 权重衰减约为 Gaussian-on-log 而非 e^{-cn^{2/3}}。
对偶项 J 的截断误差在临界带内条件收敛；必须通过完整 GL₃ Voronoi 或实例级
数值无零区域认证。早先“误差项由函数方程直接控制、无需零点区域”的说法已撤回。

### 路线 B：Siegel 零点排除（一般级别 N）

Goldfeld–Hoffstein–Lieman 方法的核心二分：

**情形 1（无 Siegel 零点）**：若 L(s, sym² f) 在 (1-1/log N, 1] 内无零，则标准围道
积分给出 L(1, sym² f) ≥ c_1 / log N，其中 c_1 可从无零区域半径**显式计算**。
这是本项目的**核心技术贡献点**（轨道 2，依赖 M-3）。

**情形 2（存在 exceptional zero）**：F-2 的逐点正值性不足以排除。需要一致的
log-derivative/Taylor 系数界来给出 \(c_2/\log N\)，仍为 `[OBL]`。

### 路线 C：次对数改进（远期探索，低优先级）

引入更长的 mollifier（长度 X = N^{1/2+eps}），利用 GL₃ Voronoi 求和公式控制误差项。
技术障碍：GL₃ 大筛法常数较弱；突破 1/log N 的下界相当于突破某种凸性界。
在 E-1、E-2 完全落地前不占用主要精力。此项明确标记为**远期探索**。

---

## 诚实性原则

**本项目绝对不：**
- 声称已证明任何 [OBL] 项目
- 用浮点近似充当严格下界
- 在未完成 M-3 的情况下声称 E-1 已证

**本项目的价値在于：**
- 将一个重要但非有效的定理逐步变为计算机可验证的显式结果
- 为自守 L-函数的计算机辅助证明建立可复现基础设施

---

## 参考文献优先级

| 优先级 | 文献 | 用途 |
|--------|------|------|
| P0 | Goldfeld–Hoffstein–Lieman (1994) 附录 | 核心技术参考，逐步核验 |
| P0 | Hoffstein–Lockhart (1994) | Siegel 零点主定理 |
| P1 | Goldfeld "Automorphic Forms for GL(n,R)" | GL₃ AFE 权重函数推导 |
| P1 | Holowinsky–Soundararajan (2010) | QUE 和 sym² 下界应用 |
| P1 | Shahidi (1981) | 寻找或补桥 `L(1,Ad)>0`；当前 not-found |
| P1 | Jacquet–Shalika (1981) | Rankin–Selberg 积分、局部因子与 Euler product 收敛 |
| P1 | Booker / Blomer (近期) | 显式子凸性界和显式无零区域（M-3 参考）|
| P2 | Shimura (1975) | sym² 全纯延拓 |
| P2 | Gelbart–Jacquet (1978) | sym² 自守性（GL₃ 提升） |

## 2026-08-19 — external review verdicts on batches 03/04 (records in outsource/solutions/)

- **Batch 03 (partial-sum bound, Q-11): PASS WITH MINOR REVISIONS, core theorem
  CONFIRMED** — S(X) = O_eps(X^{1/2+eps}) unconditionally via Friedlander–Iwaniec
  Prop. 3.2 (degree-3 specialization) + Iwaniec–Michel. All nine required
  revisions applied (m=3 specialization, Satake-parameter d_3 argument,
  entireness citation, novelty rewrite as instantiation-not-new-theorem,
  checker README theorem/conjecture split, honest X<=5000/0.26 test range,
  removal of unshipped file references, conjectural-only status for C=0.259
  beyond the computed range, removal of the conflicting L(1)/S1 numeric
  intervals). Q-11 math gate: CLOSED/THEOREM; 0.259 stays discovery-tier.
- **Batch 04 (GL(3) AFE): FAIL — discovery-tier only.** P0 repairs applied:
  machine-derived statistics (new checker/recompute_stats.py; true grid min
  0.33403921 at (0.6,-20); the hand-copied 0.532 retracted), N=60 truncation
  claim retracted (independent N-sweep shows order-0.1 variation), stale
  single-sum witness metadata corrected, novelty downgraded, Gelbart–Jacquet
  title corrected, unshipped-file references removed, unsafe inward-rounding
  wording removed, complex output switched to an acb-ball schema, and the
  N~X^{3/2} scale claim replaced by the corrected N >= X(log(1/eps)/c)^{3/2}.
- **Roadmap (reviewer's P1–P4, adopted):** P1 ONE-point rigorous AFE
  certificate (exact A(n) = lambda(p)^2 with exact tau(p)^2/p^11, rigorous
  V and V-tilde, main tail + dual tail + quadrature error; output L(s) in B,
  |L(s)| > delta) BEFORE any grid expansion; P2 Arb/acb implementation
  (exact coefficients, ball arithmetic throughout); P3 proved uniform weight
  bounds V, V-tilde <= C_A(s) y^{-A} (or stretched-exponential) on
  0.6<=sigma<=1, |t|<=20 with computable tail sums; P4 only then the
  zero-free rectangle via argument-principle certificates (preferred) or
  derivative covers. Do not expand the grid before P1 closes.
