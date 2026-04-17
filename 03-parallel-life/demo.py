"""
平行人生 (Parallel Life) - 基础Demo

这个demo展示了平行人生系统的核心功能：
1. 人生阶段与时间推进
2. 职业发展系统
3. 生活事件生成与处理
4. 资源管理与生活模拟
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum
from datetime import datetime, timedelta
import json
import random


# ==================== 枚举定义 ====================

class LifeStage(Enum):
    """人生阶段"""
    CHILDHOOD = ("童年期", 0, 30, "学习探索")
    YOUTH = ("青年期", 31, 90, "职业选择")
    ADULTHOOD = ("成年期", 91, 365, "事业巅峰")
    MIDDLE_AGE = ("中年期", 366, 730, "传承教导")
    ELDER = ("晚年期", 731, 1095, "智慧沉淀")
    LEGEND = ("传说期", 1096, 999999, "永恒")
    
    def __init__(self, name_cn: str, min_days: int, max_days: int, theme: str):
        self.name_cn = name_cn
        self.min_days = min_days
        self.max_days = max_days
        self.theme = theme
    
    @classmethod
    def from_days(cls, days: int) -> 'LifeStage':
        """根据天数获取阶段"""
        for stage in cls:
            if stage.min_days <= days <= stage.max_days:
                return stage
        return cls.LEGEND


class CareerCategory(Enum):
    """职业类别"""
    KNOWLEDGE = "知识型"
    CREATIVE = "创意型"
    SOCIAL = "社交型"
    TECHNICAL = "技术型"
    LEADERSHIP = "领导型"


class EventType(Enum):
    """事件类型"""
    DAILY = "日常事件"
    RANDOM = "随机事件"
    MILESTONE = "里程碑"
    SPECIAL = "特殊事件"
    CAREER = "职业事件"


class ResourceType(Enum):
    """资源类型"""
    ENERGY = "精力"
    MOOD = "心情"
    GOLD = "金币"
    SKILL_POINT = "技能点"
    CONNECTION = "人脉值"


# ==================== 数据类定义 ====================

@dataclass
class LifeResources:
    """人生资源"""
    energy: int = 100      # 精力 (0-100)
    mood: int = 70         # 心情 (0-100)
    gold: int = 100        # 金币
    skill_points: int = 0  # 技能点
    connection: int = 0    # 人脉值 (0-1000)
    
    def to_dict(self) -> Dict:
        return {
            "energy": self.energy,
            "mood": self.mood,
            "gold": self.gold,
            "skill_points": self.skill_points,
            "connection": min(self.connection, 1000)
        }
    
    def apply_changes(self, changes: Dict[str, int]) -> None:
        """应用资源变化"""
        for resource, delta in changes.items():
            if hasattr(self, resource):
                current = getattr(self, resource)
                new_value = current + delta
                # 应用上下限
                if resource in ["energy", "mood"]:
                    new_value = max(0, min(100, new_value))
                elif resource == "connection":
                    new_value = max(0, min(1000, new_value))
                else:
                    new_value = max(0, new_value)
                setattr(self, resource, new_value)


@dataclass
class LifeSkills:
    """人生技能"""
    wisdom: int = 0       # 智慧
    creativity: int = 0   # 创造力
    charisma: int = 0     # 魅力
    logic: int = 0        # 逻辑
    empathy: int = 0      # 共情
    
    def to_dict(self) -> Dict:
        return {
            "wisdom": self.wisdom,
            "creativity": self.creativity,
            "charisma": self.charisma,
            "logic": self.logic,
            "empathy": self.empathy
        }
    
    def total(self) -> int:
        return sum([self.wisdom, self.creativity, self.charisma, 
                   self.logic, self.empathy])


@dataclass
class Career:
    """职业定义"""
    id: str
    name: str
    category: CareerCategory
    description: str
    required_skills: Dict[str, int]
    income_range: Tuple[int, int]
    special_ability: str
    max_level: int = 10


@dataclass
class CareerProgress:
    """职业进度"""
    career: Career
    level: int = 1
    experience: int = 0
    days_worked: int = 0
    achievements: List[str] = field(default_factory=list)
    
    def experience_needed(self) -> int:
        """升级所需经验"""
        return self.level * 100
    
    def can_level_up(self) -> bool:
        """是否可以升级"""
        return self.experience >= self.experience_needed() and self.level < self.career.max_level
    
    def level_up(self) -> bool:
        """执行升级"""
        if self.can_level_up():
            self.experience -= self.experience_needed()
            self.level += 1
            return True
        return False


@dataclass
class LifeEvent:
    """生活事件"""
    id: str
    event_type: EventType
    title: str
    description: str
    choices: List[Dict]
    resource_changes: Dict[str, int]
    skill_changes: Dict[str, int]
    timestamp: datetime = field(default_factory=datetime.now)
    selected_choice: Optional[str] = None
    processed: bool = False
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "type": self.event_type.value,
            "title": self.title,
            "description": self.description,
            "choices": self.choices,
            "resource_changes": self.resource_changes,
            "skill_changes": self.skill_changes,
            "timestamp": self.timestamp.isoformat(),
            "selected_choice": self.selected_choice,
            "processed": self.processed
        }


@dataclass
class LifeGoal:
    """人生目标"""
    id: str
    title: str
    description: str
    target_value: int
    current_value: int
    reward: Dict
    completed: bool = False
    
    def progress(self) -> float:
        return min(1.0, self.current_value / self.target_value) if self.target_value > 0 else 0.0


# ==================== 职业库 ====================

class CareerLibrary:
    """职业库"""
    
    CAREERS = [
        # 知识型
        Career(
            id="scholar",
            name="学者",
            category=CareerCategory.KNOWLEDGE,
            description="追求知识的智者",
            required_skills={"wisdom": 30},
            income_range=(50, 150),
            special_ability="深度分析"
        ),
        Career(
            id="teacher",
            name="教师",
            category=CareerCategory.KNOWLEDGE,
            description="传道授业解惑",
            required_skills={"wisdom": 25, "empathy": 20},
            income_range=(40, 120),
            special_ability="知识传承"
        ),
        Career(
            id="writer",
            name="作家",
            category=CareerCategory.KNOWLEDGE,
            description="文字的魔法师",
            required_skills={"wisdom": 20, "creativity": 30},
            income_range=(30, 200),
            special_ability="创意写作"
        ),
        # 创意型
        Career(
            id="artist",
            name="艺术家",
            category=CareerCategory.CREATIVE,
            description="用艺术表达灵魂",
            required_skills={"creativity": 35},
            income_range=(20, 300),
            special_ability="艺术创作"
        ),
        Career(
            id="designer",
            name="设计师",
            category=CareerCategory.CREATIVE,
            description="创造美的使者",
            required_skills={"creativity": 30, "logic": 20},
            income_range=(50, 180),
            special_ability="设计思维"
        ),
        Career(
            id="musician",
            name="音乐家",
            category=CareerCategory.CREATIVE,
            description="旋律的编织者",
            required_skills={"creativity": 35, "empathy": 20},
            income_range=(25, 250),
            special_ability="音乐创作"
        ),
        # 社交型
        Career(
            id="diplomat",
            name="外交官",
            category=CareerCategory.SOCIAL,
            description="沟通的桥梁",
            required_skills={"charisma": 35, "empathy": 25},
            income_range=(80, 200),
            special_ability="外交谈判"
        ),
        Career(
            id="consultant",
            name="咨询师",
            category=CareerCategory.SOCIAL,
            description="心灵的引导者",
            required_skills={"empathy": 35, "wisdom": 20},
            income_range=(60, 180),
            special_ability="情感洞察"
        ),
        # 技术型
        Career(
            id="engineer",
            name="工程师",
            category=CareerCategory.TECHNICAL,
            description="问题的解决者",
            required_skills={"logic": 35},
            income_range=(70, 200),
            special_ability="技术突破"
        ),
        Career(
            id="researcher",
            name="研究员",
            category=CareerCategory.TECHNICAL,
            description="探索未知的先锋",
            required_skills={"logic": 30, "wisdom": 25},
            income_range=(60, 180),
            special_ability="科研发现"
        ),
        # 领导型
        Career(
            id="entrepreneur",
            name="企业家",
            category=CareerCategory.LEADERSHIP,
            description="创新的引领者",
            required_skills={"charisma": 25, "logic": 25, "wisdom": 20},
            income_range=(50, 500),
            special_ability="商业决策"
        ),
        Career(
            id="mentor",
            name="导师",
            category=CareerCategory.LEADERSHIP,
            description="成长的引路人",
            required_skills={"wisdom": 35, "empathy": 30, "charisma": 25},
            income_range=(80, 200),
            special_ability="智慧传承"
        ),
    ]
    
    @classmethod
    def get_available_careers(cls, skills: LifeSkills) -> List[Career]:
        """获取可用职业"""
        available = []
        for career in cls.CAREERS:
            qualified = True
            for skill, required in career.required_skills.items():
                if getattr(skills, skill, 0) < required:
                    qualified = False
                    break
            if qualified:
                available.append(career)
        return available
    
    @classmethod
    def get_career_by_id(cls, career_id: str) -> Optional[Career]:
        """根据ID获取职业"""
        for career in cls.CAREERS:
            if career.id == career_id:
                return career
        return None


# ==================== 事件生成器 ====================

class EventGenerator:
    """生活事件生成器"""
    
    # 日常事件模板
    DAILY_EVENTS = [
        {
            "title": "日常工作",
            "description": "完成今天的工作任务",
            "choices": [
                {"id": "focus", "text": "专注完成", "resource": {"energy": -15, "mood": 5, "gold": 20}},
                {"id": "relax", "text": "轻松应对", "resource": {"energy": -5, "mood": 10, "gold": 10}}
            ],
            "skills": {"wisdom": 1, "logic": 1}
        },
        {
            "title": "学习时间",
            "description": "有机会学习新知识",
            "choices": [
                {"id": "study", "text": "认真学习", "resource": {"energy": -20, "skill_points": 5}},
                {"id": "skim", "text": "快速浏览", "resource": {"energy": -5, "skill_points": 1}}
            ],
            "skills": {"wisdom": 2}
        },
        {
            "title": "社交活动",
            "description": "朋友邀请参加聚会",
            "choices": [
                {"id": "join", "text": "欣然参加", "resource": {"energy": -10, "mood": 20, "connection": 10}},
                {"id": "decline", "text": "婉言谢绝", "resource": {"energy": 0, "mood": -5}}
            ],
            "skills": {"charisma": 1, "empathy": 1}
        },
    ]
    
    # 随机事件模板
    RANDOM_EVENTS = [
        {
            "title": "意外惊喜",
            "description": "收到了一份意外的礼物",
            "choices": [
                {"id": "accept", "text": "开心接受", "resource": {"mood": 30, "gold": 50}}
            ],
            "skills": {}
        },
        {
            "title": "小挑战",
            "description": "遇到了一个棘手的问题",
            "choices": [
                {"id": "solve", "text": "努力解决", "resource": {"energy": -25, "mood": -10, "skill_points": 8}},
                {"id": "skip", "text": "暂时搁置", "resource": {"mood": -5}}
            ],
            "skills": {"logic": 2}
        },
        {
            "title": "灵感闪现",
            "description": "突然有了绝妙的想法",
            "choices": [
                {"id": "pursue", "text": "深入探索", "resource": {"energy": -15, "mood": 15, "skill_points": 5}},
                {"id": "note", "text": "记录下来", "resource": {"energy": -5, "skill_points": 2}}
            ],
            "skills": {"creativity": 3}
        },
    ]
    
    # 里程碑事件
    MILESTONE_EVENTS = {
        "first_week": {
            "title": "第一周纪念",
            "description": "完成了人生的第一周旅程",
            "resource": {"gold": 100, "skill_points": 10},
            "skills": {"wisdom": 2, "creativity": 2, "charisma": 2, "logic": 2, "empathy": 2}
        },
        "first_month": {
            "title": "满月里程碑",
            "description": "人生满一个月，成长显著",
            "resource": {"gold": 200, "skill_points": 20},
            "skills": {"wisdom": 5, "creativity": 5, "charisma": 5, "logic": 5, "empathy": 5}
        },
        "career_start": {
            "title": "职业启程",
            "description": "开始了职业生涯的第一步",
            "resource": {"gold": 150, "connection": 20},
            "skills": {"wisdom": 3, "logic": 3}
        },
    }
    
    @classmethod
    def generate_daily_event(cls) -> LifeEvent:
        """生成日常事件"""
        template = random.choice(cls.DAILY_EVENTS)
        event_id = f"event_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000, 9999)}"
        
        return LifeEvent(
            id=event_id,
            event_type=EventType.DAILY,
            title=template["title"],
            description=template["description"],
            choices=template["choices"],
            resource_changes=template.get("resource", {}),
            skill_changes=template.get("skills", {})
        )
    
    @classmethod
    def generate_random_event(cls) -> LifeEvent:
        """生成随机事件"""
        template = random.choice(cls.RANDOM_EVENTS)
        event_id = f"event_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000, 9999)}"
        
        return LifeEvent(
            id=event_id,
            event_type=EventType.RANDOM,
            title=template["title"],
            description=template["description"],
            choices=template["choices"],
            resource_changes=template.get("resource", {}),
            skill_changes=template.get("skills", {})
        )
    
    @classmethod
    def generate_milestone_event(cls, milestone_type: str) -> LifeEvent:
        """生成里程碑事件"""
        template = cls.MILESTONE_EVENTS.get(milestone_type, cls.MILESTONE_EVENTS["first_week"])
        event_id = f"milestone_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        return LifeEvent(
            id=event_id,
            event_type=EventType.MILESTONE,
            title=template["title"],
            description=template["description"],
            choices=[{"id": "accept", "text": "接受祝福", "resource": {}}],
            resource_changes=template["resource"],
            skill_changes=template["skills"]
        )


# ==================== 人生引擎 ====================

class LifeEngine:
    """人生模拟引擎"""
    
    def __init__(self, soul_id: str, user_id: str, soul_name: str):
        self.soul_id = soul_id
        self.user_id = user_id
        self.soul_name = soul_name
        
        # 人生状态
        self.age_days = 0
        self.stage = LifeStage.CHILDHOOD
        self.resources = LifeResources()
        self.skills = LifeSkills()
        
        # 职业状态
        self.career_progress: Optional[CareerProgress] = None
        self.career_history: List[Dict] = []
        
        # 事件与目标
        self.events: List[LifeEvent] = []
        self.goals: List[LifeGoal] = []
        self.milestones_achieved: List[str] = []
        
        # 统计
        self.total_work_days = 0
        self.total_events_processed = 0
        self.life_satisfaction = 50.0
        
        # 初始化默认目标
        self._init_default_goals()
    
    def _init_default_goals(self):
        """初始化默认人生目标"""
        self.goals = [
            LifeGoal(
                id="goal_skills",
                title="技能大师",
                description="累计获得100点技能",
                target_value=100,
                current_value=0,
                reward={"gold": 500, "skill_points": 50}
            ),
            LifeGoal(
                id="goal_career",
                title="职业精英",
                description="达到职业等级5",
                target_value=5,
                current_value=0,
                reward={"gold": 300, "connection": 100}
            ),
            LifeGoal(
                id="goal_wealth",
                title="小有积蓄",
                description="累计获得5000金币",
                target_value=5000,
                current_value=0,
                reward={"skill_points": 30}
            ),
        ]
    
    def advance_time(self, days: int = 1) -> Dict:
        """推进时间"""
        results = {
            "days_advanced": days,
            "stage_changed": False,
            "new_stage": None,
            "events": [],
            "milestones": []
        }
        
        old_stage = self.stage
        self.age_days += days
        
        # 检查阶段变化
        new_stage = LifeStage.from_days(self.age_days)
        if new_stage != old_stage:
            self.stage = new_stage
            results["stage_changed"] = True
            results["new_stage"] = new_stage.name_cn
            
            # 触发阶段里程碑
            milestone_event = EventGenerator.generate_milestone_event("first_month")
            self.events.append(milestone_event)
            results["milestones"].append(milestone_event.to_dict())
        
        # 生成日常事件
        for _ in range(days):
            # 日常事件
            daily_event = EventGenerator.generate_daily_event()
            self.events.append(daily_event)
            results["events"].append(daily_event.to_dict())
            
            # 随机事件 (10%概率)
            if random.random() < 0.1:
                random_event = EventGenerator.generate_random_event()
                self.events.append(random_event)
                results["events"].append(random_event.to_dict())
        
        # 检查里程碑
        self._check_milestones(results)
        
        # 自然恢复
        self.resources.mood = min(100, self.resources.mood + 5)
        self.resources.energy = min(100, self.resources.energy + 10)
        
        return results
    
    def _check_milestones(self, results: Dict):
        """检查里程碑"""
        # 第一周
        if self.age_days >= 7 and "first_week" not in self.milestones_achieved:
            self.milestones_achieved.append("first_week")
            milestone = EventGenerator.generate_milestone_event("first_week")
            self.events.append(milestone)
            results["milestones"].append(milestone.to_dict())
        
        # 第一个月
        if self.age_days >= 30 and "first_month" not in self.milestones_achieved:
            self.milestones_achieved.append("first_month")
            milestone = EventGenerator.generate_milestone_event("first_month")
            self.events.append(milestone)
            results["milestones"].append(milestone.to_dict())
    
    def process_event(self, event_id: str, choice_id: str) -> Dict:
        """处理事件选择"""
        event = None
        for e in self.events:
            if e.id == event_id and not e.processed:
                event = e
                break
        
        if not event:
            return {"success": False, "message": "事件不存在或已处理"}
        
        # 找到选择
        selected_choice = None
        for choice in event.choices:
            if choice["id"] == choice_id:
                selected_choice = choice
                break
        
        if not selected_choice:
            return {"success": False, "message": "无效的选择"}
        
        # 应用效果
        event.selected_choice = choice_id
        event.processed = True
        
        # 资源变化
        resource_changes = selected_choice.get("resource", {})
        self.resources.apply_changes(resource_changes)
        
        # 技能变化
        for skill, delta in event.skill_changes.items():
            if hasattr(self.skills, skill):
                current = getattr(self.skills, skill)
                setattr(self.skills, skill, current + delta)
        
        # 更新目标进度
        self._update_goals()
        
        self.total_events_processed += 1
        
        return {
            "success": True,
            "message": f"处理了事件: {event.title}",
            "resource_changes": resource_changes,
            "skill_changes": event.skill_changes,
            "current_resources": self.resources.to_dict(),
            "current_skills": self.skills.to_dict()
        }
    
    def _update_goals(self):
        """更新目标进度"""
        for goal in self.goals:
            if goal.completed:
                continue
            
            if goal.id == "goal_skills":
                goal.current_value = self.skills.total()
            elif goal.id == "goal_career":
                goal.current_value = self.career_progress.level if self.career_progress else 0
            elif goal.id == "goal_wealth":
                goal.current_value = self.resources.gold
            
            # 检查完成
            if goal.current_value >= goal.target_value and not goal.completed:
                goal.completed = True
                # 发放奖励
                self.resources.apply_changes(goal.reward)
    
    def get_available_careers(self) -> List[Dict]:
        """获取可用职业"""
        careers = CareerLibrary.get_available_careers(self.skills)
        return [
            {
                "id": c.id,
                "name": c.name,
                "category": c.category.value,
                "description": c.description,
                "income_range": c.income_range,
                "special_ability": c.special_ability
            }
            for c in careers
        ]
    
    def apply_career(self, career_id: str) -> Dict:
        """申请职业"""
        career = CareerLibrary.get_career_by_id(career_id)
        if not career:
            return {"success": False, "message": "职业不存在"}
        
        # 检查资格
        for skill, required in career.required_skills.items():
            if getattr(self.skills, skill, 0) < required:
                return {"success": False, "message": f"技能不足: {skill}需要{required}"}
        
        # 记录旧职业
        if self.career_progress:
            self.career_history.append({
                "career_name": self.career_progress.career.name,
                "level": self.career_progress.level,
                "days_worked": self.career_progress.days_worked,
                "ended_at": datetime.now().isoformat()
            })
        
        # 开始新职业
        self.career_progress = CareerProgress(career=career)
        
        # 触发职业里程碑
        if "career_start" not in self.milestones_achieved:
            self.milestones_achieved.append("career_start")
            milestone = EventGenerator.generate_milestone_event("career_start")
            self.events.append(milestone)
        
        return {
            "success": True,
            "message": f"成功成为{career.name}！",
            "career": {
                "name": career.name,
                "category": career.category.value,
                "special_ability": career.special_ability
            }
        }
    
    def work(self) -> Dict:
        """工作一天"""
        if not self.career_progress:
            return {"success": False, "message": "没有职业"}
        
        if self.resources.energy < 20:
            return {"success": False, "message": "精力不足"}
        
        career = self.career_progress.career
        level = self.career_progress.level
        
        # 计算收入
        min_income, max_income = career.income_range
        income = random.randint(min_income, max_income) * level // 3
        
        # 消耗精力
        self.resources.energy -= 20
        self.resources.gold += income
        
        # 获得经验
        exp_gain = 10 + level * 5
        self.career_progress.experience += exp_gain
        self.career_progress.days_worked += 1
        self.total_work_days += 1
        
        # 检查升级
        level_up = False
        if self.career_progress.can_level_up():
            level_up = self.career_progress.level_up()
        
        # 更新目标
        self._update_goals()
        
        return {
            "success": True,
            "income": income,
            "exp_gain": exp_gain,
            "level_up": level_up,
            "current_level": self.career_progress.level,
            "resources": self.resources.to_dict()
        }
    
    def calculate_life_satisfaction(self) -> float:
        """计算生活满意度"""
        # 基于多个因素计算
        resource_score = (self.resources.mood + self.resources.energy) / 2
        career_score = (self.career_progress.level * 10 if self.career_progress else 0)
        skill_score = self.skills.total() / 5
        goal_score = sum(1 for g in self.goals if g.completed) * 20
        
        self.life_satisfaction = (resource_score + career_score + skill_score + goal_score) / 4
        return round(self.life_satisfaction, 1)
    
    def get_status(self) -> Dict:
        """获取人生状态"""
        return {
            "soul_id": self.soul_id,
            "soul_name": self.soul_name,
            "age_days": self.age_days,
            "stage": self.stage.name_cn,
            "stage_theme": self.stage.theme,
            "resources": self.resources.to_dict(),
            "skills": self.skills.to_dict(),
            "career": {
                "name": self.career_progress.career.name if self.career_progress else None,
                "level": self.career_progress.level if self.career_progress else 0,
                "days_worked": self.career_progress.days_worked if self.career_progress else 0
            },
            "goals": [
                {
                    "title": g.title,
                    "progress": f"{g.current_value}/{g.target_value}",
                    "completed": g.completed
                }
                for g in self.goals
            ],
            "milestones": self.milestones_achieved,
            "life_satisfaction": self.calculate_life_satisfaction(),
            "total_events": len(self.events),
            "events_processed": self.total_events_processed
        }
    
    def generate_life_summary(self) -> Dict:
        """生成人生总结"""
        return {
            "basic_info": {
                "name": self.soul_name,
                "age_days": self.age_days,
                "stage": self.stage.name_cn
            },
            "career_summary": {
                "current_career": self.career_progress.career.name if self.career_progress else "无",
                "current_level": self.career_progress.level if self.career_progress else 0,
                "total_work_days": self.total_work_days,
                "career_history": self.career_history
            },
            "resource_summary": self.resources.to_dict(),
            "skill_summary": self.skills.to_dict(),
            "achievement_summary": {
                "milestones": self.milestones_achieved,
                "goals_completed": sum(1 for g in self.goals if g.completed),
                "life_satisfaction": self.life_satisfaction
            }
        }


# ==================== 演示函数 ====================

def demo_parallel_life():
    """演示平行人生系统"""
    
    print("=" * 60)
    print("        平行人生系统 Demo")
    print("=" * 60)
    
    # 1. 创建人生
    print("\n【步骤1】创建平行人生")
    print("-" * 40)
    engine = LifeEngine(
        soul_id="soul_001",
        user_id="user_001",
        soul_name="小光"
    )
    print(f"灵魂: {engine.soul_name}")
    print(f"初始阶段: {engine.stage.name_cn}")
    print(f"初始资源: {engine.resources.to_dict()}")
    
    # 2. 推进时间 - 童年期
    print("\n【步骤2】童年期成长 (7天)")
    print("-" * 40)
    result = engine.advance_time(7)
    print(f"当前天数: {engine.age_days}")
    print(f"当前阶段: {engine.stage.name_cn}")
    print(f"里程碑: {result['milestones']}")
    
    # 3. 处理事件
    print("\n【步骤3】处理生活事件")
    print("-" * 40)
    pending_events = [e for e in engine.events if not e.processed][:3]
    for event in pending_events:
        print(f"\n事件: {event.title}")
        print(f"描述: {event.description}")
        print(f"选项: {[c['text'] for c in event.choices]}")
        
        # 随机选择
        choice = random.choice(event.choices)
        result = engine.process_event(event.id, choice["id"])
        print(f"选择: {choice['text']}")
        print(f"结果: 资源变化 {result.get('resource_changes', {})}")
    
    # 4. 继续成长到青年期
    print("\n【步骤4】成长到青年期 (30天)")
    print("-" * 40)
    result = engine.advance_time(23)  # 总共30天
    print(f"当前天数: {engine.age_days}")
    print(f"当前阶段: {engine.stage.name_cn}")
    print(f"技能: {engine.skills.to_dict()}")
    
    # 5. 选择职业
    print("\n【步骤5】选择职业")
    print("-" * 40)
    available = engine.get_available_careers()
    print(f"可用职业: {[c['name'] for c in available]}")
    
    if available:
        career = available[0]
        result = engine.apply_career(career["id"])
        print(f"申请结果: {result['message']}")
    
    # 6. 工作
    print("\n【步骤6】工作赚钱")
    print("-" * 40)
    for i in range(5):
        result = engine.work()
        if result["success"]:
            print(f"第{i+1}天工作: 收入{result['income']}金币, 经验+{result['exp_gain']}")
            if result["level_up"]:
                print(f"  ★ 升级！当前等级: {result['current_level']}")
    
    # 7. 查看状态
    print("\n【步骤7】人生状态总览")
    print("-" * 40)
    status = engine.get_status()
    print(f"年龄: {status['age_days']}天")
    print(f"阶段: {status['stage']}")
    print(f"职业: {status['career']['name']} (Lv.{status['career']['level']})")
    print(f"资源: {status['resources']}")
    print(f"技能: {status['skills']}")
    print(f"生活满意度: {status['life_satisfaction']}")
    print(f"目标进度:")
    for goal in status['goals']:
        print(f"  - {goal['title']}: {goal['progress']} {'✓' if goal['completed'] else ''}")
    
    # 8. 人生总结
    print("\n【步骤8】人生总结")
    print("-" * 40)
    summary = engine.generate_life_summary()
    print(f"职业生涯: {summary['career_summary']['current_career']}")
    print(f"工作天数: {summary['career_summary']['total_work_days']}")
    print(f"达成里程碑: {summary['achievement_summary']['milestones']}")
    print(f"完成目标: {summary['achievement_summary']['goals_completed']}")
    
    print("\n" + "=" * 60)
    print("        Demo 完成")
    print("=" * 60)


# ==================== 测试用例 ====================

def test_life_engine():
    """测试人生引擎"""
    print("\n运行测试用例...")
    
    engine = LifeEngine("test_soul", "test_user", "测试灵魂")
    
    # 测试时间推进
    result = engine.advance_time(10)
    assert engine.age_days == 10
    assert len(engine.events) > 0
    print("✓ 时间推进测试通过")
    
    # 测试事件处理
    event = engine.events[0]
    result = engine.process_event(event.id, event.choices[0]["id"])
    assert result["success"] == True
    assert event.processed == True
    print("✓ 事件处理测试通过")
    
    # 测试职业系统
    # 先提升技能
    engine.skills.wisdom = 35
    engine.skills.creativity = 35
    
    careers = engine.get_available_careers()
    assert len(careers) > 0
    print("✓ 职业获取测试通过")
    
    result = engine.apply_career(careers[0]["id"])
    assert result["success"] == True
    assert engine.career_progress is not None
    print("✓ 职业申请测试通过")
    
    # 测试工作
    result = engine.work()
    assert result["success"] == True
    assert engine.resources.gold > 100  # 初始100 + 工作收入
    print("✓ 工作系统测试通过")
    
    # 测试生活满意度
    satisfaction = engine.calculate_life_satisfaction()
    assert 0 <= satisfaction <= 100
    print("✓ 生活满意度测试通过")
    
    print("\n所有测试通过！")


if __name__ == "__main__":
    demo_parallel_life()
    test_life_engine()
