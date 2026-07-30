import sqlite3

from config.settings import DATABASE_PATH


class Database:

    def __init__(self):

        self.connection = sqlite3.connect(DATABASE_PATH)

        self.create_tables()

    def create_tables(self):

        cursor = self.connection.cursor()

        cursor.execute("""

        CREATE TABLE IF NOT EXISTS jobs(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            filename TEXT,

            status TEXT,

            progress INTEGER,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )

        """)

        self.connection.commit()

    def create_job(self, filename):

        cursor = self.connection.cursor()

        cursor.execute(

            """

            INSERT INTO jobs(

                filename,

                status,

                progress

            )

            VALUES(

                ?,?,?

            )

            """,

            (

                filename,

                "Created",

                0

            )

        )

        self.connection.commit()

        return cursor.lastrowid

    def update_progress(

        self,

        job_id,

        status,

        progress

    ):

        cursor = self.connection.cursor()

        cursor.execute(

            """

            UPDATE jobs

            SET

                status=?,

                progress=?

            WHERE id=?

            """,

            (

                status,

                progress,

                job_id

            )

        )

        self.connection.commit()