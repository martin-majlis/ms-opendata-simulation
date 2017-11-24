#!/usr/bin/python3

import datetime
import math
import random


class Student(object):
    def __init__(
            self,
            name: str,
            heat: float,
            noise: float,
            group: []
    ):
        self.name = name
        self.heat = heat
        self.noise = noise
        self.group = group

    def __repr__(self):
        return (
            "Student ({}) = H: {}, N: {}, G: {}"
        ).format(self.name, self.heat, self.noise, self.group)


class Room(object):
    def __init__(
        self,
        name,
        heat,
        noise,
        birds
    ):
        self.name = name
        self.baseHeat = heat
        self.baseNoise = noise
        self.temperature = 0
        self.noise = 0
        self.nStudents = 0
        self.nBirds = birds

    def init(self, sun, noise):
        self.temperature = sun.temperature + \
            (self.baseHeat if sun.active else 0)
        self.noise = 30 + self.baseNoise * (noise.noise - 30)
        self.nStudents = 0

    def occupy(self, groups):
        # print(self)
        for g in groups:
            self.temperature += g.heat
            self.noise += g.noise
            self.nStudents += len(g.student)
            # print(repr(self) + "\t" + repr(gq))

    def __repr__(self):
        return (
            "Room ({}) = T: {}, N: {}, S: {}"
        ).format(self.name, self.temperature, self.noise, self.nStudents)


class Group(object):
    def __init__(
            self,
            name: str,
    ):
        self.name = name
        self.heat = 0
        self.noise = 0
        self.student = []

    def add(self, index, student):
        self.student.append(index)
        self.heat += student.heat
        self.noise += student.noise

    def __repr__(self):
        return (
            "Group ({}) = H: {}, N: {}, S: {}"
        ).format(self.name, self.heat, self.noise, self.student)


class Sensor(object):
    def __init__(
        self,
        name,
        column,
        ent=None,
    ):
        self.name = name
        self.column = column
        self.ent = ent


class Wind(object):
    def __init__(self):
        self.speed = 10.0
        self.direction = 0

    def step(self, _d, _h):
        self.speed = max(self.speed + random.gauss(0, 4), 0)
        self.direction = (360 + self.direction + random.gauss(0, 5)) % 360


class Sun(object):
    def __init__(self):
        self.temperature = 20
        self.active = False

    def step(self, _d, h):
        prob = 0.28
        self.active = False
        if h > 5 and h <= 15:
            prob = 0.75
            self.active = True

        if self.temperature < -10:
            prob += 0.2

        if self.temperature > 40:
            prob -= 0.1

        change = 2 * random.random()
        if random.random() < prob:
            self.temperature += change
        else:
            self.temperature -= change

        # print("Sun: " + str(self.temperature))


class Noise(object):
    def __init__(self):
        self.baseNoise = 30
        self.noise = self.baseNoise

    def step(self, d, h):
        prob = 0.5
        coef = 3

        if h == 0:
            self.noise = self.baseNoise + 10 + random.gauss(0, 5)

        if d < 5:
            coef = 8
            if (h >= 5 and h <= 9) or (h >= 15 and h <= 17):
                prob = 0.9
            else:
                prob = 0.2

        change = coef * random.random()
        if random.random() < prob:
            self.noise += change
        else:
            self.noise -= change

        self.noise = min(max(self.noise, 30), 100)
        # print("Noise: " + str(self.noise))


class SchoolSim(object):
    def __init__(
        self,
        nStudents: int,
        nGroups: int
    ):
        self.nGroups = nGroups
        self.nStudents = nStudents

        self._initGroups()
        self._initStudents()
        self._initSensors()

    def initialize(
        self,
        startDate,
    ):
        self.beat = 0
        self.startDate = startDate
        self.actDate = startDate
        self.wind = Wind()
        self.sun = Sun()
        self.noise = Noise()

    def step(self):
        self.beat += 1
        self.actDate += datetime.timedelta(hours=1)

        d = ((int(self.actDate.strftime("%w")) + 6) % 7)
        h = int(self.actDate.strftime("%H"))
        self.wind.step(d, h)
        self.sun.step(d, h)
        self.noise.step(d, h)

        k = self._tk(d, h)

        for r in range(self.nRooms):
            groups = self.timetable[k][r]

            room = self.room[r]
            room.init(self.sun, self.noise)
            room.occupy([self.group[g] for g in groups])

    def defineRooms(
        self,
        mapping
    ):
        self.room = []
        for row in mapping:
            for r in row:
                room = Room(*r)
                self.room.append(
                    room
                )
                heatS = Sensor(
                    "Temp-" + room.name,
                    [("Temperature", lambda room=room: room.temperature)],
                    room
                )
                self.addSensor(heatS)

                heatS = Sensor(
                    "Noise-" + room.name,
                    [("Noise", lambda room=room: room.noise)],
                    room
                )
                self.addSensor(heatS)

                countS = Sensor(
                    "Students-" + room.name,
                    [("Count", lambda room=room: room.nStudents)],
                    room,
                )
                self.addSensor(countS)

                self.addSensor(heatS)
                countS = Sensor(
                    "Birds-" + room.name,
                    [("Count", lambda room=room: (
                        int(random.gauss(1, 0.2) * (room.nBirds - room.nBirds *
                                                    min(room.nStudents / 40.0, 1)))
                    ))],
                    room,
                )
                self.addSensor(countS)

        self.nRooms = len(self.room)

    def generateTimeTable(self):
        self.timetable = {}
        for d in range(7):
            for h in range(24):
                k = self._tk(d, h)
                self.timetable[k] = [[] for _ in range(self.nRooms)]
                for g in range(self.nGroups):
                    prob = 0
                    if d < 5:  # pracovni den
                        if h > 5 and h < 17:  # doba v prubehu dne
                            if h in [6, 15, 16]:
                                prob = 0.3
                            elif h in [7, 14]:
                                prob = 0.6
                            else:
                                prob = 0.93
                    # print("%d-%d - %d => %f" % (d, h, g, prob))
                    if random.random() <= prob:
                        while True:
                            roomIndex = math.floor(
                                self.nRooms * random.random())
                            if len(self.timetable[k][roomIndex]) < 5:
                                self.timetable[k][roomIndex].append(g)
                                break

    def addSensor(self, sensor):
        self.sensors[sensor.name] = sensor

    def getSensorsMeta(self):
        res = {}
        for s in self.sensors.values():
            res[s.name] = [c[0] for c in s.column]
        return res

    def getSensorData(self):
        res = {
            'TS': self.actDate.strftime("%Y-%m-%d %H:%M:%S")
        }
        for s in self.sensors.values():
            res[s.name] = [c[1]() for c in s.column]
        return res

    def _initGroups(self):
        self.group = [Group(str(i)) for i in range(self.nGroups)]

    def _initStudents(self):
        self.student = []
        for i in range(self.nStudents):
            g1 = math.floor(self.nGroups * random.random())
            g2 = math.floor(self.nGroups * random.random())
            student = Student(
                name=str(i),
                heat=random.gauss(0.3, 0.05),
                noise=random.gauss(0.6, 0.1),
                group=[g1, g2]
            )
            for g in [g1, g2]:
                self.group[g].add(i, student)
            self.student.append(student)

    def _initSensors(self):
        self.sensors = {}
        windS = Sensor(
            "Wind",
            [
                ("Direction", lambda: self.wind.direction),
                ("Speed", lambda: self.wind.speed)
            ]
        )
        self.addSensor(windS)

        outTempS = Sensor(
            "OutTempS",
            [
                ("Temperature", lambda: self.sun.temperature - 2)
            ]
        )
        self.addSensor(outTempS)

        outTempJ = Sensor(
            "OutTempJ",
            [
                ("Temperature", lambda: self.sun.temperature +
                 (10 if self.sun.active else 0))
            ]
        )
        self.addSensor(outTempJ)

        outNoiseZ = Sensor(
            "OutNoiseZ",
            [
                ("Noise", lambda: self.noise.noise)
            ]
        )
        self.addSensor(outNoiseZ)

    def _tk(self, d, h):
        return "{}-{:02d}".format(
            ["Po", "Ut", "St", "Ct", "Pa", "So", "Ne"][d],
            h
        )


sim = SchoolSim(
    nStudents=150,
    nGroups=20
)

# Kazda mistnost ma:
# - nazev
# - jak hodne tam sviti slunce
# - jaky podil dodatecneho hluku se prenese
# Slunce sviti z jihu a rusna cesta je na zapade
sim.defineRooms(
    [[("SZ", 1, 0.95, 5), ("SS", 1, 0.95, 10), ("SV", 1, 0.75, 15)],
     [("ZZ", 5, 0.95, 10), ("CC", 5, 0.85, 0), ("VV", 5, 0.73, 20)],
     [("JZ", 10, 0.95, 10), ("JJ", 10, 0.75, 20), ("JV", 10, 0.70, 30)]]
)

sim.generateTimeTable()
# print(repr(sim.timetable))

sim.initialize(
    startDate=datetime.datetime(2017, 10, 23)
)

sensors = sim.getSensorsMeta()
fhs = {}
for (sName, columns) in sensors.items():
    fhs[sName] = open("data/data-" + sName + ".csv", "w")
    print(
        ",".join(["TS", "Name"] + columns),
        file=fhs[sName]
    )

for i in range(24 * 7 * 20):
    sim.step()
    data = sim.getSensorData()
    for sName in sensors.keys():
        print(
            ",".join(map(str, [data['TS'], sName] + data[sName])),
            file=fhs[sName]
        )
