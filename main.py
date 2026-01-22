from manim import *
import asyncio
import edge_tts
import os

# 1. 定义语音生成函数
async def generate_tts(text, output_file):
    # 使用微软 Xiaoxiao 语音，听起来非常自然
    communicate = edge_tts.Communicate(text, "zh-CN-XiaoxiaoNeural")
    await communicate.save(output_file)

class Scene3D(ThreeDScene):
    def construct(self):
        # --- 第一步：准备语音 ---
        script_text = "大家好，我是一个由代码生成的3D机器人。复杂不是限制，只是人的想象力有限。"
        audio_file = "voice.mp3"
        
        # 在渲染前生成语音
        asyncio.run(generate_tts(script_text, audio_file))
        
        # 预估语音时长为 5 秒（进阶可动态获取）
        audio_duration = 5 

        # --- 第二步：3D 建模 (马卡龙风格) ---
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        
        # 头和身体，使用你提到的 Tailwind 色系
        head = Sphere(radius=0.5, color="#F472B6").shift(OUT * 1.5) # 粉色
        body = Cylinder(radius=0.4, height=2, color="#0EA5E9")      # 天蓝色
        
        # 简单的眼睛，增加灵动感
        eye_l = Sphere(radius=0.1, color=WHITE).shift(OUT * 1.7 + RIGHT * 0.2 + FORWARD * 0.4)
        eye_r = Sphere(radius=0.1, color=WHITE).shift(OUT * 1.7 + LEFT * 0.2 + FORWARD * 0.4)
        
        character = VGroup(head, body, eye_l, eye_r)

        # --- 第三步：渲染动画 ---
        grid = NumberPlane(colors={"axis": WHITE, "lines": GREY})
        self.add(grid)
        self.play(Create(character))
        self.wait(0.5)

        # 边说话边运动：旋转并跳跃前进
        self.play(
            character.animate.shift(RIGHT * 3),
            Rotate(character, angle=PI*2, axis=OUT),
            run_time=audio_duration,
            rate_func=linear
        )
        self.wait(1)
