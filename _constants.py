#  ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####

import os
import pygame


SCREEN = (1600, 900)
FPS = 60
PARENT = os.path.realpath(os.path.dirname(__file__))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BOARD_WHITE = (255, 255, 230)
BOARD_BLACK = (100, 150, 80)

IMAGES = {}
for img in os.listdir(os.path.join(PARENT, "images")):
    if img.endswith(".png"):
        IMAGES[img.replace(".png", "")] = pygame.transform.scale(pygame.image.load(os.path.join(PARENT, "images", img)), (90, 90))