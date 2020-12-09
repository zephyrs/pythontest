import math
import re

import numpy as np

import matplotlib.pyplot as plt
import scipy.linalg
from mpl_toolkits.mplot3d import Axes3D


class Slope:
    def __init__(self, xs, ys, zs, r, name):
        self._xs, self._ys, self._zs, self._r, self._name = xs, ys, zs, r, name

    def doFit(self):
        """
        dd = []
        for i in range(len(self._xs)):
            dd.append([self._xs[i], self._ys[i], self._zs[i]])
        data = np.asarray(dd)
        A = np.c_[data[:, 0], data[:, 1], np.ones(data.shape[0])]
        C, _, _, _ = scipy.linalg.lstsq(A, data[:, 2])
        print C
        """
        # do fit
        tmp_A = []
        tmp_b = []
        for i in range(len(self._xs)):
            tmp_A.append([self._xs[i], self._ys[i], 1])
            tmp_b.append(self._zs[i])
        b = np.matrix(tmp_b).T
        A = np.matrix(tmp_A)
        self._fit = (A.T * A).I * A.T * b
        self._errors = b - A * self._fit
        self._residual = np.linalg.norm(self._errors)

        print(self._name + ":")
        print("%f x + %f y + %f = z" % (self._fit[0], self._fit[1], self._fit[2]))
        # print "errors:"
        # print self._errors
        # print "residual:"
        # print self._residual

        y_unit = 1 if self._fit[1] > 0 else -1

        ry = np.array([0, y_unit, 0])
        rslope = np.array([self._fit[0], self._fit[1], -1])
        c = np.dot(rslope, ry) / np.linalg.norm(rslope) / np.linalg.norm(ry)
        angle = np.arccos(np.clip(c, -1, 1))
        print("angle: %f" % np.degrees(angle))

        delta = self._r * np.sin(angle) * 2
        print("delta_y: %f" % delta)

        return self._fit

    def doPlot(self, xlim, ylim):
        # plot plane
        X, Y = np.meshgrid(
            np.arange(xlim[0], xlim[1]), np.arange(ylim[0] - 5, ylim[1] + 5)
        )
        Z = np.zeros(X.shape)
        for r in range(X.shape[0]):
            for c in range(X.shape[1]):
                Z[r, c] = self._fit[0] * X[r, c] + self._fit[1] * Y[r, c] + self._fit[2]

        return X, Y, Z


def parseFile(fname):
    yy = {"1": [], "2": []}
    rr = {"1": 0.0, "2": 0.0}
    with open(fname, "r") as f:
        lines = f.readlines()
        pattern1 = re.compile(r"\bslope(?P<k>[12])\s+(?P<v>.*?)\s")
        pattern2 = re.compile(r"\bslope(?P<k>[12])--->\s+R_ref:\s+(?P<v>.*?)\s")
        for l in lines:
            match1 = re.search(pattern1, l)
            if match1:
                key = match1.group("k")
                value = float(match1.group("v"))
                yy[key].append(value)
            match2 = re.search(pattern2, l)
            if match2:
                key = match2.group("k")
                value = float(match2.group("v"))
                rr[key] = value
    return yy["1"], yy["2"], rr["1"], rr["2"]


def runTest(fname):
    xs = [0, 59.5221, 91.1932, 80.1939, 31.6711, -31.6711, -80.1939, -91.1932, -59.5221]
    # ys = [85.14, 85.15, 85.2, 85.2, 85.22, 85.14, 85.15, 85.5, 85.16]
    zs = [-92.6, -70.9357, -16.0798, 46.3, 87.0155, 87.0155, 46.3, -16.0798, -70.9357]

    ys1, ys2, r1, r2 = parseFile(fname)
    print(ys1)
    print(ys2)

    # plot raw data
    plt.figure()
    ax = plt.subplot(111, projection="3d")
    ax.scatter(xs, ys1, zs, color="m")
    ax.scatter(xs, ys2, zs, color="g")

    slope1 = Slope(xs, ys1, zs, r1, "plane1")
    slope1.doFit()

    slope2 = Slope(xs, ys2, zs, r2, "plane2")
    slope2.doFit()
    """
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    X1, Y1, Z1 = slope1.doPlot(xlim, ylim)
    ax.plot_wireframe(X1, Y1, Z1, color='blue')
    X2, Y2, Z2 = slope2.doPlot(xlim, ylim)
    ax.plot_wireframe(X2, Y2, Z2, color='red')

    lim = 600
    ax.set_xlim3d(-lim, lim)
    ax.set_ylim3d(-lim, lim)
    ax.set_zlim3d(-lim, lim)
    """
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    plt.show()
    return 1


if __name__ == "__main__":
    runTest("in.txt")
