---
name: macro-chain-review
description: 用于长期多步骤任务中，需要对单条关键调用链进行深度稳定性追踪时使用。当任务跨越多个会话、需要 agent 接手上一轮调查、或需要维护调用链状态机和任务队列时触发。核心场景：多轮 agent 派发中保持注意力连续性、每轮只推进一个明确调查任务、后续 agent 不重新泛泛搜索而是从状态机接手。
---

# 宏观调用链追踪（Macro Chain Review）

## 核心假设

AI 审查要产生长期价值，必须把注意力绑定到**一条关键调用链的深度稳定性**上。有效积累一条深度调用链，比广泛搜索无目的审查重要得多。

每轮只做一件事：推进当前关键链的下一个调查任务。

## 日志结构

在项目根目录创建 `review-log/`：

```
review-log/
├── STATE.md              # 当前唯一事实源（每轮必读）
├── QUEUE.md              # 任务派发队列（每轮必读）
├── chains/
│   └── <current-chain>.md   # 当前链条节点、边、契约
├── rounds/
│   └── round-N.md        # 每轮 agent 做了什么
└── evidence/
    └── <task-id>.md      # 具体代码证据（按需读取，不默认加载）
```

**后续 agent 每轮只需读：**
- `review-log/STATE.md`
- `review-log/QUEUE.md`
- `review-log/rounds/` 最新一个文件

**不需要读：** `evidence/`、`chains/` 的完整历史（按需查阅）

## STATE.md 格式

```markdown
# 当前状态

## 当前关键链：<chain-name>
## 状态：<状态码>
## 最后更新：<日期>

## 当前阻塞点
<如果有，描述阻塞原因；无则写"无">

## 下一步
<下一轮 agent 应该做什么，一句话>
```

**状态码：**

| 状态 | 含义 |
|------|------|
| `UNSELECTED` | 尚未选择当前关键链 |
| `SELECTED` | 已选择，尚未映射节点 |
| `MAPPED` | 已完成节点和边的映射 |
| `TASK_QUEUED` | 已拆出下一步调查任务 |
| `INVESTIGATING` | 当前任务调查中 |
| `EVIDENCE_FOUND` | 找到证据，待回写 |
| `BLOCKED` | 需要运行环境、上下文或人工确认 |
| `FIX_PENDING` | 已确认问题，等待修复 |
| `VERIFY_PENDING` | 修复后等待复查 |
| `STABLE` | 当前链条稳定 |
| `ARCHIVED` | 链条暂时归档，切换到下一条 |

## QUEUE.md 格式

```markdown
# 任务队列

## 调查中
- [ ] TASK-001：验证 authService.login() → userModel.findOne() 的参数契约

## 待调查
- [ ] TASK-002：验证 JWT 中间件 → controller 的 req.user 类型一致性
- [ ] TASK-003：验证 controller 错误路径是否传播到全局错误处理

## 待复查
- [ ] TASK-001（修复后）：重新验证参数契约

## 已完成
- [x] TASK-000：映射 user-auth-chain 的完整节点列表
```

## 工作流程

### 第一轮（UNSELECTED → MAPPED）

1. 扫描项目结构，列出候选关键链（3-5 条，不审查，只列举）
2. 选择当前最重要的一条
3. 映射该链的所有节点：文件路径 + 函数名 + 输入/输出契约
4. 创建 `chains/<chain-name>.md`，写入节点列表
5. 更新 `STATE.md` 为 `MAPPED`
6. 在 `QUEUE.md` 拆出第一个调查任务
7. 创建 `rounds/round-1.md`

### 后续每轮（接手 → 推进 → 回写）

1. 读 `STATE.md` 和 `QUEUE.md`，了解当前状态和下一步
2. 从队列取出第一个"调查中"任务
3. 执行调查：沿节点顺序验证接口契约、错误传播、类型一致性
4. 把证据写入 `evidence/<task-id>.md`
5. 更新 `QUEUE.md`（完成当前任务，推进下一个）
6. 更新 `STATE.md`（更新状态码和下一步）
7. 创建 `rounds/round-N.md`

### chains/<chain-name>.md 格式

```markdown
# <链条名称>

## 描述
<这条链做什么，一句话>

## 节点列表

| 序号 | 文件 | 函数 | 输入 | 输出 | 备注 |
|-----|------|------|------|------|------|
| 1 | src/routes/auth.ts | POST /login | req.body | res.json | 入口 |
| 2 | src/controllers/authController.ts | login() | {email, password} | {token} | |
| 3 | src/services/authService.ts | authenticate() | {email, password} | User \| null | |
| 4 | src/models/User.ts | findOne() | {email} | User \| null | 数据层 |

## 已知契约问题
<每次调查发现的契约不一致，追加记录>
```

## 链边界规则

定义链之前必须明确三个边界：**起点**（第一个入口）、**终点**（最后一个输出）、**副作用边界**（链内产生的写库/发消息等）。

核心规则：一条链只包含从起点到终点的直接调用路径。不在当前请求中实际执行的节点（如只保护其他路由的中间件、启动时的初始化逻辑）不属于当前链。

> 遇到边界判断不确定的情况，读 `references/chain-boundary-examples.md` 查看典型案例。

## 状态迁移规则

状态码见 STATE.md 格式表。每个状态的进入/退出条件是硬性的，不能跳过。

> 完整迁移表和 STABLE/BLOCKED 的硬性条件，读 `references/state-machine.md`。

## 调查原则

**只检查：**
- 节点是否存在（文件/函数）
- 上下游接口是否匹配（参数类型、返回值结构、null 语义）
- 错误是否能沿链条传播或被正确处理
- 异步边界是否有正确的 await

**不检查：**
- 单个函数的业务逻辑正确性
- 算法实现
- 性能

## 常见错误

- 每轮审查多条链 → 每轮只推进当前链的一个任务
- 把 evidence/ 全量加载给后续 agent → 只加载 STATE.md 和 QUEUE.md
- 状态机不更新 → 每轮结束必须更新 STATE.md
- 发现问题后继续深挖 → 记录到 evidence/，更新队列，留给下一轮
- 把后续请求的中间件混入当前链 → 先明确链的起点/终点/副作用边界
- 跳过状态迁移条件直接写状态码 → 必须满足进入条件才能迁移
- 把"所有任务跑完"就标 STABLE → 必须确认无 FIX_PENDING 和 VERIFY_PENDING
