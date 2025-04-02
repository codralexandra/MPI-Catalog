from flask import Blueprint
from Backup.functionality import Backup
from logger import log_route_io
backup_bp = Blueprint('backup', __name__)

"""
/backup:
    - Description: Handles DB backup.
    - Request Body: NONE:
    - Response: Returns a success message if backup is successful, or an error message if the backup fails.
    """
@backup_bp.route('/backup', methods=['POST'])
@log_route_io
def backup():
    return Backup.backup()