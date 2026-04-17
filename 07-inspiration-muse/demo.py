"""
灵感缪斯 (Inspiration Muse) - 基础Demo

这个demo展示了灵感缪斯系统的核心功能：
1. 灵感类型与生成
2. 缪斯等级系统
3. 灵感风暴模式
4. 个性化灵感流
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
from datetime import datetime
import random


# ==================== 枚举定义 ====================

class InspirationType(Enum):
    """灵感类型"""
    VISUAL = "视觉灵感"
    TEXT = "文字灵感"
    THINKING = "思维灵感"
    LIFE = "生活灵感"
    EMOTION = "情感灵感"


class MuseLevel(Enum):
    """缪斯等级"""
    SEED = (1, "灵感种子", 0)
    SPROUT = (2, "创意萌芽", 500)
    SPRING = (3, "灵感之泉", 1500)
    EYE = (4, "缪斯之眼", 4000)
    MASTER = (5, "创意大师", 8000)
    SOURCE = (6, "灵感之源", 15000)
    
    def __init__(self, level: int, title: str, exp_required: int):
        self.level = level
        self.title = title
        self.exp_required = exp_required


class InspirationQuality(Enum):
    """灵感质量"""
    COMMON = "普通"
    GOOD = "良好"
    EXCELLENT = "优秀"
    MASTER = "大师级"
    LEGENDARY = "传奇"


# ==================== 数据类定义 ====================

@dataclass
class Inspiration:
    """灵感"""
    id: str
    type: InspirationType
    content: str
    quality: InspirationQuality
    tags: List[str]
    source_context: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    used: bool = False
    rating: Optional[int] = None


@dataclass
class InspirationCollection:
    """灵感收藏"""
    inspirations: List[Inspiration] = field(default_factory=list)
    favorites: List[str] = field(default_factory=list)
    
    def add(self, inspiration: Inspiration):
        self.inspirations.append(inspiration)
    
    def favorite(self, inspiration_id: str):
        if inspiration_id not in self.favorites:
            self.favorites.append(inspiration_id)
    
    def get_favorites(self) -> List[Inspiration]:
        return [i for i in self.inspirations if i.id in self.favorites]


# ==================== 缪斯类 ====================

class InspirationMuse:
    """灵感缪斯"""
    
    def __init__(self, soul_id: str, name: str):
        self.soul_id = soul_id
        self.name = name
        self.total_experience = 0
        self.collection = InspirationCollection()
        self.generation_count = 0
        self.created_at = datetime.now()
        
        # 灵感模板库
        self._inspiration_templates = {
            InspirationType.VISUAL: [
                "尝试用{color1}和{color2}的渐变，营造{mood}氛围",
                "考虑{style}风格，强调{element}元素",
                "从{source}汲取灵感，融合{technique}技法",
            ],
            InspirationType.TEXT: [
                "以\"{phrase}\"为开头，讲述一个关于{theme}的故事",
                "用{style}的笔触，描绘{scene}的场景",
                "让{character}在{setting}中，经历{event}",
            ],
            InspirationType.THINKING: [
                "从{angle}角度重新审视问题，或许能发现{insight}",
                "尝试{method}方法，结合{principle}原理",
                "将{concept1}与{concept2}关联，产生新思路",
            ],
            InspirationType.LIFE: [
                "在{time}时，尝试{activity}，会带来{benefit}",
                "用{approach}方式处理{situation}，效果可能更好",
                "给{person}一个{surprise}，让{emotion}充满生活",
            ],
            InspirationType.EMOTION: [
                "用{medium}表达{emotion}，让{target}感受到{sincerity}",
                "在{context}中，{action}能传递{feeling}",
                "以{metaphor}比喻{emotion}，让表达更加{quality}",
            ],
        }
        
        # 填充词库
        self._fill_words = {
            "color1": ["深蓝", "暖橙", "薄荷绿", "玫瑰粉", "星空紫"],
            "color2": ["象牙白", "炭灰", "金黄", "珊瑚红", "午夜蓝"],
            "mood": ["神秘", "温馨", "活力", "宁静", "梦幻"],
            "style": ["极简主义", "复古", "赛博朋克", "自然主义", "抽象"],
            "element": ["光影", "纹理", "空间", "节奏", "对比"],
            "source": ["大自然", "城市建筑", "古典艺术", "科技未来", "人文历史"],
            "technique": ["层叠", "留白", "重复", "渐变", "解构"],
            "phrase": ["那一天的阳光", "如果时间可以倒流", "在某个角落", "当风起时", "记忆中的画面"],
            "theme": ["成长", "离别", "重逢", "梦想", "勇气"],
            "scene": ["雨后的街道", "黄昏的海边", "安静的图书馆", "热闹的市集", "星空下的屋顶"],
            "character": ["一个追梦的少年", "一位沉默的旅人", "一只会说话的猫", "一个失忆的机器人", "一位神秘的老人"],
            "setting": ["漂浮的城市", "时间停止的小镇", "镜中世界", "永夜的森林", "记忆商店"],
            "event": ["一场意外的相遇", "一次重要的选择", "一个隐藏的秘密", "一段被遗忘的记忆", "一次勇敢的冒险"],
            "angle": ["逆向", "宏观", "微观", "历史", "未来"],
            "insight": ["新的可能性", "隐藏的规律", "意想不到的联系", "被忽视的细节", "潜在的机遇"],
            "method": ["头脑风暴", "类比推理", "逆向思维", "系统分析", "直觉判断"],
            "principle": ["第一性原理", "帕累托法则", "系统思维", "迭代优化", "跨界融合"],
            "concept1": ["艺术", "科技", "自然", "人文", "商业"],
            "concept2": ["情感", "功能", "美学", "效率", "体验"],
            "time": ["清晨", "午后", "黄昏", "深夜", "周末"],
            "activity": ["散步", "冥想", "阅读", "写作", "烹饪"],
            "benefit": ["内心的平静", "新的灵感", "更好的状态", "意外的收获", "美好的回忆"],
            "approach": ["轻松幽默", "认真诚恳", "创意十足", "温暖贴心", "出其不意"],
            "situation": ["日常琐事", "人际沟通", "工作压力", "时间管理", "目标规划"],
            "person": ["家人", "朋友", "同事", "自己", "陌生人"],
            "surprise": ["手写卡片", "精心准备的礼物", "一次说走就走的旅行", "一顿特别的晚餐", "一个温暖的拥抱"],
            "emotion": ["感激", "爱意", "歉意", "祝福", "思念"],
            "medium": ["文字", "音乐", "画作", "行动", "礼物"],
            "target": ["对方", "所有人", "特定的人", "自己", "世界"],
            "sincerity": ["真诚", "温暖", "深情", "纯粹", "坚定"],
            "context": ["特别的日子", "平凡的时刻", "困难的时候", "成功的瞬间", "安静的夜晚"],
            "action": ["一个微笑", "一句问候", "一次倾听", "一份陪伴", "一个承诺"],
            "feeling": ["关怀", "支持", "理解", "信任", "爱"],
            "metaphor": ["阳光", "海洋", "星空", "森林", "河流"],
            "quality": ["动人", "深刻", "诗意", "温暖", "有力"],
        }
    
    @property
    def level(self) -> MuseLevel:
        """获取当前等级"""
        for lvl in reversed(list(MuseLevel)):
            if self.total_experience >= lvl.exp_required:
                return lvl
        return MuseLevel.SEED
    
    def _fill_template(self, template: str) -> str:
        """填充模板"""
        result = template
        for key, values in self._fill_words.items():
            placeholder = "{" + key + "}"
            if placeholder in result:
                result = result.replace(placeholder, random.choice(values))
        return result
    
    def _determine_quality(self) -> InspirationQuality:
        """根据等级确定灵感质量"""
        level = self.level.level
        weights = {
            1: [70, 25, 5, 0, 0],
            2: [50, 35, 13, 2, 0],
            3: [30, 40, 25, 5, 0],
            4: [15, 35, 35, 13, 2],
            5: [5, 20, 40, 30, 5],
            6: [0, 10, 30, 40, 20],
        }
        qualities = list(InspirationQuality)
        return random.choices(qualities, weights=weights.get(level, weights[1]))[0]
    
    def generate_inspiration(self, inspiration_type: Optional[InspirationType] = None) -> Inspiration:
        """生成灵感"""
        if inspiration_type is None:
            inspiration_type = random.choice(list(InspirationType))
        
        templates = self._inspiration_templates.get(inspiration_type, ["一个独特的想法..."])
        template = random.choice(templates)
        content = self._fill_template(template)
        quality = self._determine_quality()
        
        inspiration = Inspiration(
            id=f"insp_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000, 9999)}",
            type=inspiration_type,
            content=content,
            quality=quality,
            tags=[inspiration_type.value, quality.value]
        )
        
        self.collection.add(inspiration)
        self.generation_count += 1
        self.total_experience += 5 + quality.level * 2
        
        return inspiration
    
    def inspiration_storm(self, theme: str, count: int = 5) -> List[Inspiration]:
        """灵感风暴"""
        if self.level.level < 3:
            return []
        
        inspirations = []
        for _ in range(count):
            insp = self.generate_inspiration()
            insp.source_context = f"灵感风暴: {theme}"
            inspirations.append(insp)
        
        self.total_experience += count * 3
        return inspirations
    
    def get_personalized_flow(self, count: int = 3) -> List[Inspiration]:
        """获取个性化灵感流"""
        # 根据历史偏好调整类型权重
        type_counts = {}
        for insp in self.collection.inspirations:
            if insp.rating and insp.rating >= 4:
                type_counts[insp.type] = type_counts.get(insp.type, 0) + 1
        
        inspirations = []
        for _ in range(count):
            if type_counts:
                # 偏向高评分类型
                weighted_types = [(t, type_counts.get(t, 1) + 1) for t in InspirationType]
                types, weights = zip(*weighted_types)
                chosen_type = random.choices(types, weights=weights)[0]
            else:
                chosen_type = None
            
            insp = self.generate_inspiration(chosen_type)
            inspirations.append(insp)
        
        return inspirations
    
    def rate_inspiration(self, inspiration_id: str, rating: int):
        """评价灵感"""
        for insp in self.collection.inspirations:
            if insp.id == inspiration_id:
                insp.rating = rating
                insp.used = True
                if rating >= 4:
                    self.total_experience += 10
                break
    
    def get_status(self) -> Dict:
        """获取缪斯状态"""
        return {
            "name": self.name,
            "level": self.level.title,
            "level_num": self.level.level,
            "total_experience": self.total_experience,
            "generation_count": self.generation_count,
            "collection_size": len(self.collection.inspirations),
            "favorites_count": len(self.collection.favorites),
            "next_level_exp": self.level.exp_required
        }


# ==================== 演示函数 ====================

def demo_inspiration_muse():
    """演示灵感缪斯系统"""
    
    print("=" * 60)
    print("        灵感缪斯系统 Demo")
    print("=" * 60)
    
    # 1. 创建缪斯
    print("\n【步骤1】创建灵感缪斯")
    print("-" * 40)
    muse = InspirationMuse(soul_id="soul_001", name="创意小光")
    print(f"缪斯名称: {muse.name}")
    print(f"初始等级: {muse.level.title}")
    
    # 2. 生成日常灵感
    print("\n【步骤2】生成日常灵感")
    print("-" * 40)
    for i in range(3):
        insp = muse.generate_inspiration()
        print(f"\n灵感 #{i+1}:")
        print(f"  类型: {insp.type.value}")
        print(f"  质量: {insp.quality.value}")
        print(f"  内容: {insp.content}")
    
    # 3. 生成特定类型灵感
    print("\n【步骤3】生成特定类型灵感")
    print("-" * 40)
    insp = muse.generate_inspiration(InspirationType.TEXT)
    print(f"类型: {insp.type.value}")
    print(f"内容: {insp.content}")
    
    # 4. 评价灵感
    print("\n【步骤4】评价灵感")
    print("-" * 40)
    muse.rate_inspiration(insp.id, 5)
    print(f"已评价灵感: {insp.id} -> 5星")
    
    # 5. 灵感风暴（需要等级3）
    print("\n【步骤5】提升等级并触发灵感风暴")
    print("-" * 40)
    # 模拟提升等级
    muse.total_experience = 2000
    print(f"当前等级: {muse.level.title}")
    
    if muse.level.level >= 3:
        storm = muse.inspiration_storm("夏日主题", 3)
        print(f"灵感风暴生成 {len(storm)} 个灵感:")
        for i, insp in enumerate(storm, 1):
            print(f"  {i}. {insp.content[:30]}...")
    
    # 6. 个性化灵感流
    print("\n【步骤6】获取个性化灵感流")
    print("-" * 40)
    flow = muse.get_personalized_flow(2)
    for i, insp in enumerate(flow, 1):
        print(f"  {i}. [{insp.type.value}] {insp.content[:40]}...")
    
    # 7. 最终状态
    print("\n【步骤7】缪斯最终状态")
    print("-" * 40)
    status = muse.get_status()
    print(f"等级: {status['level']} (Lv.{status['level_num']})")
    print(f"总经验: {status['total_experience']}")
    print(f"生成次数: {status['generation_count']}")
    print(f"收藏数量: {status['collection_size']}")
    
    print("\n" + "=" * 60)
    print("        Demo 完成")
    print("=" * 60)


if __name__ == "__main__":
    demo_inspiration_muse()
