import math
import numpy as np


class AnalysisMovement:
    def __init__(self, points_x, points_y, time_stamp):
        self.points_x = np.array(points_x)[0:-3]
        self.points_y = np.array(points_y)[0:-3]
        self.time_stamp = np.array(time_stamp)

        self.elapsed_time = time_stamp[-4] - time_stamp[0]
        self.trajectory_length = np.sum(np.sqrt(np.diff(self.points_x) ** 2 + np.diff(self.points_y) ** 2))
        self.dist_end_to_end = math.sqrt((points_x[-4] - points_x[0]) ** 2 + (points_y[-4] - points_y[0]) ** 2)

        self.velocities_x = (self.__rate_change(points_x))
        self.velocities_y = (self.__rate_change(points_y))
        self.velocities_x_mean = self.__mean(points_x[-4], points_x[0])
        self.velocities_y_mean = self.__mean(points_y[-4], points_y[0])
        self.velocities_x_max = np.max(self.velocities_x[:-2])
        self.velocities_y_max = np.max(self.velocities_y[:-2])
        self.velocities_x_min = np.min(self.velocities_x[:-2])
        self.velocities_y_min = np.min(self.velocities_y[:-2])

        self.velocities = np.sqrt(self.velocities_x ** 2 + self.velocities_y ** 2)
        self.velocities_mean = self.dist_end_to_end / self.elapsed_time
        self.velocities_max = np.max(self.velocities[:-2])
        self.velocities_min = np.min(self.velocities[:-2])

        self.velocities_x = self.velocities_x[:-2]
        self.velocities_y = self.velocities_y[:-2]
        self.time_stamp = self.time_stamp[:-1]

        self.accelerations = (self.__rate_change(self.velocities.tolist()))
        self.accelerations_mean = self.__mean(self.velocities[-3], self.velocities[0])
        self.accelerations_max = np.max(self.accelerations[:-1])
        self.accelerations_min = np.min(self.accelerations[:-1])
        self.a_beg_time = self.accelerations

        self.velocities = self.velocities[:-2]
        self.time_stamp = self.time_stamp[:-1]

        self.jerk = self.__rate_change(self.accelerations.tolist())
        self.jerk_mean = self.__mean(self.accelerations[-2], self.accelerations[0])
        self.jerk_max = np.max(self.jerk)
        self.jerk_min = np.min(self.jerk)

        self.accelerations = self.accelerations[:-1]
        self.time_stamp = self.time_stamp[:-1]

        self.direction = self.__calculate_direction_angle()  # wrt +x-axis
        self.sum_of_angles = np.sum(self.direction)  # wrt +x-axis
        self.straightness = abs(self.dist_end_to_end) / self.trajectory_length
        self.num_points = len(points_x)

        # Angular values
        dx = np.diff(np.array(points_x))
        dy = np.diff(np.array(points_y))
        first_derivative = dy / dx
        second_derivative = np.diff(first_derivative) / dx[:-1]
        curvature_numerator = (1 + first_derivative[:-1] ** 2) ** (3 / 2)
        self.radius_of_curvature = (curvature_numerator / np.abs(second_derivative))[:-1]
        self.radius_of_curvature_mean = np.mean(self.radius_of_curvature)
        self.radius_of_curvature_max = np.max(self.radius_of_curvature)
        self.radius_of_curvature_min = np.min(self.radius_of_curvature)

        self.angular_velocities = self.velocities / self.radius_of_curvature
        self.angular_velocities_mean = np.mean(self.angular_velocities)
        self.angular_velocities_max = np.max(self.angular_velocities)
        self.angular_velocities_min = np.min(self.angular_velocities)

    def __rate_change(self, a):
        a = np.array(a)

        delta_a = np.diff(a)
        delta_time_stamp = np.diff(self.time_stamp)

        rate_change_a = delta_a / delta_time_stamp

        return rate_change_a

    def __mean(self, f, i):
        return (f - i) / self.elapsed_time

    def __calculate_direction_angle(self):
        angles_radians = np.arctan2(self.velocities_y, self.velocities_x)
        angles_degrees = np.degrees(angles_radians)

        # Normalize the angles to be within [0, 360) degrees
        angles_degrees = np.where(angles_degrees < 0, angles_degrees + 360, angles_degrees)

        return angles_degrees


# x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# y = [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
# time = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# ma = AnalysisMovement(x, y, time)
# print(ma.points_x, ma.points_y)
# print(ma.elapsed_time, ma.dist_end_to_end, ma.trajectory_length)
# print("velociteis_x", ma.velocities_x, ma.velocities_x_mean, ma.velocities_x_max, ma.velocities_x_min)
# print("velociteis_y", ma.velocities_y, ma.velocities_y_mean, ma.velocities_y_max, ma.velocities_y_min)
# print("velocities", ma.velocities, ma.velocities_mean, ma.velocities_max, ma.velocities_min)
# print("accelerations", ma.accelerations, ma.accelerations_mean, ma.accelerations_max, ma.accelerations_min)
# print("jerk", ma.jerk, ma.jerk_mean, ma.jerk_max, ma.jerk_min)
# print("time_stamp", ma.time_stamp)
# print('\n angularvelocities', ma.angular_velocities, ma.angular_velocities_mean, ma.angular_velocities_max,
#       ma.angular_velocities_min)
# print('\n radius', ma.radius_of_curvature, ma.radius_of_curvature_mean, ma.radius_of_curvature_max,
#       ma.radius_of_curvature_min)
# print("directions",ma.direction)
