from flask import Flask, request, jsonify, send_file
import pandas as pd

import physics

app = Flask(__name__)


@app.route('/movement-data', methods=['POST'])
def process_data():
    try:
        data = request.get_json()

        x = data.get('x')
        y = data.get('y')
        time = data.get('time')

        movement_analyser = physics.AnalysisMovement(x, y, time)

        df = pd.DataFrame({
            "velocityX": movement_analyser.velocities_x,
            "velocityX_mean": movement_analyser.velocities_x_mean,
            "velocityX_max": movement_analyser.velocities_x_max,
            "velocityX_min": movement_analyser.velocities_min,
            "velocityY": movement_analyser.velocities_y,
            "velocityY_mean": movement_analyser.velocities_y_mean,
            "velocityY_max": movement_analyser.velocities_y_max,
            "velocityY_min": movement_analyser.velocities_min,
            "velocity": movement_analyser.velocities,
            "velocity_mean": movement_analyser.velocities_mean,
            "velocity_max": movement_analyser.velocities_max,
            "velocity_min": movement_analyser.velocities_min,
            "accelerations": movement_analyser.accelerations,
            "accelerations_mean": movement_analyser.accelerations_mean,
            "accelerations_max": movement_analyser.accelerations_max,
            "accelerations_min": movement_analyser.accelerations_min,
            "jerk": movement_analyser.jerk,
            "jerk_mean": movement_analyser.jerk_mean,
            "jerk_max": movement_analyser.jerk_max,
            "jerk_min": movement_analyser.jerk_min,
            "angular_velocities": movement_analyser.angular_velocities,
            "angular_velocities_mean": movement_analyser.angular_velocities_mean,
            "angular_velocities_max": movement_analyser.angular_velocities_max,
            "angular_velocities_min": movement_analyser.angular_velocities_min,
            "radius_of_curvature": movement_analyser.radius_of_curvature,
            "radius_of_curvature_mean": movement_analyser.radius_of_curvature_mean,
            "radius_of_curvature_max": movement_analyser.radius_of_curvature_max,
            "radius_of_curvature_min": movement_analyser.radius_of_curvature_min,
            "elapsed_time": movement_analyser.elapsed_time,
            "trajectory_length": movement_analyser.trajectory_length,
            "dist_end_to_end": movement_analyser.dist_end_to_end,
            "direction": movement_analyser.direction,
            "straightness": movement_analyser.straightness,
            "num_points": movement_analyser.num_points,
            "sum_of_angles": movement_analyser.sum_of_angles,
            "a_beg_time": movement_analyser.a_beg_time
        })

        csv_file_path = 'data.csv'
        df.to_csv(csv_file_path, index=False)

        return send_file(csv_file_path, mimetype='text/csv', as_attachment=True)

    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)
