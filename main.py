from manim import *
import asyncio
import edge_tts
import os

# 1. 定义语音生成函数 (增加异常处理)
async def generate_tts(text, output_file):
    try:
        communicate = edge_tts.Communicate(text, "zh-CN-XiaoxiaoNeural")
        await communicate.save(output_file)
    except Exception as e:
        print(f"TTS Error: {e}")

class Scene3D(ThreeDScene):
    def construct(self):
        # --- 1. 准备语音 ---
        script_text = "大家好，我是你的3D机器人。我已经进化出了四肢，现在可以自由行动了。"
        audio_file = "voice.mp3"
        asyncio.run(generate_tts(script_text, audio_file))
        audio_duration = 6 

        # --- 2. 3D 建模 (升级版) ---
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        
        # 头部和身体
        head = Sphere(radius=0.5, color="#F472B6").shift(UP * 1.5)
        body = Cylinder(radius=0.4, height=1.5, color="#0EA5E9").shift(UP * 0.5)
        
        # 眼睛
        eye_l = Sphere(radius=0.1, color=WHITE).shift(UP * 1.6 + RIGHT * 0.2 + OUT * 0.45)
        eye_r = Sphere(radius=0.1, color=WHITE).shift(UP * 1.6 + LEFT * 0.2 + OUT * 0.45)
        
        # 手臂 (使用圆柱体)
        arm_l = Cylinder(radius=0.08, height=0.8, color="#F472B6").rotate(90*DEGREES).shift(UP * 0.8 + LEFT * 0.7)
        arm_r = Cylinder(radius=0.08, height=0.8, color="#F472B6").rotate(90*DEGREES).shift(UP * 0.8 + RIGHT * 0.7)
        
        # 腿部
        leg_l = Cylinder(radius=0.1, height=0.7, color="#0EA5E9").shift(DOWN * 0.5 + LEFT * 0.2)
        leg_r = Cylinder(radius=0.1, height=0.7, color="#0EA5E9").shift(DOWN * 0.5 + RIGHT * 0.2)
        
        # 组合成角色
        character = VGroup(head, body, eye_l, eye_r, arm_l, arm_r, leg_l, leg_r)

        # --- 3. 渲染动画 ---
        grid = NumberPlane()
        self.add(grid)
        self.play(FadeIn(character))
        self.wait(0.5)

        # 边说话边做动作：旋转相机 + 小人平移
        self.begin_ambient_camera_rotation(rate=0.2) # 自动旋转相机
        self.play(
            character.animate.shift(RIGHT * 2),
            arm_r.animate.rotate(30*DEGREES, about_point=arm_r.get_center()),
            run_time=audio_duration,
            rate_func=linear
        )
        self.stop_ambient_camera_rotation()
        self.wait(1)
