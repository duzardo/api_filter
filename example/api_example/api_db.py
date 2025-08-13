# -*- coding: utf-8 -*-
from psycopg2 import connect
from configparser import ConfigParser
from datetime import datetime


class APIdb:
    def __init__(self):
        config = ConfigParser()
        config.read(r"/etc/api_v8/conn_api.ini")
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

    def checkIfDeviceIsCapable(self, device_id):
        with self.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT NOW()-n.last_job > CAST(CONCAT('00:', ac.config) AS TIME) AS is_true
                FROM numeros n, grupo_numero gn, api_configs ac
                WHERE n.grupo_numero_id = gn.id
                AND gn.tipo_grupo = ac.var_name
                AND n.id = {device_id}
            """
            )
            send_type = cursor.fetchone()[0]
        cursor.close()
        self.close()
        return "1" if send_type else "0"

    def getOnlyReaderBot(self, device_id):
        with self.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT gn.server_gw
                FROM numeros n, grupo_numero gn
                WHERE n.grupo_numero_id = gn.id
                AND n.id = {device_id}
            """
            )
            send_type = cursor.fetchone()[0]
        cursor.close()
        self.close()
        return str(send_type)

    def getQuantMessages(self, campanha_item_id):
        with self.cursor() as cursor:
            cursor.execute(
                f"""
            SELECT COUNT(*)
            FROM mensagem
            WHERE campanha_item_id = {campanha_item_id}
            """
            )
            quant = cursor.fetchone()[0]
        cursor.close()
        self.close()
        return quant

    def getChromeDevicesActive(self, server, slots, id_not_in):
        if id_not_in:
            query = f"""
                SELECT n.id, n.aparelho,
                    CASE
                        when gn.tipo_grupo IS NULL THEN n.last_job
                        when gn.tipo_grupo IS NOT NULL THEN n.last_job + CONCAT(ac.config, ' ', ac.description)::INTERVAL
                    END
                    AS order_time
                FROM numeros n, grupo_numero gn
                LEFT JOIN api_configs ac ON (
                    ac.var_name = gn.tipo_grupo
                    AND gn.tipo_grupo IS NOT NULL
                )
                WHERE n.grupo_numero_id = gn.id
                AND gn."server" = {server}
                AND n.id NOT IN ({id_not_in})
                AND n.ativo = TRUE
                AND gn.ativo = TRUE
                ORDER BY order_time ASC
                LIMIT {slots}
            """
        else:
            query = f"""
                SELECT n.id, n.aparelho,
                    CASE
                        when gn.tipo_grupo IS NULL THEN n.last_job
                        when gn.tipo_grupo IS NOT NULL THEN n.last_job + CONCAT(ac.config, ' ', ac.description)::INTERVAL
                    END
                    AS order_time
                FROM numeros n, grupo_numero gn
                LEFT JOIN api_configs ac ON (
                    ac.var_name = gn.tipo_grupo
                    AND gn.tipo_grupo IS NOT NULL
                )
                WHERE n.grupo_numero_id = gn.id
                AND gn."server" = {server}
                AND n.ativo = TRUE
                AND gn.ativo = TRUE
                ORDER BY order_time ASC
                LIMIT {slots}
            """
        with self.cursor() as cursor:
            cursor.execute(query)
            devices = cursor.fetchall()
        dev = []
        for i in devices:
            dev.append((i[0], i[1]))
        cursor.close()
        self.close()
        return dev

    def openInactiveDevices(self):
        with self.cursor() as cursor:
            cursor.execute(
                f"""
                select config
                from api_configs
                where var_name = 'open_inactive_devices'
            """
            )
            open_inactive_devices = cursor.fetchone()[0]
        cursor.close()
        self.close()
        if open_inactive_devices == 0:
            return "False"
        else:
            return "True"

    def getServerActiveByServer(self, server_nickname):
        with self.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT abre_navegador
                FROM api_servers
                WHERE nickname = '{server_nickname}'
            """
            )
            serv_active = cursor.fetchone()[0]
        cursor.close()
        self.close()
        if serv_active:
            return "True"
        else:
            return "False"

    def updateGreetingTime(self, device_id, last_greeting):
        with self.cursor() as cursor:
            cursor.execute(
                f"""
                UPDATE numeros
                SET last_job_gw = '{last_greeting}'
                WHERE id = {device_id}
            """
            )
        self.conn.commit()
        cursor.close()
        self.close()

    def getLastGreetingTime(self, device_id):
        with self.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT last_job_gw
                FROM numeros
                WHERE id = {device_id}
            """
            )
            last_greeting = cursor.fetchone()[0]
        cursor.close()
        self.close()
        return last_greeting

    def getServerActive(self, device_id):
        with self.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT serv.active
                FROM api_servers serv
                WHERE serv.nickname::INT4 = (
                    SELECT gn."server"
                    FROM numeros n, grupo_numero gn 
                    WHERE n.grupo_numero_id = gn.id 
                    AND n.id = {device_id}
                )
            """
            )
            serv_active = cursor.fetchone()[0]
        cursor.close()
        self.close()
        if serv_active:
            return "True"
        else:
            return "False"

    def getActiveGreetingMessages(self):
        with self.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT message
                FROM api_greeting_messages
                WHERE active = TRUE
            """
            )
            messages = cursor.fetchall()
        cursor.close()
        self.close()
        return messages

    def getAllPhones(self):
        with self.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT n.numero
                FROM numeros n, grupo_numero gn
                WHERE n.grupo_numero_id = gn.id
                AND gn."server" IS NOT NULL
            """
            )
            numbers = cursor.fetchall()
        cursor.close()
        self.close()
        return numbers

    def getSendMessagesNotGreetings(self, device_id):
        with self.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT
                id,
                contact_phone_number,
                message_type,
                message_body,
                message_body_filename,
                message_caption,
                message_custom_id,
                message_body_mimetype,
                schedule,
                check_status
                FROM api_send_messages
                WHERE device_id = {device_id}
                AND sended = FALSE
                AND check_status <> 1
            """
            )
            messages = cursor.fetchall()
        cursor.close()
        self.close()
        return messages

    def getDevicesByVMName(self, nick):
        with self.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT n.aparelho, n.numero, n.ativo, gn.ativo, n.updated_at, n.id
                FROM numeros n, grupo_numero gn
                WHERE n.grupo_numero_id = gn.id
                AND n.navegador = '{nick}'
                AND gn."server" is not null
            """
            )
            devices = cursor.fetchall()
        dev = []
        for i in devices:
            dev.append(
                {
                    "device": i[0],
                    "phone_number": i[1],
                    "device_active": i[2],
                    "group_active": i[3],
                    "modified_at": i[4],
                    "device_id": i[5],
                }
            )
        cursor.close()
        self.close()
        return dev

    def getGreetingMessages(self, device_id):
        with self.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT
                id,
                contact_phone_number,
                message_body
                FROM api_send_messages
                WHERE device_id = {device_id}
                AND check_status = 1
                AND sended = FALSE
            """
            )
            messages = cursor.fetchall()
        cursor.close()
        self.close()
        return messages

    def getGreetingNumber(self, device_id):
        with self.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT num_saudacao
                FROM numeros
                WHERE id = {device_id}
            """
            )
            greeting_number = cursor.fetchone()
        cursor.close()
        self.close()
        return greeting_number[0]

    def getRandomGreetingNum(self, device_id):
        with self.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT n.numero
                FROM numeros n, grupo_numero gn
                WHERE n.id <> {device_id}
                AND gn.id = n.grupo_numero_id
                AND gn."server" IS NOT NULL
                ORDER BY RANDOM()
                LIMIT 1
            """
            )
            greeting_number = cursor.fetchone()
        cursor.close()
        self.close()
        return greeting_number[0]

    def setGreetingNumber(self, device_id, greeting_number):
        with self.cursor() as cursor:
            cursor.execute(
                f"""
                UPDATE numeros
                SET num_saudacao = {greeting_number}
                WHERE id = {device_id}
            """
            )
        self.conn.commit()
        cursor.close()
        self.close()

    def getGreetingNumberTwo(self, device_id, vgroup_id):
        with self.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT numero
                FROM numeros n
                WHERE id <> {device_id}
                AND vgroup_id = {vgroup_id}
            """
            )
            greeting_number = cursor.fetchall()
        cursor.close()
        self.close()
        if greeting_number:
            return greeting_number
        else:
            return False

    def getGreetingNumberOne(self, device_id, group_id):
        with self.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT n.numero
                FROM numeros n, grupo_numero gn
                WHERE n.id <> {device_id}
                AND n.grupo_numero_id = gn.id
                AND n.grupo_numero_id = {group_id}
            """
            )
            greeting_number = cursor.fetchall()
        cursor.close()
        self.close()
        if greeting_number:
            return greeting_number
        else:
            return False

    def getGreetingConfigs(self, device_id):
        with self.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT gn.id, gn.opcao_grupo, n.vgroup_id, n.num_saudacao
                FROM numeros n , grupo_numero gn
                WHERE n.grupo_numero_id = gn.id
                AND n.id = {device_id}
            """
            )
            greeting = cursor.fetchall()
        cursor.close()
        self.close()
        return greeting

    def getDeviceServer(self, device_id):
        with self.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT gn."server" 
                FROM numeros n, grupo_numero gn 
                WHERE n.grupo_numero_id = gn.id 
                AND n.id = {device_id}
            """
            )
            server = cursor.fetchone()
        cursor.close()
        self.close()
        if server:
            return str(server[0])
        else:
            return ""

    def setQRCode(self, device_id, qr_code):
        status = "TRUE" if qr_code else "FALSE"
        with self.cursor() as cursor:
            cursor.execute(
                f"""
                UPDATE numeros
                SET status = {status}
                WHERE id = {device_id}
            """
            )
        self.conn.commit()
        cursor.close()
        self.close()

    def insertMonitor(self, contact_phone_number, photo, status, tick):
        with self.cursor() as cursor:
            cursor.execute(
                f"SELECT photo, status, tick FROM api_monitor WHERE contact_phone_number = '{contact_phone_number}' ORDER BY id DESC LIMIT 1"
            )
            res = cursor.fetchone()
            if res:
                if (str(res[0]), str(res[1]), str(res[2])) != (photo, status, tick):
                    cursor.execute(
                        f"""
                        INSERT INTO api_monitor (contact_phone_number, photo, status, tick)
                        VALUES ('{contact_phone_number}', {photo}, {status}, {tick})
                    """
                    )
                    self.conn.commit()
            else:
                cursor.execute(
                    f"""
                    INSERT INTO api_monitor (contact_phone_number, photo, status, tick)
                    VALUES ('{contact_phone_number}', {photo}, {status}, {tick})
                """
                )
                self.conn.commit()
        cursor.close()
        self.close()

    def getGreeting(self, device_id, contact_phone_number, sended_at):
        with self.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT id
                FROM api_greetings
                WHERE device_id = {device_id}
                AND contact_phone_number = '{contact_phone_number}'
                AND sended_at >= '{sended_at}'
            """
            )
            greeting = cursor.fetchone()[0]
        cursor.close()
        self.close()
        if greeting:
            return True
        else:
            return False

    def insertGreeting(self, device_id, contact_phone_number):
        with self.cursor() as cursor:
            cursor.execute(
                f"""
                INSERT INTO api_greetings (device_id, contact_phone_number)
                VALUES ({device_id}, '{contact_phone_number}')
            """
            )
        self.conn.commit()
        cursor.close()
        self.close()

    def setDeviceIP(self, device_id, device_ip):
        with self.cursor() as cursor:
            cursor.execute(
                f"""
                UPDATE numeros
                SET navegador = '{device_ip}'
                WHERE id = {device_id}
            """
            )
        self.conn.commit()
        cursor.close()
        self.close()

    def getDeviceIP(self, device_id):
        with self.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT navegador
                FROM numeros
                WHERE id = {device_id}
            """
            )
            ip = cursor.fetchone()[0]
        cursor.close()
        self.close()
        return ip

    def getConfig(self, config_id):
        with self.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT config
                FROM api_configs
                WHERE id = {config_id}
            """
            )
            config = cursor.fetchone()[0]
        cursor.close()
        self.close()
        return config

    def getPhones2Prank(self, group_id, device_id):
        with self.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT numero
                FROM numeros
                WHERE grupo_numero_id = {group_id}
                AND id != {device_id}
            """
            )
            phones = cursor.fetchall()
        cln_phones = []
        for i in phones:
            cln_phones.append(i[0])
        cursor.close()
        self.close()
        return cln_phones

    def getGroupByDevice(self, device_id):
        with self.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT grupo_numero_id
                FROM numeros
                WHERE id = {device_id}
            """
            )
            group_id = cursor.fetchone()[0]
        cursor.close()
        self.close()
        return group_id

    def setDeviceFreshing(self, device_id):
        with self.cursor() as cursor:
            cursor.execute(
                f"""
                UPDATE numeros
                SET is_fresh = FALSE
                WHERE id = {device_id}
            """
            )
        self.conn.commit()
        cursor.close()
        self.close()

    def isFreshDevice(self, device_id):
        with self.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT is_fresh
                FROM numeros
                WHERE id = {device_id}
            """
            )
            is_fresh = cursor.fetchone()[0]
        cursor.close()
        self.close()
        if is_fresh:
            return "True"
        else:
            return "False"

    def getEmojiCode(self, emoji_image):
        with self.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT whats_code
                FROM api_emojis
                WHERE emoji_image = '{emoji_image}'
            """
            )
            emoji_code = cursor.fetchone()
        cursor.close()
        self.close()
        return emoji_code[0]

    def postEmojis(self, emoji_code, emoji_image):
        with self.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT emoji_code
                FROM api_emojis
                WHERE emoji_code = '{emoji_code}'
            """
            )
            emoji_ok = cursor.fetchone()
            if emoji_ok is None:
                cursor.execute(
                    f"""
                    INSERT INTO api_emojis (emoji_code, emoji_image)
                    VALUES ('{emoji_code}', '{emoji_image}')
                """
                )
        self.conn.commit()
        cursor.close()
        self.close()

    def updateContactPhoneNumber(self, contact_phone_number, date_hour, isvalid: bool):
        with self.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT numero
                FROM numeros_validos
                WHERE numero = '{contact_phone_number}'
            """
            )
            numbers = cursor.fetchone()
            if isvalid:
                if numbers is None:
                    cursor.execute(
                        f"""
                        INSERT INTO numeros_validos (numero, numero_existe, update_at, checked_at)
                        VALUES ('{contact_phone_number}', TRUE, '{date_hour}', '{date_hour}')
                    """
                    )
                else:
                    cursor.execute(
                        f"""
                        UPDATE numeros_validos
                        SET update_at = '{date_hour}', numero_existe = TRUE
                        WHERE numero = '{contact_phone_number}'
                    """
                    )
            else:
                if numbers is None:
                    cursor.execute(
                        f"""
                        INSERT INTO numeros_validos (numero, numero_existe, update_at, checked_at)
                        VALUES ('{contact_phone_number}', FALSE, '{date_hour}', '{date_hour}')
                    """
                    )
                else:
                    cursor.execute(
                        f"""
                        UPDATE numeros_validos
                        SET update_at = '{date_hour}', numero_existe = FALSE
                        WHERE numero = '{contact_phone_number}'
                    """
                    )
        self.conn.commit()
        cursor.close()
        self.close()

    def unregisterServer(self, nick, at):
        with self.cursor() as cursor:
            cursor.execute(
                f"""
                UPDATE api_servers
                SET active = FALSE, registered = FALSE, unregistered_at = '{at}'
                WHERE nickname = '{nick}'
            """
            )
        self.conn.commit()
        cursor.close()
        self.close()

    def changeStatusServer(self, nick, at, status: bool):
        with self.cursor() as cursor:
            if status:
                cursor.execute(
                    f"""
                    UPDATE api_servers
                    SET active = TRUE, modified_at = '{at}'
                    WHERE nickname = '{nick}'
                """
                )
            else:
                cursor.execute(
                    f"""
                    UPDATE api_servers
                    SET active = FALSE, modified_at = '{at}'
                    WHERE nickname = '{nick}'
                """
                )
        self.conn.commit()
        cursor.close()
        self.close()

    def getServers(self):
        with self.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT nickname
                FROM api_servers
                WHERE registered = TRUE
                ORDER BY nickname ASC
            """
            )
            servers = cursor.fetchall()
        server_cleaned = []
        for i in servers:
            server_cleaned.append(i[0])
        cursor.close()
        self.close()
        return server_cleaned

    def getServer(self, nick):
        with self.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT nickname
                FROM api_servers
                WHERE nickname = '{nick}'
                AND registered = TRUE
            """
            )
            server = cursor.fetchone()
        cursor.close()
        self.close()
        return server[0]

    def postNewServer(self, ip, nick, at):
        with self.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO api_servers (ip, nickname, registered_at)
                VALUES (%s, %s, %s)""",
                (ip, nick, at),
            )
        self.conn.commit()
        cursor.close()
        self.close()

    def getDevicesToClean(self, server):
        with self.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT n.aparelho
                FROM numeros n, grupo_numero gn
                WHERE n.grupo_numero_id = gn.id
                AND gn.server = {server}
            """
            )
            devices = cursor.fetchall()
        dev = []
        for i in devices:
            dev.append(i[0])
        cursor.close()
        self.close()
        return dev

    def getChromeDevices(self, server, slots, id_not_in):
        if id_not_in:
            query = f"""
                SELECT n.id, n.aparelho,
                    CASE 
                        when gn.tipo_grupo IS NULL THEN n.last_job
                        when gn.tipo_grupo IS NOT NULL THEN n.last_job + CONCAT(ac.config, ' ', ac.description)::INTERVAL
                    END
                    AS order_time
                FROM numeros n, grupo_numero gn
                LEFT JOIN api_configs ac ON (
                    ac.var_name = gn.tipo_grupo
                    AND gn.tipo_grupo IS NOT NULL
                )
                WHERE n.grupo_numero_id = gn.id
                AND gn."server" = {server}
                AND n.id NOT IN ({id_not_in})
                ORDER BY order_time ASC
                LIMIT {slots}
            """
        else:
            query = f"""
                SELECT n.id, n.aparelho,
                    CASE 
                        when gn.tipo_grupo IS NULL THEN n.last_job
                        when gn.tipo_grupo IS NOT NULL THEN n.last_job + CONCAT(ac.config, ' ', ac.description)::INTERVAL
                    END
                    AS order_time
                FROM numeros n, grupo_numero gn
                LEFT JOIN api_configs ac ON (
                    ac.var_name = gn.tipo_grupo
                    AND gn.tipo_grupo IS NOT NULL
                )
                WHERE n.grupo_numero_id = gn.id
                AND gn."server" = {server}
                ORDER BY order_time ASC
                LIMIT {slots}
            """
        with self.cursor() as cursor:
            cursor.execute(query)
            devices = cursor.fetchall()
        dev = []
        for i in devices:
            dev.append((i[0], i[1]))
        cursor.close()
        self.close()
        return dev

    def getBotDevices(self, server):
        with self.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT n.id, n.aparelho
                FROM numeros n, grupo_numero gn
                WHERE n.grupo_numero_id = gn.id
                AND gn.server = {server}
                ORDER BY n.aparelho ASC
            """
            )
            devices = cursor.fetchall()
        dev = []
        for i in devices:
            dev.append((i[0], i[1]))
        cursor.close()
        self.close()
        return dev

    def getDevicesNGroups(self, nick):
        with self.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT n.aparelho, n.numero, n.ativo, gn.ativo, gn.nome, n.id
                FROM numeros n, grupo_numero gn
                WHERE n.grupo_numero_id = gn.id
                AND gn.server = {nick}
            """
            )
            devices = cursor.fetchall()
        dev = []
        for i in devices:
            dev.append(
                {
                    "device": i[0],
                    "phone_number": i[1],
                    "device_active": i[2],
                    "group_active": i[3],
                    "group_name": i[4],
                    "device_id": i[5],
                }
            )
        cursor.close()
        self.close()
        return dev

    def getDevices(self, nick):
        with self.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT n.aparelho, n.numero, n.ativo, gn.ativo, n.updated_at, n.id
                FROM numeros n, grupo_numero gn
                WHERE n.grupo_numero_id = gn.id
                AND gn.server = {nick}
            """
            )
            devices = cursor.fetchall()
        dev = []
        for i in devices:
            dev.append(
                {
                    "device": i[0],
                    "phone_number": i[1],
                    "device_active": i[2],
                    "group_active": i[3],
                    "modified_at": i[4],
                    "device_id": i[5],
                }
            )
        cursor.close()
        self.close()
        return dev

    def getMessagesOut(self, device_id):
        with self.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT
                message_custom_id,
                contact_phone_number,
                message,
                message_order,
                message_type,
                message_status,
                message_sent_at
                FROM api_return_messages
                WHERE device_id = {device_id}
            """
            )
            messages = cursor.fetchall()
        msg = []
        for i in messages:
            msg.append(
                {
                    "message_custom_id": i[0],
                    "contact_phone_number": i[1],
                    "message": i[2],
                    "message_order": i[3],
                    "message_type": i[4],
                    "message_status": i[5],
                    "message_sent_at": i[6],
                }
            )
        cursor.close()
        self.close()
        return msg

    def getReturnMessagesID(self, device_id, contact):
        with self.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT message_custom_id
                FROM api_return_messages
                WHERE device_id = {device_id}
                AND contact_phone_number = '{contact}'
            """
            )
            ids = cursor.fetchall()
        clean_ids = []
        for id in ids:
            clean_ids.append(id[0])
        cursor.close()
        self.close()
        return clean_ids

    def getLastMessageID(self, device_id, contact, order):
        with self.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT message_custom_id
                FROM api_return_messages
                WHERE device_id = {device_id}
                AND contact_phone_number = '{contact}'
                AND message_order = {order}
            """
            )
            ids = cursor.fetchone()
        cursor.close()
        self.close()
        return ids[0]

    def getLastMessageOrder(self, device_id, contact):
        with self.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT MAX(message_order)
                FROM api_return_messages
                WHERE device_id = {device_id}
                AND contact_phone_number = '{contact}'
            """
            )
            order = cursor.fetchone()
        cursor.close()
        self.close()
        return order[0]

    def getPhoneNumber(self, device_id):
        with self.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT numero
                FROM numeros
                WHERE id = {device_id}
            """
            )
            phone_number = cursor.fetchone()
        cursor.close()
        self.close()
        return phone_number[0]

    def getLastJob(self, device_id):
        with self.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT last_job
                FROM numeros
                WHERE id = {device_id}
            """
            )
            last_job = cursor.fetchone()
        cursor.close()
        self.close()
        return str(last_job[0])

    def getSendMessages(self, device_id):
        greetings = []
        with self.cursor() as cursor:
            cursor.execute(
                """
                SELECT config
                FROM api_configs
                WHERE var_name = 'q_greetings_to_send'
            """
            )
            q_greetings_to_send = cursor.fetchone()[0]
            cursor.execute(
                """
                SELECT telefone
                FROM whitelist
                WHERE ativo = TRUE
            """
            )
            whitelist = cursor.fetchall()
            whitelist = [x[0] for x in whitelist]
            cursor.execute(
                f"""
                SELECT
                    apikey,
                    id,
                    contact_phone_number,
                    message_type,
                    message_body,
                    message_body_filename,
                    message_caption,
                    message_custom_id,
                    message_body_mimetype,
                    schedule,
                    check_status
                FROM api_send_messages
                WHERE device_id = {device_id}
                AND sended = false
                AND check_status = 1;
            """
            )
            greetings = cursor.fetchall()

        cleaned_greetings = []
        for i in greetings:
            if i[2] in whitelist:
                cleaned_greetings.append(i)
            if len(cleaned_greetings) >= q_greetings_to_send:
                break

        if not len(cleaned_greetings) >= q_greetings_to_send:
            with self.cursor() as cursor:
                for i in greetings:
                    cursor.execute(
                        f"""
                        SELECT emp.ddd
                        FROM campanhas c, equipes e, empresas emp
                        WHERE c.equipe_id = e.id
                        AND e.empresa_id = emp.id
                        AND c.id = {i[0]};
                    """
                    )
                    ddd = cursor.fetchone()[0]
                    ddds = ddd.strip().split(",")
                    ddds = [x.strip() for x in ddds]
                    for j in ddds:
                        if j == i[2][2:4]:
                            cleaned_greetings.append(i)
                        if len(cleaned_greetings) >= q_greetings_to_send:
                            break
                    if len(cleaned_greetings) >= q_greetings_to_send:
                        break

        selected_greetings = []
        never_sended_phones = []
        ordened_sended_phones = []
        if cleaned_greetings:
            for i in cleaned_greetings:
                selected_greetings.append(i[1:])
                if len(selected_greetings) >= q_greetings_to_send:
                    break

        if not len(selected_greetings) >= q_greetings_to_send:
            less_sended_numbers_hist = []
            formatted_date = datetime.now().strftime("%Y-%m-%d")

            with self.cursor() as cursor:
                cursor.execute(
                    f"""
                    select telefone, count(*) as q_sended
                    from campanha_items_hist
                    where telefone in (
                        select telefone
                        from campanha_items
                        where campanha_id in (
                            select id
                            from campanhas
                            where created_at between '{formatted_date} 00:00:00' and '{formatted_date} 22:00:00'
                        )
                        and numero_id = {device_id}
                    )
                    group by telefone
                    order by q_sended
                """
                )
                less_sended_numbers_hist = cursor.fetchall()

            if less_sended_numbers_hist:
                less_sended_numbers = [x[0] for x in less_sended_numbers_hist]

                if greetings:
                    for i in greetings:
                        if i[2] not in less_sended_numbers:
                            never_sended_phones.append(i[1:])

                ordened_phone_greeting = [x[2] for x in greetings]

                for i in less_sended_numbers:
                    idx = 0
                    for j in ordened_phone_greeting:
                        if i == j:
                            ordened_sended_phones.append(greetings[idx][1:])
                        idx += 1

            print(ordened_sended_phones)

        selected_greetings = (
            selected_greetings + never_sended_phones + ordened_sended_phones
        )

        if not len(selected_greetings) >= q_greetings_to_send:
            for i in greetings:
                selected_greetings.append(i[1:])
                if len(selected_greetings) >= q_greetings_to_send:
                    break

        with self.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT
                    id,
                    contact_phone_number,
                    message_type,
                    message_body,
                    message_body_filename,
                    message_caption,
                    message_custom_id,
                    message_body_mimetype,
                    schedule,
                    check_status
                FROM api_send_messages
                WHERE device_id = {device_id}
                AND sended = false
                AND check_status not in (1,50);
            """
            )
            other_messages_to_send = cursor.fetchall()

        messages = selected_greetings + other_messages_to_send
        cursor.close()
        self.close()
        return messages

    def getPrankMessages(self, device_id):
        with self.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT
                id,
                contact_phone_number,
                message_type,
                message_body,
                message_body_filename,
                message_caption,
                message_custom_id,
                message_body_mimetype,
                schedule,
                check_status
                FROM api_send_messages
                WHERE device_id = {device_id}
                AND sended = FALSE
                AND check_status IS NULL
                AND "event" = 'message'
            """
            )
            messages = cursor.fetchall()
        cursor.close()
        self.close()
        return messages

    def updateJob(self, device_id, last_job):
        with self.cursor() as cursor:
            cursor.execute(
                f"""
                UPDATE numeros
                SET last_job = '{last_job}'
                WHERE id = {device_id}
            """
            )
        self.conn.commit()
        cursor.close()
        self.close()

    def updateSendMessage(self, id, sended_at):
        with self.cursor() as cursor:
            cursor.execute(
                f"""
                UPDATE api_send_messages
                SET sended = TRUE, sended_at = '{sended_at}'
                WHERE id = {id}
            """
            )
        self.conn.commit()
        cursor.close()
        self.close()

    def updateReturnMessage(self, id, returned_at):
        with self.cursor() as cursor:
            cursor.execute(
                f"""
                UPDATE api_return_messages
                SET returned = TRUE, returned_at = '{returned_at}'
                WHERE message_custom_id = '{id}'
            """
            )
        self.conn.commit()
        cursor.close()
        self.close()

    def getMessagesToReturn(self, device_id):
        with self.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT
                phone_number,
                contact_phone_number,
                message_custom_id,
                message_type,
                message_body,
                check_status,
                message_schedule,
                message_to_group,
                message_body_extension,
                message_body_mimetype,
                message_body_filename,
                message_caption,
                download,
                event
                FROM api_return_messages
                WHERE device_id = {device_id}
                AND returned = FALSE
            """
            )
            messages = cursor.fetchall()
        cleaned_messages = []
        for i in messages:
            cleaned_messages.append(
                {
                    "phone_number": i[0],
                    "contact_phone_number": i[1],
                    "message_custom_id": i[2],
                    "message_type": i[3],
                    "message_body": i[4],
                    "check_status": i[5],
                    "message_schedule": i[6],
                    "message_to_group": i[7],
                    "message_body_extension": i[8],
                    "message_body_mimetype": i[9],
                    "message_body_filename": i[10],
                    "message_caption": i[11],
                    "download": i[12],
                    "event": i[13],
                }
            )
        cursor.close()
        self.close()
        return cleaned_messages

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

    def insertSendMessages(self, message_dict):
        try:
            with self.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO api_send_messages (
                        apikey,
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
                        message_caption,
                        download,
                        event
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
