from db_utils import db_database
import os
import json
from datetime import datetime


user_collection = db_database["User"]
assignments_collection = db_database["Assignment"]
course_collection = db_database["Course"]
grade_collection = db_database["Grade"]
student_collection = db_database["Student"]

backup_path = "Backend/Backup/backups"

class Backup:
    def backup():
        # Create a timestamped backup folder
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_folder = os.path.join(backup_path, f"backup_{timestamp}")
        os.makedirs(backup_folder, exist_ok=True)

        # Copy database collections to the backup folder
        collections = {
            "User": user_collection,
            "Assignment": assignments_collection,
            "Course": course_collection,
            "Grade": grade_collection,
            "Student": student_collection,
        }

        for collection_name, collection in collections.items():
            backup_file = os.path.join(backup_folder, f"{collection_name}.json")
            with open(backup_file, "w") as f:
                data = list(collection.find())
                f.write(json.dumps(data, default=str, indent=4))

        print(f"Backup created at {backup_folder}")
        return {"message": f"Backup created at {backup_folder}"}, 200
        