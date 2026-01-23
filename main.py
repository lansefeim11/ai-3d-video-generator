from manim import *
import asyncio
import edge_tts

# 语音生成函数
async def generate_tts(text, output_file):
    communicate = edge_tts.Communicate(text, "zh-CN-XiaoxiaoNeural")
    await communicate.save(output_file)

class RobotScene(Scene):
    def construct(self):
        # --- 1. 语音准备 ---
        script = "你好！这是我的 2.0 进化版本。采用了霓虹渐变风格和动态阴影，是不是比之前的 3D 效果更有质感？"
        asyncio.run(generate_tts(script, "voice.mp3"))

        # --- 2. 颜色定义 (赛博朋克风格) ---
        color_main = [BLUE_C, PURPLE_C] # 渐变色
        color_shadow = "#222222"        # 阴影色

        # --- 3. 机器人建模 ---
        # 身体：带渐变色的圆角矩形
        body = RoundedRectangle(corner_radius=0.3, height=2.2, width=1.8)
        body.set_fill(color=color_main, opacity=1)
        body.set_stroke(WHITE, width=4)

        # 头部
        head = Circle(radius=0.7)
        head.set_fill(color=color_main, opacity=1)
        head.set_stroke(WHITE, width=4)
        head.next_to(body, UP, buff=0.1)

        # 眼睛：发光效果
        eye_l = Circle(radius=0.12, color=WHITE, fill_opacity=1).move_to(head.get_center() + LEFT*0.25 + UP*0.1)
        eye_r = Circle(radius=0.12, color=WHITE, fill_opacity=1).move_to(head.get_center() + RIGHT*0.25 + UP*0.1)
        
        # 装饰细节：胸前的按钮
        btn1 = Dot(radius=0.1, color=PINK).move_to(body.get_center() + UP*0.4 + LEFT*0.3)
        btn2 = Dot(radius=0.1, color=YELLOW).move_to(body.get_center() + UP*0.4 + RIGHT*0.3)

        # --- 4. 阴影处理 ---
        # 为整个机器人创建阴影：复制一份并向右下方偏移
        robot_group = VGroup(body, head, eye_l, eye_r, btn1, btn2)
        shadow = robot_group.copy()
        shadow.set_fill(color_shadow, opacity=0.3)
        shadow.set_stroke(color_shadow, width=0)
        shadow.shift(RIGHT*0.15 + DOWN*0.15)
        
        # 确保阴影在机器人底层
        final_robot = VGroup(shadow, robot_group).center()

        # --- 5. 动画效果 ---
        # 底部背景：让画面不那么单调
        grid = NumberPlane(background_line_style={"stroke_opacity": 0.2})
        self.add(grid)

        # 机器人入场：带有弹性效果的缩放
        self.play(FadeIn(shadow), DrawBorderThenFill(robot_group), run_time=1.5)
        self.play(final_robot.animate.scale(1.2), rate_func=there_and_back, run_time=1)

        # 说话时的动态：轻微左右晃动 + 眼睛闪烁
        self.play(
            final_robot.animate.shift(UP*0.2),
            eye_l.animate.scale(1.2),
            eye_r.animate.scale(1.2),
            run_time=3,
            rate_func=wiggle
        )
        self.wait(2)
