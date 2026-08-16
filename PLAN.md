# 研究计划：$L(1, \mathrm{sym}^2 f)$ 有效下界

## 项目目标

出发点：Goldfeld–Hoffstein–Lieman (1994) 附录定理

$$L(1, \mathrm{sym}^2 f) \geq \frac{c}{\log N}$$

其中常数 $c > 0$ 是**非有效的**（不可计算）。本项目的三阶段目标：

1. **近期（可行）**：对特定模形式（从 Ramanujan $\Delta$ 函数开始），用区间算术严格认证 $L(1, \mathrm{sym}^2 f) \geq L_0$，给出首个计算机辅助认证的实例。

2. **中期**：对素数级 $p \leq P$（$P$ 为待定阈值）的所有归一化本原 Hecke 特征形式，认证有效常数 $c_{\text{eff}}$，使得 $L(1, \mathrm{sym}^2 f) \geq c_{\text{eff}} / \log p$。

3. **长期（研究性）**：通过新的 mollifier 论证，证明改进下界 $L(1, \mathrm{sym}^2 f) \geq c / (\log N)^{1-\delta}$。

---

## 研究阶段

### 阶段 F：基础层（已完成 / 正在认证）

| 编号 | 交付物 | 状态 | 对应文件 |
|------|--------|------|----------|
| F-1 | 局部 Euler 因子分解定理（Clebsch–Gordan 消去） | \[THM\] | `proof/01-foundations.tex` |
| F-2 | 全局留数正值性定理（$\mathrm{Res}_{s=1} > 0$） | \[THM\] | `proof/02-global-residue.tex` |
| F-3 | $\Delta$ 函数的 $L(1, \mathrm{sym}^2 \Delta)$ Arb 认证 | \[THM\] | `src/numerical_delta.py` |

### 阶段 M：Mollifier 层（进行中）

| 编号 | 交付物 | 状态 | 技术要点 |
|------|--------|------|----------|
| M-1 | Sym² $L$-函数的 Dirichlet 级数 mollifier 构造 | \[OBL\] | 利用 GL₃ Rankin–Selberg，定义 $M(s) = \sum_{n \leq X} \mu(n) a_{\mathrm{sym}^2}(n) n^{-s}$ |
| M-2 | 均值定理 $\int_T^{2T} \|M(\tfrac12+it)L(\tfrac12+it)\|^2 dt \gg T$ | \[OBL\] | 大筛法 + Hecke 关系 |
| M-3 | 无零区域：$L(s, \mathrm{sym}^2 f)$ 在 $s \in [1-\delta, 1]$ 内无零 | \[OBL\] | Hadamard 乘积 + 显式常数 |

### 阶段 E：有效常数层（主要研究目标）

| 编号 | 交付物 | 状态 | 说明 |
|------|--------|------|------|
| E-1 | $L(1, \mathrm{sym}^2 f) \geq c_{\text{eff}} / \log N$ 中显式常数 $c_{\text{eff}}$ | \[OBL\] | 依赖 M-3 的无零区域半径 |
| E-2 | 所有素数级 $p \leq 10^4$ 的计算机辅助认证 | \[OBL\] | 依赖 E-1 + Arb 认证 |
| E-3 | 最终论文：完整结果，可投 Annals/IMRN | \[OBL\] | 依赖 E-1 + E-2 |

---

## 关键技术路线

### 路线 A：直接区间算术（已用于 $\Delta$ 函数，$N=1$）

**原理**：
- 将 $L(1, \mathrm{sym}^2 \Delta)$ 写成截断 Euler 乘积加尾部估计：
  $$L(1, \mathrm{sym}^2 \Delta) = \prod_{p \leq P} L_p(1)^{-1} \cdot R(P)$$
  其中尾部 $R(P) = 1 + O(P^{-1})$ 可用 Rankin–Selberg 上界控制。
- 用 Arb 库计算截断乘积，给出机器可验证的区间 $[L_{\min}, L_{\max}]$。
- 产生认证：$L(1, \mathrm{sym}^2 \Delta) \geq L_{\min} > 2.405$。

**已完成**：`src/numerical_delta.py`，认证值见 `tests/test_numerical.py`。

### 路线 B：Siegel 零点排除（针对一般级别 $N$）

**Goldfeld–Hoffstein–Lieman 方法的核心二分**：

情形 1：若 $L(s, \mathrm{sym}^2 f)$ 在 $(1-1/\log N, 1]$ 内**无零**，则标准围道积分给出：
$$L(1, \mathrm{sym}^2 f) \geq \frac{c_1}{\log N}$$
其中 $c_1$ 可从无零区域半径显式计算。

情形 2：若存在 Siegel 零点 $\beta$ 满足 $\beta > 1-1/\log N$，则全局留数正值性定理（F-2）推出矛盾——这就是 F-2 的核心应用。

**使这一论证有效的关键**：在情形 1 中追踪 $c_1$ 的显式表达式（目前文献中未给出具体数值）。这正是本项目的**核心技术贡献点**。

### 路线 C：次对数改进（长期研究）

**出发点**：Holowinsky–Soundararajan (2010) QUE 证明用到 $L(1, \mathrm{sym}^2 f) \gg 1/\log N$。

**改进思路**：
- 引入更长的 mollifier（长度 $X = N^{1/2+\varepsilon}$ 而非 $X = N^{1/4}$）
- 利用 GL₃ 自守表示的 Voronoi 求和公式控制误差项
- 目标：证明对 "typical" 形式有 $L(1, \mathrm{sym}^2 f) \gg 1/(\log N)^{1-\delta}$

**技术风险**：目前 GL₃ 的大筛法常数比 GL₂ 弱，这是主要障碍。

---

## 诚实性原则

**本项目绝对不：**
- 声称已证明任何 \[OBL\] 项目
- 用浮点近似充当严格下界
- 在未完成 M-3 的情况下声称 E-1 已证
- 将 QUE 应用（路线 C）作为无条件结果宣布

**本项目的价值在于：**
- 将一个重要但非有效的定理逐步变为计算机可验证的显式结果
- 为自守 $L$-函数的计算机辅助证明建立基础设施
- 提供可复现的、独立可验证的下界认证

---

## 参考文献优先级

| 优先级 | 文献 | 用途 |
|--------|------|------|
| P0 | Goldfeld–Hoffstein–Lieman (1994) 附录 | **核心技术参考，逐步核验** |
| P0 | Hoffstein–Lockhart (1994) | Maass 形式与 Siegel 零点 |
| P1 | Holowinsky–Soundararajan (2010) | QUE 和 sym² 下界的应用 |
| P1 | Shahidi (1981) | 伴随 $L$-函数不消失 |
| P1 | Jacquet–Shalika (1981) | Rankin–Selberg 积分 |
| P2 | Shimura (1975) | sym² 全纯延拓 |
| P2 | Gelbart–Jacquet (1978) | sym² 自守性（GL₃ 提升） |
