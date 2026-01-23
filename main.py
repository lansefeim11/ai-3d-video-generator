from manim import *
import asyncio
import edge_tts

# 语音生成
async def generate_tts(text, output_file):
    try:
        communicate = edge_tts.Communicate(text, "zh-CN-XiaoxiaoNeural")
        await communicate.save(output_file)
    except Exception as e:
        print(f"TTS Error: {e}")

class Scene3D(ThreeDScene):
    def construct(self):
        # --- 1. 语音准备 ---
        script_text = "你好，我是你的机器人朋友。现在我换了新的组装方式，绝对不会再散架了。"
        audio_file = "voice.mp3"
        asyncio.run(generate_tts(script_text, audio_file))

        # --- 2. 积木拼接建模 ---
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        
        # A. 核心地基：身体 (放在原点)
        body = Cylinder(radius=0.4, height=1.5, color="#0EA5E9")
        
        # B. 头部：直接吸附在身体的“上方” (UP方向)
        head = Sphere(radius=0.5, color="#F472B6")
        head.next_to(body, UP, buff=0) # buff=0 表示无缝衔接
        
        # C. 眼睛：在头部中心基础上，往“前方”挪一点
        eye_l = Sphere(radius=0.08, color=WHITE).move_to(head.get_center() + OUT*0.45 + RIGHT*0.2)
        eye_r = Sphere(radius=0.08, color=WHITE).move_to(head.get_center() + OUT*0.45 + LEFT*0.2)
        
        # D. 手臂：吸附在身体的“左/右”侧
        arm_l = Cylinder(radius=0.1, height=0.7, color="#F472B6").rotate(90*DEGREES)
        arm_l.next_to(body, LEFT, buff=-0.1) # buff负数表示嵌入身体一点
        
        arm_r = Cylinder(radius=0.1, height=0.7, color="#F472B6").rotate(90*DEGREES)
        arm_r.next_to(body, RIGHT, buff=-0.1)
        
        # E. 腿部：吸附在身体的“下方”
        leg_l = Cylinder(radius=0.12, height=0.6, color="#0EA5E9")
        leg_l.next_to(body, DOWN, buff=0).shift(LEFT*0.2)
        
        leg_r = Cylinder(radius=0.12, height=0.6, color="#0EA5E9")
        leg_r.next_to(body, DOWN, buff=0).shift(RIGHT*0.2)
        
        character = VGroup(head, body, eye_l, eye_r, arm_l, arm_r, leg_l, leg_r)

        # --- 3. 极简动画 (防止报错) ---
        self.add(NumberPlane())
        self.play(Create(character))
        self.begin_ambient_camera_rotation(rate=0.2)
        self.play(character.animate.shift(UP*0.5), run_time=5)
        self.wait(1)
