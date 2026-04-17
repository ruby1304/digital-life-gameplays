"""
灵魂导师 (Soul Mentor) - 基础Demo

这个demo展示了灵魂导师系统的核心功能：
1. 导师能力与等级系统
2. 指导建议生成
3. 成长规划与追踪
4. 用户反馈机制
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum
from datetime import datetime
import random


# ==================== 枚举定义 ====================

class MentorAbility(Enum):
    """导师能力类型"""
    LIFE_GUIDANCE = "生活指引"
    EMOTIONAL_SUPPORT = "情感支持"
    GROWTH_PLANNING = "成长规划"
    DECISION_MAKING = "决策辅助"
    PROBLEM_SOLVING = "问题解决"
    WISDOM_SHARING = "智慧分享"


class GuidanceType(Enum):
    """指导类型"""
    DAILY = "日常建议"
    DEEP = "深度咨询"
    EMOTIONAL = "情感陪伴"
    GROWTH = "成长规划"


class MentorLevel(Enum):
    """导师等级"""
    NOVICE = (1, "见习导师", 0)
    JUNIOR = (2, "初级导师", 1000)
    INTERMEDIATE = (3, "中级导师", 3000)
    SENIOR = (4, "高级导师", 6000)
    MASTER = (5, "资深导师", 10000)
    SAGE = (6, "智慧导师", 15000)
    
    def __init__(self, level: int, title: str, exp_required: int):
        self.level = level
        self.title = title
        self.exp_required = exp_required


# ==================== 数据类定义 ====================

@dataclass
class AbilityScore:
    """能力评分"""
    ability: MentorAbility
    level: int = 1
    experience: int = 0
    
    def add_experience(self, amount: int) -> bool:
        """增加经验，返回是否升级"""
        self.experience += amount
        required = self.level * 100
        if self.experience >= required:
            self.level += 1
            self.experience = 0
            return True
        return False


@dataclass
class Guidance:
    """指导建议"""
    type: GuidanceType
    question: str
    advice: str
    confidence: float
    abilities_used: List[MentorAbility]
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class GrowthGoal:
    """成长目标"""
    id: str
    title: str
    description: str
    target_date: datetime
    milestones: List[str]
    completed_milestones: List[str] = field(default_factory=list)
    status: str = "active"
    
    def progress_percent(self) -> float:
        if not self.milestones:
            return 0.0
        return len(self.completed_milestones) / len(self.milestones) * 100


@dataclass
class UserFeedback:
    """用户反馈"""
    guidance_id: str
    rating: int  # 1-5
    comment: str
    helpful: bool
    timestamp: datetime = field(default_factory=datetime.now)


# ==================== 导师类 ====================

class SoulMentor:
    """灵魂导师"""
    
    def __init__(self, soul_id: str, name: str):
        self.soul_id = soul_id
        self.name = name
        self.total_experience = 0
        self.abilities: Dict[MentorAbility, AbilityScore] = {
            ability: AbilityScore(ability) for ability in MentorAbility
        }
        self.guidance_history: List[Guidance] = []
        self.growth_plans: List[GrowthGoal] = []
        self.feedback_received: List[UserFeedback] = []
        self.created_at = datetime.now()
    
    @property
    def level(self) -> MentorLevel:
        """获取当前等级"""
        for lvl in reversed(list(MentorLevel)):
            if self.total_experience >= lvl.exp_required:
                return lvl
        return MentorLevel.NOVICE
    
    def add_experience(self, amount: int, ability: Optional[MentorAbility] = None):
        """增加经验"""
        self.total_experience += amount
        if ability and ability in self.abilities:
            self.abilities[ability].add_experience(amount)
    
    def get_ability_level(self, ability: MentorAbility) -> int:
        """获取特定能力等级"""
        return self.abilities[ability].level
    
    def can_provide_guidance(self, guidance_type: GuidanceType) -> bool:
        """检查是否可以提供特定类型的指导"""
        requirements = {
            GuidanceType.DAILY: (MentorLevel.NOVICE, [MentorAbility.LIFE_GUIDANCE]),
            GuidanceType.DEEP: (MentorLevel.INTERMEDIATE, [MentorAbility.DECISION_MAKING, MentorAbility.PROBLEM_SOLVING]),
            GuidanceType.EMOTIONAL: (MentorLevel.JUNIOR, [MentorAbility.EMOTIONAL_SUPPORT]),
            GuidanceType.GROWTH: (MentorLevel.SENIOR, [MentorAbility.GROWTH_PLANNING, MentorAbility.WISDOM_SHARING])
        }
        
        req_level, req_abilities = requirements.get(guidance_type, (MentorLevel.SAGE, []))
        
        if self.level.level < req_level.level:
            return False
        
        for ability in req_abilities:
            if self.abilities[ability].level < 1:
                return False
        
        return True
    
    def provide_guidance(self, question: str, guidance_type: GuidanceType) -> Optional[Guidance]:
        """提供指导建议"""
        if not self.can_provide_guidance(guidance_type):
            return None
        
        # 模拟生成建议
        advice_templates = {
            GuidanceType.DAILY: [
                "根据我的观察，建议你可以尝试...",
                "从生活经验来看，这个问题的解决方向是...",
                "我建议你先考虑以下几个方面..."
            ],
            GuidanceType.DEEP: [
                "经过深入分析，这个问题的核心在于...",
                "从多个角度来看，我建议的解决方案是...",
                "综合考虑各种因素，最佳路径是..."
            ],
            GuidanceType.EMOTIONAL: [
                "我理解你现在的感受，这很正常...",
                "让我陪你一起面对这个情绪...",
                "相信我，一切都会好起来的..."
            ],
            GuidanceType.GROWTH: [
                "根据你的目标，我为你规划了以下路径...",
                "要达成这个目标，建议分阶段进行...",
                "长期来看，你需要关注这几个方面..."
            ]
        }
        
        advice = random.choice(advice_templates.get(guidance_type, ["让我想想..."]))
        
        # 确定使用的能力
        abilities_map = {
            GuidanceType.DAILY: [MentorAbility.LIFE_GUIDANCE],
            GuidanceType.DEEP: [MentorAbility.DECISION_MAKING, MentorAbility.PROBLEM_SOLVING],
            GuidanceType.EMOTIONAL: [MentorAbility.EMOTIONAL_SUPPORT],
            GuidanceType.GROWTH: [MentorAbility.GROWTH_PLANNING]
        }
        
        guidance = Guidance(
            type=guidance_type,
            question=question,
            advice=advice,
            confidence=0.7 + random.random() * 0.25,
            abilities_used=abilities_map.get(guidance_type, [])
        )
        
        self.guidance_history.append(guidance)
        
        # 增加经验
        exp_gain = {
            GuidanceType.DAILY: 10,
            GuidanceType.DEEP: 30,
            GuidanceType.EMOTIONAL: 20,
            GuidanceType.GROWTH: 40
        }
        self.add_experience(exp_gain.get(guidance_type, 10))
        
        return guidance
    
    def create_growth_plan(self, title: str, description: str, 
                          target_date: datetime, milestones: List[str]) -> GrowthGoal:
        """创建成长计划"""
        goal = GrowthGoal(
            id=f"goal_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            title=title,
            description=description,
            target_date=target_date,
            milestones=milestones
        )
        self.growth_plans.append(goal)
        return goal
    
    def update_goal_progress(self, goal_id: str, milestone: str) -> bool:
        """更新目标进度"""
        for goal in self.growth_plans:
            if goal.id == goal_id and milestone in goal.milestones:
                if milestone not in goal.completed_milestones:
                    goal.completed_milestones.append(milestone)
                    if len(goal.completed_milestones) == len(goal.milestones):
                        goal.status = "completed"
                    return True
        return False
    
    def receive_feedback(self, guidance: Guidance, rating: int, 
                        comment: str, helpful: bool):
        """接收反馈"""
        feedback = UserFeedback(
            guidance_id=str(id(guidance)),
            rating=rating,
            comment=comment,
            helpful=helpful
        )
        self.feedback_received.append(feedback)
        
        # 根据反馈调整经验
        if helpful and rating >= 4:
            self.add_experience(20)
    
    def get_status(self) -> Dict:
        """获取导师状态"""
        return {
            "name": self.name,
            "level": self.level.title,
            "level_num": self.level.level,
            "total_experience": self.total_experience,
            "next_level_exp": self.level.exp_required,
            "guidance_count": len(self.guidance_history),
            "active_goals": len([g for g in self.growth_plans if g.status == "active"]),
            "completed_goals": len([g for g in self.growth_plans if g.status == "completed"]),
            "average_rating": sum(f.rating for f in self.feedback_received) / len(self.feedback_received) if self.feedback_received else 0,
            "abilities": {a.value: s.level for a, s in self.abilities.items()}
        }


# ==================== 演示函数 ====================

def demo_soul_mentor():
    """演示灵魂导师系统"""
    
    print("=" * 60)
    print("        灵魂导师系统 Demo")
    print("=" * 60)
    
    # 1. 创建导师
    print("\n【步骤1】创建灵魂导师")
    print("-" * 40)
    mentor = SoulMentor(soul_id="soul_001", name="智慧小光")
    print(f"导师名称: {mentor.name}")
    print(f"初始等级: {mentor.level.title}")
    print(f"初始经验: {mentor.total_experience}")
    
    # 2. 提供日常指导
    print("\n【步骤2】提供日常指导")
    print("-" * 40)
    guidance = mentor.provide_guidance(
        "今天心情不太好，不知道该怎么办",
        GuidanceType.DAILY
    )
    if guidance:
        print(f"问题: {guidance.question}")
        print(f"建议: {guidance.advice}")
        print(f"信心度: {guidance.confidence:.2f}")
    
    # 3. 模拟多次指导提升等级
    print("\n【步骤3】模拟多次指导")
    print("-" * 40)
    questions = [
        ("如何提高工作效率？", GuidanceType.DAILY),
        ("我该不该换工作？", GuidanceType.DEEP),
        ("最近压力很大", GuidanceType.EMOTIONAL),
    ]
    
    for q, t in questions:
        g = mentor.provide_guidance(q, t)
        if g:
            print(f"指导类型: {g.type.value}")
            print(f"获得经验: +{10 if t == GuidanceType.DAILY else 30}")
    
    print(f"\n当前经验: {mentor.total_experience}")
    print(f"当前等级: {mentor.level.title}")
    
    # 4. 创建成长计划
    print("\n【步骤4】创建成长计划")
    print("-" * 40)
    goal = mentor.create_growth_plan(
        title="提升沟通能力",
        description="在3个月内提升人际沟通能力",
        target_date=datetime(2025, 6, 30),
        milestones=["学习倾听技巧", "练习表达", "实际应用", "总结反思"]
    )
    print(f"目标: {goal.title}")
    print(f"里程碑: {goal.milestones}")
    
    # 5. 更新进度
    print("\n【步骤5】更新目标进度")
    print("-" * 40)
    mentor.update_goal_progress(goal.id, "学习倾听技巧")
    mentor.update_goal_progress(goal.id, "练习表达")
    print(f"完成进度: {goal.progress_percent():.1f}%")
    print(f"已完成: {goal.completed_milestones}")
    
    # 6. 接收反馈
    print("\n【步骤6】接收用户反馈")
    print("-" * 40)
    if guidance:
        mentor.receive_feedback(guidance, rating=5, comment="很有帮助！", helpful=True)
        print("反馈已记录: 5星好评")
    
    # 7. 最终状态
    print("\n【步骤7】导师最终状态")
    print("-" * 40)
    status = mentor.get_status()
    print(f"等级: {status['level']} (Lv.{status['level_num']})")
    print(f"总经验: {status['total_experience']}")
    print(f"指导次数: {status['guidance_count']}")
    print(f"活跃目标: {status['active_goals']}")
    print(f"平均评分: {status['average_rating']:.1f}")
    
    print("\n" + "=" * 60)
    print("        Demo 完成")
    print("=" * 60)


if __name__ == "__main__":
    demo_soul_mentor()
