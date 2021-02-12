from math import fabs
import numpy as np

EPS = 10 ** -5


class Point:

    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y

    def to_tuple(self):
        return self.x, self.y

    def distance_to(self, point):
        return ((self.x - point.x) ** 2 + (self.y - point.y) ** 2) ** 0.5

    def __repr__(self):
        return f'({self.x:.5f}, {self.y:.5f})'

    def __str__(self):
        return f'({self.x:.5f}, {self.y:.5f})'


class Line:

    def __init__(self, A, B, C):
        self.A = A
        self.B = B
        self.C = C

    def check_point(self, point):
        x, y = point.x, point.y
        A, B, C = self.A, self.B, self.C
        return A * x + B * y + C

    def reverse_coefs(self):
        self.A, self.B, self.C = -self.A, -self.B, -self.C

    def intersect_with_line(self, line):
        A1, B1, C1 = self.A, self.B, self.C
        A2, B2, C2 = line.A, line.B, line.C
        if fabs(A1 * B2 - A2 * B1) <= EPS:
            return None
        intersect = Point()
        intersect.x = -(C1 * B2 - C2 * B1) / (A1 * B2 - A2 * B1)
        intersect.y = -(A1 * C2 - A2 * C1) / (A1 * B2 - A2 * B1)
        return intersect

    def intersect_with_segment(self, segment):
        segment_line = segment.get_line()
        intersect = self.intersect_with_line(segment_line)
        if intersect is None:
            return None
        vec1 = Point(intersect.x - segment.a.x, intersect.y - segment.a.y)
        vec2 = Point(intersect.x - segment.b.x, intersect.y - segment.b.y)
        if vec1.x * vec2.x <= EPS and vec1.y * vec2.y <= EPS:
            return intersect
        return None


class Segment:

    def __init__(self, a: Point, b: Point):
        self.a = a
        self.b = b

    def get_line(self) -> Line:
        x_1, y_1 = self.a.to_tuple()
        x_2, y_2 = self.b.to_tuple()
        A = y_2 - y_1
        B = x_1 - x_2
        C = - x_1 * A - y_1 * B
        return Line(A, B, C)


class Polygon:

    def __init__(self, points: list):
        self.segments = []
        for i in range(0, len(points) - 1):
            self.segments.append(Segment(points[i], points[i + 1]))
        self.segments.append(Segment(points[-1], points[0]))

    def contains_point(self, point):
        ray = Ray(Segment(point, Point(point.x + 1, point.y)))
        intersects_num = 0
        for segment in self.segments:
            if ray.intersect_with_segment(segment) is not None:
                intersects_num += 1
        return bool(intersects_num % 2)


class Ray:

    def __init__(self, segment):
        self.main_line = segment.get_line()
        vec = Point(segment.b.y - segment.a.y + segment.a.x, -segment.b.x + segment.a.x + segment.a.y)
        self.side_line = Segment(segment.a, vec).get_line()
        self.point = segment.a
        if self.side_line.check_point(segment.b) < 0:
            self.side_line.reverse_coefs()

    def intersect_with_segment(self, segment: Segment):
        intersect = self.main_line.intersect_with_segment(segment)
        if intersect is not None and self.side_line.check_point(intersect) > 0:
            return intersect
        return None

    def intersect_with_polygon(self, polygon):
        points = []
        for segment in polygon.segments:
            point = self.intersect_with_segment(segment)
            if point is not None:
                points.append(point)

        if len(points) == 0:
            return None
        return min(zip(points,
                       map(lambda p: p.distance_to(self.point), points)),
                   key=lambda pd: pd[1])[0]


room_points_number = int(input())
room_points_array = np.array(list(map(float, input().split()))).reshape(-1, 2)
room_points = [Point(*p) for p in room_points_array]
moving_number, scans_num = map(int, input().split())
lead_std, moving_std_x, moving_std_y = map(float, input().split())
robot_x0, robot_y0 = None, None
t = input()
if t.split()[0] != '0':
    robot_x0, robot_y0 = list(map(float, t.split()))[1:]
logs = [np.array(list(map(float, input().split())))]
speeds = []
for i in range(moving_number):
    speeds.append(list(map(float, input().split())))
    logs.append(list(map(float, input().split())))
logs = np.array(logs)
speeds = np.array(speeds)

robot_points = list(np.full((logs.shape[0], 2), 6.).reshape(-1))
polygon = Polygon(room_points)


class Locator:

    def __init__(self, n_points, polygon_points, speeds, x_std, y_std, d_std, logs, n_rays):
        self.n_points = n_points
        self.speeds = speeds
        self.n_rays = n_rays
        self.x_std = x_std
        self.y_std = y_std
        self.d_std = d_std
        min_x, max_x = min(polygon_points[:, 0]), max(polygon_points[:, 0])
        min_y, max_y = min(polygon_points[:, 1]), max(polygon_points[:, 1])
        self.points = self.generate_random_points(n_points, min_x, max_x, min_y, max_y)
        self.polygon = Polygon([Point(*p) for p in room_points_array])
        self.logs = logs
        self.index = 0
        self.angles = np.linspace(0, 2 * np.pi, self.logs.shape[1] + 1)[:-1]

    def calc_weights(self, all_inxs=False):
        weights = np.zeros(len(self.points), dtype=np.float64)
        for i, point in enumerate(self.points):
            point_ = Point(*point)
            if not self.polygon.contains_point(point_):
                weights[i] = -np.inf
                continue
            if all_inxs:
                log_ = self.calc_log(point_)
                weights[i] = -((log_ - self.logs[self.index]) ** 2).sum() / lead_std ** 2 / 2
            else:
                #                 ray_inxs = np.random.choice(self.angles.shape[0], size=self.n_rays)
                ray_inxs = np.linspace(0, scans_num, self.n_rays + 1)[:-1].astype(int)
                log_ = self.calc_log(point_, ray_inxs)
                weights[i] = -((log_ - self.logs[self.index, ray_inxs]) ** 2).sum() / lead_std ** 2 / 2
        weights = np.exp(weights - weights.max())
        weights /= sum(weights)
        return weights

    def step(self, resample=True):
        if resample:
            self.points = self.resample(self.calc_weights(), self.points)
        self.points = self.points + self.speeds[self.index]
        n = self.points.shape[0]
        self.points += np.c_[np.random.normal(scale=self.x_std, size=(n, 1)), np.random.normal(scale=self.y_std, size=(n, 1))]
        self.index += 1

    def optimize(self):
        self.points = self.resample(self.calc_weights(), self.points)
        n = self.points.shape[0]
        self.points += np.c_[np.random.normal(scale=self.x_std / 10, size=(n, 1)), np.random.normal(scale=self.y_std / 10, size=(n, 1))]

    def calc_log(self, a, angles=None):
        if angles is None:
            angles = self.angles
        else:
            angles = self.angles[angles]
        scans = np.zeros(angles.shape[0])
        for i, angle in enumerate(angles):
            b = Point(a.x + np.cos(angle), a.y + np.sin(angle))
            ray = Ray(Segment(a, b))
            intersect = ray.intersect_with_polygon(self.polygon)
            if intersect is None:
                return None
            scans[i] = intersect.distance_to(a)
        return scans

    def resample(self, weights, points):
        delta = int((self.n_points - 100) / self.speeds.shape[0])
        if points.shape[0] <= 250:
            inxs = np.random.choice(len(points), size=100, p=weights)
        else:
            inxs = np.random.choice(len(points), size=len(points) // 2, p=weights)
        # inxs = np.random.choice(len(points), size=len(points), p=weights)
        return points[inxs]

    @staticmethod
    def generate_random_points(N, x0, x1, y0, y1):
        return np.c_[(x1 - x0) * np.random.rand(N, 1) + x0, (y1 - y0) * np.random.rand(N, 1) + y0]


locator = Locator(4000, room_points_array, speeds, moving_std_x, moving_std_y, lead_std, logs, 4)

for i in range(speeds.shape[0]):
    # locator.n_rays = min(36, locator.n_rays+1)
    locator.step()

locator.optimize()

print(*locator.points[np.argmax(locator.calc_weights())])
