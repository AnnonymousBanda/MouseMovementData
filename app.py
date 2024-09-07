from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import uuid
import physics


app = Flask(__name__)

CORS(app)


@app.route('/movement-data', methods=['POST'])
def process_data():
    try:
        data = request.get_json()
        
        x = data.get('x')
        y = data.get('y')
        time = data.get('time')
        
        # Data validation
        # x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        # y = [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
        # time = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        movement_analyser = physics.AnalysisMovement(x, y, time)

        df = pd.DataFrame({
            "UUID": [uuid.uuid4()]+[None]*(len(movement_analyser.velocities)-1),
            "velocity_x": movement_analyser.velocities_x,
            "velocity_x_mean": movement_analyser.velocities_x_mean,
            "velocity_x_max": movement_analyser.velocities_x_max,
            "velocity_X_min": movement_analyser.velocities_min,
            "velocity_y": movement_analyser.velocities_y,
            "velocity_y_mean": movement_analyser.velocities_y_mean,
            "velocity_y_max": movement_analyser.velocities_y_max,
            "velocity_y_min": movement_analyser.velocities_min,
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
            "direction": movement_analyser.direction,
            "sum_of_angles": movement_analyser.sum_of_angles,
            "straightness": [movement_analyser.straightness]+[None]*(len(movement_analyser.velocities)-1),
            "num_points": [movement_analyser.num_points]+[None]*(len(movement_analyser.velocities)-1),
            "a_beg_time": [movement_analyser.a_beg_time]+[None]*(len(movement_analyser.velocities)-1),
            "elapsed_time": [movement_analyser.elapsed_time]+[None]*(len(movement_analyser.velocities)-1),
            "trajectory_length": [movement_analyser.trajectory_length]+[None]*(len(movement_analyser.velocities)-1),
            "dist_end_to_end": [movement_analyser.dist_end_to_end]+[None]*(len(movement_analyser.velocities)-1),
        })

        print("Request Successfull")

        csv_file_path = 'data.csv'
        df.to_csv(csv_file_path, index=False)

        return send_file(csv_file_path, mimetype='text/csv', as_attachment=True)

    except Exception as e:
        print("Request Failed", str(e))
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)
