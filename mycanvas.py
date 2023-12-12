import sys
from PyQt5 import QtOpenGL, QtCore
from PyQt5.QtWidgets import *
from OpenGL.GL import *
from hetool.he.hecontroller import HeController
from hetool.he.hemodel import HeModel
from hetool.geometry.segments.line import Line
from hetool.geometry.point import Point
from hetool.compgeom.tesselation import Tesselation
from mydialog import TempDialog, SaveDialog
from math import *
import json
from mdf_solver import solve_mdf


class MyCanvas(QtOpenGL.QGLWidget):
    def __init__(self):
        super(MyCanvas, self).__init__()
        self.setGeometry(100,100,1200,800)
        self.setWindowTitle("Modelador")
        self.setMouseTracking(True)
        self.m_w = 0 # width: GL canvas horizontal size
        self.m_h = 0 # height: GL canvas vertical size
        self.m_L = -1000.0
        self.m_R = 1000.0
        self.m_B = -1000.0
        self.m_T = 1000.0
        self.list = None
        self.m_buttonPressed = False
        self.m_pt0 = QtCore.QPoint(0, 0)
        self.m_pt1 = QtCore.QPoint(0, 0)
        self.particle_hover = QtCore.QPoint(0, 0)
        self.particle_pos = QtCore.QPoint(0, 0)
        self.fencing_pt0 = QtCore.QPoint(0, 0)
        self.fencing_pt1 = QtCore.QPoint(0, 0)

        self.is_adding = False
        self.is_modeling = True
        self.is_fencing_pvc = False

        self.pvc_filename = ""

        self.m_hmodel = HeModel()
        self.m_controller = HeController(self.m_hmodel)

    def initializeGL(self):
        glClearColor(1.0, 1.0, 1.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
        glEnable(GL_LINE_SMOOTH)
        self.list = glGenLists(1)

    def resizeGL(self, _width, _height):
        # store GL canvas sizes in object properties
        self.m_w = _width
        self.m_h = _height
        if(self.m_model is None) or (self.m_model.isEmpty()):
            self.scaleWorldWindow(1.0)
        else:
            self.m_L,self.m_R,self.m_B,self.m_T = self.m_model.getBoundBox()
            self.scaleWorldWindow(1.1)
        # setup the viewport to canvas dimensions
        glViewport(0, 0, self.m_w, self.m_h)
        # reset the coordinate system
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        # establish the clipping volume by setting up an
        # orthographic projection
        # glOrtho(0.0, self.m_w, 0.0, self.m_h,-1.0, 1.0)
        glOrtho(self.m_L,self.m_R,self.m_B,self.m_T,-1.0,1.0)
        # setup display in model coordinates
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def paintGL(self):
        # clear the buffer with the current clear color
        glClear(GL_COLOR_BUFFER_BIT)
        if ((self.m_model is None) or (self.m_model.isEmpty())) and not self.is_adding:
            return
        glCallList(self.list)
        glDeleteLists(self.list, 1)
        self.list = glGenLists(1)
        glNewList(self.list, GL_COMPILE)
        pt0_U = self.convertPtCoordsToUniverse(self.m_pt0)
        pt1_U = self.convertPtCoordsToUniverse(self.m_pt1)
        # Display model polygon RGB color at its vertices
        # interpolating smoothly the color in the interior
        glColor3f(1.0, 0.0, 0.0)
        glBegin(GL_LINE_STRIP)
        glVertex2f(pt0_U.x(), pt0_U.y())
        glVertex2f(pt1_U.x(), pt1_U.y())
        glEnd()
        if not ((self.m_model == None) or (self.m_model.isEmpty())):
            verts = self.m_model.getVerts()
            glColor3f(0.0, 1.0, 0.0)  # green
            glBegin(GL_TRIANGLES)
            for vtx in verts:
                glVertex2f(vtx.getX(), vtx.getY())
            glEnd()
            curves = self.m_model.getCurves()
            glColor3f(0.0, 0.0, 1.0)  # blue
            glBegin(GL_LINES)
            for curv in curves:
                glVertex2f(curv.getP1().getX(), curv.getP1().getY())
                glVertex2f(curv.getP2().getX(), curv.getP2().getY())
            glEnd()
            particles = self.m_model.getParticles()
            glBegin(GL_POINTS)
            for part in particles:
                if part.selected:
                    glColor3f(1.0, 0.0, 0.0)
                else:
                    glColor3f(0.0, 0.0, 1.0)
                angle = 0.0
                while angle <= 2.0 * pi:
                    x = 50.0 * sin(angle)
                    y = 50.0 * cos(angle)
                    glVertex2d(x + part.getPt().getX(), y + part.getPt().getY())
                    angle += 0.01
            glEnd()
            fence = self.m_model.getFencePvc()
            if fence is not None:
                glBegin(GL_LINE_LOOP)
                glVertex2f(fence.getLU().getX(), fence.getLU().getY())
                glVertex2f(fence.getRU().getX(), fence.getRU().getY())
                glVertex2f(fence.getRB().getX(), fence.getRB().getY())
                glVertex2f(fence.getLB().getX(), fence.getLB().getY())
                glEnd()

        if not(self.m_hmodel.isEmpty()):
            patches = self.m_hmodel.getPatches()
            for pat in patches:
                pts = pat.getPoints()
                triangs = Tesselation.tessellate(pts)
                for j in range(0, len(triangs)):
                    glColor3f(1.0, 0.0, 1.0)
                    glBegin(GL_TRIANGLES)
                    glVertex2d(pts[triangs[j][0]].getX(), pts[triangs[j][0]].getY())
                    glVertex2d(pts[triangs[j][1]].getX(), pts[triangs[j][1]].getY())
                    glVertex2d(pts[triangs[j][2]].getX(), pts[triangs[j][2]].getY())
                    glEnd()
            segments = self.m_hmodel.getSegments()
            for curv in segments:
                ptc = curv.getPointsToDraw()
                glColor3f(0.0, 1.0, 1.0)
                glBegin(GL_LINES)
                for curv in curves:
                    glVertex2f(ptc[0].getX(), ptc[0].getY())
                    glVertex2f(ptc[1].getX(), ptc[1].getY())
                glEnd()

        if self.is_adding:
            ptH = self.convertPtCoordsToUniverse(self.particle_hover)
            glBegin(GL_POINTS)
            angle = 0.0
            while angle <= 2.0 * pi:
                x = 50.0 * sin(angle)
                y = 50.0 * cos(angle)
                glVertex2d(x + ptH.x(), y + ptH.y())
                angle += 0.01
            glEnd()
        glEndList()

    def setModel(self, _model):
        self.m_model = _model

    def fitWorldToViewport(self):
        print("fitWorldToViewport")
        if self.m_model is None:
            return
        self.m_L, self.m_R, self.m_B, self.m_T = self.m_model.getBoundBox()
        self.scaleWorldWindow(1.10)
        self.update()

    def addParticlesState(self):
        print("particles")
        self.is_adding = True
        self.is_modeling = False
        self.is_fencing_pvc = False

    def modelLineState(self):
        print("modeling")
        self.is_modeling = True
        self.is_adding = False
        self.is_fencing_pvc = False

    def fencingPvcState(self):
        print("fencing_pvc")
        self.is_modeling = False
        self.is_adding = False
        self.is_fencing_pvc = True

    def openTemperatureUI(self):
        print("temperature")
        self.dialog = TempDialog(self)
        self.dialog.show()

    def setParticlesTemperature(self, t):
        particles = self.m_model.getParticles()
        for part in particles:
            if part.selected:
                part.temperature = int(t)
                part.knownTemperature = 1

    def openSaveDialog(self):
        print("save")
        self.dialog = SaveDialog(self)
        self.dialog.show()

    def saveJsonFile(self, file_name):
        grid = self.m_model.setUpGridFromUX()
        connect = self.m_model.setUpConnect(grid)
        data = {"temperatures": {p.identifier: [p.knownTemperature, p.temperature] for i, p in enumerate(self.m_model.m_particles)},
                "coonect": connect}
        data["temperatures"] = dict(sorted(data["temperatures"].items()))
        with open(file_name, "w") as file:
            file.write(json.dumps(data, indent=4))
        self.pvc_filename = file_name

    def runMdfSolver(self):
        if self.pvc_filename == "":
            print("Arquivo para PVC nao selecione. Salve um arquivo PVC para poder executar o metodo MDF.")
            return
        solve_mdf(self.pvc_filename)

    def scaleWorldWindow(self, _scaleFac):
        # Compute canvas viewport distortion ratio.
        vpr = self.m_h / self.m_w
        # Get current window center.
        cx = (self.m_L + self.m_R) / 2.0
        cy = (self.m_B + self.m_T) / 2.0
        # Set new window sizes based on scaling factor.
        sizex = (self.m_R - self.m_L) * _scaleFac
        sizey = (self.m_T - self.m_B) * _scaleFac
        # Adjust window to keep the same aspect ratio of the viewport.
        if sizey > (vpr*sizex):
            sizex = sizey / vpr
        else:
            sizey = sizex * vpr
        self.m_L = cx - (sizex * 0.5)
        self.m_R = cx + (sizex * 0.5)
        self.m_B = cy - (sizey * 0.5)
        self.m_T = cy + (sizey * 0.5)
        # Establish the clipping volume by setting up an
        # orthographic projection
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(self.m_L, self.m_R, self.m_B, self.m_T, -1.0, 1.0)

    def panWorldWindow(self, _panFacX, _panFacY):
        # Compute pan distances in horizontal and vertical directions.
        panX = (self.m_R - self.m_L) * _panFacX
        panY = (self.m_T - self.m_B) * _panFacY
        # Shift current window.
        self.m_L += panX
        self.m_R += panX
        self.m_B += panY
        self.m_T += panY
        # Establish the clipping volume by setting up an
        # orthographic projection
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(self.m_L, self.m_R, self.m_B, self.m_T, -1.0, 1.0)

    def convertPtCoordsToUniverse(self, _pt):
        dX = self.m_R - self.m_L
        dY = self.m_T - self.m_B
        mX = _pt.x() * dX / self.m_w
        mY = (self.m_h - _pt.y()) * dY / self.m_h
        x = self.m_L + mX
        y = self.m_B + mY
        return QtCore.QPointF(x, y)

    def mousePressEvent(self, event):
        self.m_buttonPressed = True
        if self.is_modeling:
            self.m_pt0 = event.pos()
        elif self.is_adding:
            self.particle_pos = event.pos()
            pt = self.convertPtCoordsToUniverse(self.particle_pos)
            self.m_model.setParticle(pt.x(), pt.y())
        elif self.is_fencing_pvc:
            self.fencing_pt0 = event.pos()

    def mouseMoveEvent(self, event):
        if self.is_modeling:
            if self.m_buttonPressed:
                self.m_pt1 = event.pos()
                self.update()
        elif self.is_adding:
            if not self.m_buttonPressed:
                self.particle_hover = event.pos()
                self.update()
        elif self.is_fencing_pvc:
            if self.m_buttonPressed:
                self.fencing_pt1 = event.pos()
                self.update()
                pt1 = self.convertPtCoordsToUniverse(self.fencing_pt1)
                if self.m_model.getFencePvc() is None:
                    pt0 = self.convertPtCoordsToUniverse(self.fencing_pt0)
                    self.m_model.setFencePvc(pt0.x(), pt0.y(), pt1.x(), pt1.y())
                else:
                    self.m_model.getFencePvc().setRB(pt1.x(), pt1.y())

    def mouseReleaseEvent(self, event):
        if self.is_modeling:
            pt0_U = self.convertPtCoordsToUniverse(self.m_pt0)
            pt1_U = self.convertPtCoordsToUniverse(self.m_pt1)
            self.m_model.setCurve(pt0_U.x(), pt0_U.y(), pt1_U.x(), pt1_U.y())
            self.m_pt0.setX(0)
            self.m_pt0.setY(0)
            self.m_pt1.setX(0)
            self.m_pt1.setY(0)

            p0 = Point(pt0_U.x(), pt0_U.y())
            p1 = Point(pt1_U.x(), pt1_U.y())
            segment = Line(p0, p1)
            self.m_controller.insertSegment(segment, 0.01)
        elif self.is_fencing_pvc:
            self.m_model.unselectParticles()
            self.m_model.selectParticles()
            self.m_model.resetFencePvc()

        self.m_buttonPressed = False
        self.update()
        self.repaint()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyCanvas()
    widget.show()
    sys.exit(app.exec_())
