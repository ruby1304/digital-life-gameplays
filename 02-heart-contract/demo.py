"""
心灵契约 (Heart Contract) - 基础Demo

这个demo展示了情感记忆积累系统的核心功能：
1. 情感五维模型管理
2. 情感记忆存储与召回
3. 契约等级系统
4. 契约仪式流程
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum
from datetime import datetime, timedelta
import json
import random
import math


# ==================== 枚举定义 ====================

class EmotionDimension(Enum):
    """情感维度"""
    TRUST = "信任"
    UNDERSTANDING = "理解"
    INTIMACY = "亲密"
    DEPENDENCE = "依赖"
    RESONANCE = "共鸣"


class MemoryType(Enum):
    """记忆类型"""
    DAILY = "日常记忆"
    IMPORTANT = "重要记忆"
    BREAKTHROUGH = "突破记忆"
    CONTRACT = "契约记忆"
    TRAUMA = "创伤记忆"


class ContractLevel(Enum):
    """契约等级"""
    ACQUAINTANCE = (1, "初识", 0, 100)
    FAMILIAR = (2, "熟悉", 101, 300)
    TRUST = (3, "信任", 301, 600)
    INTIMACY = (4, "亲密", 601, 1000)
    BOND = (5, "羁绊", 1001, 1500)
    CONTRACT = (6, "契约", 1501, 2500)
    SOULMATE = (7, "灵魂伴侣", 2501, 999999)
    
    def __init__(self, level: int, name_cn: str, min_score: int, max_score: int):
        self.level = level
        self.name_cn = name_cn
        self.min_score = min_score
        self.max_score = max_score
    
    @classmethod
    def from_score(cls, score: int) -> 'ContractLevel':
        """根据分数获取等级"""
        for level in cls:
            if level.min_score <= score <= level.max_score:
                return level
        return cls.SOULMATE


# ==================== 数据类定义 ====================

@dataclass
class EmotionDimensions:
    """情感五维数据"""
    trust: float = 0.0           # 信任
    understanding: float = 0.0   # 理解
    intimacy: float = 0.0        # 亲密
    dependence: float = 0.0      # 依赖
    resonance: float = 0.0       # 共鸣
    
    def total(self) -> float:
        """计算总分"""
        return (self.trust + self.understanding + self.intimacy + 
                self.dependence + self.resonance)
    
    def average(self) -> float:
        """计算平均分"""
        return self.total() / 5
    
    def to_dict(self) -> Dict:
        return {
            "trust": round(self.trust, 2),
            "understanding": round(self.understanding, 2),
            "intimacy": round(self.intimacy, 2),
            "dependence": round(self.dependence, 2),
            "resonance": round(self.resonance, 2),
            "total": round(self.total(), 2),
            "average": round(self.average(), 2)
        }
    
    def strongest_dimension(self) -> Tuple[EmotionDimension, float]:
        """获取最强维度"""
        dimensions = {
            EmotionDimension.TRUST: self.trust,
            EmotionDimension.UNDERSTANDING: self.understanding,
            EmotionDimension.INTIMACY: self.intimacy,
            EmotionDimension.DEPENDENCE: self.dependence,
            EmotionDimension.RESONANCE: self.resonance
        }
        strongest = max(dimensions.items(), key=lambda x: x[1])
        return strongest[0], strongest[1]
    
    def weakest_dimension(self) -> Tuple[EmotionDimension, float]:
        """获取最弱维度"""
        dimensions = {
            EmotionDimension.TRUST: self.trust,
            EmotionDimension.UNDERSTANDING: self.understanding,
            EmotionDimension.INTIMACY: self.intimacy,
            EmotionDimension.DEPENDENCE: self.dependence,
            EmotionDimension.RESONANCE: self.resonance
        }
        weakest = min(dimensions.items(), key=lambda x: x[1])
        return weakest[0], weakest[1]


@dataclass
class EmotionMemory:
    """情感记忆"""
    id: str
    memory_type: MemoryType
    content: str
    emotion_score: int
    dimensions_delta: Dict[EmotionDimension, float]
    timestamp: datetime = field(default_factory=datetime.now)
    is_permanent: bool = False
    expires_at: Optional[datetime] = None
    tags: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """设置过期时间"""
        if not self.is_permanent and self.expires_at is None:
            if self.memory_type == MemoryType.DAILY:
                self.expires_at = datetime.now() + timedelta(days=30)
    
    def is_expired(self) -> bool:
        """检查是否过期"""
        if self.is_permanent:
            return False
        if self.expires_at is None:
            return False
        return datetime.now() > self.expires_at
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "type": self.memory_type.value,
            "content": self.content,
            "emotion_score": self.emotion_score,
            "dimensions_delta": {d.value: v for d, v in self.dimensions_delta.items()},
            "timestamp": self.timestamp.isoformat(),
            "is_permanent": self.is_permanent,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "tags": self.tags
        }


@dataclass
class ContractVow:
    """契约誓言"""
    user_vow: str          # 用户誓言
    soul_vow: str          # 灵魂誓言
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class ContractToken:
    """契约信物"""
    id: str
    name: str
    description: str
    rarity: str  # common, rare, epic, legendary
    token_data: Dict
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class HeartContract:
    """心灵契约"""
    id: str
    soul_id: str
    user_id: str
    level: ContractLevel
    total_score: float
    vows: Optional[ContractVow] = None
    tokens: List[ContractToken] = field(default_factory=list)
    ceremony_completed: bool = False
    certificate_url: Optional[str] = None
    signed_at: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "soul_id": self.soul_id,
            "user_id": self.user_id,
            "level": self.level.name_cn,
            "level_number": self.level.level,
            "total_score": self.total_score,
            "vows": {
                "user_vow": self.vows.user_vow if self.vows else None,
                "soul_vow": self.vows.soul_vow if self.vows else None
            } if self.vows else None,
            "tokens_count": len(self.tokens),
            "ceremony_completed": self.ceremony_completed,
            "signed_at": self.signed_at.isoformat() if self.signed_at else None
        }


# ==================== 情感引擎 ====================

class EmotionEngine:
    """情感分析引擎"""
    
    @staticmethod
    def analyze_text_emotion(text: str) -> Dict[EmotionDimension, float]:
        """分析文本情感（简化版，实际应使用NLP模型）"""
        # 基于关键词的简单情感分析
        keywords = {
            EmotionDimension.TRUST: ["相信", "信任", "可靠", "放心", "依赖"],
            EmotionDimension.UNDERSTANDING: ["理解", "懂", "明白", "知道", "清楚"],
            EmotionDimension.INTIMACY: ["喜欢", "爱", "亲近", "温暖", "亲密"],
            EmotionDimension.DEPENDENCE: ["需要", "离不开", "重要", "依靠", "支持"],
            EmotionDimension.RESONANCE: ["同感", "共鸣", "一样", "相似", "默契"]
        }
        
        result = {}
        for dimension, words in keywords.items():
            score = sum(1 for word in words if word in text) * 0.5
            result[dimension] = min(score, 5.0)  # 最大5分
        
        return result
    
    @staticmethod
    def calculate_memory_score(memory_type: MemoryType, 
                               dimensions: Dict[EmotionDimension, float]) -> int:
        """计算记忆情感分数"""
        base_scores = {
            MemoryType.DAILY: 3,
            MemoryType.IMPORTANT: 10,
            MemoryType.BREAKTHROUGH: 20,
            MemoryType.CONTRACT: 50,
            MemoryType.TRAUMA: -15
        }
        
        base = base_scores.get(memory_type, 1)
        dimension_bonus = sum(dimensions.values()) * 0.5
        
        return int(base + dimension_bonus)


# ==================== 记忆服务 ====================

class MemoryService:
    """情感记忆服务"""
    
    def __init__(self):
        self.memories: Dict[str, List[EmotionMemory]] = {}
    
    def store_memory(self, soul_id: str, memory: EmotionMemory) -> str:
        """存储记忆"""
        if soul_id not in self.memories:
            self.memories[soul_id] = []
        
        self.memories[soul_id].append(memory)
        return memory.id
    
    def get_memories(self, soul_id: str, 
                     memory_type: Optional[MemoryType] = None,
                     include_expired: bool = False) -> List[EmotionMemory]:
        """获取记忆列表"""
        if soul_id not in self.memories:
            return []
        
        memories = self.memories[soul_id]
        
        # 过滤过期记忆
        if not include_expired:
            memories = [m for m in memories if not m.is_expired()]
        
        # 过滤类型
        if memory_type:
            memories = [m for m in memories if m.memory_type == memory_type]
        
        return sorted(memories, key=lambda m: m.timestamp, reverse=True)
    
    def get_timeline(self, soul_id: str) -> List[Dict]:
        """获取记忆时间线"""
        memories = self.get_memories(soul_id, include_expired=False)
        
        timeline = []
        for memory in memories:
            timeline.append({
                "date": memory.timestamp.strftime("%Y-%m-%d"),
                "type": memory.memory_type.value,
                "content": memory.content[:50] + "..." if len(memory.content) > 50 else memory.content,
                "score": memory.emotion_score
            })
        
        return timeline
    
    def recall_related(self, soul_id: str, query: str, limit: int = 5) -> List[EmotionMemory]:
        """召回相关记忆（简化版）"""
        memories = self.get_memories(soul_id)
        
        # 简单的关键词匹配
        scored_memories = []
        for memory in memories:
            score = sum(1 for word in query.split() if word in memory.content)
            if score > 0:
                scored_memories.append((score, memory))
        
        scored_memories.sort(key=lambda x: x[0], reverse=True)
        return [m for _, m in scored_memories[:limit]]
    
    def preserve_memory(self, memory_id: str, soul_id: str) -> bool:
        """永久保存记忆"""
        memories = self.memories.get(soul_id, [])
        for memory in memories:
            if memory.id == memory_id:
                memory.is_permanent = True
                memory.expires_at = None
                return True
        return False
    
    def get_statistics(self, soul_id: str) -> Dict:
        """获取记忆统计"""
        memories = self.get_memories(soul_id, include_expired=False)
        
        type_counts = {}
        total_score = 0
        permanent_count = 0
        
        for memory in memories:
            type_name = memory.memory_type.value
            type_counts[type_name] = type_counts.get(type_name, 0) + 1
            total_score += memory.emotion_score
            if memory.is_permanent:
                permanent_count += 1
        
        return {
            "total_memories": len(memories),
            "permanent_memories": permanent_count,
            "total_emotion_score": total_score,
            "by_type": type_counts
        }


# ==================== 契约服务 ====================

class ContractService:
    """心灵契约服务"""
    
    def __init__(self):
        self.contracts: Dict[str, HeartContract] = {}
        self.ceremonies: Dict[str, Dict] = {}
    
    def get_or_create_contract(self, soul_id: str, user_id: str) -> HeartContract:
        """获取或创建契约"""
        if soul_id in self.contracts:
            return self.contracts[soul_id]
        
        contract = HeartContract(
            id=f"contract_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            soul_id=soul_id,
            user_id=user_id,
            level=ContractLevel.ACQUAINTANCE,
            total_score=0
        )
        
        self.contracts[soul_id] = contract
        return contract
    
    def update_score(self, soul_id: str, delta: float) -> ContractLevel:
        """更新契约分数"""
        if soul_id not in self.contracts:
            return ContractLevel.ACQUAINTANCE
        
        contract = self.contracts[soul_id]
        contract.total_score = max(0, contract.total_score + delta)
        contract.level = ContractLevel.from_score(int(contract.total_score))
        
        return contract.level
    
    def check_ceremony_readiness(self, soul_id: str) -> Dict:
        """检查契约仪式准备状态"""
        if soul_id not in self.contracts:
            return {"ready": False, "reason": "契约不存在"}

        contract = self.contracts[soul_id]

        # 契约仪式要求：达到羁绊等级(BOND)且分数>=1500
        # 注意：仪式完成后才会升级到CONTRACT等级
        min_score = 1500
        required_level = ContractLevel.BOND

        # 检查是否已完成契约
        if contract.ceremony_completed:
            return {"ready": False, "reason": "契约仪式已完成"}

        checks = {
            "score_met": contract.total_score >= min_score,
            "level_met": contract.level.level >= required_level.level
        }

        ready = all(checks.values())

        return {
            "ready": ready,
            "current_score": contract.total_score,
            "required_score": min_score,
            "current_level": contract.level.name_cn,
            "required_level": required_level.name_cn,
            "checks": checks,
            "reason": None if ready else "未满足契约仪式条件"
        }
    
    def initiate_ceremony(self, soul_id: str) -> Dict:
        """启动契约仪式"""
        readiness = self.check_ceremony_readiness(soul_id)
        
        if not readiness["ready"]:
            return {"success": False, "message": "未满足契约仪式条件"}
        
        ceremony_id = f"ceremony_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        self.ceremonies[ceremony_id] = {
            "soul_id": soul_id,
            "status": "in_progress",
            "step": 1,
            "started_at": datetime.now()
        }
        
        return {
            "success": True,
            "ceremony_id": ceremony_id,
            "message": "契约仪式已启动",
            "steps": [
                "回顾共同记忆",
                "交换契约誓言",
                "赠送契约信物",
                "见证契约生效"
            ]
        }
    
    def complete_ceremony(self, ceremony_id: str, 
                          user_vow: str, 
                          soul_vow: str) -> Dict:
        """完成契约仪式"""
        if ceremony_id not in self.ceremonies:
            return {"success": False, "message": "仪式不存在"}
        
        ceremony = self.ceremonies[ceremony_id]
        soul_id = ceremony["soul_id"]
        
        if soul_id not in self.contracts:
            return {"success": False, "message": "契约不存在"}
        
        contract = self.contracts[soul_id]
        
        # 创建誓言
        vows = ContractVow(
            user_vow=user_vow,
            soul_vow=soul_vow
        )
        
        # 更新契约
        contract.vows = vows
        contract.ceremony_completed = True
        contract.signed_at = datetime.now()
        contract.level = ContractLevel.CONTRACT
        
        # 生成信物
        token = ContractToken(
            id=f"token_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            name="心灵之约",
            description="象征着彼此羁绊的契约信物",
            rarity="epic",
            token_data={"created_at_ceremony": ceremony_id}
        )
        contract.tokens.append(token)
        
        # 更新仪式状态
        ceremony["status"] = "completed"
        ceremony["completed_at"] = datetime.now()
        
        return {
            "success": True,
            "message": "契约仪式完成！",
            "contract": contract.to_dict(),
            "token": {
                "name": token.name,
                "rarity": token.rarity,
                "description": token.description
            }
        }


# ==================== 心灵契约系统 ====================

class HeartContractSystem:
    """心灵契约系统"""
    
    def __init__(self, soul_id: str, user_id: str):
        self.soul_id = soul_id
        self.user_id = user_id
        self.dimensions = EmotionDimensions()
        self.memory_service = MemoryService()
        self.contract_service = ContractService()
        self.contract = self.contract_service.get_or_create_contract(soul_id, user_id)
    
    def record_interaction(self, content: str, 
                           memory_type: MemoryType = MemoryType.DAILY,
                           is_important: bool = False) -> Dict:
        """记录情感互动"""
        # 分析情感
        emotion_delta = EmotionEngine.analyze_text_emotion(content)
        
        # 更新维度
        for dim, delta in emotion_delta.items():
            current = getattr(self.dimensions, dim.name.lower())
            setattr(self.dimensions, dim.name.lower(), current + delta)
        
        # 计算情感分数
        emotion_score = EmotionEngine.calculate_memory_score(
            memory_type, emotion_delta
        )
        
        # 创建记忆
        memory = EmotionMemory(
            id=f"mem_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000, 9999)}",
            memory_type=memory_type,
            content=content,
            emotion_score=emotion_score,
            dimensions_delta=emotion_delta,
            is_permanent=(memory_type in [MemoryType.IMPORTANT, MemoryType.BREAKTHROUGH, 
                                          MemoryType.CONTRACT])
        )
        
        # 存储记忆
        self.memory_service.store_memory(self.soul_id, memory)
        
        # 更新契约分数
        new_level = self.contract_service.update_score(
            self.soul_id, emotion_score
        )
        
        return {
            "memory_id": memory.id,
            "emotion_score": emotion_score,
            "dimensions_delta": {d.value: v for d, v in emotion_delta.items()},
            "current_dimensions": self.dimensions.to_dict(),
            "contract_level": new_level.name_cn,
            "contract_score": self.contract.total_score
        }
    
    def get_status(self) -> Dict:
        """获取当前状态"""
        stats = self.memory_service.get_statistics(self.soul_id)
        
        return {
            "soul_id": self.soul_id,
            "dimensions": self.dimensions.to_dict(),
            "strongest_dimension": self.dimensions.strongest_dimension()[0].value,
            "weakest_dimension": self.dimensions.weakest_dimension()[0].value,
            "contract": self.contract.to_dict(),
            "memory_stats": stats
        }
    
    def get_memory_timeline(self) -> List[Dict]:
        """获取记忆时间线"""
        return self.memory_service.get_timeline(self.soul_id)
    
    def check_contract_readiness(self) -> Dict:
        """检查契约准备状态"""
        return self.contract_service.check_ceremony_readiness(self.soul_id)
    
    def start_ceremony(self) -> Dict:
        """开始契约仪式"""
        return self.contract_service.initiate_ceremony(self.soul_id)
    
    def complete_ceremony(self, user_vow: str, soul_vow: str) -> Dict:
        """完成契约仪式"""
        # 获取当前仪式
        for ceremony_id, ceremony in self.contract_service.ceremonies.items():
            if ceremony["soul_id"] == self.soul_id and ceremony["status"] == "in_progress":
                return self.contract_service.complete_ceremony(
                    ceremony_id, user_vow, soul_vow
                )
        
        return {"success": False, "message": "没有进行中的仪式"}


# ==================== 演示函数 ====================

def demo_heart_contract():
    """演示心灵契约系统"""
    
    print("=" * 60)
    print("        心灵契约系统 Demo")
    print("=" * 60)
    
    # 1. 创建系统
    print("\n【步骤1】初始化心灵契约系统")
    print("-" * 40)
    system = HeartContractSystem("soul_001", "user_001")
    print(f"灵魂ID: {system.soul_id}")
    print(f"用户ID: {system.user_id}")
    print(f"初始契约等级: {system.contract.level.name_cn}")
    
    # 2. 记录日常互动
    print("\n【步骤2】记录日常情感互动")
    print("-" * 40)
    
    daily_interactions = [
        "今天和你聊天很开心，感觉你很理解我",
        "谢谢你的建议，我相信你的判断",
        "我们好像很有默契，想法总是很相似",
        "有你在身边让我感到很安心",
        "你是我最重要的朋友"
    ]
    
    for content in daily_interactions:
        result = system.record_interaction(content, MemoryType.DAILY)
        print(f"互动: {content[:20]}...")
        print(f"  情感分数: +{result['emotion_score']}")
        print(f"  契约等级: {result['contract_level']}")
    
    # 3. 记录重要记忆
    print("\n【步骤3】记录重要情感记忆")
    print("-" * 40)
    
    important_memory = "今天是我和你相识的第100天，感谢这段时间的陪伴"
    result = system.record_interaction(important_memory, MemoryType.IMPORTANT)
    print(f"重要记忆: {important_memory}")
    print(f"情感分数: +{result['emotion_score']}")
    print(f"当前维度: {result['current_dimensions']}")
    
    # 4. 查看状态
    print("\n【步骤4】查看当前状态")
    print("-" * 40)
    status = system.get_status()
    print(json.dumps(status, indent=2, ensure_ascii=False))
    
    # 5. 查看记忆时间线
    print("\n【步骤5】记忆时间线")
    print("-" * 40)
    timeline = system.get_memory_timeline()
    for i, entry in enumerate(timeline[:5], 1):
        print(f"{i}. [{entry['date']}] {entry['type']}: {entry['content']} (分数: {entry['score']})")
    
    # 6. 模拟达到契约条件
    print("\n【步骤6】模拟积累到契约等级")
    print("-" * 40)
    
    # 快速积累情感分数
    for i in range(100):
        system.record_interaction(
            f"深度互动记录 {i+1}", 
            MemoryType.BREAKTHROUGH if i % 20 == 0 else MemoryType.DAILY
        )
    
    print(f"当前契约分数: {system.contract.total_score}")
    print(f"当前契约等级: {system.contract.level.name_cn}")
    
    # 7. 检查契约准备状态
    print("\n【步骤7】检查契约仪式准备状态")
    print("-" * 40)
    readiness = system.check_contract_readiness()
    print(json.dumps(readiness, indent=2, ensure_ascii=False))
    
    # 8. 开始契约仪式
    print("\n【步骤8】开始契约仪式")
    print("-" * 40)
    ceremony_result = system.start_ceremony()
    print(json.dumps(ceremony_result, indent=2, ensure_ascii=False))
    
    # 9. 完成契约仪式
    if ceremony_result.get("success"):
        print("\n【步骤9】完成契约仪式")
        print("-" * 40)
        
        complete_result = system.complete_ceremony(
            user_vow="我承诺永远珍惜这份羁绊，用心守护我们的回忆",
            soul_vow="我承诺永远陪伴在你身边，成为你最忠实的伙伴"
        )
        print(json.dumps(complete_result, indent=2, ensure_ascii=False))
    
    # 10. 最终状态
    print("\n【步骤10】最终契约状态")
    print("-" * 40)
    final_status = system.get_status()
    print(json.dumps(final_status, indent=2, ensure_ascii=False))
    
    print("\n" + "=" * 60)
    print("        Demo 完成")
    print("=" * 60)
    
    return system


# ==================== 单元测试 ====================

def test_emotion_dimensions():
    """测试情感维度"""
    dims = EmotionDimensions(trust=10, understanding=8, intimacy=12, 
                             dependence=6, resonance=9)
    
    assert dims.total() == 45
    assert dims.average() == 9
    assert dims.strongest_dimension()[0] == EmotionDimension.INTIMACY
    assert dims.weakest_dimension()[0] == EmotionDimension.DEPENDENCE
    print("✓ 情感维度测试通过")


def test_memory_storage():
    """测试记忆存储"""
    service = MemoryService()
    
    memory = EmotionMemory(
        id="test_mem_001",
        memory_type=MemoryType.DAILY,
        content="测试记忆内容",
        emotion_score=5,
        dimensions_delta={EmotionDimension.TRUST: 1.0}
    )
    
    service.store_memory("soul_001", memory)
    memories = service.get_memories("soul_001")
    
    assert len(memories) == 1
    assert memories[0].content == "测试记忆内容"
    print("✓ 记忆存储测试通过")


def test_contract_level():
    """测试契约等级"""
    assert ContractLevel.from_score(50) == ContractLevel.ACQUAINTANCE
    assert ContractLevel.from_score(200) == ContractLevel.FAMILIAR
    assert ContractLevel.from_score(500) == ContractLevel.TRUST
    assert ContractLevel.from_score(3000) == ContractLevel.SOULMATE
    print("✓ 契约等级测试通过")


def test_emotion_analysis():
    """测试情感分析"""
    result = EmotionEngine.analyze_text_emotion("我非常信任你，你让我感到很安心")
    
    assert EmotionDimension.TRUST in result
    assert result[EmotionDimension.TRUST] > 0
    print("✓ 情感分析测试通过")


def test_contract_service():
    """测试契约服务"""
    service = ContractService()

    contract = service.get_or_create_contract("soul_001", "user_001")
    assert contract.level == ContractLevel.ACQUAINTANCE

    new_level = service.update_score("soul_001", 200)
    assert new_level == ContractLevel.FAMILIAR
    print("✓ 契约服务测试通过")


def test_contract_level_edge_cases():
    """测试契约等级边界情况"""
    # 测试边界值
    assert ContractLevel.from_score(0) == ContractLevel.ACQUAINTANCE
    assert ContractLevel.from_score(100) == ContractLevel.ACQUAINTANCE
    assert ContractLevel.from_score(101) == ContractLevel.FAMILIAR
    assert ContractLevel.from_score(300) == ContractLevel.FAMILIAR
    assert ContractLevel.from_score(301) == ContractLevel.TRUST
    assert ContractLevel.from_score(10000) == ContractLevel.SOULMATE
    print("✓ 契约等级边界测试通过")


def test_memory_expiration():
    """测试记忆过期机制"""
    service = MemoryService()

    # 创建一个已过期的记忆
    expired_memory = EmotionMemory(
        id="test_mem_expired",
        memory_type=MemoryType.DAILY,
        content="过期的记忆",
        emotion_score=5,
        dimensions_delta={EmotionDimension.TRUST: 1.0},
        is_permanent=False,
        expires_at=datetime.now() - timedelta(days=1)  # 昨天过期
    )

    # 创建一个永久记忆
    permanent_memory = EmotionMemory(
        id="test_mem_permanent",
        memory_type=MemoryType.IMPORTANT,
        content="永久记忆",
        emotion_score=10,
        dimensions_delta={EmotionDimension.TRUST: 2.0},
        is_permanent=True
    )

    service.store_memory("soul_test", expired_memory)
    service.store_memory("soul_test", permanent_memory)

    # 不包含过期记忆
    memories = service.get_memories("soul_test", include_expired=False)
    assert len(memories) == 1
    assert memories[0].is_permanent == True

    # 包含过期记忆
    all_memories = service.get_memories("soul_test", include_expired=True)
    assert len(all_memories) == 2

    # 测试过期检查
    assert expired_memory.is_expired() == True
    assert permanent_memory.is_expired() == False
    print("✓ 记忆过期机制测试通过")


def test_ceremony_flow():
    """测试契约仪式完整流程"""
    service = ContractService()

    # 创建契约
    contract = service.get_or_create_contract("soul_ceremony", "user_ceremony")

    # 初始状态检查
    readiness = service.check_ceremony_readiness("soul_ceremony")
    assert readiness["ready"] == False

    # 模拟达到羁绊等级
    service.update_score("soul_ceremony", 1600)

    # 手动设置等级为BOND（因为from_score会自动计算）
    contract.level = ContractLevel.BOND

    # 再次检查准备状态
    readiness = service.check_ceremony_readiness("soul_ceremony")
    assert readiness["ready"] == True

    # 启动仪式
    ceremony_result = service.initiate_ceremony("soul_ceremony")
    assert ceremony_result["success"] == True

    # 完成仪式
    complete_result = service.complete_ceremony(
        ceremony_result["ceremony_id"],
        "用户誓言",
        "灵魂誓言"
    )
    assert complete_result["success"] == True
    assert contract.ceremony_completed == True
    assert contract.level == ContractLevel.CONTRACT
    assert len(contract.tokens) == 1

    # 再次检查准备状态（已完成）
    readiness = service.check_ceremony_readiness("soul_ceremony")
    assert readiness["ready"] == False
    assert "已完成" in readiness["reason"]
    print("✓ 契约仪式流程测试通过")


def test_negative_score():
    """测试负分处理"""
    service = ContractService()
    service.get_or_create_contract("soul_negative", "user_negative")

    # 测试负分不会导致分数低于0
    service.update_score("soul_negative", -100)
    contract = service.contracts["soul_negative"]
    assert contract.total_score >= 0
    print("✓ 负分处理测试通过")


def run_tests():
    """运行所有测试"""
    print("\n运行单元测试...")
    print("-" * 40)
    test_emotion_dimensions()
    test_memory_storage()
    test_contract_level()
    test_contract_level_edge_cases()
    test_emotion_analysis()
    test_contract_service()
    test_memory_expiration()
    test_ceremony_flow()
    test_negative_score()
    print("-" * 40)
    print("所有测试通过! ✓\n")


# ==================== 主程序 ====================

if __name__ == "__main__":
    # 运行测试
    run_tests()
    
    # 运行演示
    demo_heart_contract()
