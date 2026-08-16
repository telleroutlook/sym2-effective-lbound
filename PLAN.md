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

### 阶段 F：基础层（已完成）

| 编号 | 交付物 | 状态 | 对应文件 |
|------|--------|------|----------|
| F-1 | 局部 Euler 因子分解定理（Clebsch–Gordan 消去） | [THM] | proof/01-foundations.tex |
| F-2 | 全局留数正值性定理（Res_{s=1} > 0） | [THM] | proof/02-global-residue.tex |
| F-3 | Δ 函数的 L(1, sym² Δ) Arb 认证 | [THM] | src/numerical_delta.py |

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

### 路线 A：直接区间算术（Δ 函数，N=1）

将 L(1, sym² Δ) 写为截断 Euler 乘积加尾部估计：

    L(1, sym² Δ) = prod_{p<=P} L_p(1)^{-1} * R(P),  R(P) = 1 + O(P^{-1})

用 Arb 区间算术计算截断乘积，给出认证区间 [L_min, L_max]。

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
