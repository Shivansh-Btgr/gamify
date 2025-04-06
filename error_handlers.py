from flask import jsonify

def handle_api_error(error_message="An unexpected error occurred", status_code=400):
    """
    Standard function to handle API errors consistently
    
    Args:
        error_message (str): The error message to return
        status_code (int): HTTP status code
        
    Returns:
        JSON response with error status and message
    """
    return jsonify({
        'status': 'error',
        'message': error_message
    }), status_code

def handle_success_response(data=None, message="Operation completed successfully"):
    """
    Standard function to handle API success responses consistently
    
    Args:
        data (dict): Optional data to return
        message (str): Success message
        
    Returns:
        JSON response with success status and data
    """
    response = {
        'status': 'success',
        'message': message
    }
    
    if data:
        response.update(data)
        
    return jsonify(response)
