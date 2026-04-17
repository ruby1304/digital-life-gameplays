"""
灵魂村落 (Soul Village) - 基础Demo

这个demo展示了灵魂村落系统的核心功能：
1. 村落创建与管理
2. 灵魂社交关系系统
3. 建筑系统与村落发展
4. 村落事件与集体活动
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set, Tuple
from enum import Enum
from datetime import datetime, timedelta
import json
import random


# ==================== 枚举定义 ====================

class VillageStyle(Enum):
    """村落风格"""
    FOREST = "森林村落"
    MOUNTAIN = "山间村落"
    SEASIDE = "海滨村落"
    PLAINS = "平原村落"
    SKY = "天空村落"


class BuildingType(Enum):
    """建筑类型"""
    RESIDENCE = "居住区"
    ACADEMY = "学院"
    SHOP = "商店"
    THEATER = "剧场"
    SHRINE = "神社"
    FARM = "农田"
    PLAZA = "广场"
    LIBRARY = "图书馆"
    WORKSHOP = "工坊"


class RelationshipType(Enum):
    """关系类型"""
    NEIGHBOR = "邻居"
    ACQUAINTANCE = "相识"
    FRIEND = "朋友"
    CLOSE_FRIEND = "挚友"
    LOVER = "恋人"
    MENTOR_MENTEE = "师徒"
    RIVAL = "竞争对手"
    STRANGER = "陌生人"


class EventType(Enum):
    """事件类型"""
    DAILY = "日常事件"
    FESTIVAL = "村落节日"
    COLLECTIVE = "集体活动"
    EMERGENCY = "突发事件"
    CONSTRUCTION = "建设事件"


# ==================== 数据类定义 ====================

@dataclass
class Position:
    """位置坐标"""
    x: int
    y: int
    
    def distance_to(self, other: 'Position') -> float:
        """计算距离"""
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
    
    def is_adjacent(self, other: 'Position') -> bool:
        """是否相邻"""
        return self.distance_to(other) <= 1.5  # 对角线也算相邻


@dataclass
class VillageResources:
    """村落资源"""
    gold: int = 1000           # 金币
    food: int = 500            # 食物
    materials: int = 200       # 材料
    happiness: int = 50        # 幸福度 (0-100)
    culture: int = 0           # 文化值
    
    def to_dict(self) -> Dict:
        return {
            "gold": self.gold,
            "food": self.food,
            "materials": self.materials,
            "happiness": self.happiness,
            "culture": self.culture
        }


@dataclass
class Building:
    """建筑"""
    id: str
    building_type: BuildingType
    name: str
    level: int = 1
    position: Optional[Position] = None
    capacity: int = 0
    efficiency: float = 1.0
    unlocked: bool = True
    
    def upgrade_cost(self) -> Dict[str, int]:
        """升级成本"""
        base_cost = {
            BuildingType.RESIDENCE: {"gold": 200, "materials": 50},
            BuildingType.ACADEMY: {"gold": 300, "materials": 100},
            BuildingType.SHOP: {"gold": 250, "materials": 80},
            BuildingType.THEATER: {"gold": 400, "materials": 120},
            BuildingType.SHRINE: {"gold": 500, "materials": 150},
            BuildingType.FARM: {"gold": 150, "materials": 30},
            BuildingType.PLAZA: {"gold": 350, "materials": 100},
        }
        
        cost = base_cost.get(self.building_type, {"gold": 200, "materials": 50})
        return {k: v * self.level for k, v in cost.items()}
    
    def upgrade(self) -> bool:
        """执行升级"""
        if self.level < 5:
            self.level += 1
            self.capacity += 2
            self.efficiency += 0.1
            return True
        return False
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "type": self.building_type.value,
            "name": self.name,
            "level": self.level,
            "position": {"x": self.position.x, "y": self.position.y} if self.position else None,
            "capacity": self.capacity,
            "efficiency": self.efficiency
        }


@dataclass
class SoulProfile:
    """灵魂档案（简化版）"""
    id: str
    name: str
    personality: str  # outgoing, shy, creative, logical, kind
    interests: List[str]
    
    def compatibility_with(self, other: 'SoulProfile') -> float:
        """计算兼容性"""
        # 共同兴趣加分
        common_interests = len(set(self.interests) & set(other.interests))
        return 0.3 + common_interests * 0.2


@dataclass
class Relationship:
    """社交关系"""
    soul_a_id: str
    soul_b_id: str
    relationship_type: RelationshipType
    affinity: float = 0.0  # 好感度 0-100
    interaction_count: int = 0
    special_memories: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def update_affinity(self, delta: float) -> None:
        """更新好感度"""
        self.affinity = max(0, min(100, self.affinity + delta))
        self.updated_at = datetime.now()
        
        # 根据好感度更新关系类型
        if self.affinity >= 80:
            self.relationship_type = RelationshipType.CLOSE_FRIEND
        elif self.affinity >= 60:
            self.relationship_type = RelationshipType.FRIEND
        elif self.affinity >= 30:
            self.relationship_type = RelationshipType.ACQUAINTANCE
    
    def to_dict(self) -> Dict:
        return {
            "souls": [self.soul_a_id, self.soul_b_id],
            "type": self.relationship_type.value,
            "affinity": round(self.affinity, 1),
            "interactions": self.interaction_count,
            "memories": self.special_memories
        }


@dataclass
class VillageEvent:
    """村落事件"""
    id: str
    event_type: EventType
    title: str
    description: str
    participants: List[str]
    effects: Dict
    started_at: datetime = field(default_factory=datetime.now)
    ended_at: Optional[datetime] = None
    completed: bool = False
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "type": self.event_type.value,
            "title": self.title,
            "description": self.description,
            "participants": self.participants,
            "effects": self.effects,
            "completed": self.completed
        }


# ==================== 村落类 ====================

class Village:
    """灵魂村落"""
    
    def __init__(self, name: str, style: VillageStyle, user_id: str):
        self.id = f"village_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        self.name = name
        self.style = style
        self.user_id = user_id
        self.level = 1
        self.population = 0
        self.max_population = 10
        
        # 资源
        self.resources = VillageResources()
        
        # 建筑
        self.buildings: Dict[str, Building] = {}
        self._init_buildings()
        
        # 灵魂
        self.souls: Dict[str, SoulProfile] = {}
        self.residences: Dict[str, Position] = {}  # soul_id -> position
        
        # 社交关系
        self.relationships: Dict[Tuple[str, str], Relationship] = {}
        
        # 事件
        self.events: List[VillageEvent] = []
        self.active_events: List[str] = []
        
        # 统计
        self.total_interactions = 0
        self.festivals_held = 0
        self.created_at = datetime.now()
    
    def _init_buildings(self):
        """初始化基础建筑"""
        # 广场 - 中心
        plaza = Building(
            id="building_plaza",
            building_type=BuildingType.PLAZA,
            name="村落广场",
            position=Position(5, 5),
            capacity=20
        )
        self.buildings[plaza.id] = plaza
        
        # 初始居住区
        for i in range(2):
            residence = Building(
                id=f"building_residence_{i}",
                building_type=BuildingType.RESIDENCE,
                name=f"居住区 {chr(65+i)}",
                position=Position(3 + i * 4, 3),
                capacity=5
            )
            self.buildings[residence.id] = residence
        
        # 农田
        farm = Building(
            id="building_farm",
            building_type=BuildingType.FARM,
            name="公共农田",
            position=Position(7, 7),
            capacity=10
        )
        self.buildings[farm.id] = farm
    
    def add_soul(self, soul: SoulProfile, position: Optional[Position] = None) -> Dict:
        """添加灵魂到村落"""
        if self.population >= self.max_population:
            return {"success": False, "message": "村落人口已满"}
        
        if soul.id in self.souls:
            return {"success": False, "message": "灵魂已在村落中"}
        
        # 分配位置
        if position is None:
            # 自动分配到居住区
            for building in self.buildings.values():
                if building.building_type == BuildingType.RESIDENCE:
                    if building.position:
                        position = Position(
                            building.position.x + random.randint(-1, 1),
                            building.position.y + random.randint(-1, 1)
                        )
                        break
        
        self.souls[soul.id] = soul
        self.residences[soul.id] = position
        self.population += 1
        
        # 初始化与其他灵魂的关系
        for other_id in self.souls:
            if other_id != soul.id:
                self._create_relationship(soul.id, other_id)
        
        return {
            "success": True,
            "message": f"{soul.name} 加入了村落",
            "position": {"x": position.x, "y": position.y} if position else None
        }
    
    def remove_soul(self, soul_id: str) -> Dict:
        """移除灵魂"""
        if soul_id not in self.souls:
            return {"success": False, "message": "灵魂不在村落中"}
        
        soul = self.souls[soul_id]
        del self.souls[soul_id]
        del self.residences[soul_id]
        self.population -= 1
        
        # 清理关系
        keys_to_remove = [k for k in self.relationships if soul_id in k]
        for key in keys_to_remove:
            del self.relationships[key]
        
        return {"success": True, "message": f"{soul.name} 离开了村落"}
    
    def _create_relationship(self, soul_a_id: str, soul_b_id: str) -> Relationship:
        """创建关系"""
        key = tuple(sorted([soul_a_id, soul_b_id]))
        if key in self.relationships:
            return self.relationships[key]
        
        # 检查是否相邻
        pos_a = self.residences.get(soul_a_id)
        pos_b = self.residences.get(soul_b_id)
        
        initial_type = RelationshipType.STRANGER
        initial_affinity = 0.0
        
        if pos_a and pos_b and pos_a.is_adjacent(pos_b):
            initial_type = RelationshipType.NEIGHBOR
            initial_affinity = 10.0
        
        relationship = Relationship(
            soul_a_id=soul_a_id,
            soul_b_id=soul_b_id,
            relationship_type=initial_type,
            affinity=initial_affinity
        )
        
        self.relationships[key] = relationship
        return relationship
    
    def process_interaction(self, soul_a_id: str, soul_b_id: str, 
                           interaction_type: str) -> Dict:
        """处理灵魂互动"""
        if soul_a_id not in self.souls or soul_b_id not in self.souls:
            return {"success": False, "message": "灵魂不存在"}
        
        key = tuple(sorted([soul_a_id, soul_b_id]))
        if key not in self.relationships:
            self._create_relationship(soul_a_id, soul_b_id)
        
        relationship = self.relationships[key]
        soul_a = self.souls[soul_a_id]
        soul_b = self.souls[soul_b_id]
        
        # 计算互动效果
        compatibility = soul_a.compatibility_with(soul_b)
        
        interaction_effects = {
            "chat": {"affinity": 5, "happiness": 2},
            "gift": {"affinity": 10, "happiness": 5},
            "activity": {"affinity": 8, "happiness": 8},
            "help": {"affinity": 12, "happiness": 3},
            "conflict": {"affinity": -15, "happiness": -10}
        }
        
        effect = interaction_effects.get(interaction_type, {"affinity": 3, "happiness": 1})
        
        # 应用兼容性修正
        affinity_change = effect["affinity"] * (0.5 + compatibility * 0.5)
        relationship.update_affinity(affinity_change)
        relationship.interaction_count += 1
        
        # 更新村落幸福度
        self.resources.happiness = min(100, self.resources.happiness + effect["happiness"] * 0.1)
        
        self.total_interactions += 1
        
        return {
            "success": True,
            "interaction": interaction_type,
            "affinity_change": round(affinity_change, 1),
            "new_affinity": round(relationship.affinity, 1),
            "relationship_type": relationship.relationship_type.value
        }
    
    def get_soul_relationships(self, soul_id: str) -> List[Dict]:
        """获取灵魂的所有关系"""
        relationships = []
        for key, rel in self.relationships.items():
            if soul_id in key:
                other_id = key[0] if key[1] == soul_id else key[1]
                if other_id in self.souls:
                    relationships.append({
                        "soul_id": other_id,
                        "soul_name": self.souls[other_id].name,
                        **rel.to_dict()
                    })
        
        return sorted(relationships, key=lambda x: x["affinity"], reverse=True)
    
    def build_building(self, building_type: BuildingType, 
                       position: Position, name: str) -> Dict:
        """建造建筑"""
        # 检查成本
        building = Building(
            id=f"building_{building_type.name.lower()}_{len(self.buildings)}",
            building_type=building_type,
            name=name,
            position=position
        )
        
        cost = building.upgrade_cost()
        
        if self.resources.gold < cost["gold"] or self.resources.materials < cost["materials"]:
            return {"success": False, "message": "资源不足"}
        
        # 扣除资源
        self.resources.gold -= cost["gold"]
        self.resources.materials -= cost["materials"]
        
        # 添加建筑
        self.buildings[building.id] = building
        
        # 特殊效果
        if building_type == BuildingType.RESIDENCE:
            self.max_population += 5
        
        return {
            "success": True,
            "message": f"{name} 建造完成",
            "building": building.to_dict()
        }
    
    def upgrade_building(self, building_id: str) -> Dict:
        """升级建筑"""
        if building_id not in self.buildings:
            return {"success": False, "message": "建筑不存在"}
        
        building = self.buildings[building_id]
        cost = building.upgrade_cost()
        
        if self.resources.gold < cost["gold"] or self.resources.materials < cost["materials"]:
            return {"success": False, "message": "资源不足"}
        
        # 扣除资源并升级
        self.resources.gold -= cost["gold"]
        self.resources.materials -= cost["materials"]
        
        old_level = building.level
        building.upgrade()
        
        # 特殊效果
        if building.building_type == BuildingType.RESIDENCE:
            self.max_population += 2
        
        return {
            "success": True,
            "message": f"{building.name} 升级到 {building.level} 级",
            "old_level": old_level,
            "new_level": building.level
        }
    
    def hold_festival(self, festival_type: str) -> Dict:
        """举办节日"""
        festival_costs = {
            "harvest": {"gold": 100, "food": 50},
            "culture": {"gold": 150, "materials": 30},
            "friendship": {"gold": 80, "food": 30}
        }
        
        cost = festival_costs.get(festival_type, {"gold": 100})
        
        if self.resources.gold < cost.get("gold", 0):
            return {"success": False, "message": "资源不足"}
        
        # 扣除资源
        self.resources.gold -= cost.get("gold", 0)
        self.resources.food -= cost.get("food", 0)
        
        # 创建节日事件
        festival_names = {
            "harvest": "丰收节",
            "culture": "文化节",
            "friendship": "友谊节"
        }
        
        event = VillageEvent(
            id=f"festival_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            event_type=EventType.FESTIVAL,
            title=festival_names.get(festival_type, "村落节日"),
            description=f"全村庆祝{festival_names.get(festival_type, '节日')}",
            participants=list(self.souls.keys()),
            effects={
                "happiness": 20,
                "culture": 10,
                "affinity_boost": 5
            }
        )
        
        self.events.append(event)
        self.festivals_held += 1
        
        # 应用效果
        self.resources.happiness = min(100, self.resources.happiness + 20)
        self.resources.culture += 10
        
        # 提升所有关系
        for rel in self.relationships.values():
            rel.update_affinity(5)
        
        return {
            "success": True,
            "festival": event.to_dict(),
            "participants_count": len(event.participants)
        }
    
    def generate_daily_events(self) -> List[VillageEvent]:
        """生成日常事件"""
        events = []
        
        # 随机互动事件
        if len(self.souls) >= 2:
            soul_ids = list(self.souls.keys())
            for _ in range(min(3, len(soul_ids) // 2)):
                a, b = random.sample(soul_ids, 2)
                
                interactions = ["chat", "activity", "help"]
                interaction = random.choice(interactions)
                
                self.process_interaction(a, b, interaction)
        
        # 资源生产
        for building in self.buildings.values():
            if building.building_type == BuildingType.FARM:
                production = int(10 * building.efficiency)
                self.resources.food += production
        
        return events
    
    def get_village_stats(self) -> Dict:
        """获取村落统计"""
        # 计算社交网络密度
        max_relationships = self.population * (self.population - 1) / 2 if self.population > 1 else 0
        actual_relationships = len(self.relationships)
        network_density = actual_relationships / max_relationships if max_relationships > 0 else 0
        
        # 计算平均好感度
        avg_affinity = 0
        if self.relationships:
            avg_affinity = sum(r.affinity for r in self.relationships.values()) / len(self.relationships)
        
        return {
            "id": self.id,
            "name": self.name,
            "style": self.style.value,
            "level": self.level,
            "population": self.population,
            "max_population": self.max_population,
            "resources": self.resources.to_dict(),
            "buildings_count": len(self.buildings),
            "relationships_count": len(self.relationships),
            "network_density": round(network_density, 2),
            "avg_affinity": round(avg_affinity, 1),
            "total_interactions": self.total_interactions,
            "festivals_held": self.festivals_held,
            "age_days": (datetime.now() - self.created_at).days + 1
        }
    
    def get_social_network(self) -> Dict:
        """获取社交网络图"""
        nodes = [
            {
                "id": soul_id,
                "name": soul.name,
                "position": {"x": self.residences[soul_id].x, "y": self.residences[soul_id].y}
            }
            for soul_id, soul in self.souls.items()
        ]
        
        edges = [
            {
                "source": key[0],
                "target": key[1],
                "affinity": rel.affinity,
                "type": rel.relationship_type.value
            }
            for key, rel in self.relationships.items()
        ]
        
        return {"nodes": nodes, "edges": edges}


# ==================== 演示函数 ====================

def demo_soul_village():
    """演示灵魂村落系统"""
    
    print("=" * 60)
    print("        灵魂村落系统 Demo")
    print("=" * 60)
    
    # 1. 创建村落
    print("\n【步骤1】创建村落")
    print("-" * 40)
    village = Village(
        name="星光村",
        style=VillageStyle.FOREST,
        user_id="user_001"
    )
    print(f"村落名称: {village.name}")
    print(f"村落风格: {village.style.value}")
    print(f"初始人口上限: {village.max_population}")
    print(f"初始建筑: {[b.name for b in village.buildings.values()]}")
    
    # 2. 添加灵魂
    print("\n【步骤2】邀请灵魂入住")
    print("-" * 40)
    souls_data = [
        ("soul_001", "小光", "outgoing", ["music", "art"]),
        ("soul_002", "小影", "shy", ["reading", "art"]),
        ("soul_003", "小风", "creative", ["music", "travel"]),
        ("soul_004", "小云", "kind", ["cooking", "gardening"]),
        ("soul_005", "小月", "logical", ["reading", "chess"]),
    ]
    
    for soul_id, name, personality, interests in souls_data:
        soul = SoulProfile(
            id=soul_id,
            name=name,
            personality=personality,
            interests=interests
        )
        result = village.add_soul(soul)
        print(f"  {name}: {result['message']}")
    
    print(f"\n当前人口: {village.population}/{village.max_population}")
    
    # 3. 社交互动
    print("\n【步骤3】灵魂社交互动")
    print("-" * 40)
    
    # 小光和小影聊天
    result = village.process_interaction("soul_001", "soul_002", "chat")
    print(f"小光和小影聊天: 好感度+{result['affinity_change']} → {result['new_affinity']}")
    
    # 小光送礼物给小风
    result = village.process_interaction("soul_001", "soul_003", "gift")
    print(f"小光送礼物给小风: 好感度+{result['affinity_change']} → {result['new_affinity']}")
    
    # 小云帮助小月
    result = village.process_interaction("soul_004", "soul_005", "help")
    print(f"小云帮助小月: 好感度+{result['affinity_change']} → {result['new_affinity']}")
    
    # 4. 查看关系网络
    print("\n【步骤4】查看社交网络")
    print("-" * 40)
    network = village.get_social_network()
    print(f"节点数: {len(network['nodes'])}")
    print(f"关系数: {len(network['edges'])}")
    
    print("\n小光的关系:")
    relationships = village.get_soul_relationships("soul_001")
    for rel in relationships:
        print(f"  - {rel['soul_name']}: {rel['type']} (好感度: {rel['affinity']})")
    
    # 5. 建造建筑
    print("\n【步骤5】建造新建筑")
    print("-" * 40)
    result = village.build_building(
        BuildingType.ACADEMY,
        Position(4, 6),
        "星光学院"
    )
    print(f"建造结果: {result['message']}")
    
    result = village.build_building(
        BuildingType.SHOP,
        Position(6, 4),
        "村落商店"
    )
    print(f"建造结果: {result['message']}")
    
    print(f"\n当前建筑: {[b.name for b in village.buildings.values()]}")
    
    # 6. 举办节日
    print("\n【步骤6】举办村落节日")
    print("-" * 40)
    result = village.hold_festival("friendship")
    print(f"节日: {result['festival']['title']}")
    print(f"参与人数: {result['participants_count']}")
    print(f"村落幸福度: {village.resources.happiness}")
    
    # 7. 日常事件
    print("\n【步骤7】模拟日常事件")
    print("-" * 40)
    for day in range(3):
        village.generate_daily_events()
        print(f"第{day+1}天: 互动发生, 食物生产, 资源更新")
    
    # 8. 村落统计
    print("\n【步骤8】村落统计总览")
    print("-" * 40)
    stats = village.get_village_stats()
    print(f"村落: {stats['name']} ({stats['style']})")
    print(f"人口: {stats['population']}/{stats['max_population']}")
    print(f"资源: {stats['resources']}")
    print(f"建筑数: {stats['buildings_count']}")
    print(f"关系数: {stats['relationships_count']}")
    print(f"网络密度: {stats['network_density']}")
    print(f"平均好感度: {stats['avg_affinity']}")
    print(f"总互动次数: {stats['total_interactions']}")
    print(f"举办节日: {stats['festivals_held']}")
    
    print("\n" + "=" * 60)
    print("        Demo 完成")
    print("=" * 60)


# ==================== 测试用例 ====================

def test_village_system():
    """测试村落系统"""
    print("\n运行测试用例...")
    
    # 创建村落
    village = Village("测试村", VillageStyle.PLAINS, "test_user")
    assert village.population == 0
    assert len(village.buildings) > 0
    print("✓ 村落创建测试通过")
    
    # 添加灵魂
    soul = SoulProfile("test_soul", "测试者", "outgoing", ["test"])
    result = village.add_soul(soul)
    assert result["success"] == True
    assert village.population == 1
    print("✓ 灵魂添加测试通过")
    
    # 添加第二个灵魂
    soul2 = SoulProfile("test_soul2", "测试者2", "shy", ["test"])
    village.add_soul(soul2)
    
    # 测试互动
    result = village.process_interaction("test_soul", "test_soul2", "chat")
    assert result["success"] == True
    assert result["new_affinity"] > 0
    print("✓ 互动系统测试通过")
    
    # 测试建筑
    result = village.build_building(BuildingType.THEATER, Position(3, 3), "测试剧场")
    assert result["success"] == True
    print("✓ 建筑系统测试通过")
    
    # 测试节日
    result = village.hold_festival("harvest")
    assert result["success"] == True
    assert village.festivals_held == 1
    print("✓ 节日系统测试通过")
    
    # 测试统计
    stats = village.get_village_stats()
    assert stats["population"] == 2
    assert stats["total_interactions"] > 0
    print("✓ 统计系统测试通过")
    
    print("\n所有测试通过！")


if __name__ == "__main__":
    demo_soul_village()
    test_village_system()
