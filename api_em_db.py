from psycopg2 import connect
from configparser import ConfigParser
from datetime import datetime


class APIdb:
    def __init__(self):
        config = ConfigParser()
        config.read(r"/etc/api_em/conn_api.ini")
        self.conn = connect(
            host=config["db"]["host"],
            port=config["db"]["port"],
            database=config["db"]["database"],
            user=config["Auth"]["user"],
            password=config["Auth"]["password"],
        )

    def cursor(self):
        return self.conn.cursor()

    def close(self):
        self.conn.close()

    def insertReturnMessages(
        self,
        device_id,
        contact_phone_number,
        message_custom_id,
        message_order,
        message_schedule,
        readed_at_schedule,
        returned,
        returned_at,
    ):
        with self.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO api_return_messages (
                    device_id,
                    contact_phone_number,
                    message_custom_id,
                    message_order,
                    message_schedule,
                    readed_at_schedule,
                    returned,
                    returned_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    device_id,
                    contact_phone_number,
                    message_custom_id,
                    message_order,
                    message_schedule,
                    readed_at_schedule,
                    returned,
                    returned_at,
                ),
            )
        self.conn.commit()
        cursor.close()
        self.close()
