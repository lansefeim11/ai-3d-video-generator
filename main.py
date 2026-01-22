from manim import *
import asyncio
import edge_tts
import os

# 1. 定义语音生成函数
async def generate_tts(text, output_file):
    communicate = edge_tts.Communicate(text, "zh-CN-XiaoxiaoNeural")
    await communicate.save(output_file)

class Scene3D(ThreeDScene):
    def construct(self):
        # --- 准备语音 ---
        script_text = "大家好，我是一个由代码生成的3D机器人。复杂不是限制，只是人的想象力有限。"
        audio_file = "voice.mp3"
        asyncio.run(generate_tts(script_text, audio_file))
        audio_duration = 5 

        # --- 3D 建模 (马卡龙风格) ---
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        
        # 头和身体
        head = Sphere(radius=0.5, color="#F472B6").shift(OUT * 1.5)
        body = Cylinder(radius=0.4, height=2, color="#0EA5E9")
        
        # 修正眼睛位置：使用简单的坐标加法，避免使用未定义的 FORWARD
        # OUT 是 Z 轴正方向，UP 是 Y 轴正方向，RIGHT 是 X 轴正方向
        eye_l = Sphere(radius=0.1, color=WHITE).shift(OUT * 1.7 + RIGHT * 0.2 + UP * 0.3)
        eye_r = Sphere(radius=0.1, color=WHITE).shift(OUT * 1.7 + LEFT * 0.2 + UP * 0.3)
        
        character = VGroup(head, body, eye_l, eye_r)

        # --- 渲染动画 ---
        grid = NumberPlane()
        self.add(grid)
        self.play(Create(character))
        self.wait(0.5)

        # 边说话边运动：旋转并移动
        self.play(
            character.animate.shift(RIGHT * 3),
            Rotate(character, angle=PI*2, axis=OUT),
            run_time=audio_duration,
            rate_func=linear
        )
        self.wait(1)
