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
        script_text = "你好，我是你的代码机器人。虽然刚才出了一点小错误，但我现在已经修复完毕了。"
        audio_file = "voice.mp3"
        asyncio.run(generate_tts(script_text, audio_file))
        audio_duration = 7 

        # --- 2. 3D 建模 (坐标精调版) ---
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        
        # 身体：蓝色圆柱
        body = Cylinder(radius=0.4, height=1.2, color="#0EA5E9").shift(UP * 0.6)
        
        # 头部：粉色球体
        head = Sphere(radius=0.45, color="#F472B6").shift(UP * 1.65)
        
        # 眼睛：白色小球 (位置往外拉一点，防止埋进头里)
        eye_l = Sphere(radius=0.08, color=WHITE).shift(UP * 1.75 + RIGHT * 0.18 + OUT * 0.42)
        eye_r = Sphere(radius=0.08, color=WHITE).shift(UP * 1.75 + LEFT * 0.18 + OUT * 0.42)
        
        # 手臂：简化旋转逻辑
        arm_l = Cylinder(radius=0.08, height=0.7, color="#F472B6").rotate(90*DEGREES).shift(UP * 0.8 + LEFT * 0.65)
        arm_r = Cylinder(radius=0.08, height=0.7, color="#F472B6").rotate(90*DEGREES).shift(UP * 0.8 + RIGHT * 0.65)
        
        # 腿部
        leg_l = Cylinder(radius=0.1, height=0.6, color="#0EA5E9").shift(DOWN * 0.1 + LEFT * 0.2)
        leg_r = Cylinder(radius=0.1, height=0.6, color="#0EA5E9").shift(DOWN * 0.1 + RIGHT * 0.2)
        
        # 组合角色
        character = VGroup(head, body, eye_l, eye_r, arm_l, arm_r, leg_l, leg_r)

        # --- 3. 渲染动画 ---
        # 使用最基础的网格，避免参数报错
        grid = NumberPlane()
        self.add(grid)
        
        # 入场：淡入
        self.play(FadeIn(character))
        self.wait(0.5)

        # 核心动画：整体旋转和相机移动
        # 修正：不再使用 about_point=arm_r.get_start()，改用中心旋转
        self.begin_ambient_camera_rotation(rate=0.2) 
        self.play(
            character.animate.shift(UP * 0.3),
            arm_r.animate.rotate(30*DEGREES),
            run_time=audio_duration / 2,
            rate_func=there_and_back
        )
        self.stop_ambient_camera_rotation()
        self.wait(1)
