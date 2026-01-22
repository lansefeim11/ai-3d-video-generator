from manim import *

class Scene3D(ThreeDScene):
    def construct(self):
        # 1. 设置相机视角
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)

        # 2. 创建 3D 几何小人 (头部和身体)
        head = Sphere(radius=0.5, color=ORANGE).shift(OUT * 1.5)
        body = Cylinder(radius=0.4, height=2, color=BLUE)
        
        # 将部位组合成一个整体
        character = VGroup(head, body)

        # 3. 创建地面
        grid = NumberPlane()
        
        # 4. 动画逻辑
        self.add(grid)
        self.play(Create(character))
        self.wait(1)

        # 模拟走路（平移 + 跳跃）
        self.play(
            character.animate.shift(RIGHT * 3),
            RateFuncs.wiggle(character), # 增加一点抖动效果
            run_time=3
        )
        
        # 5. 视角旋转
        self.begin_ambient_camera_rotation(rate=0.1)
        self.play(character.animate.scale(1.5))
        self.wait(2)
