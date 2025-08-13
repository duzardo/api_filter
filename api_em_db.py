from psycopg2 import connect
from configparser import ConfigParser
from datetime import datetime

class APIdb:
    def __init__(self):
        config = ConfigParser()
        config.read(r'/etc/api_em/conn_api.ini')
        self.conn = connect(
            host = config['db']['host'],
            port = config['db']['port'],
            database = config['db']['database'],
            user = config['Auth']['user'],
            password = config['Auth']['password']
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
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    device_id,
                    contact_phone_number,
                    message_custom_id,
                    message_order,
                    message_schedule,
                ),
            )
        self.conn.commit()
        cursor.close()
        self.close()

    def insertSendMessages(self, message_dict):
        try:
            with self.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO api_send_messages (
                        device_id,
                        contact_phone_number,
                        message_custom_id,
                        message_type,
                        message_body,
                        check_status,
                        schedule,
                        message_to_group,
                        message_body_extension,
                        message_body_mimetype,
                        message_body_filename,
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        message_dict["apikey"],
                        message_dict["device_id"],
                        message_dict["contact_phone_number"],
                        message_dict["message_custom_id"],
                        message_dict["message_type"],
                        message_dict["message_body"],
                        message_dict["check_status"],
                        message_dict["schedule"],
                        message_dict["message_to_group"],
                        message_dict["message_body_extension"],
                        message_dict["message_body_mimetype"],
                        message_dict["message_body_filename"],
                        message_dict["message_caption"],
                        message_dict["download"],
                        message_dict["event"],
                    ),
                )
            self.conn.commit()
            cursor.close()
            self.close()
            return True
        except:
            return False



