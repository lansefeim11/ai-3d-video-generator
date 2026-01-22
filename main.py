from manim import *
import asyncio
import edge_tts
from moviepy.editor import VideoFileClip, AudioFileClip

# 1. 生成语音的函数
async def generate_tts(text, output_file):
    communicate = edge_tts.Communicate(text, "zh-CN-XiaoxiaoNeural")
    await communicate.save(output_file)

class Scene3D(ThreeDScene):
    def construct(self):
        # --- 语音准备 ---
        text = "大家好，我是由代码生成的3D小人。我可以一边走路一边说话！"
        audio_file = "voice.mp3"
        asyncio.run(generate_tts(text, audio_file))
        
        # 获取音频长度（这里简单设为 4 秒，进阶可用 moviepy 读取长度）
        audio_duration = 4 

        # --- 场景建模 ---
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        head = Sphere(radius=0.5, color="#F472B6").shift(OUT * 1.5) # 马卡龙粉
        body = Cylinder(radius=0.4, height=2, color="#0EA5E9")      # 天空蓝
        character = VGroup(head, body)
        
        # --- 动画流程 ---
        self.add(NumberPlane())
        self.play(Create(character))
        
        # 说话时的动作：边走边跳，时长与语音同步
        self.play(
            character.animate.shift(RIGHT * 4),
            rate_func=there_and_back,
            run_time=audio_duration
        )
        self.wait(1)

# --- 自动缝合逻辑 ---
# 这一步通常在 GitHub Actions 里通过命令行完成，但也可以写在 Python 里
