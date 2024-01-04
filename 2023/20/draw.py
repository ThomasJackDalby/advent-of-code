import sys
import random
# from svg_toolkit import *
from puzzle import load_file
from p5 import *

def add(a, b):
    return (a[0]+b[0], a[1]+b[1])

def sub(a, b):
    return (a[0]-b[0], a[1]-b[1])

def multiply(a, factor):
    return (a[0]*factor, a[1]*factor)

SPRING_CONSTANT = 0.01
SPRING_LENGTH = 100

class Module:
    def __init__(self, name):
        self.name = name
        self.targets = []

file_path = sys.argv[1]
modules = load_file(file_path)
for module_name, module in modules.items():
    module.name = module_name
module_array = list(modules.values())

def setup():
    modules["rx"] = Module("rx")
    for module in modules.values():
        module.x = 100 + random.random() * 300
        module.y = 100 + random.random() * 300
        module.fixed = False
        module.vx = 0
        module.vy = 0
        module.force = (0, 0)
    modules["broadcaster"].fixed = True
    modules["broadcaster"].x = 250
    modules["broadcaster"].y = 10

    size(500, 500)

def get_force_magnitude(distance, is_target):
    extension = abs(SPRING_LENGTH - distance)
    if distance < SPRING_LENGTH:
        return 0.001 * max(-2 * extension, -100)
    elif is_target:
        return 0.001 * min(10 * extension, 100)
    else: return 0

def plot():
    import matplotlib.pyplot as plt

    distance = range(0, 200)
    force = [get_force_magnitude(d) for d in distance]
    plt.plot(distance, force)
    plt.show()

def draw():
    # add gravity
    for i in range(len(module_array)):
        module = module_array[i]
        module.force = (0, 0)
        module.force = add(module.force, (0, 0.001))

    # add springs
    for i in range(len(module_array)):
        module = module_array[i]
        for j in range(i+1, len(module_array)):
            target = module_array[j]
            distance = pow(module.x - target.x, 2) + pow(module.y - target.y, 2)
            
            force_magnitude = get_force_magnitude(distance, target.name in module.targets or module.name in target.targets)
            if distance != 0: direction = multiply(sub((target.x, target.y), (module.x, module.y)), 1/distance)
            else: direction = (0, 0)

            module.force = add(module.force, multiply(direction, force_magnitude))
            target.force = add(target.force, multiply(direction, -force_magnitude))

    for module in modules.values():
        if module.fixed: continue
        ax, ay = module.force
        module.vx += ax
        module.vy += ay
        module.vx *= 0.9
        module.vy *= 0.9
        
        module.x += module.vx
        module.y += module.vy

    background(255, 255, 255)
    for module in modules.values():
        stroke(0, 0, 0)
        ellipse(module.x, module.y, 20, 20)

        for target_name in module.targets:
            target = modules[target_name]
            stroke(0, 0, 0)
            line(module.x, module.y, target.x, target.y)
        
        stroke(255, 0, 0)
        line(module.x, module.y, module.x+module.force[0]*100, module.y+module.force[1]*100)

run()
# plot()