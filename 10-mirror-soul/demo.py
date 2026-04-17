"""
镜中灵魂 (Mirror Soul) - 基础Demo

这个demo展示了镜中灵魂系统的核心功能：
1. 镜像维度与生成
2. 深度对话机制
3. 特质分析系统
4. 洞察报告生成
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
from datetime import datetime
import random
import re


# ==================== 枚举定义 ====================

class MirrorDimension(Enum):
    """镜像维度"""
    PERSONALITY = "性格镜像"
    EMOTION = "情感镜像"
    VALUE = "价值镜像"
    POTENTIAL = "潜能镜像"
    SHADOW = "阴影镜像"


class MirrorDepth(Enum):
    """镜像深度"""
    SURFACE = (1, "表层镜像", 0)
    SHALLOW = (2, "浅层镜像", 5)
    MIDDLE = (3, "中层镜像", 15)
    DEEP = (4, "深层镜像", 30)
    SUBCONSCIOUS = (5, "潜意识镜像", 50)
    ORIGIN = (6, "本源镜像", 100)
    
    def __init__(self, level: int, name: str, dialogues_required: int):
        self.level = level
        self.name = name
        self.dialogues_required = dialogues_required


class TraitType(Enum):
    """特质类型"""
    STRENGTH = "优势特质"
    GROWTH = "成长空间"
    HIDDEN = "隐藏特质"
    SHADOW = "阴影特质"


# ==================== 数据类定义 ====================

@dataclass
class Trait:
    """特质"""
    name: str
    type: TraitType
    dimension: MirrorDimension
    score: float  # 0-1
    description: str
    evidence: List[str] = field(default_factory=list)


@dataclass
class Dialogue:
    """对话记录"""
    id: str
    user_message: str
    soul_response: str
    dimension: MirrorDimension
    depth: MirrorDepth
    insights: List[str]
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class MirrorReport:
    """镜像报告"""
    dimension: MirrorDimension
    depth: MirrorDepth
    traits: List[Trait]
    patterns: List[str]
    recommendations: List[str]
    generated_at: datetime = field(default_factory=datetime.now)


# ==================== 镜像灵魂类 ====================

class MirrorSoul:
    """镜中灵魂"""
    
    def __init__(self, soul_id: str, name: str):
        self.soul_id = soul_id
        self.name = name
        self.dialogues: List[Dialogue] = []
        self.traits: List[Trait] = []
        self.total_insights = 0
        self.created_at = datetime.now()
        
        # 特质词库
        self._trait_library = {
            MirrorDimension.PERSONALITY: {
                TraitType.STRENGTH: ["善于思考", "富有同理心", "坚韧不拔", "创造力强", "善于沟通"],
                TraitType.GROWTH: ["需要更多自信", "可以更果断", "学会拒绝", "接受不完美", "放下控制"],
                TraitType.HIDDEN: ["内在的领导力", "隐藏的艺术天赋", "潜在的冒险精神", "深层的直觉力"],
                TraitType.SHADOW: ["对失败的恐惧", "完美主义倾向", "被压抑的表达欲", "隐藏的愤怒"],
            },
            MirrorDimension.EMOTION: {
                TraitType.STRENGTH: ["情感细腻", "善于共情", "情绪稳定", "自我觉察", "情感表达"],
                TraitType.GROWTH: ["学会表达需求", "处理负面情绪", "建立边界", "接纳脆弱"],
                TraitType.HIDDEN: ["深层的温柔", "隐藏的热情", "内在的平静", "潜在的爱"],
                TraitType.SHADOW: ["被压抑的悲伤", "隐藏的嫉妒", "未处理的创伤", "深层的孤独"],
            },
            MirrorDimension.VALUE: {
                TraitType.STRENGTH: ["重视诚实", "追求成长", "珍视关系", "崇尚自由", "尊重差异"],
                TraitType.GROWTH: ["明确优先级", "坚持原则", "平衡理想与现实", "接受妥协"],
                TraitType.HIDDEN: ["内在的使命感", "隐藏的理想主义", "深层的利他心"],
                TraitType.SHADOW: ["价值观冲突", "隐藏的功利心", "被压抑的欲望"],
            },
            MirrorDimension.POTENTIAL: {
                TraitType.STRENGTH: ["学习能力", "适应能力", "创新能力", "领导潜力", "艺术感知"],
                TraitType.GROWTH: ["专注力提升", "执行力加强", "风险管理", "资源整合"],
                TraitType.HIDDEN: ["未开发的才华", "沉睡的创造力", "潜在的影响力", "隐藏的智慧"],
                TraitType.SHADOW: ["对成功的恐惧", "自我设限", "隐藏的野心", "被压抑的梦想"],
            },
            MirrorDimension.SHADOW: {
                TraitType.STRENGTH: ["自我觉察", "接纳能力", "整合能力", "转化能力"],
                TraitType.GROWTH: ["面对阴影", "接纳黑暗面", "整合矛盾", "释放压抑"],
                TraitType.HIDDEN: ["阴影中的力量", "黑暗中的智慧", "痛苦中的成长"],
                TraitType.SHADOW: ["核心恐惧", "深层创伤", "被否认的自我", "投射的特质"],
            },
        }
        
        # 对话回应模板
        self._response_templates = {
            "reflect": [
                "我感受到你说这句话时，内心似乎{emotion}...",
                "这让我想到，也许在你的内心深处，{insight}...",
                "从你的话语中，我看到了一个{trait}的你。",
            ],
            "probe": [
                "当你这样说的时候，你内心真正的感受是什么？",
                "这对你来说意味着什么？",
                "如果可以更深入地看，你觉得会是什么？",
            ],
            "insight": [
                "我注意到一个模式：{pattern}。这让你想到了什么？",
                "也许这背后有一个更深层的原因，关于{topic}...",
                "你的灵魂在告诉我，{message}...",
            ],
        }
        
        # 情感词库
        self._emotion_words = [
            "有些犹豫", "充满期待", "带着一丝不安", "有着深深的渴望",
            "带着平静", "有些困惑", "充满力量", "带着温柔",
        ]
        
        # 洞察词库
        self._insight_words = [
            "你比表现出来的更在乎这件事",
            "有一个声音在等待被听见",
            "你正在寻找某种答案",
            "内心深处有一个被忽视的需求",
            "你比自己认为的更有力量",
            "有一个伤口正在等待愈合",
        ]
    
    @property
    def depth(self) -> MirrorDepth:
        """获取当前深度"""
        dialogue_count = len(self.dialogues)
        for depth in reversed(list(MirrorDepth)):
            if dialogue_count >= depth.dialogues_required:
                return depth
        return MirrorDepth.SURFACE
    
    def _analyze_message(self, message: str) -> Dict:
        """分析用户消息"""
        # 简单的关键词分析
        analysis = {
            "length": len(message),
            "emotion_keywords": [],
            "topic_keywords": [],
        }
        
        # 情感关键词
        emotion_patterns = {
            "开心": "喜悦", "难过": "悲伤", "害怕": "恐惧",
            "愤怒": "愤怒", "焦虑": "焦虑", "平静": "平静",
            "迷茫": "困惑", "期待": "希望", "孤独": "孤独",
        }
        
        for keyword, emotion in emotion_patterns.items():
            if keyword in message:
                analysis["emotion_keywords"].append(emotion)
        
        # 主题关键词
        topic_patterns = {
            "工作": "事业", "关系": "关系", "自己": "自我",
            "未来": "成长", "过去": "回忆", "家人": "家庭",
            "朋友": "社交", "梦想": "理想", "失败": "挑战",
        }
        
        for keyword, topic in topic_patterns.items():
            if keyword in message:
                analysis["topic_keywords"].append(topic)
        
        return analysis
    
    def _generate_response(self, message: str, dimension: MirrorDimension) -> str:
        """生成回应"""
        analysis = self._analyze_message(message)
        
        # 根据深度选择回应类型
        depth = self.depth.level
        
        if depth <= 2:
            # 表层/浅层：简单反映
            template = random.choice(self._response_templates["reflect"])
            emotion = random.choice(self._emotion_words)
            return template.format(emotion=emotion, insight="", trait="真实")
        
        elif depth <= 4:
            # 中层/深层：引导探索
            template = random.choice(self._response_templates["probe"])
            return template
        
        else:
            # 潜意识/本源：深度洞察
            template = random.choice(self._response_templates["insight"])
            insight = random.choice(self._insight_words)
            pattern = "你经常在类似情境下有相似的感受"
            return template.format(pattern=pattern, topic="你的核心需求", message=insight)
    
    def _extract_insights(self, message: str, response: str) -> List[str]:
        """提取洞察"""
        insights = []
        
        # 基于消息长度和深度
        if len(message) > 50 and self.depth.level >= 3:
            insights.append("你愿意深入分享，这显示了信任和开放")
        
        if self.depth.level >= 4:
            insights.append(random.choice(self._insight_words))
        
        return insights
    
    def dialogue(self, message: str, 
                dimension: Optional[MirrorDimension] = None) -> Dialogue:
        """进行对话"""
        if dimension is None:
            dimension = random.choice(list(MirrorDimension))
        
        # 生成回应
        response = self._generate_response(message, dimension)
        
        # 提取洞察
        insights = self._extract_insights(message, response)
        
        # 创建对话记录
        dialogue = Dialogue(
            id=f"dialogue_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000, 9999)}",
            user_message=message,
            soul_response=response,
            dimension=dimension,
            depth=self.depth,
            insights=insights
        )
        
        self.dialogues.append(dialogue)
        self.total_insights += len(insights)
        
        # 更新特质
        self._update_traits(message, dimension)
        
        return dialogue
    
    def _update_traits(self, message: str, dimension: MirrorDimension):
        """更新特质"""
        # 随机发现新特质（模拟）
        if random.random() < 0.2:  # 20%概率发现新特质
            trait_type = random.choice(list(TraitType))
            trait_names = self._trait_library.get(dimension, {}).get(trait_type, [])
            
            if trait_names:
                trait_name = random.choice(trait_names)
                
                # 检查是否已存在
                if not any(t.name == trait_name for t in self.traits):
                    trait = Trait(
                        name=trait_name,
                        type=trait_type,
                        dimension=dimension,
                        score=random.uniform(0.5, 0.95),
                        description=f"通过对话发现的{trait_type.value}",
                        evidence=[message[:50] + "..."]
                    )
                    self.traits.append(trait)
    
    def generate_report(self, dimension: MirrorDimension) -> MirrorReport:
        """生成镜像报告"""
        # 筛选相关特质
        dimension_traits = [t for t in self.traits if t.dimension == dimension]
        
        # 如果特质不足，生成一些
        while len(dimension_traits) < 3:
            trait_type = random.choice(list(TraitType))
            trait_names = self._trait_library.get(dimension, {}).get(trait_type, [])
            if trait_names:
                trait_name = random.choice(trait_names)
                if not any(t.name == trait_name for t in dimension_traits):
                    trait = Trait(
                        name=trait_name,
                        type=trait_type,
                        dimension=dimension,
                        score=random.uniform(0.4, 0.9),
                        description=f"基于对话分析得出的{trait_type.value}"
                    )
                    dimension_traits.append(trait)
        
        # 生成模式分析
        patterns = [
            f"在{dimension.value}维度，你展现出{dimension_traits[0].name}的特质",
            f"你的{dimension_traits[0].name}与{dimension_traits[1].name}形成有趣的平衡",
        ]
        
        # 生成建议
        recommendations = [
            f"建议更多地关注你的{dimension_traits[0].name}",
            f"可以尝试探索{dimension_traits[1].name}的深层含义",
        ]
        
        return MirrorReport(
            dimension=dimension,
            depth=self.depth,
            traits=dimension_traits[:5],
            patterns=patterns,
            recommendations=recommendations
        )
    
    def get_status(self) -> Dict:
        """获取状态"""
        return {
            "name": self.name,
            "depth": self.depth.name,
            "depth_level": self.depth.level,
            "total_dialogues": len(self.dialogues),
            "total_insights": self.total_insights,
            "discovered_traits": len(self.traits),
            "dimensions_explored": len(set(d.dimension for d in self.dialogues)) if self.dialogues else 0
        }


# ==================== 演示函数 ====================

def demo_mirror_soul():
    """演示镜中灵魂系统"""
    
    print("=" * 60)
    print("        镜中灵魂系统 Demo")
    print("=" * 60)
    
    # 1. 创建镜像灵魂
    print("\n【步骤1】创建镜像灵魂")
    print("-" * 40)
    mirror = MirrorSoul(soul_id="soul_001", name="心灵之镜")
    print(f"灵魂名称: {mirror.name}")
    print(f"初始深度: {mirror.depth.name}")
    
    # 2. 进行对话
    print("\n【步骤2】进行镜像对话")
    print("-" * 40)
    
    test_messages = [
        "最近工作压力很大，我感到有些迷茫",
        "我总是害怕让别人失望",
        "有时候我觉得自己不够好",
        "我想改变，但不知道从哪里开始",
        "其实我有很多想法，但不敢表达",
    ]
    
    for i, msg in enumerate(test_messages, 1):
        dialogue = mirror.dialogue(msg, MirrorDimension.PERSONALITY)
        print(f"\n对话 #{i}:")
        print(f"  你: {msg}")
        print(f"  镜: {dialogue.soul_response}")
        if dialogue.insights:
            print(f"  洞察: {dialogue.insights[0]}")
    
    # 3. 查看深度变化
    print("\n【步骤3】查看深度变化")
    print("-" * 40)
    print(f"当前深度: {mirror.depth.name} (Lv.{mirror.depth.level})")
    print(f"对话次数: {len(mirror.dialogues)}")
    
    # 4. 发现的特质
    print("\n【步骤4】发现的特质")
    print("-" * 40)
    for trait in mirror.traits[:5]:
        print(f"  [{trait.type.value}] {trait.name}")
        print(f"    维度: {trait.dimension.value}")
        print(f"    强度: {trait.score:.0%}")
    
    # 5. 生成镜像报告
    print("\n【步骤5】生成镜像报告")
    print("-" * 40)
    report = mirror.generate_report(MirrorDimension.PERSONALITY)
    print(f"维度: {report.dimension.value}")
    print(f"深度: {report.depth.name}")
    print(f"\n特质分析:")
    for trait in report.traits:
        print(f"  - {trait.name} ({trait.type.value}): {trait.score:.0%}")
    print(f"\n模式发现:")
    for pattern in report.patterns:
        print(f"  - {pattern}")
    
    # 6. 最终状态
    print("\n【步骤6】最终状态")
    print("-" * 40)
    status = mirror.get_status()
    print(f"深度: {status['depth']} (Lv.{status['depth_level']})")
    print(f"总对话: {status['total_dialogues']}次")
    print(f"总洞察: {status['total_insights']}个")
    print(f"发现特质: {status['discovered_traits']}个")
    print(f"探索维度: {status['dimensions_explored']}个")
    
    print("\n" + "=" * 60)
    print("        Demo 完成")
    print("=" * 60)


if __name__ == "__main__":
    demo_mirror_soul()
