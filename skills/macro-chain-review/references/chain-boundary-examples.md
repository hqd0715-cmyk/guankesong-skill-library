# 链边界判断参考

## 三个边界的定义

| 边界 | 说明 | 示例 |
|------|------|------|
| 起点 | 链的第一个入口，通常是外部请求或事件触发 | `POST /login` 接收请求 |
| 终点 | 链的最后一个输出，通常是响应或副作用完成 | `res.json({token})` 返回 |
| 副作用边界 | 链内产生的所有副作用（写库、发消息、更新缓存） | 写入 User 记录、签发 JWT |

## 典型链边界案例

### 案例 1：登录链 vs 受保护请求链

**登录链（user-login-chain）**
- 起点：`POST /login`
- 终点：返回 `{token}`
- 节点：routes → controller → authService → User.findOne → comparePassword
- **不包含**：JWT 验证中间件（它只在受保护路由上运行，不参与登录流程）

**受保护请求链（protected-request-chain）**
- 起点：任意受保护路由的请求
- 终点：业务响应
- 节点：JWT 中间件 → controller → service → ...
- **不包含**：登录链的节点

**判断依据**：JWT 中间件在登录请求中根本不执行，因此不属于登录链。

---

### 案例 2：数据写入链 vs 缓存同步链

**数据写入链（data-write-chain）**
- 起点：`POST /orders`
- 终点：数据库写入成功，返回 `{orderId}`
- 副作用边界：仅写入 orders 表

**缓存同步链（cache-sync-chain）**
- 起点：orders 表写入事件（或消息队列消费）
- 终点：缓存更新完成
- **不包含**：数据写入链的节点（即使它们在时序上紧接着）

**判断依据**：两条链的触发机制不同，即使时序相邻也应分开映射。

---

### 案例 3：初始化依赖不是链节点

**错误做法**：把数据库连接初始化放进业务链节点
```
节点1: app.ts → connectDB()   ← 错误，这是启动依赖
节点2: routes/orders.ts → POST /orders
节点3: controllers/orderController.ts → create()
```

**正确做法**：业务链从第一个处理请求的节点开始
```
节点1: routes/orders.ts → POST /orders   ← 正确起点
节点2: controllers/orderController.ts → create()
节点3: services/orderService.ts → createOrder()
节点4: models/Order.ts → save()
备注: 依赖数据库连接（启动时已初始化）
```

## 常见边界错误速查

| 错误 | 正确做法 |
|------|---------|
| 把后续请求的中间件混入当前链 | 检查该中间件是否在当前请求中实际执行 |
| 把初始化逻辑当作链节点 | 只包含处理当前请求的直接调用路径 |
| 把两条独立链合并 | 检查触发机制是否相同，不同则分开 |
| 把共享工具函数重复放入多条链 | 工具函数可出现在多条链，各链独立映射 |
