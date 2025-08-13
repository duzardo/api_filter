# -*- coding: utf-8 -*-
from psycopg2 import connect
from configparser import ConfigParser


class CreateDB:
    def __init__(self):
        self.conn = self.connDB()

    def connDB(self):
        config = ConfigParser()
        config.read(r"/etc/api_v8/conn_api.ini")
        return connect(
            host=config["db"]["host"],
            port=config["db"]["port"],
            database=config["db"]["database"],
            user=config["Auth"]["user"],
            password=config["Auth"]["password"],
        )

    def cursor(self):
        return self.conn.cursor()

    def createSendGreetingsTable(self):
        if self.conn.closed:
            self.conn = self.connDB()
        with self.cursor() as cursor:
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS api_greetings (
                    id serial PRIMARY KEY,
                    device_id INT8 NOT NULL,
                    contact_phone_number VARCHAR(13) NOT NULL,
                    sended BOOLEAN DEFAULT FALSE NOT NULL,
                    sended_at TIMESTAMP(0) WITHOUT TIME ZONE,
                    FOREIGN KEY (device_id) REFERENCES numeros(id) ON DELETE RESTRICT ON UPDATE CASCADE
                );"""
            )
        self.conn.commit()
        cursor.close()

    def createSendMessagesTable(self):
        if self.conn.closed:
            self.conn = self.connDB()
        with self.cursor() as cursor:
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS api_teste_loco (
                    id serial PRIMARY KEY,
                    device_id INT8 NOT NULL,
                    apikey VARCHAR(36) DEFAULT NULL,
                    contact_phone_number VARCHAR(13) NOT NULL,
                    message_custom_id VARCHAR(36) DEFAULT NULL,
                    message_type VARCHAR(11) DEFAULT 'text' NOT NULL,
                    message_body TEXT NOT NULL,
                    check_status SMALLINT DEFAULT NULL,
                    schedule TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
                    message_to_group BOOLEAN DEFAULT FALSE,
                    message_body_extension VARCHAR(8) DEFAULT NULL,
                    message_body_mimetype TEXT DEFAULT NULL,
                    message_body_filename TEXT DEFAULT NULL,
                    message_caption TEXT DEFAULT NULL,
                    download BOOLEAN DEFAULT FALSE,
                    event VARCHAR(36) DEFAULT 'message',
                    sended BOOLEAN DEFAULT FALSE NOT NULL,
                    sended_at TIMESTAMP(0) WITHOUT TIME ZONE,
                    FOREIGN KEY (device_id) REFERENCES numeros(id) ON DELETE RESTRICT ON UPDATE CASCADE
                );"""
            )
        self.conn.commit()
        cursor.close()

    def createReturnMessagesTable(self):
        if self.conn.closed:
            self.conn = self.connDB()
        with self.cursor() as cursor:
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS api_return_messages (
                    id serial PRIMARY KEY,
                    device_id INT8 NOT NULL,
                    contact_phone_number VARCHAR(13) NOT NULL,
                    message_custom_id VARCHAR(36) DEFAULT NULL,
                    message_order SMALLINT NOT NULL,
                    message_type VARCHAR(11) DEFAULT 'text' NOT NULL,
                    check_status SMALLINT DEFAULT NULL,
                    message_schedule TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
                    readed_at_schedule TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
                    event VARCHAR(36) DEFAULT 'message',
                    returned BOOLEAN DEFAULT FALSE NOT NULL,
                    returned_at TIMESTAMP(0) WITHOUT TIME ZONE,
                    FOREIGN KEY (device_id) REFERENCES numeros(id) ON DELETE RESTRICT ON UPDATE CASCADE
                )"""
            )
        self.conn.commit()
        cursor.close()

    def createServersTable(self):
        if self.conn.closed:
            self.conn = self.connDB()
        with self.cursor() as cursor:
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS api_servers (
                    id serial PRIMARY KEY,
                    ip VARCHAR(15) NOT NULL,
                    nickname VARCHAR(3) NOT NULL,
                    active BOOLEAN DEFAULT FALSE NOT NULL,
                    modified_at TIMESTAMP(0) WITHOUT TIME ZONE,
                    registered BOOLEAN DEFAULT TRUE NOT NULL,
                    registered_at TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
                    unregistered_at TIMESTAMP(0) WITHOUT TIME ZONE
                )"""
            )
        self.conn.commit()
        cursor.close()

    def createValidatorTable(self):
        if self.conn.closed:
            self.conn = self.connDB()
        with self.cursor() as cursor:
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS api_validator (
                    id serial PRIMARY KEY,
                    phone_number VARCHAR(15) NOT NULL,
                    campanha_items_id INT8 NOT NULL,
                    checked BOOLEAN DEFAULT FALSE NOT NULL,
                    checking BOOLEAN DEFAULT FALSE NOT NULL,
                    checked_at TIMESTAMP(0) WITHOUT TIME ZONE
                )"""
            )
        self.conn.commit()
        cursor.close()


insert_tables = CreateDB()
insert_tables.createValidatorTable()
# insert_tables.createSendMessagesTable()
# insert_tables.createReturnMessagesTable()
# insert_tables.createServersTable()

# ALTER TABLE public.api_send_messages ALTER COLUMN id TYPE bigserial USING id::bigserial;
# ALTER TABLE public.api_send_messages ADD device_id int8;
# ALTER TABLE public.api_send_messages ADD CONSTRAINT api_send_messages_device_id FOREIGN KEY (device_id) REFERENCES public.numeros(id) ON DELETE RESTRICT ON UPDATE CASCADE;
