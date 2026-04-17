"""
命运剧场 (Fate Theater) - 基础Demo

这个demo展示了命运剧场系统的核心功能：
1. 剧本与章节管理
2. 选择分支系统
3. 情感追踪
4. 结局达成
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
from datetime import datetime
import random
import json


# ==================== 枚举定义 ====================

class ScriptType(Enum):
    """剧本类型"""
    GROWTH = "成长之路"
    FATE = "命运抉择"
    EMOTION = "情感羁绊"
    ADVENTURE = "冒险传奇"
    DAILY = "日常物语"


class EmotionType(Enum):
    """情感类型"""
    JOY = "喜悦"
    SADNESS = "悲伤"
    ANGER = "愤怒"
    FEAR = "恐惧"
    SURPRISE = "惊讶"
    TRUST = "信任"
    ANTICIPATION = "期待"


class EndingType(Enum):
    """结局类型"""
    TRUE = "真结局"
    GOOD = "好结局"
    NORMAL = "普通结局"
    BAD = "坏结局"
    SECRET = "隐藏结局"


# ==================== 数据类定义 ====================

@dataclass
class Choice:
    """选择项"""
    id: str
    text: str
    effects: Dict[str, int]  # 对情感/属性的影响
    next_scene_id: str
    required_flags: List[str] = field(default_factory=list)


@dataclass
class Dialogue:
    """对话"""
    speaker: str
    text: str
    emotion: Optional[EmotionType] = None


@dataclass
class Scene:
    """场景"""
    id: str
    dialogues: List[Dialogue]
    choices: List[Choice]
    background: str = ""
    music: str = ""


@dataclass
class Chapter:
    """章节"""
    id: str
    title: str
    scenes: List[Scene]
    summary: str = ""


@dataclass
class Ending:
    """结局"""
    type: EndingType
    title: str
    description: str
    required_choices: List[str]
    required_flags: List[str]


@dataclass
class EmotionState:
    """情感状态"""
    emotions: Dict[EmotionType, int] = field(default_factory=lambda: {
        EmotionType.JOY: 50,
        EmotionType.SADNESS: 20,
        EmotionType.ANGER: 10,
        EmotionType.FEAR: 15,
        EmotionType.SURPRISE: 30,
        EmotionType.TRUST: 50,
        EmotionType.ANTICIPATION: 40
    })
    
    def apply_effects(self, effects: Dict[str, int]):
        """应用情感效果"""
        for emotion_name, change in effects.items():
            try:
                emotion = EmotionType(emotion_name)
                self.emotions[emotion] = max(0, min(100, 
                    self.emotions.get(emotion, 50) + change))
            except ValueError:
                pass
    
    def get_dominant_emotion(self) -> EmotionType:
        """获取主导情感"""
        return max(self.emotions.items(), key=lambda x: x[1])[0]
    
    def to_dict(self) -> Dict:
        return {e.value: v for e, v in self.emotions.items()}


@dataclass
class ChoiceRecord:
    """选择记录"""
    chapter_id: str
    scene_id: str
    choice_id: str
    choice_text: str
    timestamp: datetime = field(default_factory=datetime.now)


# ==================== 剧本类 ====================

class Script:
    """剧本"""
    
    def __init__(self, title: str, script_type: ScriptType, 
                 description: str = ""):
        self.id = f"script_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        self.title = title
        self.script_type = script_type
        self.description = description
        self.chapters: List[Chapter] = []
        self.endings: List[Ending] = []
        self.characters: Dict[str, Dict] = {}
    
    def add_chapter(self, chapter: Chapter):
        """添加章节"""
        self.chapters.append(chapter)
    
    def add_ending(self, ending: Ending):
        """添加结局"""
        self.endings.append(ending)


# ==================== 剧本进度管理 ====================

class ScriptProgress:
    """剧本进度"""
    
    def __init__(self, script: Script, soul_id: str):
        self.script = script
        self.soul_id = soul_id
        self.current_chapter_idx = 0
        self.current_scene_idx = 0
        self.emotion_state = EmotionState()
        self.choices_made: List[ChoiceRecord] = []
        self.flags: List[str] = []
        self.started_at = datetime.now()
        self.completed = False
        self.achieved_ending: Optional[Ending] = None
    
    def get_current_scene(self) -> Optional[Scene]:
        """获取当前场景"""
        if self.current_chapter_idx < len(self.script.chapters):
            chapter = self.script.chapters[self.current_chapter_idx]
            if self.current_scene_idx < len(chapter.scenes):
                return chapter.scenes[self.current_scene_idx]
        return None
    
    def make_choice(self, choice: Choice) -> bool:
        """做出选择"""
        # 检查前置条件
        for flag in choice.required_flags:
            if flag not in self.flags:
                return False
        
        # 记录选择
        scene = self.get_current_scene()
        if scene:
            record = ChoiceRecord(
                chapter_id=self.script.chapters[self.current_chapter_idx].id,
                scene_id=scene.id,
                choice_id=choice.id,
                choice_text=choice.text
            )
            self.choices_made.append(record)
        
        # 应用效果
        self.emotion_state.apply_effects(choice.effects)
        
        # 推进到下一场景
        self._advance_to_scene(choice.next_scene_id)
        
        # 检查结局
        self._check_endings()
        
        return True
    
    def _advance_to_scene(self, scene_id: str):
        """推进到指定场景"""
        for ch_idx, chapter in enumerate(self.script.chapters):
            for sc_idx, scene in enumerate(chapter.scenes):
                if scene.id == scene_id:
                    self.current_chapter_idx = ch_idx
                    self.current_scene_idx = sc_idx
                    return
        
        # 如果找不到场景，尝试推进到下一章节
        self.current_chapter_idx += 1
        self.current_scene_idx = 0
    
    def _check_endings(self):
        """检查是否达成结局"""
        choice_ids = [c.choice_id for c in self.choices_made]
        
        for ending in self.script.endings:
            # 检查选择条件
            choices_match = all(
                cid in choice_ids for cid in ending.required_choices
            )
            # 检查标志条件
            flags_match = all(
                flag in self.flags for flag in ending.required_flags
            )
            
            if choices_match and flags_match:
                self.achieved_ending = ending
                self.completed = True
                return
    
    def get_progress(self) -> Dict:
        """获取进度信息"""
        total_scenes = sum(len(ch.scenes) for ch in self.script.chapters)
        current_scene_num = sum(
            len(self.script.chapters[i].scenes) 
            for i in range(self.current_chapter_idx)
        ) + self.current_scene_idx + 1
        
        return {
            "script_title": self.script.title,
            "current_chapter": self.current_chapter_idx + 1,
            "total_chapters": len(self.script.chapters),
            "current_scene": current_scene_num,
            "total_scenes": total_scenes,
            "progress_percent": round(current_scene_num / total_scenes * 100, 1),
            "emotion_state": self.emotion_state.to_dict(),
            "dominant_emotion": self.emotion_state.get_dominant_emotion().value,
            "choices_count": len(self.choices_made),
            "completed": self.completed,
            "ending": self.achieved_ending.title if self.achieved_ending else None
        }


# ==================== 剧本生成器 ====================

class ScriptGenerator:
    """剧本生成器"""
    
    @staticmethod
    def create_sample_script() -> Script:
        """创建示例剧本"""
        script = Script(
            title="命运的十字路口",
            script_type=ScriptType.FATE,
            description="一个关于选择与成长的故事"
        )
        
        # 第一章
        chapter1 = Chapter(
            id="ch1",
            title="启程",
            scenes=[
                Scene(
                    id="scene1_1",
                    dialogues=[
                        Dialogue("旁白", "清晨的阳光洒在小镇上..."),
                        Dialogue("主角", "新的一天开始了。"),
                        Dialogue("神秘老人", "年轻人，你面前有三条路...")
                    ],
                    choices=[
                        Choice("c1", "选择智慧之路", 
                               {"信任": 10, "期待": 5}, "scene1_2a"),
                        Choice("c2", "选择情感之路", 
                               {"喜悦": 10, "信任": 5}, "scene1_2b"),
                        Choice("c3", "选择冒险之路", 
                               {"惊讶": 10, "期待": 15}, "scene1_2c")
                    ]
                ),
                Scene(id="scene1_2a", dialogues=[
                    Dialogue("旁白", "你踏上了追求智慧的道路...")
                ], choices=[
                    Choice("c1a", "向导师请教", {"信任": 15}, "scene1_3")
                ]),
                Scene(id="scene1_2b", dialogues=[
                    Dialogue("旁白", "你选择了倾听内心的声音...")
                ], choices=[
                    Choice("c1b", "帮助他人", {"喜悦": 15}, "scene1_3")
                ]),
                Scene(id="scene1_2c", dialogues=[
                    Dialogue("旁白", "你踏上了未知的冒险...")
                ], choices=[
                    Choice("c1c", "勇往直前", {"惊讶": 15}, "scene1_3")
                ]),
                Scene(id="scene1_3", dialogues=[
                    Dialogue("旁白", "第一章结束，新的旅程即将开始...")
                ], choices=[])
            ],
            summary="故事的开端，命运的抉择"
        )
        
        script.add_chapter(chapter1)
        
        # 添加结局
        script.add_ending(Ending(
            type=EndingType.GOOD,
            title="智慧之光",
            description="通过智慧找到了人生的真谛",
            required_choices=["c1", "c1a"],
            required_flags=[]
        ))
        
        script.add_ending(Ending(
            type=EndingType.GOOD,
            title="情感羁绊",
            description="用真心赢得了珍贵的羁绊",
            required_choices=["c2", "c1b"],
            required_flags=[]
        ))
        
        script.add_ending(Ending(
            type=EndingType.NORMAL,
            title="冒险归来",
            description="经历冒险，收获成长",
            required_choices=["c3", "c1c"],
            required_flags=[]
        ))
        
        return script


# ==================== 演示函数 ====================

def demo_fate_theater():
    """演示命运剧场系统"""
    
    print("=" * 60)
    print("        命运剧场系统 Demo")
    print("=" * 60)
    
    # 1. 创建剧本
    print("\n【步骤1】加载剧本")
    print("-" * 40)
    script = ScriptGenerator.create_sample_script()
    print(f"剧本: {script.title}")
    print(f"类型: {script.script_type.value}")
    print(f"章节数: {len(script.chapters)}")
    print(f"结局数: {len(script.endings)}")
    
    # 2. 开始剧本
    print("\n【步骤2】开始剧本")
    print("-" * 40)
    progress = ScriptProgress(script, soul_id="soul_001")
    print(f"剧本已开始: {progress.started_at}")
    
    # 3. 播放场景
    print("\n【步骤3】播放场景")
    print("-" * 40)
    scene = progress.get_current_scene()
    if scene:
        print(f"当前场景: {scene.id}")
        for dialogue in scene.dialogues:
            print(f"  [{dialogue.speaker}]: {dialogue.text}")
        
        print("\n可选选择:")
        for i, choice in enumerate(scene.choices, 1):
            print(f"  {i}. {choice.text}")
    
    # 4. 做出选择
    print("\n【步骤4】做出选择")
    print("-" * 40)
    if scene and scene.choices:
        choice = scene.choices[0]  # 选择第一个选项
        print(f"选择: {choice.text}")
        success = progress.make_choice(choice)
        print(f"选择结果: {'成功' if success else '失败'}")
        print(f"情感效果: {choice.effects}")
    
    # 5. 查看进度
    print("\n【步骤5】查看进度")
    print("-" * 40)
    progress_info = progress.get_progress()
    print(f"当前章节: {progress_info['current_chapter']}/{progress_info['total_chapters']}")
    print(f"进度: {progress_info['progress_percent']}%")
    print(f"主导情感: {progress_info['dominant_emotion']}")
    print(f"选择次数: {progress_info['choices_count']}")
    
    # 6. 继续剧情
    print("\n【步骤6】继续剧情")
    print("-" * 40)
    scene = progress.get_current_scene()
    if scene and scene.choices:
        for dialogue in scene.dialogues:
            print(f"  [{dialogue.speaker}]: {dialogue.text}")
        
        if scene.choices:
            choice = scene.choices[0]
            print(f"\n选择: {choice.text}")
            progress.make_choice(choice)
    
    # 7. 最终状态
    print("\n【步骤7】最终状态")
    print("-" * 40)
    progress_info = progress.get_progress()
    print(f"剧本完成: {progress_info['completed']}")
    print(f"达成结局: {progress_info['ending'] or '未达成'}")
    print(f"情感状态: {progress_info['emotion_state']}")
    
    print("\n" + "=" * 60)
    print("        Demo 完成")
    print("=" * 60)


if __name__ == "__main__":
    demo_fate_theater()
