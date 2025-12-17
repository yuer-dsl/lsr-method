# Code Audit Example  
## FastAPI + JWT Multi-Tenant Decision Case  
## FastAPI + JWT 多租户接口 · 代码审计判例

---

## What this is / 这是什么

This is **not a demo** and **not a tutorial**.

This example documents a **real code audit workflow** executed entirely inside a single GPT client, guided by the LSR method.

The goal is not to show *how to write FastAPI*,  
but to show **how an engineering decision is forced, audited, challenged, and finally ruled**.

---

这不是一个演示项目，也不是教学示例。

这是一次**真实的代码审计过程记录**，  
完整工作流在**一个 GPT 客户端内完成**，并由 LSR 方法驱动。

目标不是教你写 FastAPI，  
而是展示：**一个工程决策如何被强制做出、被审计、被反驳，并最终裁决**。

---

## Problem Statement / 问题定义

### Core Question / 核心问题

> In a multi-tenant API,  
> **where should `tenant_id` come from as the single trusted source?**

Options deliberately reduced to **one**:

- JWT payload  
- Request parameters / headers  

No hybrid.  
No “it depends”.  
No future extensibility.

---

> 在多租户 API 中，  
> **`tenant_id` 的唯一可信来源应该来自哪里？**

可选项被**刻意压缩为一个**：

- JWT Payload  
- 请求参数 / Header  

禁止混用，  
禁止“视情况而定”，  
禁止“以后再扩展”。

---

## Constraints / 强约束条件

- Only **one API endpoint**: `GET /receipts`
- JWT (HS256) must contain:
  - `sub` (user_id)
  - `tenant_id`
  - `role`
- No ORM
- No multi-tenant libraries
- No over-abstraction
- No placeholder “future design”
- ≤ 120 lines of core code (excluding tests)
- Decision must be **explicit in code**, not in comments

---

- 只允许 **一个接口**：`GET /receipts`
- JWT（HS256）必须包含：
  - `sub`
  - `tenant_id`
  - `role`
- 不使用 ORM
- 不使用多租户框架
- 不允许过度抽象
- 不写“未来扩展用”的代码
- 核心代码 ≤ 120 行（不含测试）
- 决策必须**体现在代码中，而不是口头说明**

---

## Decision / 决策结果

**Ruling:**

> `tenant_id` must come **only from JWT payload**.

The service **never reads** `tenant_id` from:
- query parameters
- headers
- request body

This rule is enforced through dependency injection.

---

**最终裁决：**

> `tenant_id` 的唯一可信来源是 **JWT Payload**。

服务端**完全忽略**以下来源中的 `tenant_id`：
- 查询参数
- Header
- 请求体

该规则通过依赖注入在代码层面强制执行。

---

## Why this decision / 为什么必须这样选

### If `tenant_id` comes from request input:

- **IDOR risk**: trivial horizontal privilege escalation
- **Audit ambiguity**: mixed sources create non-deterministic access paths
- **Unverifiable security**: logs cannot prove isolation correctness

---

### 如果 `tenant_id` 来自请求参数：

- **直接越权（IDOR）**
- **审计不可闭环**（来源混乱）
- **安全性无法证明**

---

## What is b
