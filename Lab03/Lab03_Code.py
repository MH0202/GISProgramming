file = open(r"D:/PhD_TAMU/Courses/GEOG 676 GIS Programming/Lab/GISProgramming/Lab03\shape.txt")
lines = file.readlines()
file.close()

totalShape = []


# Class definition
class Shape():
    def __init__(self) -> None:
        pass
    def getArea(self):
        pass

class Rectangle (Shape):
    def __init__(self, l, w):
        #super().__init__()
        self.l = l
        self.w = w
    def getArea(self):
        return self.l * self.w
    
class Circle(Shape):
    def __init__(self, radius):
        #super().__init__()
        self.radius = radius
    def getArea (self):
        return 3.14 * (self.radius) * (self.radius)
class Triangle (Shape):
    def __init__(self, b, h):
        #super().__init__()
        self.b = b
        self.h = h
    def getArea (self):
        return 0.5*self.b*self.h
    
for line in lines:
    componets = line.split(',')
    shape = componets[0]
    # print(shape)

    if shape == "Rectangle":
        l = float(componets[1])
        w = float(componets[2])
        totalShape.append(Rectangle(l,w))
    elif shape== "Circle":
        radius = float(componets[1])
        totalShape.append(Circle(radius))
    elif shape == "Triangle":
        b = float(componets[1])
        h = float (componets[2])
        totalShape.append(Triangle(b, h))
    else:
        pass
for shape in totalShape:
    print("Area", shape.getArea())