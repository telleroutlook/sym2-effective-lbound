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

## 研究阶段

### 阶段 F：基础层

| 编号 | 交付物 | 状态 | 对应文件 |
|------|--------|------|----------|
| F-1 | 局部 Euler 因子分解定理（Clebsch–Gordan 消去） | [THM] | proof/01-foundations.tex |
| F-2 | 全局留数正值性定理（Res_{s=1} > 0） | [THM] | proof/02-global-residue.tex |
| F-3 | Δ 函数的 L(1, sym² Δ) 认证 | [OBL] | discovery/rs_estimate.py |

**F-3 状态说明**（2026-08-16 更新）：
前版本将 F-3 标为 [THM]，声称通过截断 Euler 乘积认证
L(1,sym²Δ) ∈ [2.405,2.407]。**此结论已撤回**。

发现的数学事实：
- GL₃ L-函数在 s=1 处的 Euler 乘积 ∏_p L_p(1,sym²Δ)^{-1} 不收敛到 L(1)，
  它因 ∏_p(1−1/p) → 0 分量而**趋近于零**（而非趋近 L(1)）。
- TAU_PRIMES 表在 p ≥ 47 处存在错误（两种独立算法 + Ramanujan 同余 mod 691 核验
  均给出 τ(47) = 2687348496；表中 −134722488 已纠正）。
- 正确方法：Rankin–Selberg 公式
  ∑_{n≤N} τ(n)²/n^{11} / N → L(1, sym²Δ)（Tauberian 渐近）。
  N=5000 处的探索层估计：**L(1, sym²Δ) ≈ 0.3839**。
- 证明层认证需要近似函数方程（AFE），见 [OBL F-3 / OBL E-2]。

### 阶段 M：Mollifier 层（进行中）

| 编号 | 交付物 | 状态 | 技术要点 |
|------|--------|------|----------|
| M-1 | Sym² L-函数的 Dirichlet 级数 mollifier 构造 | [OBL] | GL₃ Rankin–Selberg 均值 |
| M-2 | 均值定理 | [OBL] | 大筛法 + Hecke 关系 |
| M-3 | 无零区域：L(s, sym² f) 在 [1-δ,1] 内无零 | [OBL] | Hadamard 乘积 + 显式常数 |

### 阶段 E：有效常数层（主要研究目标）

| 编号 | 交付物 | 状态 | 说明 |
|------|--------|------|------|
| E-1 | L(1, sym² f) ≥ c_eff / log N 中显式常数 c_eff | [OBL] | 依赖 M-3 的无零区域半径 |
| E-2 | 素数级 p ≤ 10⁴ 的计算机辅助认证 | [OBL] | 依赖 E-1 + Arb 认证 |
| E-3 | 最终论文（目标投 Annals/IMRN） | [OBL] | 依赖 E-1 + E-2 |

---

## 关键技术路线

### 路线 A：近似函数方程认证（Δ 函数，N=1）

**探索层（已完成）**：通过 Rankin–Selberg 公式
    L(1, sym² Δ) = lim_{N→∞} (∑_{n≤N} τ(n)²/n^{11}) / N
在 N=5000 处得到 L(1, sym²Δ) ≈ 0.3839（见 discovery/rs_estimate.py）。

**证明层（[OBL]）**：需要实现近似函数方程（AFE）。AFE 给出
    L(1, sym² Δ) = 2 ∑_{n≤X} τ(n)²/n^{11} × W(n/X) + (小尾部误差)
其中 W 是适当的检验函数，X ~ (conductor)^{1/2}，误差项可用 Arb 区间算术认证。

### 路线 B：Siegel 零点排除（一般级别 N）

Goldfeld–Hoffstein–Lieman 方法的核心二分：

**情形 1（无 Siegel 零点）**：若 L(s, sym² f) 在 (1-1/log N, 1] 内无零，则标准围道
积分给出 L(1, sym² f) ≥ c_1 / log N，其中 c_1 可从无零区域半径**显式计算**。
这是本项目的**核心技术贡献点**。

**情形 2（存在 Siegel 零点）**：全局留数正值性定理（F-2）排除此情形。

### 路线 C：次对数改进（长期研究）

引入更长的 mollifier（长度 X = N^{1/2+eps}），利用 GL₃ Voronoi 求和公式控制误差项。
技术障碍：GL₃ 大筛法常数较弱。

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
| P1 | Holowinsky–Soundararajan (2010) | QUE 和 sym² 下界应用 |
| P1 | Shahidi (1981) | 伴随 L-函数不消失 |
| P1 | Jacquet–Shalika (1981) | Rankin–Selberg 积分 |
| P2 | Shimura (1975) | sym² 全纯延拓 |
| P2 | Gelbart–Jacquet (1978) | sym² 自守性（GL₃ 提升） |
