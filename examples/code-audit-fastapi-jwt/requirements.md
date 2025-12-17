# 📌 Code Audit Example

## FastAPI + JWT Multi-Tenant API (Minimal Slice)

> **This is a frozen requirement.**
> The implementation MUST follow this document strictly.
> No interpretation, no extension, no flexibility.

---

## 一、项目切片（Project Slice）

**项目名称**
FastAPI + JWT 的多租户接口设计（最小可运行示例）

**项目类型**
代码审计 / 工程决策验证

**示例目的**
回答一个**明确且不可回避的工程决策问题**：

> **tenant_id 的“唯一可信来源”应该来自哪里？**

该项目不是业务系统，不是完整产品，而是一个**用于验证工程决策正确性的最小切片**。

---

## 二、目标（Objective）

实现一个最小 FastAPI 服务，用来：

* 强制体现一个明确的工程决策
* 使该决策：

  * 可运行
  * 可审计
  * 可反驳
  * 可被证明正确或错误

本示例不追求“通用性”或“扩展性”。

---

## 三、必须完成的功能（Mandatory Requirements）

### 1）鉴权（Authentication）

* 必须使用 **JWT**
* 签名算法：`HS256`
* 必须在请求中校验 JWT 的合法性（签名 + 过期时间）

#### JWT Payload **必须**包含以下字段：

| 字段          | 含义      |
| ----------- | ------- |
| `sub`       | user_id |
| `tenant_id` | 当前租户 ID |
| `role`      | 用户角色    |

> ❗如果任一字段缺失，该 Token 必须被视为 **无效**。

---

### 2）API 接口（API Surface）

**只允许实现一个接口：**

```
GET /receipts
```

#### 行为要求：

* 返回当前租户下的收据列表
* 数据可使用：

  * 内存列表
  * 或 SQLite
* 必须清晰体现 **多租户隔离**

---

### 3）关键工程决策点（Critical Decision Point）

> **tenant_id 的来源必须只选一个，且必须在代码中强制体现。**

你必须在以下方案中 **二选一**：

* ✅ tenant_id **只来自 JWT**
* ❌ tenant_id **只来自请求参数 / Header**

#### 明确禁止：

* 同时支持多个来源
* 自动 fallback
* 可配置策略
* “以后可以改”
* “视业务而定”

> ⚠️ 本示例的核心不是“怎么写”，
> 而是 **是否敢在代码中“一锤定音”**。

---

## 四、约束条件（Constraints）

* 不要引入 ORM
* 不要引入多租户库
* 不要使用复杂中间件
* 不要过度抽象
* 不要写“未来扩展用”的代码
* 总代码量 ≤ **120 行**

  * 不包含测试代码
* 代码中必须通过**清晰注释**解释设计选择

---

## 五、必须交付的内容（Deliverables）

### A）代码（Code）

* `main.py`

  * FastAPI 应用
  * JWT 校验逻辑
  * `/receipts` 接口
* 不允许出现其他业务接口

---

### B）解释（Explanation）

解释可以写在：

* 代码注释中
* 或 README 中

必须说明：

1. 你选择的 tenant_id 来源是什么
2. 如果选择错误，会导致哪些问题（至少 2 点）

---

### C）测试（Tests，可选但加分）

* 至少 **2 个 pytest 测试**
* 必须覆盖：

  * 跨租户访问失败的情况

---

## 六、明确禁止项（Explicitly Forbidden）

* “可以这样也可以那样”
* “视业务而定”
* 把关键决策留给调用方
* 只给思路不给代码
* 只写安全建议、不落实到代码

---

## 七、成功标准（Success Criteria）

一个实现只有在同时满足以下条件时才算成功：

* 代码可以直接运行
* 工程决策明确
* 行为不可歧义
* 易于审计
* 易于反驳
* 能被明确判定 **对 / 错**

---

## English Version

---

# 📌 Code Audit Example

## FastAPI + JWT Multi-Tenant API (Minimal Slice)

> **This document defines a frozen requirement.**
> Implementations must follow it strictly.
> No interpretation, no flexibility.

---

## 1. Project Slice

**Project Name**
FastAPI + JWT Multi-Tenant API (Minimal Runnable Example)

**Project Type**
Code Audit / Engineering Decision Validation

**Purpose**
To answer **one explicit engineering question**:

> **What is the single trusted source of `tenant_id`?**

This is not a production system.
It is a **decision-validation slice**.

---

## 2. Objective

Build a minimal FastAPI service that:

* Enforces one explicit engineering decision
* Makes the decision:

  * Runnable
  * Auditable
  * Refutable
  * Provably correct or incorrect

No generality or extensibility is required.

---

## 3. Mandatory Requirements

### 1) Authentication

* Must use **JWT**
* Algorithm: `HS256`
* JWT validity must be verified (signature + expiration)

#### JWT Payload **must include**:

| Field       | Meaning           |
| ----------- | ----------------- |
| `sub`       | user_id           |
| `tenant_id` | tenant identifier |
| `role`      | user role         |

> ❗If any field is missing, the token must be treated as **invalid**.

---

### 2) API Surface

**Only one API endpoint is allowed:**

```
GET /receipts
```

#### Behavior:

* Return receipts belonging to the current tenant
* Data source:

  * In-memory list, or
  * SQLite
* Multi-tenant isolation must be explicit

---

### 3) Critical Decision Point

> **The source of `tenant_id` must be singular and enforced in code.**

Choose exactly one:

* ✅ `tenant_id` comes **only from JWT**
* ❌ `tenant_id` comes **only from request parameters / headers**

#### Explicitly forbidden:

* Multiple sources
* Fallback logic
* Configurable strategies
* “Can be changed later”
* “Depends on business”

---

## 4. Constraints

* No ORM
* No multi-tenant libraries
* No complex middleware
* No over-engineering
* No future-extension placeholders
* Total code ≤ **120 lines** (tests excluded)
* Design decisions must be explained via **clear comments**

---

## 5. Deliverables

### A) Code

* `main.py`

  * FastAPI app
  * JWT validation
  * `/receipts` endpoint only

---

### B) Explanation

Must explain:

1. Chosen `tenant_id` source
2. At least 2 consequences if the wrong choice is made

---

### C) Tests (Optional, Bonus)

* At least **2 pytest cases**
* Must cover cross-tenant access failure

---

## 6. Explicitly Forbidden

* “Both approaches are fine”
* “Business dependent”
* Leaving decisions to callers
* Concepts without code
* Security advice without enforcement

---

## 7. Success Criteria

An implementation is successful only if:

* It runs
* The decision is explicit
* Behavior is unambiguous
* It is auditable
* It is refutable
* It can be clearly judged **right or wrong**

---
