import random
from typing import Dict, List, Optional  # noqa: UP035


class World:
    # 常量定义
    RADIUS = 30
    VILLAGE_POS = [30, 30]
    TILE = {  # noqa: RUF012
        "VILLAGE": "A",
        "IRON_MINE": "I",
        "COAL_MINE": "C",
        "SULPHUR_MINE": "S",
        "FOREST": ";",
        "FIELD": ",",
        "BARRENS": ".",
        "ROAD": "#",
        "HOUSE": "H",
        "CAVE": "V",
        "TOWN": "O",
        "CITY": "Y",
        "OUTPOST": "P",
        "SHIP": "W",
        "BOREHOLE": "B",
        "BATTLEFIELD": "F",
        "SWAMP": "M",
        "CACHE": "U",
        "EXECUTIONER": "X",
    }

    # 地形概率
    TILE_PROBS = {TILE["FOREST"]: 0.15, TILE["FIELD"]: 0.35, TILE["BARRENS"]: 0.5}

    # 地标配置
    LANDMARKS = {
        TILE["OUTPOST"]: {"num": 0, "minRadius": 0, "maxRadius": 0, "scene": "outpost", "label": "An&nbsp;Outpost"},
        TILE["IRON_MINE"]: {"num": 1, "minRadius": 5, "maxRadius": 5, "scene": "ironmine", "label": "Iron&nbsp;Mine"},
        TILE["COAL_MINE"]: {"num": 1, "minRadius": 10, "maxRadius": 10, "scene": "coalmine", "label": "Coal&nbsp;Mine"},
        TILE["SULPHUR_MINE"]: {
            "num": 1,
            "minRadius": 20,
            "maxRadius": 20,
            "scene": "sulphurmine",
            "label": "Sulphur&nbsp;Mine",
        },
        TILE["HOUSE"]: {
            "num": 10,
            "minRadius": 0,
            "maxRadius": RADIUS * 1.5,
            "scene": "house",
            "label": "An&nbsp;Old&nbsp;House",
        },
        TILE["CAVE"]: {"num": 5, "minRadius": 3, "maxRadius": 10, "scene": "cave", "label": "A&nbsp;Damp&nbsp;Cave"},
        TILE["TOWN"]: {
            "num": 10,
            "minRadius": 10,
            "maxRadius": 20,
            "scene": "town",
            "label": "An&nbsp;Abandoned&nbsp;Town",
        },
        TILE["CITY"]: {
            "num": 20,
            "minRadius": 20,
            "maxRadius": RADIUS * 1.5,
            "scene": "city",
            "label": "A&nbsp;Ruined&nbsp;City",
        },
        TILE["SHIP"]: {
            "num": 1,
            "minRadius": 28,
            "maxRadius": 28,
            "scene": "ship",
            "label": "A&nbsp;Crashed&nbsp;Starship",
        },
        TILE["BOREHOLE"]: {
            "num": 10,
            "minRadius": 15,
            "maxRadius": RADIUS * 1.5,
            "scene": "borehole",
            "label": "A&nbsp;Borehole",
        },
        TILE["BATTLEFIELD"]: {
            "num": 5,
            "minRadius": 18,
            "maxRadius": RADIUS * 1.5,
            "scene": "battlefield",
            "label": "A&nbsp;Battlefield",
        },
        TILE["SWAMP"]: {
            "num": 1,
            "minRadius": 15,
            "maxRadius": RADIUS * 1.5,
            "scene": "swamp",
            "label": "A&nbsp;Murky&nbsp;Swamp",
        },
        TILE["EXECUTIONER"]: {
            "num": 1,
            "minRadius": 28,
            "maxRadius": 28,
            "scene": "executioner",
            "label": "A&nbsp;Ravaged&nbsp;Battleship",
        },
    }

    STICKINESS = 0.5
    LIGHT_RADIUS = 2
    BASE_WATER = 10
    MOVES_PER_FOOD = 2
    MOVES_PER_WATER = 1
    DEATH_COOLDOWN = 120
    FIGHT_CHANCE = 0.20
    BASE_HEALTH = 10
    BASE_HIT_CHANCE = 0.8
    MEAT_HEAL = 8
    MEDS_HEAL = 20
    HYPO_HEAL = 30
    FIGHT_DELAY = 3

    # 方向向量
    NORTH = [0, -1]
    SOUTH = [0, 1]
    WEST = [-1, 0]
    EAST = [1, 0]

    # 武器定义
    Weapons = {
        "fists": {"verb": "punch", "type": "unarmed", "damage": 1, "cooldown": 2},
        "bone spear": {"verb": "stab", "type": "melee", "damage": 2, "cooldown": 2},
        "iron sword": {"verb": "swing", "type": "melee", "damage": 4, "cooldown": 2},
        "steel sword": {"verb": "slash", "type": "melee", "damage": 6, "cooldown": 2},
        "bayonet": {"verb": "thrust", "type": "melee", "damage": 8, "cooldown": 2},
        "rifle": {"verb": "shoot", "type": "ranged", "damage": 5, "cooldown": 1, "cost": {"bullets": 1}},
        "laser rifle": {"verb": "blast", "type": "ranged", "damage": 8, "cooldown": 1, "cost": {"energy cell": 1}},
        "grenade": {"verb": "lob", "type": "ranged", "damage": 15, "cooldown": 5, "cost": {"grenade": 1}},
        "bolas": {"verb": "tangle", "type": "ranged", "damage": "stun", "cooldown": 15, "cost": {"bolas": 1}},
        "plasma rifle": {
            "verb": "disintegrate",
            "type": "ranged",
            "damage": 12,
            "cooldown": 1,
            "cost": {"energy cell": 1},
        },
        "energy blade": {"verb": "slice", "type": "melee", "damage": 10, "cooldown": 2},
        "disruptor": {"verb": "stun", "type": "ranged", "damage": "stun", "cooldown": 15},
    }

    def __init__(self, options=None):
        self.options = options or {}
        self.state = {"map": self.generate_map(), "mask": self.new_mask()}
        self.cur_pos = self.VILLAGE_POS.copy()
        self.water = self.BASE_WATER
        self.health = self.BASE_HEALTH
        self.food_move = 0
        self.water_move = 0
        self.starvation = False
        self.thirst = False
        self.dead = False
        self.danger = False
        self.fight_move = 0
        self.used_outposts = {}
        self.seen_all = False
        self.outfit = {}
        self.ship_pos = self.map_search(self.TILE["SHIP"], self.state["map"], 1)
        self.direction = self.compass_dir(self.ship_pos[0]) if self.ship_pos else ""

    @staticmethod
    def get_distance(pos1: List[int], pos2: Optional[List[int]] = None) -> int:
        """计算两点之间的曼哈顿距离"""
        if pos2 is None:
            pos2 = World.VILLAGE_POS
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def new_mask(self) -> List[List[bool]]:
        """创建新的地图遮罩（初始可见区域）"""
        size = self.RADIUS * 2 + 1
        mask = [[False for _ in range(size)] for _ in range(size)]
        self.light_map(self.RADIUS, self.RADIUS, mask)
        return mask

    def light_map(self, x: int, y: int, mask: List[List[bool]]):
        """照亮指定点周围的区域"""
        r = self.LIGHT_RADIUS
        self.uncover_map(x, y, r, mask)

    def uncover_map(self, x: int, y: int, r: int, mask: List[List[bool]]):
        """揭示指定点周围的区域"""
        size = self.RADIUS * 2
        mask[x][y] = True

        for i in range(-r, r + 1):
            for j in range(-r + abs(i), r - abs(i) + 1):
                nx, ny = x + i, y + j
                if 0 <= nx <= size and 0 <= ny <= size:
                    mask[nx][ny] = True

    def generate_map(self) -> List[List[str]]:
        """生成世界地图"""
        size = self.RADIUS * 2 + 1
        map_data = [["" for _ in range(size)] for _ in range(size)]

        # 村庄放在中心
        map_data[self.RADIUS][self.RADIUS] = self.TILE["VILLAGE"]

        # 螺旋生成地形
        for r in range(1, self.RADIUS + 1):
            for t in range(r * 8):
                if t < 2 * r:
                    x = self.RADIUS - r + t
                    y = self.RADIUS - r
                elif t < 4 * r:
                    x = self.RADIUS + r
                    y = self.RADIUS - (3 * r) + t
                elif t < 6 * r:
                    x = self.RADIUS + (5 * r) - t
                    y = self.RADIUS + r
                else:
                    x = self.RADIUS - r
                    y = self.RADIUS + (7 * r) - t

                # 确保坐标在范围内
                x = max(0, min(size - 1, x))
                y = max(0, min(size - 1, y))

                map_data[x][y] = self.choose_tile(x, y, map_data)

        # 放置地标
        for tile_type, landmark in self.LANDMARKS.items():
            for _ in range(landmark["num"]):
                self.place_landmark(landmark["minRadius"], landmark["maxRadius"], tile_type, map_data)

        return map_data

    def choose_tile(self, x: int, y: int, map_data: List[List[str]]) -> str:
        """根据周围地形选择新地块类型"""
        adjacent = []
        size = self.RADIUS * 2

        # 获取相邻地块
        if y > 0:
            adjacent.append(map_data[x][y - 1])
        if y < size:
            adjacent.append(map_data[x][y + 1])
        if x < size:
            adjacent.append(map_data[x + 1][y])
        if x > 0:
            adjacent.append(map_data[x - 1][y])

        chances = {}
        non_sticky = 1.0

        # 计算相邻地块影响
        for tile in adjacent:
            if tile == self.TILE["VILLAGE"]:
                return self.TILE["FOREST"]
            if tile and tile in self.TILE_PROBS:
                chances[tile] = chances.get(tile, 0.0) + self.STICKINESS
                non_sticky -= self.STICKINESS

        # 添加基础概率
        for tile, prob in self.TILE_PROBS.items():
            chances[tile] = chances.get(tile, 0.0) + prob * non_sticky

        # 根据概率选择地块
        total = sum(chances.values())
        rand_val = random.uniform(0, total)
        cumulative = 0.0

        for tile, prob in chances.items():
            cumulative += prob
            if rand_val <= cumulative:
                return tile

        return self.TILE["BARRENS"]

    def place_landmark(self, min_radius: int, max_radius: int, landmark: str, map_data: List[List[str]]):
        """在地图上放置地标"""
        size = self.RADIUS * 2
        while True:
            r = random.randint(min_radius, max_radius)
            x_dist = random.randint(0, r)
            y_dist = r - x_dist

            if random.random() < 0.5:
                x_dist = -x_dist
            if random.random() < 0.5:
                y_dist = -y_dist

            x = self.RADIUS + x_dist
            y = self.RADIUS + y_dist

            # 确保坐标在范围内
            x = max(0, min(size, x))
            y = max(0, min(size, y))

            # 检查是否是有效位置
            if self.is_terrain(map_data[x][y]):
                map_data[x][y] = landmark
                return [x, y]

    @staticmethod
    def is_terrain(tile: str) -> bool:
        """检查是否是基础地形"""
        return tile in {World.TILE["FOREST"], World.TILE["FIELD"], World.TILE["BARRENS"]}

    def move(self, direction: List[int]):
        """玩家移动逻辑"""
        old_x, old_y = self.cur_pos
        new_x = old_x + direction[0]
        new_y = old_y + direction[1]

        # 边界检查
        size = self.RADIUS * 2
        if 0 <= new_x <= size and 0 <= new_y <= size:
            old_tile = self.state["map"][old_x][old_y]
            self.cur_pos = [new_x, new_y]
            new_tile = self.state["map"][new_x][new_y]

            # 更新可见区域
            self.light_map(new_x, new_y, self.state["mask"])
            self.check_danger()
            self.use_supplies()
            self.do_space()

    def move_north(self):
        self.move(self.NORTH)

    def move_south(self):
        self.move(self.SOUTH)

    def move_west(self):
        self.move(self.WEST)

    def move_east(self):
        self.move(self.EAST)

    def check_danger(self) -> bool:
        """检查危险区域"""
        distance = self.get_distance(self.cur_pos)

        if not self.danger:
            if distance >= 8:  # 进入危险区
                self.danger = True
                return True
        else:
            if distance < 8:  # 离开危险区
                self.danger = False
                return True
        return False

    def use_supplies(self):
        """消耗食物和水资源"""
        self.food_move += 1
        self.water_move += 1

        # 食物消耗
        moves_per_food = self.MOVES_PER_FOOD
        if self.food_move >= moves_per_food:
            self.food_move = 0
            if "cured meat" in self.outfit and self.outfit["cured meat"] > 0:
                self.outfit["cured meat"] -= 1
                self.health = min(self.get_max_health(), self.health + self.MEAT_HEAL)
            else:
                # 饥饿处理
                if not self.starvation:
                    self.starvation = True
                else:
                    self.die()

        # 水消耗
        moves_per_water = self.MOVES_PER_WATER
        if self.water_move >= moves_per_water:
            self.water_move = 0
            if self.water > 0:
                self.water -= 1
            else:
                # 脱水处理
                if not self.thirst:
                    self.thirst = True
                else:
                    self.die()

    def get_max_health(self) -> int:
        """计算最大生命值（基于装备）"""
        # 在实际实现中，这里会检查玩家装备
        return self.BASE_HEALTH + 10  # 示例值

    def get_max_water(self) -> int:
        """计算最大携带水量（基于装备）"""
        # 在实际实现中，这里会检查玩家装备
        return self.BASE_WATER + 5  # 示例值

    def do_space(self):
        """处理当前位置事件"""
        x, y = self.cur_pos
        current_tile = self.state["map"][x][y]

        if current_tile == self.TILE["VILLAGE"]:
            self.go_home()
        elif current_tile == self.TILE["EXECUTIONER"]:
            # 触发特殊事件
            pass
        elif current_tile in self.LANDMARKS:
            # 触发地标事件
            pass
        else:
            self.check_fight()

    def check_fight(self):
        """检查是否触发战斗"""
        self.fight_move += 1
        if self.fight_move > self.FIGHT_DELAY and random.random() < self.FIGHT_CHANCE:
            self.fight_move = 0
            # 触发战斗
            pass

    def die(self):
        """玩家死亡处理"""
        if not self.dead:
            self.dead = True
            # 重置状态
            self.state = None
            self.outfit = {}
            # 返回村庄
            self.go_home()

    def go_home(self):
        """返回村庄处理"""
        # 保存游戏状态
        # game_state.save(self.state)

        # 处理收集的资源
        for item, amount in self.outfit.items():
            if not self.leave_at_home(item):
                # 添加到村庄库存
                pass

        # 重置探险状态
        self.cur_pos = self.VILLAGE_POS.copy()
        self.water = self.get_max_water()
        self.health = self.get_max_health()
        self.food_move = 0
        self.water_move = 0
        self.starvation = False
        self.thirst = False

    @staticmethod
    def leave_at_home(item: str) -> bool:
        """判断物品是否应留在村庄"""
        return item not in ["cured meat", "bullets", "energy cell", "medicine"]

    def map_search(self, target: str, map_data: List[List[str]], max_results: int = 1) -> List[Dict]:
        """在地图上搜索特定目标"""
        results = []
        size = self.RADIUS * 2

        for x in range(size + 1):
            for y in range(size + 1):
                if map_data[x][y] == target:
                    results.append({"x": x - self.RADIUS, "y": y - self.RADIUS})
                    if len(results) >= max_results:
                        return results
        return results

    @staticmethod
    def compass_dir(pos: Dict) -> str:
        """获取指南针方向"""
        if pos["x"] == 0 and pos["y"] == 0:
            return "here"

        if abs(pos["x"]) > 2 * abs(pos["y"]):
            return "east" if pos["x"] > 0 else "west"
        elif abs(pos["y"]) > 2 * abs(pos["x"]):
            return "south" if pos["y"] > 0 else "north"
        else:
            vertical = "south" if pos["y"] > 0 else "north"
            horizontal = "east" if pos["x"] > 0 else "west"
            return f"{vertical}{horizontal}"

    def draw_road(self):
        """绘制道路到当前位置"""
        # 在实际实现中，这会修改地图数据
        pass

    def outpost_used(self, x: Optional[int] = None, y: Optional[int] = None) -> bool:
        """检查哨站是否已使用"""
        x = x or self.cur_pos[0]
        y = y or self.cur_pos[1]
        return f"{x},{y}" in self.used_outposts

    def use_outpost(self):
        """使用哨站"""
        self.water = self.get_max_water()
        self.used_outposts[f"{self.cur_pos[0]},{self.cur_pos[1]}"] = True


# 示例用法
if __name__ == "__main__":
    world = World()
    print("Generated world map size:", len(world.state["map"]))
    print("Player starting position:", world.cur_pos)

    # 模拟移动
    world.move_north()
    print("After moving north:", world.cur_pos)

    # 模拟消耗资源
    for _ in range(3):
        world.use_supplies()
    print(f"Water: {world.water}, Health: {world.health}")
