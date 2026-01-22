from manim import *
import asyncio
import edge_tts
import os

# 1. 定义语音生成函数
async def generate_tts(text, output_file):
    try:
        communicate = edge_tts.Communicate(text, "zh-CN-XiaoxiaoNeural")
        await communicate.save(output_file)
    except Exception as e:
        print(f"TTS Error: {e}")

class Scene3D(ThreeDScene):
    def construct(self):
        # --- 1. 准备语音 ---
        script_text = "大家好，我的 3D 身体已经组装完成了！现在比例非常协调，准备开始今天的任务。"
        audio_file = "voice.mp3"
        asyncio.run(generate_tts(script_text, audio_file))
        audio_duration = 7 

        # --- 2. 3D 建模 (坐标精调版) ---
        # 设置初始相机视角
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        
        # 身体：放在中心，底部接触地面
        body = Cylinder(radius=0.4, height=1.2, color="#0EA5E9").shift(UP * 0.6)
        
        # 头部：精准落在身体上方
        head = Sphere(radius=0.45, color="#F472B6").shift(UP * 1.65)
        
        # 眼睛：贴在头部的正前方 (OUT方向)
        eye_l = Sphere(radius=0.08, color=WHITE).shift(UP * 1.75 + RIGHT * 0.18 + OUT * 0.4)
        eye_r = Sphere(radius=0.08, color=WHITE).shift(UP * 1.75 + LEFT * 0.18 + OUT * 0.4)
        
        # 手臂：放在身体两侧中间高度
        arm_l = Cylinder(radius=0.08, height=0.7, color="#F472B6").rotate(90*DEGREES).shift(UP * 0.8 + LEFT * 0.65)
        arm_r = Cylinder(radius=0.08, height=0.7, color="#F472B6").rotate(90*DEGREES).shift(UP * 0.8 + RIGHT * 0.65)
        
        # 腿部：在身体下方对称
        leg_l = Cylinder(radius=0.1, height=0.6, color="#0EA5E9").shift(DOWN * 0.1 + LEFT * 0.2)
        leg_r = Cylinder(radius=0.1, height=0.6, color="#0EA5E9").shift(DOWN * 0.1 + RIGHT * 0.2)
        
        # 组合角色
        character = VGroup(head, body, eye_l, eye_r, arm_l, arm_r, leg_l, leg_r)

        # --- 3. 渲染动画 ---
        grid = NumberPlane(colors={"axis": WHITE, "grid": BLUE_E})
        self.add(grid)
        
        # 入场：整体从地面升起
        self.play(FadeIn(character, shift=UP), run_time=1.5)
        self.wait(0.5)

        # 核心动画：边说话边旋转相机 + 手臂微摆
        self.begin_ambient_camera_rotation(rate=0.3) # 开启自动相机旋转
        
        self.play(
            # 小人做一个轻微的上下漂浮动作（呼吸感）
            character.animate.shift(UP * 0.2),
            # 右手臂向上挥动
            arm_r.animate.rotate(45*DEGREES, about_point=arm_r.get_start()),
            run_time=audio_duration / 2,
            rate_func=there_and_back
        )
        
        self.stop_ambient_camera_rotation()
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES) # 回到初始视角
        self.wait(1)
