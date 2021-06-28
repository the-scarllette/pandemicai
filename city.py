from gameobject import GameObject
from graphics import *

class City(GameObject):

    def __init__(self, name, colour, connected_cities, window, x, y, game):
        super().__init__(window, x, y)
        self.__name = name
        self.__colour = colour
        self.__connected_cities = connected_cities.copy()
        self.__game = game
        self.__radius = 10
        self.__left_city = False
        self.__right_city = False
        self.__cubes = {"blue": 0, "yellow": 0, "black": 0, "red": 0}
        self.__blue_cube_text = Text(Point(self.x - 10, self.y - 10), "0")
        self.__blue_cube_text.setSize(15)
        self.__blue_cube_text.setFill("blue")
        self.__yellow_cube_text = Text(Point(self.x + 10, self.y - 10), "0")
        self.__blue_cube_text.setSize(15)
        self.__yellow_cube_text.setFill("yellow")
        self.__black_cube_text = Text(Point(self.x - 10, self.y + 10), "0")
        self.__black_cube_text.setSize(15)
        self.__black_cube_text.setOutline("black")
        self.__red_cube_text = Text(Point(self.x + 10, self.y + 10), "0")
        self.__red_cube_text.setSize(15)
        self.__red_cube_text.setOutline("red")
        self.__cube_text = {"blue": self.__blue_cube_text, "yellow": self.__yellow_cube_text, "black": self.__black_cube_text, "red": self.__red_cube_text}
        self.__has_res_station = False
        self.__res_station_image = Polygon(Point(self.x + 20, self.y - 5), Point(self.x + 25, self.y - 10), Point(self.x + 30, self.y - 5), Point(self.x + 30, self.y + 5), Point(self.x + 20, self.y + 5))
        self.__res_station_image.setFill("White")
        self.__has_outbreaked = False

        self.__center = Point(self.x, self.y)
        self.__image = Circle(self.__center, self.__radius)
        self.__image.setFill(self.__colour)
        self.__image.setOutline(self.__colour)

    def get_center(self):
        return self.__center

    def get_colour(self):
        return self.__colour

    def get_connected_cities(self):
        return self.__connected_cities.copy()

    def get_name(self):
        return self.__name


    def set_connected_cities(self, to_set):
        self.__connected_cities = to_set.copy()

    def set_left_city(self, to_set):
        self.__left_city = to_set

    def set_right_city(self, to_set):
        self.__right_city = to_set

    def set_has_outbreaked(self, to_set):
        self.__has_outbreaked = to_set

    def set_has_res_station(self, to_set):
        self.__has_res_station = to_set

    def click(self):
        self.inc_cubes(self.__colour)

    def draw_city(self):
        self.__image.draw(self.window)
        city_name = Text(Point(self.x, self.y + self.__radius + 5), self.__name)
        city_name.draw(self.window)
        if self.__has_res_station:
            self.__res_station_image.draw(self.window)

    def draw_cubes(self):
        for cube_text in self.__cube_text.values():
            cube_text.undraw()
            cube_text.draw(self.window)

    def draw_paths(self):
        for city in self.__connected_cities:
            if self.__left_city and city.is_right_city():
                line_end = Point(0, city.y)
            elif self.__right_city and city.is_left_city():
                line_end = Point(1050, city.y)
            else:
                line_end = city.get_center()
            line = Line(self.__center, line_end)
            line.setFill("purple")
            line.setWidth(5)
            line.draw(self.window)

    def equals(self, to_check):
        return self.__name == to_check.get_name()

    def inc_cubes(self, colour):
        if self.__cubes[colour] >= 3:
            if not self.__has_outbreaked:
                self.__game.inc_outbreaks()
                self.__has_outbreaked = True
                for city in self.__connected_cities:
                    city.inc_cubes(colour)
        else:
            self.__cubes[colour] += 1

        self.__cube_text[colour].setText(str(self.__cubes[colour]))
        self.draw_cubes()

    def is_clicked(self, mouse_x, mouse_y):
        return ((self.x - mouse_x)**2 + (self.y - mouse_y)**2) <= self.__radius**2

    def is_left_city(self):
        return self.__left_city

    def is_right_city(self):
        return self.__right_city