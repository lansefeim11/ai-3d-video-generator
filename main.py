from manim import *
import asyncio
import edge_tts
import os

# 语音生成
async def generate_tts(text, output_file):
    try:
        communicate = edge_tts.Communicate(text, "zh-CN-XiaoxiaoNeural")
        await communicate.save(output_file)
    except Exception as e:
        print(f"TTS Error: {e}")

class Scene3D(ThreeDScene):
    def construct(self):
        # 1. 准备语音
        script_text = "你好，我是修复完毕的3D机器人。现在我的头、身体和四肢已经完全对齐了。"
        audio_file = "voice.mp3"
        asyncio.run(generate_tts(script_text, audio_file))
        audio_duration = 6

        # 2. 3D 建模 (使用相对对齐逻辑，防止散架)
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        
        # 身体是基准
        body = Cylinder(radius=0.4, height=1.5, color="#0EA5E9")
        
        # 头吸附在身体上方 (UP方向)
        head = Sphere(radius=0.5, color="#F472B6").next_to(body, UP, buff=0)
        
        # 眼睛贴在头上 (向 OUT 方向偏移)
        eye_l = Sphere(radius=0.08, color=WHITE).move_to(head.get_center() + OUT*0.45 + RIGHT*0.2 + UP*0.1)
        eye_r = Sphere(radius=0.08, color=WHITE).move_to(head.get_center() + OUT*0.45 + LEFT*0.2 + UP*0.1)
        
        # 手臂对称分布
        arm_l = Cylinder(radius=0.1, height=0.8, color="#F472B6").rotate(90*DEGREES).next_to(body, LEFT, buff=-0.1).shift(UP*0.2)
        arm_r = Cylinder(radius=0.1, height=0.8, color="#F472B6").rotate(90*DEGREES).next_to(body, RIGHT, buff=-0.1).shift(UP*0.2)
        
        # 腿部
        leg_l = Cylinder(radius=0.12, height=0.8, color="#0EA5E9").next_to(body, DOWN, buff=0).shift(LEFT*0.2)
        leg_r = Cylinder(radius=0.12, height=0.8, color="#0EA5E9").next_to(body, DOWN, buff=0).shift(RIGHT*0.2)
        
        character = VGroup(head, body, eye_l, eye_r, arm_l, arm_r, leg_l, leg_r)

        # 3. 渲染动画
        self.add(NumberPlane())
        self.play(FadeIn(character))
        self.wait(0.5)

        # 简单的整体旋转动画，避开所有可能报错的函数
        self.begin_ambient_camera_rotation(rate=0.4)
        self.play(
            character.animate.shift(UP * 0.5),
            run_time=audio_duration,
            rate_func=there_and_back
        )
        self.stop_ambient_camera_rotation()
        self.wait(1)
