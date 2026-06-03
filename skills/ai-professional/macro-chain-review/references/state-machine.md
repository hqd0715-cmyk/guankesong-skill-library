# 状态机完整参考

## 状态迁移表

| 状态 | 进入条件 | 退出条件 | 退出到 |
|------|---------|---------|--------|
| `UNSELECTED` | 初始状态 | 已选定一条关键链 | `SELECTED` |
| `SELECTED` | 已选链，未映射节点 | 已完成节点列表和边界定义 | `MAPPED` |
| `MAPPED` | 节点已映射 | 已拆出至少一个调查任务到 QUEUE | `TASK_QUEUED` |
| `TASK_QUEUED` | 队列有待调查任务 | agent 开始执行某个任务 | `INVESTIGATING` |
| `INVESTIGATING` | 任务执行中 | 找到代码证据 → `EVIDENCE_FOUND`；需外部信息 → `BLOCKED`；任务完成无问题 → `TASK_QUEUED` | 见左 |
| `EVIDENCE_FOUND` | 找到真实代码证据 | 证据已写入 evidence/，QUEUE 已更新 | `FIX_PENDING` 或 `TASK_QUEUED` |
| `BLOCKED` | 需要运行环境/日志/人工确认 | 阻塞解除 | `INVESTIGATING` |
| `FIX_PENDING` | 已确认问题，等待修复 | 修复完成，进入复查 | `VERIFY_PENDING` |
| `VERIFY_PENDING` | 修复后等待复查 | 复查通过 → `TASK_QUEUED`；复查失败 → `FIX_PENDING` | 见左 |
| `STABLE` | 所有 QUEUE 任务完成，无 FIX_PENDING | 选择下一条链 | `ARCHIVED` |
| `ARCHIVED` | 当前链已稳定或暂停 | 选择新链 | `UNSELECTED`（新链） |

## 进入 STABLE 的硬性条件

必须同时满足：
- QUEUE 中无"调查中"和"待调查"任务
- QUEUE 中无"待复查"任务
- 所有 `EVIDENCE_FOUND` 的问题已进入 `FIX_PENDING` 或已修复

## 进入 BLOCKED 的硬性条件（满足任一）

- 需要实际运行代码才能验证（如运行时行为、日志输出）
- 需要外部系统的响应才能确认（如第三方 API 行为）
- 代码路径存在但无法静态推断执行结果
