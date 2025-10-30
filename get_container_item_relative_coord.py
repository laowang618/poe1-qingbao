#获取容器里(背包，仓库)物品的相对坐标
import pydirectinput
#from windowed_coord import WindowedCoord
from windowed_coord import WindowedCoord
import time


class GetContainerItemRelativeCoord:
    def __init__(self, container_type:str, grid_size:int):
        self.coord_array = []
        # 背包
        if container_type == "backpack":
            if grid_size == 1:
                x_array = []
                y_array = []
                count = 0
                while count < 12:
                    x_array.append(count * 54 + 1296)
                    count += 1
                count = 0
                while count < 5:
                    y_array.append(count * 54 + 614)
                    count += 1
                for x in x_array:
                    for y in y_array:
                        self.coord_array.append([x, y])
        # 大仓无嵌套
        if container_type == "large_warehouse_no_nesting":
            if grid_size == 1:
                x_array = []
                y_array = []
                count = 0
                while count < 24:
                    x_array.append(count * 27 + 27)
                    count += 1
                count = 0
                while count < 24:
                    y_array.append(count * 27 + 154)
                    count += 1
                for x in x_array:
                    for y in y_array:
                        self.coord_array.append([x, y])
        # 大仓有嵌套
        if container_type == "large_warehouse_is_nesting":
            if grid_size == 1:
                x_array = []
                y_array = []
                count = 0
                while count < 24:
                    x_array.append(count * 27 + 27)
                    count += 1
                count = 0
                while count < 24:
                    y_array.append(count * 27 + 181)
                    count += 1
                for x in x_array:
                    for y in y_array:
                        self.coord_array.append([x, y])
        # 小仓无嵌套
        if container_type == "small_warehouse_no_nesting":
            if grid_size == 1:
                x_array = []
                y_array = []
                count = 0
                while count < 12:
                    x_array.append(count * 54 + 39)
                    count += 1
                count = 0
                while count < 12:
                    y_array.append(count * 54 + 158)
                    count += 1
                for x in x_array:
                    for y in y_array:
                        self.coord_array.append([x, y])
        # 小仓有嵌套
        if container_type == "small_warehouse_is_nesting":
            if grid_size == 1:
                x_array = []
                y_array = []
                count = 0
                while count < 12:
                    x_array.append(count * 54 + 39)
                    count += 1
                count = 0
                while count < 12:
                    y_array.append(count * 54 + 194)
                    count += 1
                for x in x_array:
                    for y in y_array:
                        self.coord_array.append([x, y])

        print("初始化执行GetContainerItemRelativeCoord")

    def get_coord(self, cycle_number:int):
        x = self.coord_array[cycle_number][0]

        y = self.coord_array[cycle_number][1]
        return self.get_relative_coord(self, x, y)

    @WindowedCoord
    def get_relative_coord(self, x, y):
        return x,y

if __name__ == "__main__":
    backpack = GetContainerItemRelativeCoord("backpack",1)  # 需要先创建类的实例
    x,y = backpack.get_coord(0)
    pydirectinput.moveTo(x, y)  # 通过实例调用方法




