from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import sqlite3
import json

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "students.db"


class Handler(SimpleHTTPRequestHandler):

    def do_POST(self):
        if self.path != "/add":
            self.send_error(404)
            return

        try:
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            data = json.loads(body.decode("utf-8"))

            first_name = data["first_name"].strip()
            last_name = data["last_name"].strip()
            roll_number = int(data["roll_number"])
            department = data["department"].strip()

            if not first_name or not last_name or not department:
                raise ValueError("All fields are required.")

            with sqlite3.connect(DB_PATH) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS students (
                        first_name TEXT NOT NULL,
                        last_name TEXT NOT NULL,
                        roll_number INTEGER PRIMARY KEY,
                        department TEXT NOT NULL
                    )
                """)

                conn.execute(
                    """INSERT INTO students
                       (first_name, last_name, roll_number, department)
                       VALUES (?, ?, ?, ?)""",
                    (first_name, last_name, roll_number, department)
                )

            self.send_json(200, {"message": "Student saved successfully!"})

        except sqlite3.IntegrityError:
            self.send_json(409, {"message": "That roll number already exists."})

        except (ValueError, KeyError, TypeError, json.JSONDecodeError):
            self.send_json(400, {"message": "Invalid student data."})

        except Exception as e:
            print("ERROR:", repr(e))
            self.send_json(500, {"message": str(e)})

    def send_json(self, status, data):
        response = json.dumps(data).encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)


if __name__ == "__main__":
    import os

    os.chdir(BASE_DIR)

    server = HTTPServer(("localhost", 8000), Handler)

    print("Server running at http://localhost:8000")
    server.serve_forever()