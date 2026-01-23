from manim import *
import asyncio
import edge_tts

async def generate_tts(text, output_file):
    communicate = edge_tts.Communicate(text, "zh-CN-XiaoxiaoNeural")
    await communicate.save(output_file)

class Scene3D(ThreeDScene):
    def construct(self):
        # --- 1. 语音 ---
        asyncio.run(generate_tts("你好，我是修复完毕的机器人。现在我的头、身体和四肢已经完全对齐了。", "voice.mp3"))

        # --- 2. 积木式建模 (绝对对齐逻辑) ---
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        
        # 身体：作为中心地基
        body = Cylinder(radius=0.4, height=1.5, color="#0EA5E9")
        
        # 头部：使用 next_to(body, UP) 强制吸附在身体正上方，绝不会偏移到侧面
        head = Sphere(radius=0.5, color="#F472B6").next_to(body, UP, buff=0)
        
        # 眼睛：基于头中心定位，向 OUT(前) 挪动，确保贴在脸上
        eye_l = Sphere(radius=0.08, color=WHITE).move_to(head.get_center()).shift(OUT*0.48 + RIGHT*0.2 + UP*0.1)
        eye_r = Sphere(radius=0.08, color=WHITE).move_to(head.get_center()).shift(OUT*0.48 + LEFT*0.2 + UP*0.1)
        
        # 手臂：吸附在身体左右侧
        arm_l = Cylinder(radius=0.1, height=0.7, color="#F472B6").rotate(90*DEGREES).next_to(body, LEFT, buff=-0.1)
        arm_r = Cylinder(radius=0.1, height=0.7, color="#F472B6").rotate(90*DEGREES).next_to(body, RIGHT, buff=-0.1)
        
        # 腿部：吸附在身体下方
        leg_l = Cylinder(radius=0.12, height=0.7, color="#0EA5E9").next_to(body, DOWN, buff=0).shift(LEFT*0.2)
        leg_r = Cylinder(radius=0.12, height=0.7, color="#0EA5E9").next_to(body, DOWN, buff=0).shift(RIGHT*0.2)
        
        character = VGroup(body, head, eye_l, eye_r, arm_l, arm_r, leg_l, leg_r)

        # --- 3. 极简动画 ---
        self.add(NumberPlane())
        self.play(Create(character))
        self.begin_ambient_camera_rotation(rate=0.2)
        self.play(character.animate.shift(UP * 0.5), run_time=5)
        self.wait()
