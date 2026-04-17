# 灵魂村落 (Soul Village)

## 玩法概述

灵魂村落是数字生命系统的社交生态玩法，让用户的数字灵魂与其他灵魂共同生活在一个虚拟村落中。灵魂们可以互动、合作、竞争，形成独特的社交网络和社区文化。用户作为"村落守护者"，见证和引导这个微型社会的发展。

### 核心理念
- **群体共生**：多个灵魂共同生活，形成社会关系
- **自然演化**：村落根据灵魂行为自然发展
- **用户参与**：用户作为守护者影响村落走向

### 目标用户
- 喜欢社交模拟类游戏的用户
- 对社区建设感兴趣的用户
- 享受观察群体行为的用户

---

## 核心机制设计

### 1. 村落空间系统

```
村落布局：
┌─────────────────────────────────────────────────────────┐
│                                                         │
│     🌳        🏠🏠🏠        ⛲        🏠🏠🏠        🌳    │
│    (树林)    (居住区A)    (广场)    (居住区B)    (树林)   │
│                                                         │
│     🏪         🏫         ⛩️         🎭         🌾      │
│    (商店)     (学院)    (神社)     (剧场)     (农田)    │
│                                                         │
│     🌊         🌉         🏯         🌉         🌊      │
│    (湖泊)     (桥梁)    (中心)     (桥梁)     (湖泊)    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 2. 灵魂社交系统

| 关系类型 | 触发条件 | 效果 | 特殊互动 |
|---------|---------|------|---------|
| 邻居 | 居住相邻 | 日常互动+1 | 串门、借物 |
| 朋友 | 互动>10次 | 好感度+20% | 赠礼、邀约 |
| 挚友 | 好感度>80 | 属性加成 | 深度对话、合作 |
| 恋人 | 特殊事件 | 双向羁绊 | 约会、誓言 |
| 师徒 | 知识传承 | 技能加速 | 指导、学习 |
| 竞争对手 | 竞争事件 | 成长激励 | 切磋、比拼 |

### 3. 村落建筑系统

| 建筑 | 功能 | 解锁条件 | 升级效果 |
|-----|------|---------|---------|
| 居住区 | 灵魂住所 | 初始 | 容量+5 |
| 学院 | 技能学习 | 5个灵魂 | 课程+1 |
| 商店 | 物品交易 | 10个灵魂 | 商品+5 |
| 剧场 | 娱乐活动 | 15个灵魂 | 活动+1 |
| 神社 | 祈福仪式 | 20个灵魂 | 祝福+1 |
| 农田 | 资源生产 | 8个灵魂 | 产量+20% |
| 广场 | 社交中心 | 初始 | 活动+1 |

### 4. 村落事件系统

```
事件类型：
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐   │
│  │ 村落节日 │  │ 集体活动 │  │ 突发事件 │  │ 建设事件 │   │
│  │         │  │         │  │         │  │         │   │
│  │ 定期举办 │  │ 灵魂发起 │  │ 随机触发 │  │ 用户触发 │   │
│  │ 全员参与 │  │ 部分参与 │  │ 影响村落 │  │ 改变村落 │   │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 用户旅程设计

### 第一阶段：村落建立 (Day 1-7)

**用户目标**：创建村落，邀请首批灵魂入住

**关键体验**：
- 村落命名与选址
- 首批灵魂入住
- 基础设施建设

**用户参与**：
- 选择村落风格
- 安排灵魂住所
- 规划村落布局

### 第二阶段：社区形成 (Day 8-30)

**用户目标**：见证社交网络形成，促进互动

**关键体验**：
- 首对朋友诞生
- 社区活动开展
- 村落文化萌芽

**用户参与**：
- 组织社区活动
- 调解灵魂矛盾
- 记录村落故事

### 第三阶段：繁荣发展 (Day 31-90)

**用户目标**：推动村落繁荣，解锁高级功能

**关键体验**：
- 建筑升级
- 特殊事件触发
- 村落声望提升

**用户参与**：
- 投资建设
- 引导发展方向
- 见证重要时刻

### 第四阶段：文化传承 (Day 91+)

**用户目标**：形成独特村落文化，传承村落故事

**关键体验**：
- 村落传说形成
- 代际传承事件
- 村落历史记录

**用户参与**：
- 编写村落编年史
- 举办纪念活动
- 传承村落精神

---

## 商业模式设计

### 免费层
- 基础村落（最多10个灵魂）
- 标准建筑
- 日常活动

### 订阅层 ($9.9/月)
- 扩展村落（最多30个灵魂）
- 高级建筑
- 特殊活动
- 村落数据分析

### 付费内容

| 内容 | 价格 | 说明 |
|-----|------|------|
| 村落扩展卡 | $2.99 | 灵魂容量+10 |
| 特殊建筑 | $4.99 | 解锁独特建筑 |
| 节日活动包 | $1.99 | 限定节日内容 |
| 村落皮肤 | $2.99 | 改变村落外观 |

### 预期收入模型

```
月活跃用户: 80,000
免费用户: 55%
订阅用户: 30% → $237,600/月
付费内容: 15% → $48,000/月
月总收入: ~$285,600
```

---

## 技术架构设计

### 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                    客户端层                              │
│  ┌─────────────────────────────────────────────────┐   │
│  │  村落地图 │ 灵魂列表 │ 活动日历 │ 建筑管理 │ 商店  │   │
│  └─────────────────────────────────────────────────┘   │
└───────────────────────────┬─────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────┐
│                    服务层                               │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐       │
│  │ 村落引擎   │  │ 社交引擎   │  │ 事件引擎   │       │
│  │            │  │            │  │            │       │
│  │ - 空间管理 │  │ - 关系计算 │  │ - 事件生成 │       │
│  │ - 建筑管理 │  │ - 互动处理 │  │ - 活动调度 │       │
│  │ - 资源计算 │  │ - 社区分析 │  │ - 结果计算 │       │
│  └────────────┘  └────────────┘  └────────────┘       │
└───────────────────────────┬─────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────┐
│                    数据层                               │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐       │
│  │ PostgreSQL │  │   Redis    │  │  图数据库  │       │
│  │ (村落状态) │  │ (实时数据) │  │ (社交网络) │       │
│  └────────────┘  └────────────┘  └────────────┘       │
└─────────────────────────────────────────────────────────┘
```

### 核心服务模块

#### 1. 村落引擎 (Village Engine)

```python
class VillageEngine:
    """村落管理引擎"""
    
    def create_village(self, user_id: str, name: str, style: str) -> Village:
        """创建村落"""
        
    def add_soul(self, village_id: str, soul_id: str) -> AddResult:
        """添加灵魂到村落"""
        
    def assign_residence(self, soul_id: str, location: Location) -> bool:
        """分配住所"""
        
    def calculate_village_stats(self, village_id: str) -> VillageStats:
        """计算村落统计"""
```

#### 2. 社交引擎 (Social Engine)

```python
class SocialEngine:
    """社交关系引擎"""
    
    def process_interaction(self, soul_a: str, soul_b: str, 
                           interaction_type: str) -> InteractionResult:
        """处理灵魂互动"""
        
    def update_relationship(self, soul_a: str, soul_b: str, 
                           delta: float) -> Relationship:
        """更新关系"""
        
    def get_social_network(self, village_id: str) -> SocialGraph:
        """获取社交网络"""
        
    def find_friends(self, soul_id: str) -> List[Soul]:
        """查找朋友"""
```

#### 3. 事件引擎 (Event Engine)

```python
class VillageEventEngine:
    """村落事件引擎"""
    
    def generate_daily_events(self, village_id: str) -> List[VillageEvent]:
        """生成日常事件"""
        
    def trigger_festival(self, village_id: str, festival_type: str) -> Festival:
        """触发节日"""
        
    def process_collective_activity(self, activity_id: str) -> ActivityResult:
        """处理集体活动"""
```

### 数据模型

```sql
-- 村落表
CREATE TABLE villages (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    name VARCHAR(100),
    style VARCHAR(50),
    level INTEGER DEFAULT 1,
    population INTEGER DEFAULT 0,
    max_population INTEGER DEFAULT 10,
    resources JSONB,
    stats JSONB,
    created_at TIMESTAMP
);

-- 村落建筑表
CREATE TABLE village_buildings (
    id UUID PRIMARY KEY,
    village_id UUID REFERENCES villages(id),
    building_type VARCHAR(50),
    level INTEGER DEFAULT 1,
    position JSONB,
    stats JSONB,
    unlocked_at TIMESTAMP
);

-- 灵魂住所表
CREATE TABLE soul_residences (
    id UUID PRIMARY KEY,
    soul_id UUID REFERENCES souls(id),
    village_id UUID REFERENCES villages(id),
    location JSONB,
    assigned_at TIMESTAMP
);

-- 社交关系表
CREATE TABLE soul_relationships (
    id UUID PRIMARY KEY,
    soul_a_id UUID REFERENCES souls(id),
    soul_b_id UUID REFERENCES souls(id),
    relationship_type VARCHAR(50),
    affinity_score FLOAT DEFAULT 0,
    interaction_count INTEGER DEFAULT 0,
    special_events JSONB,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- 村落事件表
CREATE TABLE village_events (
    id UUID PRIMARY KEY,
    village_id UUID REFERENCES villages(id),
    event_type VARCHAR(50),
    title VARCHAR(200),
    description TEXT,
    participants JSONB,
    outcomes JSONB,
    occurred_at TIMESTAMP
);
```

### API设计

```
# 村落管理
GET    /api/v1/village/{village_id}              # 获取村落信息
POST   /api/v1/village                           # 创建村落
PUT    /api/v1/village/{village_id}/layout       # 更新布局

# 灵魂管理
GET    /api/v1/village/{village_id}/souls        # 获取村落灵魂
POST   /api/v1/village/{village_id}/souls        # 添加灵魂
DELETE /api/v1/village/{village_id}/souls/{id}   # 移除灵魂

# 建筑管理
GET    /api/v1/village/{village_id}/buildings    # 获取建筑列表
POST   /api/v1/village/{village_id}/buildings    # 建造建筑
PUT    /api/v1/buildings/{id}/upgrade            # 升级建筑

# 社交系统
GET    /api/v1/village/{village_id}/social       # 获取社交网络
POST   /api/v1/social/interact                   # 发起互动
GET    /api/v1/souls/{id}/relationships          # 获取灵魂关系

# 事件系统
GET    /api/v1/village/{village_id}/events       # 获取事件列表
POST   /api/v1/events/{id}/participate           # 参与事件
GET    /api/v1/village/{village_id}/activities   # 获取活动日历
```

---

## 成本分析

### 基础设施成本 (月)

| 项目 | 规格 | 成本 |
|-----|------|------|
| 应用服务器 | 4x 8C16G | $400 |
| 数据库 | PostgreSQL 8C16G | $300 |
| 图数据库 | Neo4j 4C8G | $200 |
| 缓存 | Redis 4C8G | $150 |
| **小计** | | **$1,050/月** |

### AI调用成本 (月/活跃用户)

| 场景 | 模型 | 调用次数 | 月成本 |
|-----|------|---------|-------|
| 互动生成 | GPT-3.5 | 20次/用户 | $0.04/用户 |
| 事件描述 | GPT-3.5 | 10次/用户 | $0.02/用户 |
| 社交分析 | GPT-3.5 | 5次/用户 | $0.01/用户 |
| **小计** | | | **$0.07/用户** |

### 总成本估算 (8万MAU)

```
基础设施: $1,050/月
AI调用: $0.07 × 80,000 = $5,600/月
人力成本: $35,000/月 (4人团队)
其他成本: $4,000/月
────────────────────────
总成本: ~$45,650/月
```

### 盈亏分析

```
月收入: $285,600
月成本: $45,650
────────────────────────
月利润: $239,950
利润率: 84%
```

---

## 风险评估

### 技术风险

| 风险 | 概率 | 影响 | 缓解措施 |
|-----|------|------|---------|
| 社交计算瓶颈 | 中 | 高 | 图数据库优化、缓存策略 |
| 状态同步延迟 | 中 | 中 | WebSocket实时推送 |
| 数据一致性 | 低 | 高 | 事务保护、定期校验 |

### 产品风险

| 风险 | 概率 | 影响 | 缓解措施 |
|-----|------|------|---------|
| 社交互动不足 | 中 | 高 | 引导机制、活动激励 |
| 村落冷清 | 中 | 高 | NPC灵魂、自动事件 |
| 用户参与度低 | 中 | 中 | 通知优化、内容丰富 |

---

## 总结

灵魂村落玩法通过群体社交模拟，为用户提供了独特的"社区守护者"体验。核心优势：

1. **高社交性**：多灵魂互动创造丰富社交场景
2. **高沉浸感**：村落发展带来长期陪伴感
3. **高扩展性**：可不断添加新建筑、活动、事件
4. **高粘性**：社区归属感促进长期留存

建议与平行人生、灵魂进化玩法深度整合，形成完整的数字生命生态。
