import uuid

class MyPoint:
    def __init__(self):
        self.m_x = 0
        self.m_y = 0

    def __init__(self,_x,_y):
        self.m_x = _x
        self.m_y = _y

    def setX(self,_x):
        self.m_x = _x

    def setY(self,_y):
        self.m_y = _y

    def getX(self):
        return self.m_x

    def getY(self):
        return self.m_y


class MyCurve:
    def __init__(self, _p1=None, _p2=None):
        self.m_p1 = _p1
        self.m_p2 = _p2

    def setP1(self, _p1):
        self.m_p1 = _p1

    def setP2(self, _p2):
        self.m_p2 = _p2

    def getP1(self):
        return self.m_p1

    def getP2(self):
        return self.m_p2


class MyParticle:
    def __init__(self, _pt=None, _r=None):
        self.m_pt = _pt
        self.m_r = _r
        self.selected = False
        self.temperature = 0
        self.knownTemperature = 0  # 0 nao conhece, 1 conhece sim
        self.identifier = uuid.uuid4()
        self.restr_x = 0
        self.restr_y = 0
        self.forces_x = 0
        self.forces_y = 0

    def setPt(self,_pt):
        self.m_pt = _pt

    def getPt(self):
        return self.m_pt

    def getR(self):
        return self.m_r


class MyFencePvc:
    def __init__(self, _p1=None, _p2=None):
        self.left_upper = _p1
        self.right_bottom = _p2
        self.right_upper = MyPoint(_p2.getX(), _p1.getY())
        self.left_bottom = MyPoint(_p1.getX(), _p2.getY())

    def setLU(self, x, y):
        self.left_upper = MyPoint(x, y)

    def setRB(self, x, y):
        self.right_bottom = MyPoint(x, y)
        self.right_upper.setX(x)
        self.left_bottom.setY(y)

    def getLU(self):
        return self.left_upper

    def getRB(self):
        return self.right_bottom

    def getLB(self):
        return self.left_bottom

    def getRU(self):
        return self.right_upper


class MyModel:
    def __init__(self):
        self.m_verts = []
        self.m_curves = []
        self.m_particles = []
        self.m_fence_pvc = None

    def setVerts(self, _x, _y):
        self.m_verts.append(MyPoint(_x, _y))

    def getVerts(self):
        return self.m_verts

    def setCurve(self, _x1, _y1, _x2, _y2):
        self.m_curves.append(MyCurve(MyPoint(_x1, _y1), MyPoint(_x2, _y2)))

    def getCurves(self):
        return self.m_curves

    def setParticle(self, _x, _y):
        self.m_particles.append(MyParticle(MyPoint(_x, _y), 50))

    def getParticles(self):
        return self.m_particles

    def setFencePvc(self, _x1, _y1, _x2, _y2):
        self.m_fence_pvc = MyFencePvc(MyPoint(_x1, _y1), MyPoint(_x2, _y2))

    def getFencePvc(self):
        return self.m_fence_pvc

    def resetFencePvc(self):
        self.m_fence_pvc = None

    def selectParticles(self):
        if self.m_fence_pvc is None:
            return
        xmin = min(self.m_fence_pvc.getLU().getX(), self.m_fence_pvc.getRU().getX())
        xmax = max(self.m_fence_pvc.getLU().getX(), self.m_fence_pvc.getRU().getX())
        ymin = min(self.m_fence_pvc.getLB().getY(), self.m_fence_pvc.getLU().getY())
        ymax = max(self.m_fence_pvc.getLB().getY(), self.m_fence_pvc.getLU().getY())
        for p in self.m_particles:
            x = p.getPt().getX()
            y = p.getPt().getY()
            in_x_bound = xmin <= x <= xmax
            in_y_bound = ymin <= y <= ymax
            if in_x_bound and in_y_bound:
                p.selected = True

    def unselectParticles(self):
        for p in self.m_particles:
            p.selected = False

    def setUpGridFromUX(self):
        lines = dict()  # Particle.X: [Particle.X, Particle2.X, Particle3.X...]
        columns = dict()  # Particle.Y: [Particle.Y, Particle2.Y, Particle3.Y...]
        for p in self.m_particles:
            found_reference_particle = False
            for k in lines.keys():  # Saber qual linha de particula ela pertence
                if abs(p.getPt().getY() - k) <= 100:  # Da uma margem de erro de 2 raios, para particulas na mesma linha
                    found_reference_particle = True
                    lines[k].append(p)
            if not found_reference_particle:
                lines[p.getPt().getY()] = [p]

            found_reference_particle = False
            for k in columns.keys():  # Saber qual coluna de particula ela pertence
                if abs(p.getPt().getX() - k) <= 100:  # Da uma margem de erro de 2 raios, para particulas na mesma coluna
                    found_reference_particle = True
                    columns[k].append(p)
            if not found_reference_particle:
                columns[p.getPt().getX()] = [p]

        lines = dict(sorted(lines.items()))
        columns = dict(sorted(columns.items()))

        i = 1
        copied_keys = list(lines.keys())
        for k in copied_keys:
            lines[i] = lines.pop(k)
            i += 1
        j = 1
        copied_keys = list(columns.keys())
        for k in copied_keys:
            columns[j] = columns.pop(k)
            j += 1

        # Para cruzar as infos de linha X coluna, e saber ao mesmo tempo qual linha e coluna eh a particula
        grid = [[0 for _ in range(len(columns.keys()))] for _ in range(len(lines.keys()))]
        for i in range(1, len(grid) + 1):
            for j in range(1, len(grid[i - 1]) + 1):
                linha = lines[i]
                col = columns[j]
                for elem in linha:
                    for elem2 in col:
                        if elem.identifier == elem2.identifier:
                            grid[i - 1][j - 1] = elem

        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if isinstance(grid[i][j], MyParticle):
                    grid[i][j].identifier = (i * len(grid[i])) + (j + 1)

        return grid

    def setUpConnect(self, grid):
        lines = len(grid)
        columns = len(grid[0])
        connect = [[0 for _ in range(5)] for _ in range(lines * columns)]
        for i in range(len(connect)):
            connect[i][-1] = i + 1
            connect[i][0] = 0 if i % columns == 0 else i
            connect[i][1] = 0 if (i + 1) % columns == 0 else i + 2
            connect[i][2] = 0 if i - columns + 1 <= 0 else i - columns + 1
            connect[i][3] = 0 if i + columns + 1 > lines * columns else i + columns + 1
        return connect

    def isEmpty(self):
        return (len(self.m_verts) == 0) and (len(self.m_curves) == 0) and (len(self.m_particles) == 0)

    def getBoundBox(self):
        if (len(self.m_verts) < 1) and (len(self.m_curves) < 1):
            return 0.0, 10.0, 0.0, 10.0
        if len(self.m_verts) > 0:
            xmin = self.m_verts[0].getX()
            xmax = xmin
            ymin = self.m_verts[0].getY()
            ymax = ymin
            for i in range(1, len(self.m_verts)):
                if self.m_verts[i].getX() < xmin:
                    xmin = self.m_verts[i].getX()
                if self.m_verts[i].getX() > xmax:
                    xmax = self.m_verts[i].getX()
                if self.m_verts[i].getY() < ymin:
                    ymin = self.m_verts[i].getY()
                if self.m_verts[i].getY() > ymax:
                    ymax = self.m_verts[i].getY()
        if len(self.m_curves) > 0:
            if len(self.m_verts) == 0:
                xmin = min(self.m_curves[0].getP1().getX(), self.m_curves[0].getP2().getX())
                xmax = max(self.m_curves[0].getP1().getX(), self.m_curves[0].getP2().getX())
                ymin = min(self.m_curves[0].getP1().getY(), self.m_curves[0].getP2().getY())
                ymax = max(self.m_curves[0].getP1().getY(), self.m_curves[0].getP2().getY())
            for i in range(1, len(self.m_curves)):
                temp_xmin = min(self.m_curves[i].getP1().getX(), self.m_curves[i].getP2().getX())
                temp_xmax = max(self.m_curves[i].getP1().getX(), self.m_curves[i].getP2().getX())
                temp_ymin = min(self.m_curves[i].getP1().getY(), self.m_curves[i].getP2().getY())
                temp_ymax = max(self.m_curves[i].getP1().getY(), self.m_curves[i].getP2().getY())
                if temp_xmin < xmin:
                    xmin = temp_xmin
                if temp_xmax > xmax:
                    xmax = temp_xmax
                if temp_ymin < ymin:
                    ymin = temp_ymin
                if temp_ymax > ymax:
                    ymax = temp_ymax
        return xmin, xmax, ymin, ymax
