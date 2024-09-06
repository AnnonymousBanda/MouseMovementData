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

        self.velocities_x = (self.__rate_change(points_x))[0:-2]
        self.velocities_y = (self.__rate_change(points_y))[0:-2]
        self.velocities_x_mean = self.__mean(points_x[-4], points_x[0])
        self.velocities_y_mean = self.__mean(points_y[-4], points_y[0])
        self.velocities_x_max = np.max(self.velocities_x)
        self.velocities_y_max = np.max(self.velocities_y)
        self.velocities_x_min = np.min(self.velocities_x)
        self.velocities_y_min = np.min(self.velocities_y)

        self.velocities = np.sqrt(self.velocities_x ** 2 + self.velocities_y ** 2)
        self.velocities_mean = self.dist_end_to_end / self.elapsed_time
        self.velocities_max = np.max(self.velocities)
        self.velocities_min = np.min(self.velocities)

        self.time_stamp = self.time_stamp[0:-1]

        self.accelerations = (self.__rate_change(self.velocities.tolist()))[0:-1]
        self.accelerations_mean = self.__mean(self.velocities[-1], self.velocities[0])
        self.accelerations_max = np.max(self.accelerations)
        self.accelerations_min = np.min(self.accelerations)
        self.a_beg_time = self.accelerations

        self.time_stamp = self.time_stamp[0:-1]

        self.jerk = self.__rate_change(self.accelerations.tolist())
        self.jerk_mean = self.__mean(self.accelerations[-1], self.accelerations[0])
        self.jerk_max = np.max(self.jerk)
        self.jerk_min = np.min(self.jerk)

        self.time_stamp = self.time_stamp[0:-1]

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

    def __mean(self, i, f):
        return (f - i) / self.elapsed_time

    def __calculate_direction_angle(self):
        angles_radians = np.arctan2(self.velocities_y, self.velocities_x)
        angles_degrees = np.degrees(angles_radians)

        # Normalize the angles to be within [0, 360) degrees
        angles_degrees = np.where(angles_degrees < 0, angles_degrees + 360, angles_degrees)

        return angles_degrees
