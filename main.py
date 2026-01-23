from manim import *
import asyncio
import edge_tts

# 语音生成
async def generate_tts(text, output_file):
    communicate = edge_tts.Communicate(text, "zh-CN-XiaoxiaoNeural")
    await asyncio.wait_for(communicate.save(output_file), timeout=10)

class RobotScene(Scene):
    def construct(self):
        # 1. 语音准备
        script = "你好！既然3D世界太复杂，我决定换个2.5D的身体。你看，现在我不仅对齐了，还很帅气。"
        asyncio.run(generate_tts(script, "voice.mp3"))

        # 2. 2.5D 机器人建模 (使用平面图形堆叠)
        # 身体：圆角矩形
        body = RoundedRectangle(corner_radius=0.2, height=2, width=1.5, color=BLUE, fill_opacity=0.8)
        
        # 头部：圆形，直接对齐到身体上方
        head = Circle(radius=0.6, color=PINK, fill_opacity=1).next_to(body, UP, buff=0.1)
        
        # 眼睛：两个小点
        eye_l = Dot(color=WHITE).move_to(head.get_center() + LEFT*0.2 + UP*0.1)
        eye_r = Dot(color=WHITE).move_to(head.get_center() + RIGHT*0.2 + UP*0.1)
        
        # 天线：模拟 3D 感
        antenna = Line(head.get_top(), head.get_top() + UP*0.5, color=WHITE)
        tip = Dot(antenna.get_end(), color=RED)
        
        # 手臂：左右伸出
        arm_l = Line(body.get_left(), body.get_left() + LEFT*0.8, stroke_width=8, color=BLUE_A)
        arm_r = Line(body.get_right(), body.get_right() + RIGHT*0.8, stroke_width=8, color=BLUE_A)

        robot = VGroup(body, head, eye_l, eye_r, antenna, tip, arm_l, arm_r).center()

        # 3. 动画：模拟 3D 的灵动感
        self.play(DrawBorderThenFill(robot))
        self.play(robot.animate.scale(1.1).set_color(BLUE_B), run_time=1, rate_func=there_and_back)
        
        # 说话时的微动（呼吸感）
        self.play(
            robot.animate.shift(UP*0.3),
            tip.animate.set_color(YELLOW),
            run_time=3,
            rate_func=wiggle
        )
        self.wait(2)
