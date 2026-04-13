from panda3d.core import WindowProperties # импортируем класс для взаимодействиями с свойствами окна
from direct.showbase.ShowBase import ShowBase



class Game(ShowBase):
    def __init__(self):
        super().__init__()
        self.map = loader.loadModel('models/environment')
        self.map.reparentTo(render)
        self.map.setPos(0, 90, -50)
        base.camLens.setFov(90)

        self.hero = loader.loadModel('blueminnow/blueminnow.egg')
        self.hero.setScale(20)
        self.hero.reparentTo(render)
        self.hero.setPos(0, 90, 20)
        self.hero.setH(270)
        self.mouse_use() # активация задачи
        self.focus_camera() # активация привязки


    def focus_camera(self):
    # привязка камеры к персонажу
       base.disableMouse()
       base.camera.setH(180)
       base.camera.reparentTo(self.hero)
       base.camera.setPos(0, 0, 1.5)


    def mouse_use(self):
        self.props = WindowProperties()# получаем обькт наделенный свойствами для взаимодействия с окном
        self.props.setCursorHidden(True)  # Скрыть курсор
        self.props.setMouseMode(WindowProperties.M_relative)  #Реализуем движение мыши относительно обьекта
        base.win.requestProperties(self.props) #устанавливаем набор изменных свойств

        self.rotation_angle = 0  # Накопленный угол поворота

        taskMgr.add(self.update_mouse_position, 'update_mouse') #добавляем в список задач новую. Список задач будет проверяться автоматически

    def update_mouse_position(self, task):
        if base.mouseWatcherNode.hasMouse(): # проверяем узел мыши, был ли он задействован
            # Получаем относительное смещение мыши
            dx = base.mouseWatcherNode.getMouseX() # дельта по x
            dy = base.mouseWatcherNode.getMouseY() # дельта по x

            # Чувствительность (можно настроить)
            sensitivity = 10

            # Накапливаем угол поворота по горизонтали (например, по оси X)
            self.rotation_angle += dx * sensitivity

            # Устанавливаем поворот объекта
            self.hero.setH(-self.rotation_angle)

            # Сбрасываем мышь в центр экрана. что позволяет после повората смотреть именно в центр экрана.
        base.win.movePointer(
            0,
            base.win.getXSize() // 2,
            base.win.getYSize() // 2
        )

        return task.cont

app = Game()
app.run()