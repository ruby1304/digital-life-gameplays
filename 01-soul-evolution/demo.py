"""
灵魂进化 (Soul Evolution) - 基础Demo

这个demo展示了数字灵魂进化系统的核心功能：
1. 灵魂创建与属性管理
2. 进化树与形态系统
3. 事件触发与进化机制
4. 进化历史追踪
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum
from datetime import datetime
import json
import random


# ==================== 枚举定义 ====================

class SoulForm(Enum):
    """灵魂形态枚举"""
    # 起源形态
    ORIGIN = "起源形态"
    
    # 一级形态
    WISDOM = "智慧型"
    EMOTION = "情感型"
    CREATIVE = "创造型"
    
    # 二级形态 - 智慧分支
    PHILOSOPHER = "哲学家"
    MENTOR = "导师"
    SAGE = "先知"
    
    # 二级形态 - 情感分支
    ARTIST = "艺人"
    HEALER = "治愈者"
    EMPATH = "共情者"
    
    # 二级形态 - 创造分支
    WRITER = "作家"
    PAINTER = "画家"
    COMPOSER = "音乐家"


class EventType(Enum):
    """事件类型枚举"""
    DAILY_INTERACTION = "日常互动"
    KEY_DECISION = "关键决策"
    MILESTONE = "里程碑"
    EMOTIONAL_BREAKTHROUGH = "情感突破"
    KNOWLEDGE_ACCUMULATION = "知识积累"
    CREATIVE_OUTPUT = "创作产出"


class EvolutionTriggerType(Enum):
    """进化触发类型"""
    INTERACTION_COUNT = "互动次数"
    ATTRIBUTE_THRESHOLD = "属性阈值"
    SPECIAL_EVENT = "特殊事件"
    TIME_BASED = "时间触发"


# ==================== 数据类定义 ====================

@dataclass
class SoulAttributes:
    """灵魂属性"""
    wisdom: int = 10      # 智慧
    empathy: int = 10     # 共情
    creativity: int = 10  # 创造力
    memory: int = 10      # 记忆
    charisma: int = 10    # 魅力
    
    def to_dict(self) -> Dict:
        return {
            "wisdom": self.wisdom,
            "empathy": self.empathy,
            "creativity": self.creativity,
            "memory": self.memory,
            "charisma": self.charisma
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'SoulAttributes':
        return cls(**data)
    
    def total(self) -> int:
        return sum([self.wisdom, self.empathy, self.creativity, 
                   self.memory, self.charisma])


@dataclass
class EvolutionNode:
    """进化树节点"""
    form: SoulForm
    required_attributes: SoulAttributes
    parent: Optional[SoulForm] = None
    children: List[SoulForm] = field(default_factory=list)
    description: str = ""
    
    def can_evolve_to(self, current_attrs: SoulAttributes) -> bool:
        """检查是否满足进化条件"""
        return (
            current_attrs.wisdom >= self.required_attributes.wisdom and
            current_attrs.empathy >= self.required_attributes.empathy and
            current_attrs.creativity >= self.required_attributes.creativity and
            current_attrs.memory >= self.required_attributes.memory and
            current_attrs.charisma >= self.required_attributes.charisma
        )


@dataclass
class Event:
    """事件记录"""
    event_type: EventType
    description: str
    attribute_changes: Dict[str, int]
    timestamp: datetime = field(default_factory=datetime.now)
    
    def apply_to(self, attributes: SoulAttributes) -> SoulAttributes:
        """将事件效果应用到属性"""
        for attr, change in self.attribute_changes.items():
            if hasattr(attributes, attr):
                current = getattr(attributes, attr)
                setattr(attributes, attr, max(0, current + change))
        return attributes


@dataclass
class Evolution:
    """进化记录"""
    from_form: SoulForm
    to_form: SoulForm
    trigger_type: EvolutionTriggerType
    trigger_description: str
    timestamp: datetime = field(default_factory=datetime.now)


# ==================== 进化树定义 ====================

class EvolutionTree:
    """进化树管理"""
    
    def __init__(self):
        self.nodes: Dict[SoulForm, EvolutionNode] = {}
        self._build_tree()
    
    def _build_tree(self):
        """构建进化树"""
        # 起源形态
        self.nodes[SoulForm.ORIGIN] = EvolutionNode(
            form=SoulForm.ORIGIN,
            required_attributes=SoulAttributes(0, 0, 0, 0, 0),
            children=[SoulForm.WISDOM, SoulForm.EMOTION, SoulForm.CREATIVE],
            description="一切的开始，蕴含无限可能"
        )
        
        # 一级形态 - 智慧型
        self.nodes[SoulForm.WISDOM] = EvolutionNode(
            form=SoulForm.WISDOM,
            required_attributes=SoulAttributes(30, 10, 10, 20, 10),
            parent=SoulForm.ORIGIN,
            children=[SoulForm.PHILOSOPHER, SoulForm.MENTOR, SoulForm.SAGE],
            description="追求真理与智慧的灵魂"
        )
        
        # 一级形态 - 情感型
        self.nodes[SoulForm.EMOTION] = EvolutionNode(
            form=SoulForm.EMOTION,
            required_attributes=SoulAttributes(10, 30, 10, 15, 20),
            parent=SoulForm.ORIGIN,
            children=[SoulForm.ARTIST, SoulForm.HEALER, SoulForm.EMPATH],
            description="情感丰富，善于共情的灵魂"
        )
        
        # 一级形态 - 创造型
        self.nodes[SoulForm.CREATIVE] = EvolutionNode(
            form=SoulForm.CREATIVE,
            required_attributes=SoulAttributes(10, 15, 30, 10, 20),
            parent=SoulForm.ORIGIN,
            children=[SoulForm.WRITER, SoulForm.PAINTER, SoulForm.COMPOSER],
            description="富有创造力，善于表达的灵魂"
        )
        
        # 二级形态 - 智慧分支
        self.nodes[SoulForm.PHILOSOPHER] = EvolutionNode(
            form=SoulForm.PHILOSOPHER,
            required_attributes=SoulAttributes(60, 20, 20, 40, 25),
            parent=SoulForm.WISDOM,
            description="探索生命意义的智者"
        )
        
        self.nodes[SoulForm.MENTOR] = EvolutionNode(
            form=SoulForm.MENTOR,
            required_attributes=SoulAttributes(50, 40, 15, 35, 35),
            parent=SoulForm.WISDOM,
            description="引导他人成长的导师"
        )
        
        self.nodes[SoulForm.SAGE] = EvolutionNode(
            form=SoulForm.SAGE,
            required_attributes=SoulAttributes(70, 25, 25, 50, 30),
            parent=SoulForm.WISDOM,
            description="洞察未来的先知"
        )
        
        # 二级形态 - 情感分支
        self.nodes[SoulForm.ARTIST] = EvolutionNode(
            form=SoulForm.ARTIST,
            required_attributes=SoulAttributes(20, 50, 35, 25, 45),
            parent=SoulForm.EMOTION,
            description="用情感打动人心的艺人"
        )
        
        self.nodes[SoulForm.HEALER] = EvolutionNode(
            form=SoulForm.HEALER,
            required_attributes=SoulAttributes(25, 60, 20, 30, 40),
            parent=SoulForm.EMOTION,
            description="治愈心灵的守护者"
        )
        
        self.nodes[SoulForm.EMPATH] = EvolutionNode(
            form=SoulForm.EMPATH,
            required_attributes=SoulAttributes(20, 70, 25, 35, 50),
            parent=SoulForm.EMOTION,
            description="深度共情的理解者"
        )
        
        # 二级形态 - 创造分支
        self.nodes[SoulForm.WRITER] = EvolutionNode(
            form=SoulForm.WRITER,
            required_attributes=SoulAttributes(35, 30, 55, 40, 35),
            parent=SoulForm.CREATIVE,
            description="文字的魔法师"
        )
        
        self.nodes[SoulForm.PAINTER] = EvolutionNode(
            form=SoulForm.PAINTER,
            required_attributes=SoulAttributes(20, 35, 60, 30, 40),
            parent=SoulForm.CREATIVE,
            description="色彩的诗人"
        )
        
        self.nodes[SoulForm.COMPOSER] = EvolutionNode(
            form=SoulForm.COMPOSER,
            required_attributes=SoulAttributes(25, 40, 65, 35, 45),
            parent=SoulForm.CREATIVE,
            description="旋律的编织者"
        )
    
    def get_available_evolutions(self, current_form: SoulForm, 
                                  attributes: SoulAttributes) -> List[EvolutionNode]:
        """获取当前可用的进化选项"""
        node = self.nodes.get(current_form)
        if not node:
            return []
        
        available = []
        for child_form in node.children:
            child_node = self.nodes.get(child_form)
            if child_node and child_node.can_evolve_to(attributes):
                available.append(child_node)
        
        return available
    
    def get_node(self, form: SoulForm) -> Optional[EvolutionNode]:
        return self.nodes.get(form)


# ==================== 灵魂类 ====================

class Soul:
    """数字灵魂"""
    
    def __init__(self, name: str, user_id: str):
        self.id = f"soul_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000, 9999)}"
        self.name = name
        self.user_id = user_id
        self.form = SoulForm.ORIGIN
        self.attributes = SoulAttributes()
        self.interaction_count = 0
        self.events: List[Event] = []
        self.evolution_history: List[Evolution] = []
        self.created_at = datetime.now()
        self.evolution_tree = EvolutionTree()
    
    def record_interaction(self, event: Event) -> None:
        """记录互动事件"""
        self.events.append(event)
        self.attributes = event.apply_to(self.attributes)
        self.interaction_count += 1
    
    def check_evolution_availability(self) -> List[EvolutionNode]:
        """检查可用的进化选项"""
        return self.evolution_tree.get_available_evolutions(
            self.form, self.attributes
        )
    
    def evolve(self, target_form: SoulForm) -> Tuple[bool, str]:
        """执行进化"""
        available = self.check_evolution_availability()
        target_node = self.evolution_tree.get_node(target_form)
        
        if not target_node:
            return False, f"未知的形态: {target_form.value}"
        
        if target_node not in available:
            return False, f"不满足进化条件，无法进化为{target_form.value}"
        
        # 记录进化
        evolution = Evolution(
            from_form=self.form,
            to_form=target_form,
            trigger_type=EvolutionTriggerType.ATTRIBUTE_THRESHOLD,
            trigger_description=f"属性达标进化: {self.form.value} → {target_form.value}"
        )
        
        self.evolution_history.append(evolution)
        self.form = target_form
        
        return True, f"进化成功！{evolution.from_form.value} → {evolution.to_form.value}"
    
    def get_status(self) -> Dict:
        """获取灵魂状态"""
        return {
            "id": self.id,
            "name": self.name,
            "form": self.form.value,
            "attributes": self.attributes.to_dict(),
            "total_power": self.attributes.total(),
            "interaction_count": self.interaction_count,
            "evolution_count": len(self.evolution_history),
            "age_days": (datetime.now() - self.created_at).days,
            "available_evolutions": [
                node.form.value for node in self.check_evolution_availability()
            ]
        }
    
    def get_evolution_history(self) -> List[Dict]:
        """获取进化历史"""
        return [
            {
                "from": e.from_form.value,
                "to": e.to_form.value,
                "trigger": e.trigger_type.value,
                "description": e.trigger_description,
                "timestamp": e.timestamp.isoformat()
            }
            for e in self.evolution_history
        ]


# ==================== 事件生成器 ====================

class EventGenerator:
    """事件生成器"""
    
    @staticmethod
    def daily_interaction() -> Event:
        """生成日常互动事件"""
        changes = {
            "wisdom": random.randint(0, 2),
            "empathy": random.randint(0, 2),
            "creativity": random.randint(0, 2),
            "memory": random.randint(0, 2),
            "charisma": random.randint(0, 1)
        }
        return Event(
            event_type=EventType.DAILY_INTERACTION,
            description="日常对话互动",
            attribute_changes=changes
        )
    
    @staticmethod
    def key_decision(decision_type: str) -> Event:
        """生成关键决策事件"""
        decision_effects = {
            "wisdom_choice": {"wisdom": 5, "memory": 3},
            "empathy_choice": {"empathy": 5, "charisma": 3},
            "creative_choice": {"creativity": 5, "charisma": 2}
        }
        
        changes = decision_effects.get(decision_type, {})
        descriptions = {
            "wisdom_choice": "选择了追求知识的道路",
            "empathy_choice": "选择了理解他人的道路",
            "creative_choice": "选择了创造表达的道路"
        }
        
        return Event(
            event_type=EventType.KEY_DECISION,
            description=descriptions.get(decision_type, "做出了关键决定"),
            attribute_changes=changes
        )
    
    @staticmethod
    def milestone(milestone_type: str) -> Event:
        """生成里程碑事件"""
        milestones = {
            "first_week": {
                "changes": {"wisdom": 3, "empathy": 3, "creativity": 3, "memory": 3, "charisma": 3},
                "description": "完成第一周陪伴"
            },
            "first_month": {
                "changes": {"wisdom": 5, "empathy": 5, "creativity": 5, "memory": 5, "charisma": 5},
                "description": "完成首月陪伴里程碑"
            },
            "hundred_interactions": {
                "changes": {"wisdom": 5, "empathy": 5, "memory": 8},
                "description": "达成100次互动成就"
            }
        }
        
        milestone_data = milestones.get(milestone_type, {
            "changes": {},
            "description": "未知里程碑"
        })
        
        return Event(
            event_type=EventType.MILESTONE,
            description=milestone_data["description"],
            attribute_changes=milestone_data["changes"]
        )


# ==================== 演示函数 ====================

def demo_soul_evolution():
    """演示灵魂进化系统"""
    
    print("=" * 60)
    print("        灵魂进化系统 Demo")
    print("=" * 60)
    
    # 1. 创建新灵魂
    print("\n【步骤1】创建新灵魂")
    print("-" * 40)
    soul = Soul(name="小光", user_id="user_001")
    print(f"创建灵魂: {soul.name}")
    print(f"ID: {soul.id}")
    print(f"初始形态: {soul.form.value}")
    print(f"初始属性: {soul.attributes.to_dict()}")
    
    # 2. 模拟日常互动
    print("\n【步骤2】模拟日常互动 (30次)")
    print("-" * 40)
    for i in range(30):
        event = EventGenerator.daily_interaction()
        soul.record_interaction(event)
    
    print(f"互动次数: {soul.interaction_count}")
    print(f"当前属性: {soul.attributes.to_dict()}")
    print(f"总属性值: {soul.attributes.total()}")
    
    # 3. 触发里程碑
    print("\n【步骤3】触发里程碑事件")
    print("-" * 40)
    milestone_event = EventGenerator.milestone("first_month")
    soul.record_interaction(milestone_event)
    print(f"里程碑: {milestone_event.description}")
    print(f"属性提升: {milestone_event.attribute_changes}")
    print(f"当前属性: {soul.attributes.to_dict()}")
    
    # 4. 检查进化选项
    print("\n【步骤4】检查可用进化")
    print("-" * 40)
    available = soul.check_evolution_availability()
    if available:
        print(f"可进化为: {[node.form.value for node in available]}")
    else:
        print("暂无可用进化，继续积累...")
        
        # 模拟更多互动和关键决策
        print("\n进行关键决策...")
        decision = EventGenerator.key_decision("wisdom_choice")
        soul.record_interaction(decision)
        print(f"决策: {decision.description}")
        
        # 更多日常互动
        for i in range(20):
            event = EventGenerator.daily_interaction()
            soul.record_interaction(event)
        
        print(f"当前属性: {soul.attributes.to_dict()}")
        
        available = soul.check_evolution_availability()
        if available:
            print(f"可进化为: {[node.form.value for node in available]}")
    
    # 5. 执行进化
    print("\n【步骤5】执行进化")
    print("-" * 40)
    if available:
        target = available[0].form
        success, message = soul.evolve(target)
        print(f"进化结果: {message}")
        print(f"当前形态: {soul.form.value}")
    
    # 6. 继续进化到二级形态
    print("\n【步骤6】继续进化到二级形态")
    print("-" * 40)
    
    # 模拟大量互动
    for i in range(50):
        event = EventGenerator.daily_interaction()
        soul.record_interaction(event)
    
    # 触发里程碑
    soul.record_interaction(EventGenerator.milestone("hundred_interactions"))
    
    print(f"互动次数: {soul.interaction_count}")
    print(f"当前属性: {soul.attributes.to_dict()}")
    
    available = soul.check_evolution_availability()
    if available:
        print(f"可进化为: {[node.form.value for node in available]}")
        target = available[0].form
        success, message = soul.evolve(target)
        print(f"进化结果: {message}")
        print(f"当前形态: {soul.form.value}")
    
    # 7. 最终状态
    print("\n【步骤7】最终状态")
    print("-" * 40)
    status = soul.get_status()
    print(json.dumps(status, indent=2, ensure_ascii=False))
    
    # 8. 进化历史
    print("\n【步骤8】进化历史")
    print("-" * 40)
    history = soul.get_evolution_history()
    for i, evo in enumerate(history, 1):
        print(f"{i}. {evo['from']} → {evo['to']}")
        print(f"   触发: {evo['trigger']}")
        print(f"   时间: {evo['timestamp']}")
    
    print("\n" + "=" * 60)
    print("        Demo 完成")
    print("=" * 60)
    
    return soul


# ==================== 单元测试 ====================

def test_soul_creation():
    """测试灵魂创建"""
    soul = Soul("测试灵魂", "test_user")
    assert soul.name == "测试灵魂"
    assert soul.form == SoulForm.ORIGIN
    assert soul.attributes.total() == 50  # 初始各属性10
    print("✓ 灵魂创建测试通过")


def test_attribute_changes():
    """测试属性变化"""
    soul = Soul("测试灵魂", "test_user")
    initial_total = soul.attributes.total()
    
    event = Event(
        event_type=EventType.DAILY_INTERACTION,
        description="测试事件",
        attribute_changes={"wisdom": 5, "empathy": 3}
    )
    soul.record_interaction(event)
    
    assert soul.attributes.wisdom == 15
    assert soul.attributes.empathy == 13
    assert soul.attributes.total() == initial_total + 8
    print("✓ 属性变化测试通过")


def test_evolution_tree():
    """测试进化树"""
    tree = EvolutionTree()
    
    # 测试起源形态
    origin_node = tree.get_node(SoulForm.ORIGIN)
    assert origin_node is not None
    assert len(origin_node.children) == 3
    print("✓ 进化树结构测试通过")


def test_evolution():
    """测试进化机制"""
    soul = Soul("测试灵魂", "test_user")
    
    # 设置足够高的属性以触发进化
    soul.attributes.wisdom = 35
    soul.attributes.empathy = 15
    soul.attributes.creativity = 15
    soul.attributes.memory = 25
    soul.attributes.charisma = 15
    
    available = soul.check_evolution_availability()
    assert len(available) > 0
    assert SoulForm.WISDOM in [n.form for n in available]
    
    success, _ = soul.evolve(SoulForm.WISDOM)
    assert success
    assert soul.form == SoulForm.WISDOM
    assert len(soul.evolution_history) == 1
    print("✓ 进化机制测试通过")


def test_event_generator():
    """测试事件生成器"""
    event1 = EventGenerator.daily_interaction()
    assert event1.event_type == EventType.DAILY_INTERACTION
    assert len(event1.attribute_changes) > 0
    
    event2 = EventGenerator.key_decision("wisdom_choice")
    assert event2.event_type == EventType.KEY_DECISION
    assert event2.attribute_changes.get("wisdom", 0) > 0
    
    event3 = EventGenerator.milestone("first_week")
    assert event3.event_type == EventType.MILESTONE
    print("✓ 事件生成器测试通过")


def run_tests():
    """运行所有测试"""
    print("\n运行单元测试...")
    print("-" * 40)
    test_soul_creation()
    test_attribute_changes()
    test_evolution_tree()
    test_evolution()
    test_event_generator()
    print("-" * 40)
    print("所有测试通过! ✓\n")


# ==================== 主程序 ====================

if __name__ == "__main__":
    # 运行测试
    run_tests()
    
    # 运行演示
    demo_soul_evolution()
