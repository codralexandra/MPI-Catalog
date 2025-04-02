import logging
import json
from functools import wraps
from flask import request, jsonify, Response

def log_route_io(f):
    """
    A decorator to log the input and output of Flask routes.
    """

    @wraps(f)
    def wrapped(*args, **kwargs):
        try:
            # Log input
            input_data = {}
            if request.method in ['POST', 'PUT', 'PATCH']:
                try:
                    input_data = request.get_json()
                except Exception as e:
                    logging.warning(f"Failed to parse JSON input: {e}")
                    input_data = request.form.to_dict()  # Try form data
            elif request.args:
                input_data = request.args.to_dict()

            logging.info(f"Route: {request.path}, Method: {request.method}, Input: {json.dumps(input_data)}")

            # Execute the route
            result = f(*args, **kwargs)

            # Log output
            if isinstance(result, Response):  # Proper Flask Response handling
                try:
                    output_data = result.get_json()
                except Exception:
                    output_data = result.get_data(as_text=True)
            elif isinstance(result, tuple):  # Handle tuple responses (data, status)
                output_data = result[0] if isinstance(result[0], (dict, list, str)) else str(result)
            else:
                output_data = result if isinstance(result, (dict, list, str)) else str(result)

            logging.info(f"Route: {request.path}, Method: {request.method}, Output: {json.dumps(output_data)}")
            return result

        except Exception as e:
            logging.error(f"Error in route {request.path}: {e}", exc_info=True)
            return jsonify({"error": str(e)}), 500

    return wrapped