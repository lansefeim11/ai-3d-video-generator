from manim import *

class Scene3D(ThreeDScene):
    def construct(self):
        # 1. 设置相机视角
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)

        # 2. 创建 3D 几何小人 (头部和身体)
        # 使用 Sphere 和 Cylinder 构建
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

        # 模拟走路：平移的同时加上缩放呼吸效果（替代报错的 wiggle）
        self.play(
            character.animate.shift(RIGHT * 3),
            character.animate.scale(1.2),
            run_time=2,
            rate_func=there_and_back # 这是一个内置的平滑往复函数
        )
        
        # 5. 视角旋转
        self.begin_ambient_camera_rotation(rate=0.2)
        self.play(character.animate.rotate(PI/4, axis=UP))
        self.wait(2)
