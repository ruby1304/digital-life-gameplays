"""
挑战者契约 (Challenger Contract) - 基础Demo

这个demo展示了挑战者契约系统的核心功能：
1. 契约创建与管理
2. 打卡签到机制
3. 进度追踪系统
4. 奖励结算
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
from datetime import datetime, timedelta
import random


# ==================== 枚举定义 ====================

class ContractType(Enum):
    """契约类型"""
    HABIT = "习惯契约"
    GOAL = "目标契约"
    CHALLENGE = "挑战契约"
    QUIT = "戒除契约"
    EXPLORE = "探索契约"


class ContractStatus(Enum):
    """契约状态"""
    ACTIVE = "进行中"
    COMPLETED = "已完成"
    FAILED = "已失败"
    PAUSED = "已暂停"


class ContractLevel(Enum):
    """契约等级"""
    NOVICE = (1, "契约新手", 1)
    APPRENTICE = (2, "契约学徒", 2)
    WALKER = (3, "契约行者", 3)
    MASTER = (4, "契约大师", 5)
    GRANDMASTER = (5, "契约宗师", 7)
    LEGEND = (6, "契约传奇", 10)
    
    def __init__(self, level: int, title: str, max_contracts: int):
        self.level = level
        self.title = title
        self.max_contracts = max_contracts


# ==================== 数据类定义 ====================

@dataclass
class CheckIn:
    """打卡记录"""
    date: datetime
    success: bool
    note: str = ""
    proof: Optional[str] = None


@dataclass
class Contract:
    """契约"""
    id: str
    type: ContractType
    title: str
    description: str
    target_days: int
    current_streak: int = 0
    longest_streak: int = 0
    total_check_ins: int = 0
    status: ContractStatus = ContractStatus.ACTIVE
    created_at: datetime = field(default_factory=datetime.now)
    check_ins: List[CheckIn] = field(default_factory=list)
    rewards_earned: int = 0
    
    @property
    def progress(self) -> float:
        """完成进度"""
        if not self.check_ins:
            return 0.0
        return min(1.0, self.total_check_ins / self.target_days)
    
    @property
    def is_completed(self) -> bool:
        """是否完成"""
        return self.total_check_ins >= self.target_days


@dataclass
class CompletionReward:
    """完成奖励"""
    experience: int
    soul_energy: int
    special_items: List[str]
    achievement: Optional[str] = None


# ==================== 契约引擎类 ====================

class ChallengerContract:
    """挑战者契约系统"""
    
    def __init__(self, soul_id: str, soul_name: str):
        self.soul_id = soul_id
        self.soul_name = soul_name
        self.contracts: List[Contract] = []
        self.total_experience = 0
        self.completed_contracts = 0
        self.created_at = datetime.now()
        
        # 契约模板
        self._contract_templates = {
            ContractType.HABIT: [
                ("早起挑战", "每天早上7点前起床", 21),
                ("运动习惯", "每天运动30分钟", 30),
                ("阅读计划", "每天阅读30分钟", 30),
                ("冥想练习", "每天冥想15分钟", 21),
            ],
            ContractType.GOAL: [
                ("学习新技能", "掌握一项新技能的基础", 60),
                ("完成项目", "完成一个个人项目", 45),
                ("考取证书", "获得一项专业认证", 90),
            ],
            ContractType.CHALLENGE: [
                ("极限挑战", "完成一项极限运动", 7),
                ("创意挑战", "每天创作一个作品", 30),
                ("社交挑战", "每天认识一个新朋友", 14),
            ],
            ContractType.QUIT: [
                ("戒烟计划", "完全戒烟", 90),
                ("早睡计划", "每晚11点前入睡", 30),
                ("减少手机", "每天屏幕时间<3小时", 21),
            ],
            ContractType.EXPLORE: [
                ("新体验", "尝试10件从未做过的事", 30),
                ("新技能", "学习一项全新技能", 45),
                ("新领域", "探索一个新知识领域", 60),
            ],
        }
        
        # 激励语库
        self._motivations = [
            "每一次坚持都是对自己的投资！",
            "你比想象中更强大！",
            "今天的努力是明天的骄傲！",
            "灵魂与你同在，一起加油！",
            "突破舒适区，遇见更好的自己！",
            "坚持就是胜利，你已经很棒了！",
            "每一步都算数，继续前进！",
            "你的决心正在改变命运！",
        ]
    
    @property
    def level(self) -> ContractLevel:
        """获取当前等级"""
        for lvl in reversed(list(ContractLevel)):
            if self.completed_contracts >= (lvl.level - 1) * 3:
                return lvl
        return ContractLevel.NOVICE
    
    @property
    def active_contracts(self) -> List[Contract]:
        """获取活跃契约"""
        return [c for c in self.contracts if c.status == ContractStatus.ACTIVE]
    
    def can_create_contract(self) -> bool:
        """是否可以创建新契约"""
        return len(self.active_contracts) < self.level.max_contracts
    
    def create_contract(self, contract_type: ContractType, 
                       title: Optional[str] = None,
                       description: Optional[str] = None,
                       target_days: Optional[int] = None) -> Optional[Contract]:
        """创建契约"""
        if not self.can_create_contract():
            return None
        
        # 使用模板或自定义
        if title is None:
            templates = self._contract_templates.get(contract_type, [])
            if templates:
                title, description, target_days = random.choice(templates)
            else:
                title = f"自定义{contract_type.value}"
                description = "自定义目标描述"
                target_days = 21
        
        contract = Contract(
            id=f"contract_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000, 9999)}",
            type=contract_type,
            title=title,
            description=description,
            target_days=target_days
        )
        
        self.contracts.append(contract)
        return contract
    
    def check_in(self, contract_id: str, 
                 success: bool = True,
                 note: str = "",
                 proof: Optional[str] = None,
                 force_date: Optional[datetime] = None) -> Dict:
        """打卡签到
        
        Args:
            contract_id: 契约ID
            success: 是否成功
            note: 备注
            proof: 证明
            force_date: 强制指定日期（用于测试）
        """
        contract = next((c for c in self.contracts if c.id == contract_id), None)
        if not contract or contract.status != ContractStatus.ACTIVE:
            return {"success": False, "message": "契约不存在或已结束"}
        
        # 检查今日是否已打卡
        check_date = force_date if force_date else datetime.now()
        today = check_date.date()
        if any(ci.date.date() == today for ci in contract.check_ins):
            return {"success": False, "message": "今日已打卡"}
        
        # 创建打卡记录
        check_in = CheckIn(
            date=check_date,
            success=success,
            note=note,
            proof=proof
        )
        contract.check_ins.append(check_in)
        
        if success:
            contract.total_check_ins += 1
            contract.current_streak += 1
            contract.longest_streak = max(contract.longest_streak, contract.current_streak)
            
            # 检查是否完成
            if contract.is_completed:
                return self._complete_contract(contract)
        else:
            contract.current_streak = 0
        
        # 计算奖励
        streak_bonus = min(contract.current_streak * 2, 20)
        exp_earned = 5 + streak_bonus
        
        return {
            "success": True,
            "message": random.choice(self._motivations),
            "current_streak": contract.current_streak,
            "progress": f"{contract.total_check_ins}/{contract.target_days}",
            "exp_earned": exp_earned,
            "motivation": random.choice(self._motivations)
        }
    
    def _complete_contract(self, contract: Contract) -> Dict:
        """完成契约"""
        contract.status = ContractStatus.COMPLETED
        self.completed_contracts += 1
        
        # 计算奖励
        base_exp = contract.target_days * 10
        streak_bonus = contract.longest_streak * 5
        total_exp = base_exp + streak_bonus
        
        self.total_experience += total_exp
        
        # 特殊奖励
        special_items = []
        if contract.longest_streak >= contract.target_days:
            special_items.append("完美坚持徽章")
        if contract.target_days >= 60:
            special_items.append("毅力之星")
        
        reward = CompletionReward(
            experience=total_exp,
            soul_energy=total_exp // 2,
            special_items=special_items,
            achievement=f"{contract.title}完成者"
        )
        
        return {
            "success": True,
            "completed": True,
            "message": f"恭喜完成契约【{contract.title}】！",
            "reward": {
                "experience": reward.experience,
                "soul_energy": reward.soul_energy,
                "special_items": reward.special_items,
                "achievement": reward.achievement
            }
        }
    
    def get_contract_status(self, contract_id: str) -> Optional[Dict]:
        """获取契约状态"""
        contract = next((c for c in self.contracts if c.id == contract_id), None)
        if not contract:
            return None
        
        return {
            "id": contract.id,
            "title": contract.title,
            "type": contract.type.value,
            "status": contract.status.value,
            "progress": f"{contract.total_check_ins}/{contract.target_days}",
            "progress_percent": f"{contract.progress * 100:.1f}%",
            "current_streak": contract.current_streak,
            "longest_streak": contract.longest_streak,
            "days_remaining": max(0, contract.target_days - contract.total_check_ins)
        }
    
    def get_overall_status(self) -> Dict:
        """获取整体状态"""
        return {
            "soul_name": self.soul_name,
            "level": self.level.title,
            "level_num": self.level.level,
            "max_contracts": self.level.max_contracts,
            "active_contracts": len(self.active_contracts),
            "total_contracts": len(self.contracts),
            "completed_contracts": self.completed_contracts,
            "total_experience": self.total_experience
        }


# ==================== 演示函数 ====================

def demo_challenger_contract():
    """演示挑战者契约系统"""
    
    print("=" * 60)
    print("        挑战者契约系统 Demo")
    print("=" * 60)
    
    # 1. 创建契约系统
    print("\n【步骤1】创建契约系统")
    print("-" * 40)
    system = ChallengerContract(soul_id="soul_001", soul_name="契约守护者")
    print(f"灵魂名称: {system.soul_name}")
    print(f"初始等级: {system.level.title}")
    print(f"可同时进行契约数: {system.level.max_contracts}")
    
    # 2. 创建契约
    print("\n【步骤2】创建契约")
    print("-" * 40)
    contract1 = system.create_contract(ContractType.HABIT)
    print(f"契约名称: {contract1.title}")
    print(f"契约描述: {contract1.description}")
    print(f"目标天数: {contract1.target_days}天")
    
    contract2 = system.create_contract(ContractType.CHALLENGE)
    if contract2:
        print(f"\n契约名称: {contract2.title}")
        print(f"契约描述: {contract2.description}")
        print(f"目标天数: {contract2.target_days}天")
    else:
        print(f"\n无法创建第二个契约（已达上限）")
    
    # 3. 打卡签到
    print("\n【步骤3】打卡签到")
    print("-" * 40)
    for i in range(5):
        result = system.check_in(contract1.id, success=True, note=f"第{i+1}天打卡")
        if result["success"]:
            print(f"Day {i+1}: {result['message']}")
            print(f"  连续: {result['current_streak']}天 | 进度: {result['progress']}")
        else:
            print(f"Day {i+1}: {result['message']}")
    
    # 4. 查看契约状态
    print("\n【步骤4】查看契约状态")
    print("-" * 40)
    status = system.get_contract_status(contract1.id)
    print(f"契约: {status['title']}")
    print(f"状态: {status['status']}")
    print(f"进度: {status['progress_percent']}")
    print(f"当前连续: {status['current_streak']}天")
    print(f"最长连续: {status['longest_streak']}天")
    
    # 5. 模拟完成契约
    print("\n【步骤5】模拟完成契约")
    print("-" * 40)
    # 先完成第一个契约以提升等级（使用不同日期模拟）
    print("完成第一个契约以解锁更多契约槽...")
    from datetime import timedelta
    for i in range(contract1.target_days - contract1.total_check_ins):
        # 模拟不同日期的打卡
        fake_date = datetime.now() + timedelta(days=i)
        result = system.check_in(contract1.id, success=True, force_date=fake_date)
        if result.get("completed"):
            print(f"契约【{contract1.title}】完成！")
            break
    
    # 创建一个短期契约用于演示完成
    short_contract = system.create_contract(
        ContractType.HABIT,
        title="7天早起挑战",
        description="连续7天早起",
        target_days=7
    )
    
    if short_contract:
        print(f"创建短期契约: {short_contract.title}")
        
        # 连续打卡完成
        for i in range(7):
            fake_date = datetime.now() + timedelta(days=i)
            result = system.check_in(short_contract.id, success=True, force_date=fake_date)
            if result.get("completed"):
                print(f"\n契约完成！")
                print(f"获得经验: {result['reward']['experience']}")
                print(f"灵魂能量: {result['reward']['soul_energy']}")
                print(f"特殊奖励: {result['reward']['special_items']}")
                print(f"成就: {result['reward']['achievement']}")
    else:
        print("无法创建新契约")
    
    # 6. 整体状态
    print("\n【步骤6】整体状态")
    print("-" * 40)
    overall = system.get_overall_status()
    print(f"等级: {overall['level']} (Lv.{overall['level_num']})")
    print(f"活跃契约: {overall['active_contracts']}/{overall['max_contracts']}")
    print(f"已完成契约: {overall['completed_contracts']}")
    print(f"总经验: {overall['total_experience']}")
    
    print("\n" + "=" * 60)
    print("        Demo 完成")
    print("=" * 60)


if __name__ == "__main__":
    demo_challenger_contract()
