import numpy as np
from scipy.special import comb
import random
import time
import string 
import turtle
import math
from itertools import islice


class Motion():
    def __init__(self):
        self.r = lambda i, n, t: comb(n, i) * ( t**(n-i) ) * (1 - t)**i
        self.points = []
        self.box = []
        self.box2 = []
        self.boxes = {
            "0": self._betw([131,282],[177,310]),
            "1": self._betw([250,274],[313,318]),
            "2": self._betw([390,274],[438,324]),
            "3": self._betw([122,408],[187,456]),
            "4": self._betw([250,400],[314,451]),
            "5": self._betw([386,400],[448,466]),
            "6": self._betw([124,530],[188,584]),
            "7": self._betw([250,539],[313,588]),
            "8": self._betw([387,537],[446,579])
        }

    def _betw(self, p1:list=[], p2:list=[]):
        points = []
        for x in range(min(p1[0], p2[0]), max(p1[0], p2[0]) + 1):
            for y in range(min(p1[1], p2[1]), max(p1[1],p2[1]) + 1):
                points.append([x, y])
        return points

    def _curve(self, points, am_c):
        nPoints = len(points)
        xPoints = np.array([p[0] for p in points])
        yPoints = np.array([p[1] for p in points])
        t = np.linspace(0.0, 1.0, am_c)
        polynomial_array = np.array([self.r(i, nPoints-1, t) for i in range(0, nPoints)])
        xvals = np.dot(xPoints, polynomial_array)
        yvals = np.dot(yPoints, polynomial_array)
        return xvals, yvals

    def _create(self, points, am_c):
        x,y = self._curve(points, am_c)
        for i in range(len(x)):
            x_p, y_p = x[i], y[i]
            self.points.append([round(x_p),round(y_p)])

        return self.points
    
    def convert_correct_answers(self, positions:list=[]):
        x = []
        for point in positions:
            new_pos = random.choice(self.boxes[str(point)])
            x.append(new_pos)
        
        return x

    def _box(self, points:list=[], thickness:int=10):
        self.p = points
        #[[0,0],[40,40]]
        for x in range(abs(self.p[0][0]-self.p[1][0])):
            for y in range(abs(self.p[0][1]-self.p[1][1])):
                self.box.append([x+1,y+1])
                self.box2.append([x+1,y+1])
        for point in points:
            for coord in point:
                points[points.index(point)][point.index(coord)] += 5
        for x in range(abs(self.p[0][0]-self.p[1][0])):
            for y in range(abs(self.p[0][1]-self.p[1][1])):
                if [x-thickness,y-thickness] in self.box:
                    self.box.remove([x-thickness,y-thickness])
                if [x+thickness,y+thickness] in self.box2:
                    self.box2.remove([x+thickness,y+thickness])
        for x in self.box2:
            self.box.append(x)
        r = []
        for x in self.box:
            if x not in r:
                r.append(x)
        return r


    def create_curve_points(self, p1:list=[], p2:list=[], pass_point:list=[],amount:int=10):
        """
        .create_curve_points(start, end, point_to_curve_to, amount)
        """
        r = self._create(points=np.array([p2,pass_point,p1]), am_c=amount)
        return r

    def show(self, points):
        turtle.goto(points[0])
        for point in points:
            p = tuple(point)

            turtle.pendown()
            turtle.goto(p)
            turtle.penup()

        turtle.hideturtle()
        turtle.exitonclick()

    def main(self, positions):
        w = []
        #[[282, 285], [135, 439], [303, 414], [181, 568], [307, 587], [417, 566]]
        to_go = self.convert_correct_answers(positions=positions)
        r = 0
        for points in to_go:
            try:
                print(r,r+1)
                box = self._box(points=[to_go[r],to_go[r+1]])
                
                c = self.create_curve_points(p1=to_go[r], p2=to_go[r+1], pass_point=random.choice(box))
                for pt in c:
                    w.append(pt)
                r+=1
            except:
                pass

        return w, to_go
    
class TimeStamp():
    def __init__(self, motion, time_spent:int=14) -> None:
        self.motion = motion
        self.ts = time_spent
        self.time_spent = time_spent + 2
        self.timestamps = []

    def create_timestamps(self):
        r = 1
        while r != self.time_spent:
            initial = round(time.time()*1000)/1000
            self.timestamps.append(initial+r)
            r+=1

    def split_motion_for_timestamps(self):
        rand_n = [random.random() for i in range(self.ts)]
        split_xy = [list(islice(iter(self.motion), elem))
            for elem in [math.floor(i * len(self.motion) / sum(rand_n)) for i in rand_n]]
        return split_xy
    
    """
    
    set timestamps
    split motion
    put timestamps to end of motion
    
    """



    def create_motion(self):
        ts = round(time.time()*1000)
        self.create_timestamps()
        #[[], [[282, 285], [135, 439], [303, 414], [181, 568]], [[282, 285]]]
        mot = {}
        split = self.split_motion_for_timestamps()
        for x in self.timestamps:
            mot[x] = []
        for coords in range(len(split)):
            for point in split[coords]:
                mot[self.timestamps[coords]].append(point)
        
        final = []
        for key, value in mot.items():
            for v in value:
                final.append([list(v)[0], list(v)[1], key])
        return ts, final


class Complete():
    def __init__(self) -> None:
        self.motion = {"st":
            0,
            "dct":
            0,
            "mm": [],
            "mm-mp": 0,
            "md": [],
            "md-mp": 0,
            "mu": [],
            "mu-mp":0,
            "topLevel": {
                "inv":
                "false",
                "st": 0,
                "sc": {
                "availWidth": 1920,
                "availHeight": 1040,
                "width": 1920,
                "height": 1080,
                "colorDepth": 24,
                "pixelDepth": 24,
                "availLeft": 0,
                "availTop": 0,
                "onchange": "null",
                "isExtended": "true"
                },
                "nv": {
                "vendorSub":
                "",
                "productSub":
                "20030107",
                "vendor":
                "Google Inc.",
                "maxTouchPoints":
                0,
                "scheduling": {},
                "userActivation": {},
                "doNotTrack":
                "null",
                "geolocation": {},
                "connection": {},
                "pdfViewerEnabled":
                "true",
                "webkitTemporaryStorage": {},
                "hardwareConcurrency":
                8,
                "cookieEnabled":
                "true",
                "appCodeName":
                "Mozilla",
                "appName":
                "Netscape",
                "appVersion":
                "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
                "platform":
                "Win32",
                "product":
                "Gecko",
                "userAgent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
                "language":
                "en-GB",
                "languages": ["en-GB", "en-US", "en"],
                "onLine":
                "true",
                "webdriver":
                "false",
                "bluetooth": {},
                "clipboard": {},
                "credentials": {},
                "keyboard": {},
                "managed": {},
                "mediaDevices": {},
                "storage": {},
                "serviceWorker": {},
                "virtualKeyboard": {},
                "wakeLock": {},
                "deviceMemory":
                8,
                "ink": {},
                "hid": {},
                "locks": {},
                "mediaCapabilities": {},
                "mediaSession": {},
                "permissions": {},
                "presentation": {},
                "serial": {},
                "usb": {},
                "windowControlsOverlay": {},
                "xr": {},
                "userAgentData": {
                    "brands": [{
                    "brand": "Chromium",
                    "version": "110"
                    }, {
                    "brand": "Not A(Brand",
                    "version": "24"
                    }, {
                    "brand": "Google Chrome",
                    "version": "110"
                    }],
                    "mobile":
                    "false",
                    "platform":
                    "Windows"
                },
                "plugins": [
                    "internal-pdf-viewer", "internal-pdf-viewer", "internal-pdf-viewer",
                    "internal-pdf-viewer", "internal-pdf-viewer"
                ]
                },
                "dr":
                "",
                "exec":
                "false",
                "wn": [],
                "wn-mp":
                0,
                "xy": [],
                "xy-mp":
                0,
                "mm": [],
                "mm-mp": 0
            }, "v": 1
            }
        
    def find_closest(self, x, array2d):
        least_diff = 999
        least_diff_index = -1
        for num, elm in enumerate(array2d):
            diff = abs(x[0]-elm[0]) + abs(x[1]-elm[1])
            if diff < least_diff:
                least_diff = diff
                least_diff_index = num
        return array2d[least_diff_index]

    def finish(self, positions):
        curves, pos_pts = Motion().main(positions)
        timestamp = TimeStamp(curves)
        st, motion = timestamp.create_motion()
        print(pos_pts)
        mu = []
        md = []

        for pos in pos_pts:
            d = self.find_closest(pos, motion)
            if d in mu:
                pass
            else:
                mu.append(d)
                md.append([d[0]+1, d[1]-1, d[2]])
            
        print(mu)

            


        #TimeStamp
        self.motion["st"] = st
        self.motion["dct"] = st
        self.motion["topLevel"]["st"] = st
        #Motion
        self.motion["mm"] = motion
        self.motion["md"] = md
        self.motion["mu"] = mu
        self.motion["topLevel"]["mm"] = motion
        #Motion Points

        return self.motion



print(Complete().finish([0,1,8]))