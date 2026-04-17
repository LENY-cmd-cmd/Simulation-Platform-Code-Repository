# # import asyncio
# # from PhantasyIslandPythonRemoteControl import AirplaneController
# # from PhantasyIslandPythonRemoteControl.airplane_manager import get_airplane_manager
# # import cv2
# # import numpy as np
# # from collections import deque
# #
# # # ===================== 全局参数 =====================
# # PosList = [
# #     [150, 150, 200],
# #     [450, 150, 200],
# #     [150, 450, 200],
# #     [450, 450, 200],
# #     [150, 750, 200],
# #     [450, 750, 200]
# # ]
# #
# # big_maze = [[[0,0,0,0] for _ in range(6)] for _ in range(9)]
# # FLY_HEIGHT = 100
# # START_POINT = (50, 150)
# #
# # # 降落区范围：x 50~550，y 800~900，三机间隔 >50
# # LANDING = {
# #     'c3': (150, 850),
# #     'c4': (300, 850),
# #     'c5': (450, 850)
# # }
# #
# # # ===================== 图像识别 =====================
# # def wall_ratio(binary_img, y0, y1, x0, x1):
# #     h, w = binary_img.shape
# #     y0 = max(0, y0)
# #     y1 = min(h, y1)
# #     x0 = max(0, x0)
# #     x1 = min(w, x1)
# #     if y0 >= y1 or x0 >= x1:
# #         return 0.0
# #     region = binary_img[y0:y1, x0:x1]
# #     return np.mean(region)
# #
# # def maze_to_3x3_array(img):
# #     wall = (img < 80).astype(np.uint8)
# #     x_edges = [40, 120, 200, 280]
# #     y_edges = [0, 80, 160, 235]
# #     band = 6
# #     margin = 8
# #     threshold = 0.18
# #     result = []
# #     for r in range(3):
# #         row_result = []
# #         for c in range(3):
# #             xl, xr = x_edges[c], x_edges[c+1]
# #             yt, yb = y_edges[r], y_edges[r+1]
# #             top_ratio = wall_ratio(wall, yt-band, yt+band, xl+margin, xr-margin)
# #             top = 1 if top_ratio > threshold else 0
# #             bottom_ratio = wall_ratio(wall, yb-band, yb+band, xl+margin, xr-margin)
# #             bottom = 1 if bottom_ratio > threshold else 0
# #             left_ratio = wall_ratio(wall, yt+margin, yb-margin, xl-band, xl+band)
# #             left = 1 if left_ratio > threshold else 0
# #             right_ratio = wall_ratio(wall, yt+margin, yb-margin, xr-band, xr+band)
# #             right = 1 if right_ratio > threshold else 0
# #             row_result.append([top, bottom, left, right])
# #         result.append(row_result)
# #     return result
# #
# # def handle_image(img, x, y):
# #     img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# #     result = maze_to_3x3_array(img_gray)
# #     print(f"拍摄点位 ({x},{y}) 识别结果：")
# #     for row in result:
# #         print(row)
# #
# #     if x < 300:
# #         start_col = 0
# #     else:
# #         start_col = 3
# #     if y > 600:
# #         start_row = 0
# #     elif y > 300:
# #         start_row = 3
# #     else:
# #         start_row = 6
# #
# #     for i in range(3):
# #         for j in range(3):
# #             big_maze[start_row + i][start_col + j] = result[i][j]
# #
# # # ===================== 墙壁修复 =====================
# # def fix_walls(maze):
# #     rows = len(maze)
# #     cols = len(maze[0])
# #     for i in range(rows):
# #         for j in range(cols):
# #             if j < cols - 1:
# #                 w = max(maze[i][j][3], maze[i][j+1][2])
# #                 maze[i][j][3] = w
# #                 maze[i][j+1][2] = w
# #             if i < rows - 1:
# #                 w = max(maze[i][j][1], maze[i+1][j][0])
# #                 maze[i][j][1] = w
# #                 maze[i+1][j][0] = w
# #     return maze
# #
# # # ===================== BFS 路径 =====================
# # def find_maze_path(big_maze, start_coord, end_coord):
# #     rows = 9
# #     cols = 6
# #
# #     def coord_to_index(coord):
# #         x, y = coord
# #         col = (x - 50) // 100
# #         row = 8 - (y - 50) // 100
# #         return int(row), int(col)
# #
# #     def index_to_coord(row, col):
# #         x = 50 + 100 * col
# #         y = 50 + 100 * (8 - row)
# #         return (x, y)
# #
# #     def get_neighbors(row, col):
# #         ns = []
# #         w = big_maze[row][col]
# #         if w[0] == 0 and row - 1 >= 0:
# #             ns.append((row - 1, col))
# #         if w[1] == 0 and row + 1 < rows:
# #             ns.append((row + 1, col))
# #         if w[2] == 0 and col - 1 >= 0:
# #             ns.append((row, col - 1))
# #         if w[3] == 0 and col + 1 < cols:
# #             ns.append((row, col + 1))
# #         return ns
# #
# #     start = coord_to_index(start_coord)
# #     end = coord_to_index(end_coord)
# #     q = deque([start])
# #     vis = {start}
# #     parent = {start: None}
# #
# #     while q:
# #         cur = q.popleft()
# #         if cur == end:
# #             break
# #         for nxt in get_neighbors(*cur):
# #             if nxt not in vis:
# #                 vis.add(nxt)
# #                 parent[nxt] = cur
# #                 q.append(nxt)
# #
# #     path_idx = []
# #     cur = end
# #     while cur in parent:
# #         path_idx.append(cur)
# #         cur = parent[cur]
# #     path_idx.reverse()
# #     return [index_to_coord(r, c) for r, c in path_idx]
# #
# # # ===================== 单机拍照任务 =====================
# # async def shoot_task(plane: AirplaneController, points):
# #     for x, y, z in points:
# #         print(f"前往拍照：({x},{y})")
# #         plane.goto(x, y, z)
# #         await asyncio.sleep(7)
# #
# #         def cb(img, x=x, y=y):
# #             handle_image(img, x, y)
# #
# #         plane.cap_image(user_receive_callback=cb)
# #         await asyncio.sleep(7)
# #
# # # ===================== 主函数：三机全动 =====================
# # async def main():
# #     m = get_airplane_manager()
# #     m.flush()
# #     m.start()
# #     m.flush()
# #
# #     c3 = m.get_airplane('FH0C:COM3')
# #     c4 = m.get_airplane('FH0C:COM4')
# #     c5 = m.get_airplane('FH0C:COM5')
# #
# #     # 三机初始化
# #     for p in [c3, c4, c5]:
# #         p.use_fast_mode(False, True)
# #         p.speed(200)
# #
# #     # 同时起飞
# #     print("===== 三机同时起飞 =====")
# #     for p in [c3, c4, c5]:
# #         p.takeoff(FLY_HEIGHT)
# #     await asyncio.sleep(3)
# #
# #     # 6个点平分给3架飞机，每机拍2个，速度最快
# #     tasks = [
# #         shoot_task(c3, PosList[0:2]),
# #         shoot_task(c4, PosList[2:4]),
# #         shoot_task(c5, PosList[4:6])
# #     ]
# #     await asyncio.gather(*tasks)
# #
# #     # 迷宫处理
# #     print("\n===== 迷宫拼接完成 =====")
# #     maze_fixed = fix_walls(big_maze)
# #     print("完整迷宫：")
# #     for row in maze_fixed:
# #         print(row)
# #
# #     # 路径计算
# #     path = find_maze_path(maze_fixed, (50, 150), (550, 750))
# #     print("\n最短路径：", path)
# #
# #     # 三机分别飞往不同降落点，x间距均 >50
# #     print("\n===== 飞往降落区（x间隔>50） =====")
# #     c3.goto(150, 850, FLY_HEIGHT)
# #     c4.goto(300, 850, FLY_HEIGHT)
# #     c5.goto(450, 850, FLY_HEIGHT)
# #     await asyncio.sleep(10)
# #
# #     # 降落
# #     print("===== 全部降落 =====")
# #     c3.land()
# #     c4.land()
# #     c5.land()
# #     await asyncio.sleep(3)
# #
# # if __name__ == '__main__':
# #     asyncio.run(main())
# import asyncio
# import cv2
# import numpy as np
# from PhantasyIslandPythonRemoteControl.airplane_manager import get_airplane_manager
#
# # ===================== 全局参数与地图 =====================
# FLY_HEIGHT = 100
# MAX_STEP = 100  # 单次最大飞行距离
# SPEED = 150  # 飞行速度
#
# # 全局地图：9行6列 (对应 900x600 的区域)
# # 每个格子存 [上墙, 下墙, 左墙, 右墙]
# big_maze = [[[0, 0, 0, 0] for _ in range(6)] for _ in range(9)]
# maze_lock = asyncio.Lock()  # 防止多机同时写地图冲突
#
# # 降落区
# LANDING_ZONES = [(150, 850), (300, 850), (450, 850)]
#
#
# # ===================== 图像处理 =====================
# def wall_ratio(binary_img, y0, y1, x0, x1):
#     h, w = binary_img.shape
#     y0, y1 = max(0, y0), min(h, y1)
#     x0, x1 = max(0, x0), min(w, x1)
#     if y0 >= y1 or x0 >= x1: return 0.0
#     return np.mean(binary_img[y0:y1, x0:x1])
#
#
# def process_image_to_walls(img, center_x, center_y):
#     """
#     处理图片，返回 3x3 的墙壁信息，并计算该区域在大地圖中的偏移
#     """
#     if img is None: return None
#
#     # 1. 识别墙壁
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     wall = (gray < 80).astype(np.uint8)  # 假设黑线是墙
#
#     # 定义 3x3 网格的切割线 (根据摄像头视野调整，这里假设视野覆盖 300x300 左右)
#     # 这里简化处理，假设拍照点就是 3x3 格子的中心
#     # 实际需要根据相机焦距和高度计算视野范围
#     # 假设视野覆盖周围 150cm (即 1.5个格子半径)
#
#     # 这里为了演示，我们简化为：
#     # 拍照点 (x,y) 对应地图上的某个 3x3 区域
#     # 我们需要把 (x,y) 转换为地图索引
#     # 地图每个格子 100x100
#
#     # 计算左上角在地图中的索引
#     # 假设拍照点 (50, 50) 对应地图 (0,0) 格子中心
#     start_col = int((center_x - 50) / 100)
#     start_row = int((center_y - 50) / 100)
#
#     # 简单的 3x3 扫描逻辑 (实际需根据相机视野精细调整)
#     # 这里模拟返回一个 3x3 的墙壁数据
#     # 真实逻辑需要像之前代码那样切分图片
#     # 为了代码可运行，这里复用之前的切分逻辑（需根据实际相机视野调整参数）
#
#     x_edges = [center_x - 75, center_x - 25, center_x + 25, center_x + 75]  # 模拟视野
#     y_edges = [center_y - 75, center_y - 25, center_y + 25, center_y + 75]
#
#     # 注意：这里只是示例逻辑，真实情况需要根据图片像素坐标映射
#     # 这里假设我们成功识别出了局部墙壁
#     local_walls = []
#     # ... (此处省略复杂的图片切分代码，直接填入 dummy 数据演示流程)
#     # 实际请填入你之前的 maze_to_3x3_array 逻辑
#
#     return start_row, start_col, local_walls
#
#
# # ===================== 无人机任务类 =====================
# class DroneScout:
#     def __init__(self, plane, name, start_pos, waypoints):
#         self.plane = plane
#         self.name = name
#         self.x, self.y = start_pos
#         self.waypoints = waypoints  # 侦察点列表
#         self.event = asyncio.Event()
#
#     def on_photo(self, img):
#         """拍照回调：处理图片并更新全局地图"""
#         try:
#             # 这里调用你的图像处理函数
#             # row, col, walls = process_image_to_walls(img, self.x, self.y)
#             print(f"[{self.name}] 收到图片，正在处理...")
#             # 模拟处理耗时
#             # 将结果写入 big_maze (需加锁)
#         finally:
#             self.event.set()
#
#     async def smart_move(self, tx, ty, z):
#         """
#         核心移动函数：自动分段，保证单次不超过 MAX_STEP
#         """
#         while True:
#             dist = ((tx - self.x) ** 2 + (ty - self.y) ** 2) ** 0.5
#             if dist < 10:  # 到达终点
#                 self.x, self.y = tx, ty
#                 break
#
#             # 计算下一步
#             if dist <= MAX_STEP:
#                 nx, ny = tx, ty
#             else:
#                 scale = MAX_STEP / dist
#                 nx = int(self.x + (tx - self.x) * scale)
#                 ny = int(self.y + (ty - self.y) * scale)
#
#             print(f"[{self.name}] 飞向 ({nx}, {ny})")
#             self.plane.goto(nx, ny, z)
#             self.x, self.y = nx, ny
#
#             # 估算飞行时间 (距离/速度) + 缓冲
#             await asyncio.sleep(dist / SPEED + 0.5)
#
#     async def run_mission(self):
#         """执行侦察任务"""
#         # 1. 飞往各个侦察点
#         for wx, wy in self.waypoints:
#             await self.smart_move(wx, wy, FLY_HEIGHT)
#
#             # 2. 拍照并等待处理
#             self.event.clear()
#             self.plane.cap_image(user_receive_callback=self.on_photo)
#             await self.event.wait()  # 精准等待图片回来
#
#         # 3. 任务完成，去降落区 (不直接降落，先去汇合点)
#         # 根据名字选择降落点
#         landing_x, landing_y = LANDING_ZONES[int(self.name[1]) - 3]  # C3->0, C4->1...
#         await self.smart_move(landing_x, landing_y, FLY_HEIGHT)
#         self.plane.land()
#         print(f"[{self.name}] 任务结束，已降落")
#
#
# # ===================== 主程序 =====================
# async def main():
#     # 1. 初始化
#     m = get_airplane_manager()
#     m.flush()
#     m.start()
#     m.flush()
#
#     p3 = m.get_airplane('FH0C:COM3')
#     p4 = m.get_airplane('FH0C:COM4')
#     p5 = m.get_airplane('FH0C:COM5')
#
#     for p in [p3, p4, p5]:
#         p.use_fast_mode(False, True)
#         p.speed(SPEED)
#
#     # 2. 起飞
#     print(">>> 三机起飞")
#     for p in [p3, p4, p5]:
#         p.takeoff(FLY_HEIGHT)
#     await asyncio.sleep(5)
#
#     # 3. 定义侦察路线 (直线穿越)
#     # 为了建图，我们需要定义一系列“拍照点”
#     # 假设我们要扫描整个 600x900 地图，可以定义几个关键点
#     # 这里演示：每架飞机负责一列，从南飞到北
#
#     # C3 负责左边 (x=150), C4 中间 (x=300), C5 右边 (x=450)
#     # 路径点：从 (y=150) 飞到 (y=750)
#     route_c3 = [(150, 150), (150, 450), (150, 750)]
#     route_c4 = [(300, 150), (300, 450), (300, 750)]
#     route_c5 = [(450, 150), (450, 450), (450, 750)]
#
#     # 4. 并行执行
#     print(">>> 开始并行侦察")
#     await asyncio.gather(
#         DroneScout(p3, "C3", (150, 150), route_c3).run_mission(),
#         DroneScout(p4, "C4", (300, 150), route_c4).run_mission(),
#         DroneScout(p5, "C5", (450, 150), route_c5).run_mission()
#     )
#
#     # 5. 计算路径 (所有飞机降落/任务结束后执行)
#     print(">>> 所有飞机完成任务，正在计算最短路径...")
#     # 这里调用你的 BFS 算法，使用全局变量 big_maze
#     # path = find_maze_path(big_maze, (50, 150), (550, 750))
#     # print("最短路径:", path)
#
#
# if __name__ == '__main__':
#     asyncio.run(main())
import asyncio
from PhantasyIslandPythonRemoteControl import AirplaneController
from PhantasyIslandPythonRemoteControl.airplane_manager import get_airplane_manager
import cv2
import numpy as np
from collections import deque

# ===================== 全局参数 =====================
PosList = [
    [150, 150, 200],
    [450, 150, 200],
    [150, 450, 200],
    [450, 450, 200],
    [150, 750, 200],
    [450, 750, 200]
]

big_maze = [[[0,0,0,0] for _ in range(6)] for _ in range(9)]
FLY_HEIGHT = 100
START_POINT = (50, 150)

# 降落区范围：x 50~550，y 800~900，三机间隔 >50
LANDING = {
    'c3': (150, 850),
    'c4': (300, 850),
    'c5': (450, 850)
}

# ===================== 图像识别 =====================
def wall_ratio(binary_img, y0, y1, x0, x1):
    h, w = binary_img.shape
    y0 = max(0, y0)
    y1 = min(h, y1)
    x0 = max(0, x0)
    x1 = min(w, x1)
    if y0 >= y1 or x0 >= x1:
        return 0.0
    region = binary_img[y0:y1, x0:x1]
    return np.mean(region)

def maze_to_3x3_array(img):
    wall = (img < 80).astype(np.uint8)
    x_edges = [40, 120, 200, 280]
    y_edges = [0, 80, 160, 235]
    band = 6
    margin = 8
    threshold = 0.18
    result = []
    for r in range(3):
        row_result = []
        for c in range(3):
            xl, xr = x_edges[c], x_edges[c+1]
            yt, yb = y_edges[r], y_edges[r+1]
            top_ratio = wall_ratio(wall, yt-band, yt+band, xl+margin, xr-margin)
            top = 1 if top_ratio > threshold else 0
            bottom_ratio = wall_ratio(wall, yb-band, yb+band, xl+margin, xr-margin)
            bottom = 1 if bottom_ratio > threshold else 0
            left_ratio = wall_ratio(wall, yt+margin, yb-margin, xl-band, xl+band)
            left = 1 if left_ratio > threshold else 0
            right_ratio = wall_ratio(wall, yt+margin, yb-margin, xr-band, xr+band)
            right = 1 if right_ratio > threshold else 0
            row_result.append([top, bottom, left, right])
        result.append(row_result)
    return result

def handle_image(img, x, y):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    result = maze_to_3x3_array(img_gray)
    print(f"拍摄点位 ({x},{y}) 识别结果：")
    for row in result:
        print(row)

    if x < 300:
        start_col = 0
    else:
        start_col = 3
    if y > 600:
        start_row = 0
    elif y > 300:
        start_row = 3
    else:
        start_row = 6

    for i in range(3):
        for j in range(3):
            big_maze[start_row + i][start_col + j] = result[i][j]

# ===================== 墙壁修复 =====================
def fix_walls(maze):
    rows = len(maze)
    cols = len(maze[0])
    for i in range(rows):
        for j in range(cols):
            if j < cols - 1:
                w = max(maze[i][j][3], maze[i][j+1][2])
                maze[i][j][3] = w
                maze[i][j+1][2] = w
            if i < rows - 1:
                w = max(maze[i][j][1], maze[i+1][j][0])
                maze[i][j][1] = w
                maze[i+1][j][0] = w
    return maze

# ===================== BFS 路径 =====================
def find_maze_path(big_maze, start_coord, end_coord):
    rows = 9
    cols = 6

    def coord_to_index(coord):
        x, y = coord
        col = (x - 50) // 100
        row = 8 - (y - 50) // 100
        return int(row), int(col)

    def index_to_coord(row, col):
        x = 50 + 100 * col
        y = 50 + 100 * (8 - row)
        return (x, y)

    def get_neighbors(row, col):
        ns = []
        w = big_maze[row][col]
        if w[0] == 0 and row - 1 >= 0:
            ns.append((row - 1, col))
        if w[1] == 0 and row + 1 < rows:
            ns.append((row + 1, col))
        if w[2] == 0 and col - 1 >= 0:
            ns.append((row, col - 1))
        if w[3] == 0 and col + 1 < cols:
            ns.append((row, col + 1))
        return ns

    start = coord_to_index(start_coord)
    end = coord_to_index(end_coord)
    q = deque([start])
    vis = {start}
    parent = {start: None}

    while q:
        cur = q.popleft()
        if cur == end:
            break
        for nxt in get_neighbors(*cur):
            if nxt not in vis:
                vis.add(nxt)
                parent[nxt] = cur
                q.append(nxt)

    path_idx = []
    cur = end
    while cur in parent:
        path_idx.append(cur)
        cur = parent[cur]
    path_idx.reverse()
    return [index_to_coord(r, c) for r, c in path_idx]

# ===================== 单机拍照任务 =====================
async def shoot_task(plane: AirplaneController, points):
    for x, y, z in points:
        print(f"前往拍照：({x},{y})")
        plane.goto(x, y, z)
        await asyncio.sleep(7)

        def cb(img, x=x, y=y):
            handle_image(img, x, y)

        plane.cap_image(user_receive_callback=cb)
        await asyncio.sleep(7)

# ===================== 主函数：三机全动 =====================
async def main():
    m = get_airplane_manager()
    m.flush()
    m.start()
    m.flush()

    c3 = m.get_airplane('FH0C:COM3')
    c4 = m.get_airplane('FH0C:COM4')
    c5 = m.get_airplane('FH0C:COM5')

    # 三机初始化
    for p in [c3, c4, c5]:
        p.use_fast_mode(False, True)
        p.speed(200)

    # 同时起飞
    print("===== 三机同时起飞 =====")
    for p in [c3, c4, c5]:
        p.takeoff(FLY_HEIGHT)
    await asyncio.sleep(3)

    # 6个点平分给3架飞机，每机拍2个，速度最快
    tasks = [
        shoot_task(c3, PosList[0:2]),
        shoot_task(c4, PosList[2:4]),
        shoot_task(c5, PosList[4:6])
    ]
    await asyncio.gather(*tasks)

    # 迷宫处理
    print("\n===== 迷宫拼接完成 =====")
    maze_fixed = fix_walls(big_maze)
    print("完整迷宫：")
    for row in maze_fixed:
        print(row)

    # 路径计算
    path = find_maze_path(maze_fixed, (50, 150), (550, 750))
    print("\n最短路径：", path)

    # 三机分别飞往不同降落点，x间距均 >50
    print("\n===== 飞往降落区（x间隔>50） =====")
    c3.goto(150, 850, FLY_HEIGHT)
    c4.goto(300, 850, FLY_HEIGHT)
    c5.goto(450, 850, FLY_HEIGHT)
    await asyncio.sleep(10)

    # 降落
    print("===== 全部降落 =====")
    c3.land()
    c4.land()
    c5.land()
    await asyncio.sleep(3)

if __name__ == '__main__':
    asyncio.run(main())