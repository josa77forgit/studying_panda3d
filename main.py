from direct.showbase.ShowBase import ShowBase
from direct.interval.IntervalGlobal import LerpPosInterval, Sequence, LerpHprInterval,
from panda3d.core import Point3
class Game(ShowBase):
    def __init__(self):
        super().__init__()
        self.map = loader.loadModel('models/environment')
        self.map.reparentTo(render)
        self.map.setPos(0, 90, -50)
        base.camLens.setFov(90)

        self.fish = loader.loadModel('blueminnow/blueminnow.egg')
        self.fish.setScale(20)
        self.fish.reparentTo(render)
        self.fish.setPos(0, 90, 20)
        self.fish.setH(270) # возможность поворачивать объект по оси x. так же есть возможность работать через setR(), setP() для других осей
                            #попрактикйся и попробой как они будут работать для других направлений

        self.start_pos = (0, 90, 20)
        self.finish_pos = (100, 90,20)

        self.interval = LerpPosInterval(self.fish, duration=5.0, pos=self.finish_pos,startPos=self.fish.getPos())
        #движение из точки startPos в точку pos

        self.rotation_interval = LerpHprInterval(self.fish, duration=2.0, hpr=(self.fish.getH()+180, 0, 0))
        #поворот вокруг оси на указанный угол

        self.secq = Sequence(self.interval,self.rotation_interval)
        #создание очередей анимаций действий


        self.secq.start()
        #запуск очереди анимаций

        taskMgr.doMethodLater(0.1, self.reverse, "checkMovementStatusTask")
        #установка задачи на постоянное выполнение с интервалом в 0.1 может быть и другой, далее функция которая будет вызываться, имя задачи в система

    

    def reverse(self, task):
        if self.secq.isStopped():#проверка остановился ли цикл анимаций и если остановился то перезапускаем
            self.start_pos, self.finish_pos = self.finish_pos, self.start_pos
            self.interval = LerpPosInterval(self.fish, duration=5.0, pos=self.finish_pos,
                                    startPos=self.fish.getPos())

            self.rotation_interval = LerpHprInterval(self.fish, duration=2.0, hpr=(self.fish.getH()+180, 0, 0))
            self.secq = Sequence(self.interval,self.rotation_interval)
            self.secq.start()

        return task.again #возвращаем сигнал для возвращаения функции в список задач



        base.useDrive()
        base.useTrackball()



app = Game()
app.run()