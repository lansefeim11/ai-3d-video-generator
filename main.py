from manim import *
import asyncio
import edge_tts

async def generate_tts(text, output_file):
    communicate = edge_tts.Communicate(text, "zh-CN-XiaoxiaoNeural")
    await communicate.save(output_file)

class Scene3D(ThreeDScene):
    def construct(self):
        # 1. 语音
        asyncio.run(generate_tts("你好，我是你的3D机器人。这次我采用了自动吸附组装，身体各部位绝对不会再乱跑了。", "voice.mp3"))

        # 2. 建模
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        
        # 先做身体
        body = Cylinder(radius=0.5, height=1.5, color="#0EA5E9")
        
        # 用 next_to 就像贴磁铁一样：把头贴在身体的 UP（上方）
        head = Sphere(radius=0.5, color="#F472B6").next_to(body, UP, buff=0)
        
        # 眼睛：先放在头中心，再往外推（OUT）和往两边挪
        eye_l = Sphere(radius=0.08, color=WHITE).move_to(head.get_center()).shift(OUT*0.48 + RIGHT*0.2 + UP*0.1)
        eye_r = Sphere(radius=0.08, color=WHITE).move_to(head.get_center() + OUT*0.48 + LEFT*0.2 + UP*0.1)
        
        # 手臂：贴在身体左右
        arm_l = Cylinder(radius=0.1, height=0.8, color="#F472B6").rotate(90*DEGREES).next_to(body, LEFT, buff=-0.1)
        arm_r = Cylinder(radius=0.1, height=0.8, color="#F472B6").rotate(90*DEGREES).next_to(body, RIGHT, buff=-0.1)
        
        # 腿：贴在身体下方
        leg_l = Cylinder(radius=0.12, height=0.8, color="#0EA5E9").next_to(body, DOWN, buff=0).shift(LEFT*0.2)
        leg_r = Cylinder(radius=0.12, height=0.8, color="#0EA5E9").next_to(body, DOWN, buff=0).shift(RIGHT*0.2)
        
        robot = VGroup(body, head, eye_l, eye_r, arm_l, arm_r, leg_l, leg_r)
        
        # 3. 动画
        self.add(NumberPlane())
        self.play(Create(robot))
        self.begin_ambient_camera_rotation(rate=0.3)
        self.play(robot.animate.shift(UP*1), run_time=5)
        self.wait()
