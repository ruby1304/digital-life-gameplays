"""
时间守护者 (Time Guardian) - 基础Demo

这个demo展示了时间守护者系统的核心功能：
1. 日程规划与管理
2. 习惯追踪系统
3. 时间分析报告
4. 生活节奏优化
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
from datetime import datetime, timedelta
import random


# ==================== 枚举定义 ====================

class GuardianLevel(Enum):
    """守护者等级"""
    APPRENTICE = (1, "时间学徒", 0)
    GUARDIAN = (2, "时间守护者", 800)
    KEEPER = (3, "时间管家", 2500)
    MASTER = (4, "时间大师", 6000)
    SAGE = (5, "时间贤者", 12000)
    LORD = (6, "时间之主", 20000)
    
    def __init__(self, level: int, title: str, exp_required: int):
        self.level = level
        self.title = title
        self.exp_required = exp_required


class HabitType(Enum):
    """习惯类型"""
    DAILY = "每日习惯"
    WEEKLY = "每周习惯"
    CHALLENGE = "挑战习惯"
    LONG_TERM = "长期习惯"


class TaskPriority(Enum):
    """任务优先级"""
    URGENT = "紧急"
    HIGH = "高"
    MEDIUM = "中"
    LOW = "低"


# ==================== 数据类定义 ====================

@dataclass
class Task:
    """任务"""
    id: str
    title: str
    priority: TaskPriority
    estimated_minutes: int
    deadline: Optional[datetime] = None
    completed: bool = False
    completed_at: Optional[datetime] = None


@dataclass
class Habit:
    """习惯"""
    id: str
    name: str
    habit_type: HabitType
    target_count: int  # 目标次数
    current_streak: int = 0  # 当前连续
    best_streak: int = 0  # 最佳连续
    total_completions: int = 0
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class HabitRecord:
    """习惯记录"""
    habit_id: str
    completed_at: datetime
    note: str = ""


@dataclass
class TimeBlock:
    """时间块"""
    start: datetime
    end: datetime
    task: Optional[Task] = None
    type: str = "free"  # free, task, break


@dataclass
class DaySchedule:
    """日程"""
    date: datetime
    time_blocks: List[TimeBlock] = field(default_factory=list)
    tasks: List[Task] = field(default_factory=list)
    
    def add_task(self, task: Task):
        self.tasks.append(task)
    
    def complete_task(self, task_id: str) -> bool:
        for task in self.tasks:
            if task.id == task_id and not task.completed:
                task.completed = True
                task.completed_at = datetime.now()
                return True
        return False


@dataclass
class TimeAnalysis:
    """时间分析"""
    total_tasks: int
    completed_tasks: int
    completion_rate: float
    focus_hours: float
    break_hours: float
    productivity_score: float
    suggestions: List[str]


# ==================== 时间守护者类 ====================

class TimeGuardian:
    """时间守护者"""
    
    def __init__(self, soul_id: str, name: str):
        self.soul_id = soul_id
        self.name = name
        self.total_experience = 0
        self.habits: Dict[str, Habit] = {}
        self.habit_records: List[HabitRecord] = []
        self.schedules: Dict[str, DaySchedule] = {}
        self.created_at = datetime.now()
    
    @property
    def level(self) -> GuardianLevel:
        """获取当前等级"""
        for lvl in reversed(list(GuardianLevel)):
            if self.total_experience >= lvl.exp_required:
                return lvl
        return GuardianLevel.APPRENTICE
    
    def create_task(self, title: str, priority: TaskPriority, 
                   estimated_minutes: int, deadline: Optional[datetime] = None) -> Task:
        """创建任务"""
        task = Task(
            id=f"task_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(100, 999)}",
            title=title,
            priority=priority,
            estimated_minutes=estimated_minutes,
            deadline=deadline
        )
        return task
    
    def add_task_to_schedule(self, date: datetime, task: Task):
        """添加任务到日程"""
        date_key = date.strftime("%Y-%m-%d")
        if date_key not in self.schedules:
            self.schedules[date_key] = DaySchedule(date=date)
        self.schedules[date_key].add_task(task)
    
    def complete_task(self, date: datetime, task_id: str) -> int:
        """完成任务，返回获得的经验"""
        date_key = date.strftime("%Y-%m-%d")
        schedule = self.schedules.get(date_key)
        if schedule and schedule.complete_task(task_id):
            exp_gain = 10
            self.total_experience += exp_gain
            return exp_gain
        return 0
    
    def create_habit(self, name: str, habit_type: HabitType, 
                    target_count: int = 1) -> Habit:
        """创建习惯"""
        habit = Habit(
            id=f"habit_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(100, 999)}",
            name=name,
            habit_type=habit_type,
            target_count=target_count
        )
        self.habits[habit.id] = habit
        return habit
    
    def check_in_habit(self, habit_id: str, note: str = "") -> int:
        """习惯打卡，返回获得的经验"""
        habit = self.habits.get(habit_id)
        if not habit:
            return 0
        
        # 记录打卡
        record = HabitRecord(
            habit_id=habit_id,
            completed_at=datetime.now(),
            note=note
        )
        self.habit_records.append(record)
        
        # 更新习惯统计
        habit.total_completions += 1
        habit.current_streak += 1
        habit.best_streak = max(habit.best_streak, habit.current_streak)
        
        # 计算经验
        exp_gain = {
            HabitType.DAILY: 10,
            HabitType.WEEKLY: 30,
            HabitType.CHALLENGE: 50,
            HabitType.LONG_TERM: 20
        }.get(habit.habit_type, 10)
        
        # 连续奖励
        if habit.current_streak >= 7:
            exp_gain += 20
        elif habit.current_streak >= 3:
            exp_gain += 5
        
        self.total_experience += exp_gain
        return exp_gain
    
    def break_streak(self, habit_id: str):
        """中断连续"""
        habit = self.habits.get(habit_id)
        if habit:
            habit.current_streak = 0
    
    def analyze_time_usage(self, date: datetime) -> TimeAnalysis:
        """分析时间使用"""
        date_key = date.strftime("%Y-%m-%d")
        schedule = self.schedules.get(date_key)
        
        if not schedule:
            return TimeAnalysis(
                total_tasks=0,
                completed_tasks=0,
                completion_rate=0.0,
                focus_hours=0.0,
                break_hours=0.0,
                productivity_score=0.0,
                suggestions=["开始记录你的日程吧！"]
            )
        
        total = len(schedule.tasks)
        completed = sum(1 for t in schedule.tasks if t.completed)
        rate = completed / total if total > 0 else 0
        
        # 估算专注时间
        focus_minutes = sum(
            t.estimated_minutes for t in schedule.tasks if t.completed
        )
        
        # 生产力评分
        score = rate * 60 + min(focus_minutes / 60, 8) * 40
        
        suggestions = []
        if rate < 0.5:
            suggestions.append("尝试减少任务数量，专注于重要事项")
        if focus_minutes < 120:
            suggestions.append("建议每天至少保持2小时专注时间")
        if rate >= 0.8:
            suggestions.append("做得很好！保持这个节奏")
        
        return TimeAnalysis(
            total_tasks=total,
            completed_tasks=completed,
            completion_rate=round(rate, 2),
            focus_hours=round(focus_minutes / 60, 1),
            break_hours=round((480 - focus_minutes) / 60, 1),
            productivity_score=round(score, 1),
            suggestions=suggestions
        )
    
    def get_habit_status(self, habit_id: str) -> Dict:
        """获取习惯状态"""
        habit = self.habits.get(habit_id)
        if not habit:
            return {}
        
        return {
            "name": habit.name,
            "type": habit.habit_type.value,
            "current_streak": habit.current_streak,
            "best_streak": habit.best_streak,
            "total_completions": habit.total_completions,
            "progress": min(habit.current_streak / 21 * 100, 100)  # 21天养成
        }
    
    def get_status(self) -> Dict:
        """获取守护者状态"""
        return {
            "name": self.name,
            "level": self.level.title,
            "level_num": self.level.level,
            "total_experience": self.total_experience,
            "habits_count": len(self.habits),
            "total_check_ins": len(self.habit_records),
            "active_streaks": sum(1 for h in self.habits.values() if h.current_streak > 0),
            "best_streak": max((h.best_streak for h in self.habits.values()), default=0)
        }


# ==================== 演示函数 ====================

def demo_time_guardian():
    """演示时间守护者系统"""
    
    print("=" * 60)
    print("        时间守护者系统 Demo")
    print("=" * 60)
    
    # 1. 创建守护者
    print("\n【步骤1】创建时间守护者")
    print("-" * 40)
    guardian = TimeGuardian(soul_id="soul_001", name="时间小光")
    print(f"守护者: {guardian.name}")
    print(f"初始等级: {guardian.level.title}")
    
    # 2. 创建日程和任务
    print("\n【步骤2】创建今日任务")
    print("-" * 40)
    today = datetime.now()
    
    tasks = [
        guardian.create_task("完成项目报告", TaskPriority.HIGH, 120),
        guardian.create_task("回复邮件", TaskPriority.MEDIUM, 30),
        guardian.create_task("学习新技能", TaskPriority.LOW, 60),
    ]
    
    for task in tasks:
        guardian.add_task_to_schedule(today, task)
        print(f"  - {task.title} ({task.priority.value}, {task.estimated_minutes}分钟)")
    
    # 3. 完成任务
    print("\n【步骤3】完成任务")
    print("-" * 40)
    for task in tasks[:2]:  # 完成前两个
        exp = guardian.complete_task(today, task.id)
        print(f"  完成: {task.title} -> +{exp}经验")
    
    # 4. 创建习惯
    print("\n【步骤4】创建习惯")
    print("-" * 40)
    habits = [
        guardian.create_habit("早起", HabitType.DAILY),
        guardian.create_habit("运动", HabitType.DAILY),
        guardian.create_habit("阅读", HabitType.DAILY),
    ]
    
    for habit in habits:
        print(f"  - {habit.name} ({habit.habit_type.value})")
    
    # 5. 习惯打卡
    print("\n【步骤5】习惯打卡")
    print("-" * 40)
    for habit in habits:
        exp = guardian.check_in_habit(habit.id)
        print(f"  打卡: {habit.name} -> +{exp}经验")
    
    # 6. 模拟连续打卡
    print("\n【步骤6】模拟连续打卡")
    print("-" * 40)
    for _ in range(6):  # 模拟连续6天
        guardian.check_in_habit(habits[0].id)
    
    status = guardian.get_habit_status(habits[0].id)
    print(f"  {habits[0].name}: 连续{status['current_streak']}天")
    print(f"  最佳记录: {status['best_streak']}天")
    
    # 7. 时间分析
    print("\n【步骤7】时间分析报告")
    print("-" * 40)
    analysis = guardian.analyze_time_usage(today)
    print(f"  总任务: {analysis.total_tasks}")
    print(f"  完成率: {analysis.completion_rate * 100:.0f}%")
    print(f"  专注时间: {analysis.focus_hours}小时")
    print(f"  生产力评分: {analysis.productivity_score}")
    print(f"  建议: {analysis.suggestions[0] if analysis.suggestions else '无'}")
    
    # 8. 最终状态
    print("\n【步骤8】守护者最终状态")
    print("-" * 40)
    status = guardian.get_status()
    print(f"等级: {status['level']} (Lv.{status['level_num']})")
    print(f"总经验: {status['total_experience']}")
    print(f"习惯数: {status['habits_count']}")
    print(f"总打卡: {status['total_check_ins']}")
    print(f"最佳连续: {status['best_streak']}天")
    
    print("\n" + "=" * 60)
    print("        Demo 完成")
    print("=" * 60)


if __name__ == "__main__":
    demo_time_guardian()
