# -*- coding: utf-8 -*-
"""
py -m pip install PyQt5 selenium==4.6.0 flask flask-cors opencv-python pyautogui emoji selenium_stealth requests psycopg2 psutil python-magic python-magic-bin pyinstaller

### NOVO SISTEMA
- LEITURA DE QRCODE

### MELHORIAS
- INICIAR JÁ NO WHATSAPP
- Stealth webdriver in chrome 97

### CORREÇÕES
- Combo de imagens

GoogleChromePortableBeta_97.0.4692.71

https://stackoverflow.com/questions/56528631/is-there-a-version-of-selenium-webdriver-that-is-not-detectable
https://sourceforge.net/projects/portableapps/files/Google%20Chrome%20Portable/
https://bot.sannysoft.com/
"""
from gc import collect as collect_gc, enable as enable_gc
from logging import getLogger, basicConfig, StreamHandler, Formatter, INFO
from os import makedirs, remove, listdir, chmod
from base64 import b64decode, b64encode
from time import sleep, time
from requests import get, post
from re import compile, sub, search
from json import load
from sys import exit
from os.path import isdir, isfile, join
from mimetypes import guess_type
from shutil import copytree
from pyautogui import size
from emoji import emoji_count
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException, ElementClickInterceptedException
from selenium_stealth import stealth
from random import uniform, choice, randint
from bs4 import BeautifulSoup
from typing import Union
from cv2 import (
    COLOR_BGR2GRAY, THRESH_BINARY_INV, THRESH_OTSU, MORPH_RECT,
    MORPH_CLOSE, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE,
    imread, cvtColor, GaussianBlur, threshold, getStructuringElement,
    morphologyEx, findContours, arcLength, approxPolyDP,
    boundingRect, contourArea, rectangle, imwrite
)

class CDACob: #(QObject):
    # is_eternal = pyqtSignal(bool)
    xpaths = load(open("xpaths.json", "r"))
    __waLink = "https://web.whatsapp.com/"
    __sendURL = __waLink + "send?phone="

    def __init__(self, device, port, device_id, driver_number):
        enable_gc()
        self.device = device
        self.port = port
        self.device_id = device_id
        self.driver_number = driver_number
        self.has_greetings = True
        self.greetings = self.setGreetings()
        self.re_inn_html = compile(r"<(.*?)>")
        self.re_emoji = compile(r"\\U[0-9a-fA-F]{8}")
        self.re_contact_number = compile(r"^\+55 \d{2} \d{4,5}-\d{4}$")
        self.re_phone_number = compile(r"^55\d{10,11}$")
        self.filename_list = ['Lorem', 'ipsum', 'dolor', 'sit', 'amet', 'consectetur', 'adipisicing', 'elit', 'Reiciendis', 'molestias', 'eius', 'voluptates', 'amet', 'eligendi', 'sed', 'Eum', 'reprehenderit', 'eos', 'voluptatem', 'placeat', 'magni', 'non', 'nobis,', 'corporis', 'impedit', 'amet', 'animi', 'Aspernatur', 'voluptatum', 'consequuntur', 'et', 'eum', 'eaque,', 'in', 'unde', 'Quo', 'qui', 'at', 'nam', 'sit', 'repudiandae', 'eveniet', 'cupiditate,', 'optio', 'ratione', 'voluptates', 'quam', 'dolor', 'facere', 'provident', 'quas', 'praesentium', 'corrupti', 'pariatur', 'fugiat', 'corporis', 'error', 'ipsum', 'possimus', 'minus', 'iusto', 'animi', 'Quod', 'non', 'nulla', 'corrupti', 'vel', 'sequi', 'minus', 'dolores', 'unde,', 'itaque', 'quibusdam', 'Doloremque', 'aperiam', 'quas', 'sit', 'numquam', 'Dolore', 'perferendis', 'rerum', 'illo,', 'sequi', 'est', 'corrupti', 'reprehenderit', 'adipisci', 'excepturi', 'magnam', 'soluta', 'qui,', 'quasi', 'sed', 'aliquam', 'minima', 'eveniet', 'ex', 'repellendus', 'Cum', 'doloremque', 'blanditiis,', 'et', 'iste', 'nulla', 'minus', 'ducimus', 'fuga', 'dolore', 'voluptatem', 'sit', 'optio', 'ab', 'culpa,', 'repudiandae', 'suscipit', 'neque', 'provident', 'natus', 'Nisi,', 'nostrum', 'recusandae', 'Dolor', 'fugit', 'error', 'tempora', 'quasi', 'accusamus,', 'vel', 'Quod', 'ex', 'alias', 'nisi,', 'officiis', 'porro', 'delectus', 'consequuntur', 'ullam', 'at', 'sed', 'illum', 'impedit', 'debitis,', 'veritatis', 'repellat', 'corrupti', 'placeat', 'dolores', 'molestias,', 'dolor', 'consectetur', 'optio', 'laboriosam', 'blanditiis', 'ut', 'eos', 'dolore', 'Expedita', 'animi', 'soluta', 'voluptas', 'quo', 'dignissimos', 'ipsam', 'unde', 'officiis', 'possimus', 'rem', 'sequi', 'porro', 'repellendus', 'omnis', 'nostrum,', 'amet', 'totam', 'eos', 'iusto', 'Facere', 'quia', 'voluptas,', 'enim', 'explicabo', 'numquam', 'possimus', 'ad', 'incidunt,', 'accusamus', 'mollitia', 'sapiente', 'sunt', 'beatae', 'quo', 'eos', 'ea', 'Voluptates', 'ratione', 'voluptatibus,', 'provident', 'nesciunt', 'esse', 'ipsum', 'placeat', 'dolorum', 'dicta', 'iure,', 'amet,', 'explicabo', 'modi', 'temporibus', 'harum', 'assumenda', 'perspiciatis', 'dolores', 'quo', 'At', 'modi', 'quo', 'explicabo', 'Ipsa', 'perferendis', 'nihil,', 'deleniti', 'animi', 'ex', 'delectus', 'libero', 'adipisci', 'aperiam', 'magni', 'quod', 'quos', 'iusto', 'voluptas', 'odio', 'atque', 'temporibus', 'incidunt', 'quae', 'dicta,', 'et', 'esse', 'Nemo', 'nam', 'quos', 'libero', 'quasi', 'impedit', 'ipsam', 'laudantium,', 'ea,', 'ad', 'incidunt', 'voluptatibus', 'quis,', 'quaerat', 'ex', 'velit', 'adipisci', 'fugit', 'atque', 'fugiat', 'iure', 'itaque', 'Animi,', 'ipsa', 'ex', 'sequi', 'deleniti', 'accusamus,', 'quibusdam', 'fuga', 'eos', 'expedita', 'a', 'tenetur', 'pariatur', 'Tempore', 'magnam,', 'eum', 'provident', 'dignissimos', 'doloremque', 'maxime', 'et', 'rerum', 'ex,', 'tempora', 'in', 'iste', 'temporibus', 'aperiam', 'atque', 'nemo', 'minus', 'perspiciatis', 'similique', 'blanditiis', 'velit', 'hic', 'voluptatibus', 'Necessitatibus', 'beatae,', 'vero', 'fuga', 'deleniti', 'minima', 'distinctio,', 'quod', 'vitae', 'cum', 'nesciunt', 'expedita,', 'neque', 'Ipsa', 'rerum', 'magnam', 'libero', 'soluta', 'eum', 'eveniet', 'voluptatum', 'alias', 'nesciunt,', 'aliquam', 'deleniti', 'aspernatur', 'reiciendis', 'Voluptatibus', 'voluptatum', 'quaerat', 'alias', 'necessitatibus', 'ipsa', 'ratione', 'minus', 'a', 'fugit,', 'illo', 'non', 'Laboriosam', 'enim', 'non', 'voluptates', 'aliquam', 'quo', 'molestiae', 'incidunt,', 'itaque', 'soluta', 'eveniet', 'totam', 'Fugiat', 'dolor', 'expedita', 'commodi', 'laborum', 'illum', 'rerum,', 'consequuntur', 'ipsam,', 'tempore', 'maxime', 'provident', 'deserunt', 'dignissimos', 'Temporibus', 'cupiditate', 'odio', 'recusandae', 'quam,', 'esse,', 'sed', 'ullam', 'rem', 'exercitationem', 'expedita', 'accusamus,', 'sequi', 'quisquam', 'Sed', 'at', 'adipisci', 'assumenda', 'deserunt', 'et', 'facere', 'nam', 'aliquid', 'numquam', 'qui', 'Eligendi', 'quo', 'quia', 'omnis', 'officiis', 'doloribus', 'pariatur', 'enim', 'magni', 'aliquid', 'porro', 'iste', 'officia', 'harum,', 'unde', 'suscipit', 'nesciunt,', 'iusto', 'eaque,', 'dolores', 'praesentium', 'vel', 'Labore', 'quo', 'rerum', 'hic', 'Cumque,', 'vero', 'consectetur', 'Neque,', 'saepe', 'eos', 'esse', 'quis', 'necessitatibus', 'magnam', 'quae', 'cum', 'id', 'voluptates', 'a', 'Quibusdam,', 'Nostrum', 'accusantium', 'sunt', 'nobis', 'Molestias', 'voluptate', 'quidem', 'dolorum', 'alias', 'error', 'Incidunt', 'dolor', 'placeat', 'dolores', 'provident', 'libero', 'quis', 'cupiditate', 'doloremque', 'Mollitia', 'recusandae', 'blanditiis', 'maxime,', 'adipisci', 'rerum', 'sit', 'ducimus', 'debitis', 'ut', 'voluptatibus', 'nostrum', 'obcaecati', 'Aut', 'numquam', 'qui', 'ratione', 'et', 'quae', 'fugiat', 'pariatur,', 'reiciendis', 'praesentium', 'itaque,', 'ipsam', 'non', 'vitae,', 'totam', 'voluptatibus', 'saepe', 'harum', 'aperiam', 'reprehenderit', 'Repudiandae', 'iste', 'ea,', 'repellat', 'quae', 'dolorem', 'vitae', 'Repellat', 'nesciunt', 'sint', 'aperiam', 'rerum', 'praesentium', 'ea', 'commodi', 'saepe', 'libero', 'eveniet', 'alias', 'laborum', 'nihil', 'tenetur', 'consectetur', 'voluptatem', 'optio', 'beatae', 'possimus', 'iste', 'pariatur', 'odit', 'nostrum', 'laboriosam', 'Quisquam', 'adipisci', 'doloremque', 'ex', 'suscipit', 'voluptate', 'sint', 'iusto', 'culpa', 'sequi', 'voluptates', 'similique', 'reiciendis', 'saepe', 'illum', 'a', 'nam', 'omnis', 'soluta', 'exercitationem', 'voluptatem', 'cum', 'totam', 'esse', 'voluptas', 'quos', 'Illo', 'dolore', 'natus', 'iure', 'asperiores', 'deleniti', 'voluptatum', 'voluptas', 'ab', 'beatae', 'vitae', 'numquam', 'ipsa', 'eos', 'quam', 'suscipit', 'velit', 'laborum', 'odio', 'ratione', 'modi', 'ad', 'obcaecati', 'architecto', 'error', 'quas', 'ut', 'Iste', 'distinctio', 'sint', 'qui', 'facilis', 'praesentium', 'quisquam', 'aliquam', 'consequatur', 'in', 'quia', 'non', 'inventore', 'tempora', 'sapiente', 'excepturi', 'libero', 'nemo', 'assumenda', 'aperiam', 'animi', 'Facilis', 'quasi', 'neque', 'totam', 'cumque', 'sequi', 'qui', 'exercitationem', 'Libero', 'veniam', 'ipsa', 'vel', 'quo', 'perspiciatis', 'Laborum', 'ab', 'tempore', 'esse', 'iure', 'reprehenderit', 'rem', 'architecto', 'animi', 'impedit', 'reiciendis', 'porro', 'mollitia', 'necessitatibus', 'pariatur', 'sapiente', 'recusandae', 'omnis', 'exercitationem', 'qui', 'Numquam', 'officia', 'eaque', 'consequuntur', 'nesciunt', 'eum', 'laborum', 'voluptates', 'quo', 'dolorem', 'sint', 'nobis', 'provident', 'et', 'nisi', 'nemo', 'facilis', 'sapiente', 'libero', 'est', 'beatae', 'quisquam', 'porro', 'quis', 'praesentium', 'ipsum', 'nostrum', 'earum', 'voluptatibus', 'Praesentium', 'similique', 'libero', 'velit', 'enim', 'tenetur', 'deleniti', 'officia', 'nulla', 'distinctio', 'veritatis', 'blanditiis', 'ad', 'facilis', 'impedit', 'sed', 'nobis', 'delectus', 'voluptatem', 'amet', 'eligendi', 'mollitia', 'Reprehenderit', 'consequuntur', 'distinctio', 'nihil', 'Optio', 'nesciunt', 'nisi', 'quo', 'perferendis', 'dolor', 'similique', 'autem', 'minima', 'laborum', 'asperiores', 'sed', 'earum', 'modi', 'sunt', 'blanditiis', 'debitis', 'eligendi', 'corporis', 'consectetur', 'quis', 'rerum', 'Magnam', 'voluptatum', 'voluptate', 'minima', 'rerum', 'itaque', 'laudantium', 'cupiditate', 'nesciunt', 'dignissimos', 'cum', 'obcaecati', 'autem', 'corporis', 'neque', 'Distinctio', 'iusto', 'quidem', 'hic', 'ab', 'sapiente', 'fugiat', 'voluptatem', 'odio', 'dignissimos', 'repudiandae', 'numquam', 'quas', 'ullam', 'sit', 'tenetur', 'velit', 'alias', 'praesentium', 'culpa', 'exercitationem', 'veritatis', 'aliquam', 'Amet', 'odio', 'possimus', 'harum', 'quisquam', 'numquam', 'est', 'nostrum', 'magnam', 'voluptatem', 'quidem', 'exercitationem', 'doloribus', 'porro', 'ad', 'soluta', 'nam', 'Qui', 'repellat', 'itaque', 'commodi', 'nostrum', 'expedita', 'temporibus', 'optio', 'facere', 'voluptatem', 'Laboriosam', 'est', 'nisi', 'vero', 'aliquid', 'minus', 'possimus', 'similique', 'iusto', 'optio', 'reprehenderit', 'doloremque', 'ex', 'molestias', 'quam', 'eos', 'ducimus', 'provident', 'corrupti', 'id', 'reiciendis', 'numquam', 'Impedit', 'repudiandae', 'dolor', 'harum', 'Saepe', 'cum', 'et', 'odit', 'molestiae', 'debitis', 'tempore', 'eius', 'non', 'facilis', 'fugiat', 'hic', 'ipsa', 'explicabo', 'commodi', 'nulla', 'quaerat', 'dicta', 'earum', 'tenetur', 'Cum', 'eligendi', 'obcaecati', 'harum', 'consequatur', 'laborum', 'esse', 'praesentium', 'mollitia', 'impedit', 'autem', 'at', 'temporibus', 'ut', 'earum', 'recusandae', 'odit', 'repellendus', 'architecto', 'aperiam', 'alias', 'quibusdam', 'quos', 'natus', 'tempore', 'Ab', 'quidem', 'excepturi', 'itaque', 'labore', 'iste', 'dolores', 'alias', 'voluptas', 'Aspernatur', 'quis', 'nobis', 'beatae', 'quaerat', 'quisquam', 'a', 'architecto', 'necessitatibus', 'sapiente', 'iure', 'ex', 'voluptas', 'veniam', 'aut', 'dolorem', 'dolore', 'nisi', 'fugit', 'laudantium', 'molestiae', 'dolor', 'tempore', 'reiciendis', 'porro', 'assumenda', 'totam', 'ipsa', 'officia', 'Accusamus', 'rerum', 'porro', 'perferendis', 'nihil', 'corrupti', 'nam', 'veniam', 'harum', 'Aliquid', 'quibusdam', 'saepe', 'vitae', 'obcaecati', 'Incidunt', 'a', 'accusamus', 'distinctio', 'velit', 'iste', 'beatae', 'amet', 'vero', 'aspernatur', 'obcaecati', 'unde', 'odit', 'consectetur', 'vitae', 'nostrum', 'quaerat', 'quibusdam', 'odio', 'cupiditate', 'rem', 'repellendus', 'Reiciendis', 'praesentium', 'quidem', 'fugit', 'similique', 'minima', 'adipisci', 'corporis', 'rerum', 'veniam', 'laudantium', 'nam', 'exercitationem', 'cupiditate', 'architecto', 'possimus', 'et', 'doloribus', 'Ducimus', 'sed', 'blanditiis', 'doloribus', 'porro', 'Dolor', 'doloribus', 'ex', 'laborum', 'alias', 'incidunt', 'nesciunt', 'repellendus', 'voluptate', 'saepe', 'reprehenderit', 'hic', 'molestiae', 'doloremque', 'nam', 'Autem', 'consequatur', 'porro', 'ad', 'maxime', 'officia', 'ea', 'cum', 'facilis', 'distinctio', 'voluptate', 'possimus', 'corrupti', 'aperiam', 'suscipit', 'vitae', 'animi', 'eum', 'quod', 'odio', 'blanditiis', 'numquam', 'qui', 'amet', 'assumenda', 'quaerat', 'Amet', 'recusandae', 'ratione', 'error', 'vitae', 'expedita', 'dolores', 'rem', 'cupiditate', 'dignissimos', 'laudantium', 'voluptates', 'impedit', 'eaque', 'velit', 'consequuntur', 'maiores', 'cumque', 'non', 'ipsam', 'minima', 'fugit', 'similique', 'totam', 'ducimus', 'Porro', 'dolorum', 'nostrum', 'Beatae', 'quasi', 'porro', 'eligendi', 'nam', 'Tempora', 'sed', 'alias', 'sint', 'cupiditate', 'vero', 'enim', 'ipsam', 'labore', 'eaque', 'animi', 'optio', 'ratione', 'assumenda', 'veritatis', 'voluptatum', 'voluptas', 'ipsum', 'corrupti', 'aliquid', 'in', 'maxime', 'Vitae', 'saepe', 'Numquam', 'obcaecati', 'pariatur', 'perferendis', 'rerum', 'veniam', 'harum', 'distinctio', 'Temporibus', 'natus', 'dolor', 'consequatur', 'odio', 'eaque', 'distinctio', 'ullam', 'illum', 'vero', 'dolorem', 'reiciendis', 'magnam', 'dicta', 'numquam', 'amet', 'cum', 'iste', 'nulla', 'earum', 'Architecto', 'officia', 'porro', 'sit', 'quaerat', 'maxime', 'sunt', 'consequuntur', 'sapiente', 'magnam', 'veritatis', 'dolore', 'nobis', 'tenetur', 'iste', 'sequi', 'Voluptatum', 'debitis', 'adipisci', 'minus', 'sapiente', 'aliquid', 'sunt', 'tempore', 'in', 'repudiandae', 'harum', 'est', 'totam', 'deleniti', 'recusandae', 'repellat', 'perferendis', 'obcaecati', 'Consequatur', 'magnam', 'pariatur', 'numquam', 'qui', 'voluptates', 'expedita', 'eveniet', 'possimus', 'aliquam', 'architecto', 'autem', 'praesentium', 'quam', 'eius', 'ad', 'dolor', 'incidunt', 'ducimus', 'vero', 'cum', 'Quos', 'cum', 'incidunt', 'Doloremque', 'quaerat', 'neque', 'odio', 'a', 'iste', 'doloribus', 'minus', 'fugiat', 'voluptates', 'tenetur', 'praesentium', 'asperiores', 'rerum', 'optio', 'saepe', 'enim', 'qui', 'rem', 'accusamus', 'exercitationem', 'sed', 'ea', 'in', 'dolorem', 'quis', 'magni', 'veritatis', 'Non', 'facere', 'optio', 'quam', 'ratione', 'explicabo', 'unde', 'debitis', 'possimus', 'molestias', 'dolor', 'corrupti', 'tempora', 'cumque', 'error', 'alias', 'perferendis', 'nihil', 'ipsa', 'laborum', 'eum', 'voluptate', 'Perferendis', 'ullam', 'explicabo', 'nemo', 'sunt', 'odio', 'nostrum', 'aperiam', 'enim', 'consectetur', 'expedita', 'delectus', 'inventore', 'Saepe', 'quae', 'maiores', 'molestiae', 'aspernatur', 'distinctio', 'temporibus', 'repellendus', 'maxime', 'quod', 'autem', 'ullam', 'quasi', 'quisquam', 'Similique', 'in', 'quidem', 'dolore', 'tempore', 'hic', 'exercitationem', 'suscipit', 'sit', 'soluta', 'aut', 'nobis', 'Iusto', 'debitis', 'Sapiente', 'ullam', 'consequatur', 'placeat', 'inventore', 'voluptate', 'hic', 'eos', 'nobis', 'vitae', 'debitis', 'facere', 'id', 'rem', 'vero', 'laboriosam', 'iure', 'quod', 'sit', 'temporibus', 'adipisci', 'Obcaecati', 'debitis', 'minima', 'optio', 'itaque', 'harum', 'quae', 'suscipit', 'vitae', 'sapiente', 'quas', 'qui', 'temporibus', 'nam', 'Laboriosam', 'ipsa', 'consectetur', 'repudiandae', 'pariatur', 'officia', 'Similique', 'qui', 'velit', 'molestiae', 'cumque', 'quae', 'labore', 'Quibusdam', 'aliquid', 'quae', 'veniam', 'autem', 'nulla', 'deserunt', 'laborum', 'minima', 'cupiditate', 'blanditiis', 'obcaecati', 'error', 'accusamus', 'aspernatur', 'nam', 'molestiae', 'iste', 'dolorem', 'assumenda', 'odit', 'nemo', 'velit', 'quia', 'veritatis', 'reiciendis', 'delectus', 'voluptatibus', 'Commodi', 'id', 'necessitatibus', 'optio', 'qui', 'nesciunt', 'eius', 'porro', 'eaque', 'nihil', 'similique', 'a', 'quos', 'itaque', 'iure', 'molestias', 'Neque', 'dolore', 'dignissimos', 'explicabo', 'adipisci', 'repudiandae', 'nesciunt', 'error', 'ipsam', 'unde', 'accusamus', 'sed', 'distinctio', 'dolor', 'labore', 'harum', 'eum', 'Dolorem', 'eligendi', 'odio', 'amet', 'earum', 'Dignissimos', 'temporibus', 'perspiciatis', 'molestiae', 'in', 'recusandae', 'assumenda', 'rerum', 'laborum', 'architecto', 'voluptatum', 'qui', 'reiciendis', 'neque', 'veritatis', 'praesentium', 'Cumque', 'neque', 'tempore', 'itaque', 'voluptatibus', 'possimus', 'nam', 'distinctio', 'voluptate', 'eos', 'vel', 'quae', 'commodi', 'a', 'incidunt', 'beatae', 'placeat', 'soluta', 'pariatur', 'molestiae', 'dignissimos', 'magnam', 'architecto', 'molestias', 'Vero', 'quod', 'ipsa', 'eligendi', 'corrupti', 'maiores', 'repellendus', 'consequuntur', 'doloremque', 'expedita', 'itaque', 'repudiandae', 'et', 'possimus', 'quia', 'ex', 'perspiciatis', 'facere', 'unde', 'aspernatur', 'quos', 'quae', 'molestias', 'Similique', 'nobis', 'fugit', 'quaerat', 'commodi', 'autem', 'quisquam', 'maxime', 'minima', 'dolorem', 'nulla', 'possimus', 'magni', 'magnam', 'reiciendis', 'distinctio', 'vitae', 'repellendus', 'explicabo', 'ratione', 'odit', 'ipsam', 'labore', 'mollitia', 'illo', 'facere', 'ducimus', 'Quibusdam', 'fuga', 'temporibus', 'qui', 'id', 'officia', 'quidem', 'optio', 'eveniet', 'ad', 'fugiat', 'itaque', 'delectus', 'nisi', 'vitae', 'ullam', 'quisquam', 'quam', 'deserunt', 'veritatis', 'similique', 'libero', 'dolorum', 'iure', 'laborum', 'nesciunt', 'Officia', 'atque', 'quam', 'unde', 'maiores', 'aliquam', 'assumenda', 'distinctio', 'nostrum', 'repellat', 'ut', 'sint', 'nesciunt', 'libero', 'aut', 'est', 'quisquam', 'eaque', 'earum', 'maxime', 'consequuntur', 'delectus', 'praesentium', 'doloribus', 'optio', 'Illo', 'recusandae', 'aspernatur', 'atque', 'similique', 'voluptates', 'modi', 'unde', 'voluptatem', 'fuga', 'dignissimos', 'ducimus', 'quod', 'doloribus', 'facere', 'qui', 'consectetur', 'dicta', 'Molestias']
        self.point_greeting = ['α', 'β', 'γ', 'δ', 'ε', 'ζ', 'η', 'θ', 'ι', 'κ', 'λ', 'μ', 'ν', 'ξ', 'ο', 'π', 'ρ', 'σ', 'ς', 'τ', 'υ', 'φ', 'χ', 'ω']
        # self.re_phone_number_plus = compile(r"^\+55\d{1'0',11}$")
        self.logs_path = self.xpaths["path"] + device + "\logs\\"
        self.downloads_path = self.xpaths["path"] + device + "\downloads\\"
        self.qrcode_path = self.xpaths["path"] + device + "\qrcode\\"
        self.binary_path = self.xpaths["path"] + device + "\chrome\\"
        self.down_of_screen = size()[1]
        self.middle_of_screen = self.down_of_screen/2
        self.day_flag = ""
        self.last_contact = ""
        self.greeting_number = ""
        self.crashed_returns = []
        self.createPath()
        self.log = self.logger(self.device)
        self.driver = self.runChromeDriver()
        self.postDriverArguments()
        self.ac = ActionChains(self.driver)
        self.sincronizeWhatsApp()
        self.setStatusDevice(True)
        self.ac.send_keys(Keys.ESCAPE).perform()
        self.postQRCodeAPI()
        self.create_params()
        try:
            if self.xpaths['eternalConn'] == '1':
                self.eternalConn()
            else:
                self.setStatusDevice(True)
                self.postQRCodeAPI()
                self.flow()
                # self.flow()
                self.updateJob()
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'ok',
                    "message": '',
                    "contact": ''
                }
            )
            self.close()
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": 'Error on __init__ function: ' + str(e),
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error on __init__ function: " + str(e))
            self.close()

    def eternalConn(self):
        while True:
            self.create_params()
            if self.isWhatsAppAvailable():
                self.setStatusDevice(True)
                self.postQRCodeAPI()
            self.flow()
            self.updateJob()
            sleep(10)
            collect_gc()

    def create_params(self):
        self.archive_chats_time = float(self.getAPIConfig(int(self.xpaths["archive_chats_time"])))/1000
        self.min_prank_time = float(self.getAPIConfig(int(self.xpaths["min_prank_time"])))
        self.max_prank_time = float(self.getAPIConfig(int(self.xpaths["max_prank_time"])))
        self.min_greeting_time = float(self.getAPIConfig(int(self.xpaths["min_greeting_time"])))
        self.greetings_panel = self.getAPIConfig(int(self.xpaths["greetingsToMeID"]))
        self.greeting_is_fake_image = self.getAPIConfig(int(self.xpaths["greetingFakeImageID"])) == 1
        self.greeting_is_image = self.getAPIConfig(int(self.xpaths["greetingImageID"])) == 1
        self.greeting_is_message = self.getAPIConfig(int(self.xpaths["onlyMessageID"])) == 1
        self.send_greetings = self.getAPIConfig(int(self.xpaths["sendGreetingsID"])) == 1
        self.server_is_active = self.checkServerActive()
        if not self.send_greetings and self.server_is_active:
            self.send_greetings = True
        self.send_pranks = self.getAPIConfig(int(self.xpaths["sendPrankID"])) == 1
        self.send_gen_messages = self.getAPIConfig(int(self.xpaths["sendGenMessagesID"])) == 1
        self.greeting_is_audio = self.getAPIConfig(int(self.xpaths["greetingAudioID"])) == 1
        self.prank_send_media = self.getAPIConfig(int(self.xpaths["prankSendMediaID"])) == 1
        self.send_with_link = self.getAPIConfig(int(self.xpaths["sendWithLinkID"])) == 1
        self.prank_image_ratio = float(self.getAPIConfig(int(self.xpaths["prankImageRatioID"]))) / 100
        self.prank_video_ratio = float(self.getAPIConfig(int(self.xpaths["prankVideoRatioID"]))) / 100
        self.prank_audio_ratio = float(self.getAPIConfig(int(self.xpaths["prankAudioRatioID"]))) / 100
        self.prank_document_ratio = float(self.getAPIConfig(int(self.xpaths["prankDocumentRatioID"]))) / 100
        self.send_single_messages = self.getAPIConfig(int(self.xpaths["singleMessagesID"])) == 1

    def flow(self):
        self.update_greeting_time = False
        post(
            self.xpaths["api_log"],
            params = {
                "number": self.getPhoneNumber(),
                "event": 'connected',
                "message": '',
                "contact": ''
            }
        )
        # self.pinChatsEver()
        check_if_send = self.checkIfSend()
        send_only_desktop = self.getAPIConfig(int(self.xpaths["sendMessagesID"])) == 1
        self.verifyArchiveChats()
        self.collectMessagesAndReturn()
        if not self.worked_today:
            self.greeting_number = self.setGreetingNumber()
        else:
            self.greeting_number = self.getGreetingNumber()
        self.ac.send_keys(Keys.ESCAPE).perform()
        only_reader_bot = self.checkIfOnlyReader()
        if check_if_send and not only_reader_bot:
            self.sendMessages(self.collectMessagesToSend())
        elif not check_if_send and not send_only_desktop:
            self.sendMessages(self.collectMessagesToSend())
        else:
            self.log.info(f"{self.device} - Messages are not sent, only send with Desktop")
            self.sendMessages(self.collectMessagesToSend(True))
        if only_reader_bot:
            self.sendMediaMessages(self.collectMessagesToSend())
        self.verifyArchiveChats()
        # self.pinChatsEver()
        self.chats = self.createChats()
        self.worked_chats_list = []
        self.runInNotReadedChats()
        self.ac.send_keys(Keys.ESCAPE).perform()
        if self.chats['messages']:
            self.returnMessages()
        if self.crashed_returns:
            self.returnFailedMessages()
        if self.xpaths['sendGreetingBySelf'] == '1' and not send_only_desktop:
            while self.has_greetings:
                self.sendGreetings()
        if self.update_greeting_time:
            self.updateGreetingTime()
        self.sendFirstReturnMessages(self.collectMessagesToSend())
        
    def sendFirstReturnMessages(self, messages):
        try:
            self.log.info("Sending messages for the second time...")
            oth_messages = self.messageStructure()
            oth_messages['check_status'] = []

            c = 0
            for i in messages['check_status']:
                if i == 0:
                    oth_messages['id'].append(messages['id'][c])
                    oth_messages['contact_phone_number'].append(messages['contact_phone_number'][c])
                    oth_messages['message_body'].append(messages['message_body'][c])
                    oth_messages['message_type'].append(messages['message_type'][c])
                    oth_messages['message_body_filename'].append(messages['message_body_filename'][c])
                    oth_messages['message_caption'].append(messages['message_caption'][c])
                    oth_messages['message_custom_id'].append(messages['message_custom_id'][c])
                    oth_messages['message_body_mimetype'].append(messages['message_body_mimetype'][c])
                    oth_messages['check_status'].append(messages['check_status'][c])
                c += 1
            c = 0 
            for i in oth_messages['message_type']:
                if self.send_gen_messages:
                    if i == "text":
                        self.sendMessageText(
                            oth_messages['id'][c],
                            oth_messages['contact_phone_number'][c],
                            oth_messages['message_body'][c]
                        )
                    else:
                        self.sendAttachedMessage(
                            oth_messages['id'][c],
                            oth_messages['contact_phone_number'][c],
                            oth_messages['message_body'][c],
                            oth_messages['message_caption'][c],
                            oth_messages['message_body_filename'][c],
                            oth_messages['message_custom_id'][c],
                            oth_messages['message_body_mimetype'][c]
                        )
                c += 1
                sleep(round(uniform(2, 2.5), 2))
            sleep(round(uniform(0, .75), 2))
            self.ac.send_keys(Keys.ESCAPE).perform()
            self.log.info("Second Messages has been sent")
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": "Error on sendFirstReturnMessages function: " + str(e),
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error on sendFirstReturnMessages function: " + str(e))
            self.close()
            
    def checkIfOnlyReader(self):
        try:
            only_reader_bot = get(
                self.xpaths["api"] + "get_only_reader_bot",
                params = {
                    "device_id": self.device_id
                }
            )
            if only_reader_bot.status_code == 200:
                if only_reader_bot.text == 'True':
                    return True
                else:
                    return False
            else:
                return True
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": "Error on checkIfOnlyReader function: " + str(e),
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error on checkIfOnlyReader function: " + str(e))
            self.close()

    def checkServerActive(self):
        try:
            is_active = get(
                self.xpaths["api"] + "get_server_active",
                params = {
                    "device_id": self.device_id
                }
            )
            if is_active.status_code == 200:
                if is_active.text == 'True':
                    return True
                else:
                    return False
            else:
                return True
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": "Error on checkServerActive function: " + str(e),
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error on checkServerActive function: " + str(e))
            self.close()

    def checkIfSend(self):
        try:
            browser = get(
                self.xpaths["api_app"] + "get_device_ip",
                params = {
                    "device_id": self.device_id
                }
            )
            if browser.status_code == 200:
                if browser.text.isnumeric():
                    return False
                else:
                    return True
            else:
                return True
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": "Error on checkIfSend function: " + str(e),
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error on checkIfSend function: " + str(e))
            self.close()

    def getGreetingMessages(self):
        try:
            messages = get(self.xpaths["api"] + "get_active_greeting_messages")
            if messages.status_code == 200:
                return [x[0] for x in messages.json()]
            else:
                self.log.error("Messages not found")
                return []
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": "Error on getGreetingMessages function: " + str(e),
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error on getGreetingMessages function: " + str(e))
            self.close()

    def getGreetingNumber(self):
        try:
            greeting_number = get(
                self.xpaths["api"] + "get_greeting_number",
                params = {
                    "device_id": self.device_id
                }
            )
            if greeting_number.status_code == 200:
                if greeting_number.text == 'None':
                    return self.setGreetingNumber()
                else:
                    return greeting_number.text
            else:
                self.log.error("Greeting number not found")
                return None
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": "Error on getGreetingNumber function: " + str(e),
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error on getGreetingNumber function: " + str(e))
            self.close()

    def setGreetingNumber(self):
        configs = self.getGreetingConfigs()[0]
        # gn.id, gn.opcao_grupo, n.vgroup_id, n.num_saudacao
        greeting_numbers = []
        if configs[1] == 1:
            greeting_numbers = self.getGreetingNumber1(configs[0])
        elif configs[1] == 2:
            if configs[2]:
                greeting_numbers = self.getGreetingNumber2(configs[2])
            else:
                greeting_numbers = [self.getRandomGreetingNum()]
        else:
            greeting_numbers = [self.getRandomGreetingNum()]
        if greeting_numbers:
            greeting_number = greeting_numbers[randint(0, len(greeting_numbers)-1)]
        else:
            greeting_number = self.getRandomGreetingNum()
        if isinstance(greeting_number, list):
            greeting_number = greeting_number[0]
        self.setGreetingNumberDB(greeting_number)
        return greeting_number

    def getRandomGreetingNum(self):
        try:
            random_greetin_num = get(
                self.xpaths["api"] + "get_random_greeting_num",
                params = {
                    "device_id": self.device_id
                }
            )
            if random_greetin_num.status_code == 200:
                return random_greetin_num.text
            else:
                self.log.error("Greeting number not found")
                return None
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": "Error on getRandomGreetingNum function: " + str(e),
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error on getRandomGreetingNum function: " + str(e))
            self.close()

    def setGreetingNumberDB(self, greeting_number):
        try:
            return_message = post(
                self.xpaths["api"] + 'set_greeting_number',
                params = {
                    "device_id": self.device_id,
                    "greeting_number": greeting_number
                }
            )
            if return_message.text == 'OK':
                self.log.info(f"{self.device} - Greeting number inserted on DB")
            else:
                self.log.error(f"{self.device} - Error on insert greeting number on DB")
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": "Error on setGreetingNumberDB function: " + str(e),
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error on setGreetingNumberDB function: " + str(e))
            self.close()

    def getGreetingNumber2(self, vgroup_id):
        try:
            greeting_number = get(
                self.xpaths["api"] + "get_greeting_number_two",
                params = {
                    "device_id": self.device_id,
                    "vgroup_id": vgroup_id
                }
            )
            if greeting_number.status_code == 200:
                if greeting_number.text == 'None':
                    self.log.error("Greeting number not found, using random")
                    return [self.getRandomGreetingNum()]
                else:
                    return greeting_number.json()
            else:
                self.log.error("Greeting number not found")
                return None
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": "Error on getGreetingNumber2 function: " + str(e),
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error on getGreetingNumber2 function: " + str(e))
            self.close()

    def getGreetingNumber1(self, group_id):
        try:
            greeting_number = get(
                self.xpaths["api"] + "get_greeting_number_one",
                params = {
                    "device_id": self.device_id,
                    "group_id": group_id
                }
            )
            if greeting_number.status_code == 200:
                if greeting_number.text == 'None':
                    self.log.error("Greeting number not found, using random")
                    return [self.getRandomGreetingNum()]
                else:
                    return greeting_number.json()
            else:
                self.log.error("Greeting number not found")
                return None
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": "Error on getGreetingNumber1 function: " + str(e),
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error on getGreetingNumber1 function: " + str(e))
            self.close()

    def getGreetingConfigs(self):
        try:
            greeting_configs = get(
                self.xpaths["api"] + "get_greeting_configs",
                params = {
                    "device_id": self.device_id
                }
            )
            if greeting_configs.status_code == 200:
                return greeting_configs.json()
            else:
                self.log.error("Greeting number not found")
                return None
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": "Error on getGreetingConfigs function: " + str(e),
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error on getGreetingConfigs function: " + str(e))
            self.close()

    def createChats(self):
        return {
            'readeds': [],
            'numbers': [],
            'messages': []
        }

    def setGreetings(self):
        if datetime.now().hour < 12:
            return [
                'Olá',
                'Olá, bom dia',
                'Bom dia',
                'Oi',
                'Oi, bom dia',
                ' Bom dia ',
                'Bom dia!!',
                'Bom dia!',
                'Bom dia, tudo bem?',
                ' Bom dia, tudo bem??',
                'Bom dia, tudo bem???',
            ]
        elif datetime.now().hour < 18:
            return [
                'Olá',
                'Olá, boa tarde',
                'Boa tarde',
                'Oi',
                'Oi, boa tarde',
                ' Boa tarde ',
                'Boa tarde!!',
                'Boa tarde!',
                'Boa tarde, tudo bem?',
                ' Boa tarde, tudo bem??',
                'Boa tarde, tudo bem???',
            ]
        else:
            return [
                'Olá',
                'Olá, boa noite',
                'Boa noite',
                'Oi',
                'Oi, boa noite',
                ' Boa noite ',
                'Boa noite!!',
                'Boa noite!',
                'Boa noite, tudo bem?',
                ' Boa noite, tudo bem??',
                'Boa noite, tudo bem???',
            ]

    def sendGreetings(self):
        try:
            chats = self.getOrdenedChats()
            me_chat = False
            for i in chats:
                if self.elementExistsInElement(i, self.xpaths['youLabel']):
                    me_chat = i
                    if not self.elementExistsInElement(i, self.xpaths['pinnedChat']):
                        self.pinChat(i)
                    break
            if me_chat:
                me_chat.click()
                self.cleanSendedGreetings()
                self.sendGreetingText()
            else:
                self.has_greetings = False
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": f"Error on sendGreetings function: {e}",
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error on sendGreetings function: {e}")

    def pinChatsEver(self):
        try:
            chats = self.getOrdenedChats()[:10]
            for i in chats:
                if self.elementExistsInElement(i, self.xpaths['youLabel']):
                    if not self.elementExistsInElement(i, self.xpaths['pinnedChat']):
                        self.pinChat(i)
                    break
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": f"Error on sendGreetings function: {e}",
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error on sendGreetings function: {e}")

    def pinChat(self, el):
        try:
            self.ac.context_click(el).perform()
            WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, self.xpaths['menuArchiveChats'])))
            WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, self.xpaths['buttonPinChats'])))
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, self.xpaths['buttonPinChats'])))
            WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, self.xpaths['buttonPinChats'])))
            self.driver.find_element(By.XPATH, self.xpaths['buttonPinChats']).click()
            self.log.info(f"{self.device} - Chat pinned")
            sleep(0.3)
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": "Error on pinChat function: " + str(e),
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error on pinChat function: " + str(e))
            self.close()

    def cleanSendedGreetings(self):
        try:
            messages_out = self.getMessagesOut()
            for i in messages_out:
                if not isinstance(i, str):
                    try:
                        contacts = i.find_elements(By.XPATH, self.xpaths['greetingContacts'])
                    except:
                        contacts = []
                    c = 0
                    for j in contacts:
                        if self.checkGreetingSended(j.text):
                            c += 1
                    if c == len(contacts) and c != 0:
                        self.removeMessage(i)
            self.log.info(f"{self.device} - Cleaned sended greetings.")
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": f"Error on cleanSendedGreetings function: {e}",
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error on cleanSendedGreetings function: {e}")

    def removeMessage(self, el):
        self.ac.move_to_element(el.find_element(By.XPATH, self.xpaths['greetingContacts'])).perform()
        self.driver.find_element(By.XPATH, self.xpaths['removeMsgDropDownBtn']).click()
        WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, self.xpaths['removeMessagePopUp'])))
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, self.xpaths['removeMessagePopUp'])))
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, self.xpaths['removeMessageButton'])))
        self.driver.find_element(By.XPATH, self.xpaths['removeMessageButton']).click()
        WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, self.xpaths['confirmRemoveMessage'])))
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, self.xpaths['confirmRemoveMessage'])))
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, self.xpaths['confirmButtonRmMsg'])))
        self.driver.find_element(By.XPATH, self.xpaths['confirmButtonRmMsg']).click()
        sleep(round(uniform(1, 1.5), 2))

    def sendGreetingText(self):
        try:
            greeting_sended = True
            messages_out = self.getMessagesOut()
            for i in messages_out:
                greeting_sended = True
                if not isinstance(i, str):
                    try:
                        contacts = i.find_elements(By.XPATH, self.xpaths['greetingContacts'])
                    except:
                        contacts = []
                    for j in contacts:
                        contact_phone_number = j.text
                        if contact_phone_number:
                            contact_phone_number = contact_phone_number.replace('+', '')
                        if self.re_phone_number.match(contact_phone_number) is None:
                            continue
                        greeting_sended = self.checkGreetingSended(contact_phone_number)
                        if not greeting_sended:
                            j.click()
                            WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, self.xpaths['sendGreetingPopUp'])))
                            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, self.xpaths['sendGreetingPopUp'])))
                            WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, self.xpaths['sendGreetingButton'])))
                            self.driver.find_element(By.XPATH, self.xpaths['sendGreetingButton']).click()
                            break
                if not greeting_sended:
                    break
            if not greeting_sended:
                sleep(round(uniform(1, 1.5), 2))
                self.sendWritingMessage(choice(self.greetings))
                self.insertGreetingSended(contact_phone_number)
                self.ac.send_keys(Keys.ESCAPE).perform()
            else:
                self.has_greetings = False
            self.log.info(f"{self.device} - Greetings sended.")
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": f"Error on sendGreetingText function: {e}",
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error on sendGreetingText function: {e}")

    def checkGreetingSended(self, contact_phone_number):
        try:
            return_message = get(
                self.xpaths["api"] + 'get_greeting',
                params = {
                    "device_id": self.device_id,
                    "contact_phone_number": contact_phone_number
                }
            )
            if return_message.text == 'OK':
                return True
            else:
                return False
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": f"Error on checkGreetingSended function: " + str(e),
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error on checkGreetingSended function: " + str(e))
            self.close()

    def insertGreetingSended(self, contact_phone_number):
        try:
            return_message = post(
                self.xpaths["api"] + 'insert_greeting',
                params = {
                    "device_id": self.device_id,
                    "contact_phone_number": contact_phone_number
                }
            )
            if return_message.text == 'OK':
                self.log.info(f"{self.device} - Greeting inserted on DB")
            else:
                self.log.error(f"{self.device} - Error on insert greeting on DB")
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": "Error on insertGreetingSended function: " + str(e),
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error on insertGreetingSended function: " + str(e))
            self.close()

    def getMessagesOut(self):
        try:
            while not self.elementExistsInDriver(self.xpaths['messagesChat']):
                sleep(1)
            sleep(1)
            all_chat = self.driver.find_element(By.XPATH, self.xpaths['messagesChat'])
            all_messages = all_chat.find_elements(By.XPATH, "./child::*")
            messages = []
            for i in all_messages:
                try:
                    j = i.find_element(By.XPATH, "./child::*")
                    if "NÃO LIDA" in j.text:
                        continue
                    elif self.xpaths['messageOutAttr'] in j.get_attribute('class'):
                        messages.append(j)
                    elif self.xpaths['messageOutAttr'] in j.find_element(By.XPATH, "./child::*").get_attribute('class'):
                        messages.append(j)
                    elif self.xpaths['messageDateAttr3'] in i.get_attribute('class') or self.xpaths['messageDateAttr'] in i.get_attribute('class') or self.xpaths['messageDateAttr2'] in i.get_attribute('class'):
                        messages.append(i.text)
                    elif self.xpaths['messageOutAttr'] in j.get_attribute('class'):
                        continue
                except:
                    continue
            idx = None
            for i in messages:
                if isinstance(i, str) and i == self.day_flag:
                    idx = messages.index(i)
            if not idx:
                if self.day_flag == 'SÁBADO':
                    for i in messages:
                        if isinstance(i, str) and i == 'ONTEM':
                            idx = messages.index(i)
            if not idx:
                for i in messages:
                    if isinstance(i, str) and i == 'HOJE':
                        idx = messages.index(i)
            if idx is None:
                return []
            else:
                return messages[idx+1:]
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": f"Error on getMessagesOut function: {e}",
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error on getMessagesOut function: {e}")
            return []

    def returnFailedMessages(self):
        try:
            self.log.info("Returning failed messages...")
            for i in range(3):
                c = 0
                sended_idx_list = []
                for i in self.crashed_returns:
                    try:
                        if self.re_phone_number.match(i[0]['contact_phone_number']):
                            return_cromos = post('http://192.168.7.100:8090/cromos_forward_failed', json=i[0], timeout=4)
                        if return_cromos.status_code == 200:
                            self.insertReturnMessages(i[0]['contact_phone_number'], i[0]['message_custom_id'], i[1], i[0]['schedule'], i[2], True)
                            sended_idx_list.append(i)
                        else:
                            self.log.error(f"{self.device} - Error on return crashed message to Cromos.\nStatus code: {return_cromos.status_code}")
                    except Exception as e:
                        post(
                            self.xpaths["api_log"],
                            params = {
                                "number": self.getPhoneNumber(),
                                "event": 'error',
                                "message": f"Error return cromos: {e}",
                                "contact": ''
                            }
                        )
                        self.log.error(f"{self.device} - Error: {e}")
                    c += 1
                for i in sended_idx_list:
                    self.crashed_returns.remove(i)
                if len(self.crashed_returns) == 0:
                    break
            self.log.info(f"{self.device} - Failed messages sent back with success")
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": f"Error on returnFailedMessages function {e}",
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error on returnFailedMessages function {e}")
            self.close()

    def updateJob(self):
        try:
            update_job = get(
                self.xpaths["api"] + "update_job",
                params = {
                    "device_id": self.device_id,
                    "last_job": datetime.now()
                }
            )
            if update_job.status_code == 200:
                self.log.info("Job updated")
            else:
                self.log.error("Job not updated")
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": "Job not updated: " + str(e),
                    "contact": ''
                }
            )
            self.log.error("Job not updated: " + str(e))
            self.close()

    def returnMessages(self):
        try:
            self.log.info("Sending back messages...")
            phone_number = self.getPhoneNumber()
            phone_number = phone_number if phone_number else "5541999999999"
            for i in range(len(self.chats['numbers'])):
                for j in range(len(self.chats['messages'][i]['times'])):
                    if self.chats['messages'][i]['bodies'][j]:
                        k = {
                            'phone_number': phone_number,
                            'contact_phone_number': self.chats['numbers'][i],
                            'message_custom_id': self.chats['messages'][i]['ids'][j],
                            'message_type': self.chats['messages'][i]['types'][j],
                            'message_body': self.chats['messages'][i]['bodies'][j],
                            'schedule': self.chats['messages'][i]['times'][j],
                            'message_body_extension': self.chats['messages'][i]['extensions'][j],
                            'message_body_mimetype': self.chats['messages'][i]['mimetypes'][j],
                            'message_body_filename': self.chats['messages'][i]['filenames'][j],
                            'message_caption': self.chats['messages'][i]['captions'][j],
                            'event': 'message'
                        }
                        try:
                            if self.re_phone_number.match(k['contact_phone_number']):
                                return_cromos = post('http://192.168.7.100:8090/cromos_forward_return', json=k, timeout=12)
                                if return_cromos.status_code == 200:
                                    self.insertReturnMessages(
                                        self.chats['numbers'][i], self.chats['messages'][i]['ids'][j],
                                        self.chats['messages'][i]['order'][j], self.chats['messages'][i]['times'][j],
                                        self.chats['messages'][i]['readedsAt'][j], True
                                    )
                                else:
                                    self.log.error(f"""
                                        Error on sending back message to Cromos.\n
                                        Device: {self.device}
                                        Contact: {self.chats['numbers'][i]}
                                        ID: {self.chats['messages'][i]['ids'][j]}
                                        Type: {self.chats['messages'][i]['types'][j]}
                                        Mime: {self.chats['messages'][i]['mimetypes'][j]}
                                        Body: {self.chats['messages'][i]['bodies'][j]}
                                    """)
                                    try:
                                        self.crashed_returns.append([k, self.chats['messages'][i]['order'][j], self.chats['messages'][i]['readedsAt'][j]])
                                        self.log.error(f"{return_cromos.status_code}")
                                    except:
                                        pass
                        except Exception as e:
                            post(
                                self.xpaths["api_log"],
                                params = {
                                    "number": self.getPhoneNumber(),
                                    "event": 'error',
                                    "message": f"Error returnMessages to cromos: {e}",
                                    "contact": ''
                                }
                            )
                            self.log.error(f"""
                                Error on sending back message to Cromos.\n
                                Device: {self.device}
                                Contact: {self.chats['numbers'][i]}
                                ID: {self.chats['messages'][i]['ids'][j]}
                                Type: {self.chats['messages'][i]['types'][j]}
                                Mime: {self.chats['messages'][i]['mimetypes'][j]}
                                Body: {self.chats['messages'][i]['bodies'][j]}
                            """)
                            self.crashed_returns.append([k, self.chats['messages'][i]['order'][j], self.chats['messages'][i]['readedsAt'][j]])
                            self.log.error(f"{self.device} - Erro returnMessages: {e}")
            self.log.info(f"{self.device} - Messages sent back")
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": f"Error on returnMessages to cromos function {e}",
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error on returnMessages function {e}")
            self.close()

    def insertReturnMessages(self, contact_phone_number, id, order, message_time, readed_at, returned):
        try:
            return_message = post(
                self.xpaths["return"],
                data = {
                    "device_id": self.device_id,
                    "contact_phone_number": contact_phone_number,
                    "custom_id": id,
                    "order": order,
                    "message_time": message_time,
                    "readed_at": readed_at,
                    "returned": returned
                }
            )
            if return_message.text != 'OK':
                self.log.error("Message not inserted on DB\n" + return_message.text)
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": "Error on insertReturnMessages function: " + str(e),
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error on insertReturnMessages function: " + str(e))
            self.close()

    def getPhoneNumber(self):
        try:
            phone_number = get(
                self.xpaths["api"] + "get_phone_number",
                params = {
                    "device_id": self.device_id
                }
            )
            if phone_number.status_code == 200:
                return phone_number.text
            else:
                self.log.error("Phone number not found")
                return None
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": "Error on getPhoneNumber function: " + str(e),
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error on getPhoneNumber function: " + str(e))
            return None

    def collectMessagesAndReturn(self):
        try:
            self.log.info(f"Reading {self.device} messages...")
            self.worked_today = self.getLastJob()
            self.worked_today = str(self.worked_today).split(" ")[0] if self.worked_today else None
            today = datetime.now().strftime(f"%Y-%m-%d")
            self.worked_today = True if self.worked_today == today else False
            today = datetime.today().weekday()
            if not self.worked_today and today == 0:
                self.day_flag = "SÁBADO"
            elif not self.worked_today:
                self.day_flag = "ONTEM"
            else:
                self.day_flag = "HOJE"
            if not self.worked_today:
                self.chats = self.createChats()
                self.worked_chats_list = []
                self.runInChats(self.getOrdenedChats()[:int(self.xpaths["firstRunInChats"])])
                self.returnMessages()
                self.chats = self.createChats()
                self.worked_chats_list = []
                self.runInNotReadedChats()
                self.returnMessages()
            else:
                self.chats = self.createChats()
                self.worked_chats_list = []
                self.runInChats(self.getOrdenedChats()[:int(self.xpaths["runInChats"])])
                self.returnMessages()
                self.chats = self.createChats()
                self.worked_chats_list = []
                self.runInNotReadedChats()
                self.returnMessages()
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": "Error collectMessagesToReturn function: " + str(e),
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error collectMessagesToReturn function: " + str(e))
            self.close()

    def getLastJob(self):
        try:
            last_job = get(
                self.xpaths["api"] + "get_last_job",
                params = {
                    "device_id": self.device_id
                }
            )
            if last_job.status_code == 200:
                return last_job.text
            else:
                self.log.error("Last job not found")
                return None
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": "Error getLastJob function: " + str(e),
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error getLastJob function: " + str(e))
            self.close()

    def getAllPhonesFromDB(self):
        try:
            phones = get(self.xpaths["api"] + "get_all_phones")
            if phones.status_code == 200:
                return phones.json()
            else:
                self.log.error("Phones not found")
                return []
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": "Error getAllPhonesFromDB function: " + str(e),
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error getAllPhonesFromDB function: " + str(e))
            self.close()

    def getAllNamesFromDB(self):
        try:
            names = get("http://192.168.7.100:8787/get_names")
            if names.status_code == 200:
                return names.json()
            else:
                self.log.error("Phones not found")
                return []
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": "Error getAllNamesFromDB function: " + str(e),
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error getAllNamesFromDB function: " + str(e))
            self.close()

    def verifyArchiveChats(self):
        try:
            list_changed = True
            while list_changed:
                list_changed = False
                chats = self.getOrdenedChats()[:int(self.xpaths['verifyArchive'])]

                for i in chats:
                    try:
                        if self.elementExistsInElement(i, self.xpaths['youLabel']):
                            continue
                        chat_name = i.find_element(By.XPATH, self.xpaths['chatsListNames']).text.strip()
                        if '# ~ #' in chat_name:
                            self.archiveChats(i)
                            list_changed = True
                            sleep(self.archive_chats_time)
                            break
                        elif self.re_contact_number.match(chat_name) is None:
                            self.archiveChats(i)
                            list_changed = True
                            sleep(self.archive_chats_time)
                            break
                    except StaleElementReferenceException:
                        list_changed = True
                        sleep(self.archive_chats_time)
                        break
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": "Error on verifyArchiveChats function: " + str(e),
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error on verifyArchiveChats function: " + str(e))
            self.close()

    def archiveChats(self, chat):
        try:
            self.ac.context_click(chat).perform()
            WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, self.xpaths['menuArchiveChats'])))
            WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, self.xpaths['buttonArchiveChats'])))
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, self.xpaths['buttonArchiveChats'])))
            WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, self.xpaths['buttonArchiveChats'])))
            self.driver.find_element(By.XPATH, self.xpaths['buttonArchiveChats']).click()
            self.log.info(f"{self.device} - Chat archived")
            sleep(self.archive_chats_time)
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": "Error on archiveChats function: " + str(e),
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error on archiveChats function: " + str(e))
            self.close()

    def runInChats(self, chats, previous="First fake"):
        try:
            phones_to_archive = self.getAllPhonesFromDB()
            phones_to_archive = [x[0] for x in phones_to_archive]
            if chats in self.worked_chats_list:
                self.log.info("Messages has been readed.")
                return
            for i in chats:
                try:
                    chat_name = i.find_element(By.XPATH, self.xpaths['chatsListNames']).text
                    chat_phone = chat_name.replace(' ', '').replace('+', '').replace('-', '')
                except StaleElementReferenceException:
                    continue
                if chat_name in self.chats['readeds'] or chat_phone in phones_to_archive: # or self.re_contact_number.match(chat_name) is None:
                    continue
                worked = False
                while not worked:
                    try:
                        i.click()
                        worked = True
                    except ElementClickInterceptedException:
                        previous.click()
                self.readMessages()
                previous = i
            self.worked_chats_list.append(chats)
            self.runInChats(chats, previous)
            return
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": "Error runInChats function: " + str(e),
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error runInChats function: " + str(e))
            self.close()

    def runInNotReadedChats(self, previous="First fake"):
        try:
            phones_to_archive = self.getAllPhonesFromDB()
            phones_to_archive = [x[0] for x in phones_to_archive]
            chats = self.getOrdenedChats()
            if chats in self.worked_chats_list:
                self.log.info("Messages has been readed.")
                return
            for i in chats:
                try:
                    chat_name = i.find_element(By.XPATH, self.xpaths['chatsListNames']).text
                    chat_phone = chat_name.replace(' ', '').replace('+', '').replace('-', '')
                except StaleElementReferenceException:
                    continue
                if chat_name in self.chats['readeds'] or chat_phone in phones_to_archive or self.re_contact_number.match(chat_name) is None:
                    continue
                else:
                    worked = False
                    is_today = False
                    while not worked:
                        try:
                            if self.elementExistsInElement(i, self.xpaths['chatsListUnreaded']):
                                i.click()
                                is_today = True
                            worked = True
                        except ElementClickInterceptedException:
                            try:
                                previous.click()
                            except AttributeError:
                                count = 0
                                while not self.elementExistsInDriver(self.xpaths['popUpError']):
                                    sleep(1)
                                    count += 1
                                    if count > 4:
                                        break
                                self.ac.send_keys(Keys.ESCAPE).perform()
                                sleep(1)
                            finally:
                                continue
                    if is_today:
                        self.readMessages()
                previous = i
            self.worked_chats_list.append(chats)
            self.runInNotReadedChats(previous)
            return
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": "Error runInNotReadedChats function: " + str(e),
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error runInNotReadedChats function: " + str(e))
            self.close()

    def insertMonitor(self, contact_phone_number, photo, status, tick):
        try:
            insert_monitor = post(
                self.xpaths["api"] + '/insert_monitor',
                params = {
                    "contact_phone_number": contact_phone_number,
                    "photo": photo,
                    "status": status,
                    "tick": tick
                }
            )
            if insert_monitor.status_code == 200:
                self.log.info("Contact phone number monitored")
            else:
                self.log.error(f"{self.device} - Error on monitoring contact phone number")
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": "Error on insertMonitor function: " + str(e),
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error on insertMonitor function: " + str(e))
            self.close()

    def formatPhoneNumber(self, phone_name):
        phone_number = phone_name.split(" ")
        nine = "9" if int(phone_number[2][0]) > 5 and len(phone_number[2]) == 9 else ""
        return phone_number[0][1:] + phone_number[1] + nine + phone_number[2].replace("-", "")

    def getNumberFromContactData(self):
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, self.xpaths['chatOptionsButton'])))
        self.driver.find_element(By.XPATH, self.xpaths['chatOptionsButton']).click()
        WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, self.xpaths['chatOptionsPopUp'])))
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, self.xpaths['chatOptionsPopUp'])))
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, self.xpaths['chatOptionsDataButton'])))
        if 'grupo' in self.driver.find_element(By.XPATH, self.xpaths['chatOptionsDataButton']).text:
            return ''
        self.driver.find_element(By.XPATH, self.xpaths['chatOptionsDataButton']).click()
        try:
            WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, self.xpaths['contactData'])))
            WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located((By.XPATH, self.xpaths['contactData'])))
            return self.driver.find_element(By.XPATH, self.xpaths['contactData']).text
        except:
            WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, self.xpaths['contactData2'])))
            return self.driver.find_element(By.XPATH, self.xpaths['contactData2']).text

    def getChatPhoneForce(self):
        while not self.elementExistsInDriver(self.xpaths['chatPhoneNumber']):
            sleep(1)
        WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, self.xpaths['chatPhoneNumber'])))
        phone_name = self.driver.find_element(By.XPATH, self.xpaths['chatPhoneNumber']).text
        try:
            phone_number = self.formatPhoneNumber(phone_name)
        except:
            phone_number = phone_name
        if self.re_contact_number.match(phone_name):
            return phone_name, phone_number
        else:
            phone_name = self.getNumberFromContactData()
            if not phone_name:
                return '', ''
            try:
                phone_number = self.formatPhoneNumber(phone_name)
            except:
                phone_number = phone_name
            phone_name = self.driver.find_element(By.XPATH, self.xpaths['chatPhoneNumber']).text
        self.ac.send_keys(Keys.ESCAPE).perform()
        return phone_name, phone_number

    def readMessages(self):
        try:
            contact_phone_name, contact_phone_number = self.getChatPhoneForce()
            # photo_check, status_check, tick_check = self.checkContactPhotoStatus()
            # self.insertMonitor(contact_phone_number, photo_check, status_check, tick_check)
            self.chats['readeds'].append(contact_phone_name)
            self.chats['numbers'].append(contact_phone_number)
            order = self.getLastMessageOrder(contact_phone_number)
            order = int(order) if order != 'None' else 0
            self.chats['messages'].append(self.getChatMessages(contact_phone_number, order))
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": "Error readMessages function: " + str(e),
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error readMessages function: " + str(e))
            self.close()

    def getLastMessageOrder(self, contact_phone_number):
        last_message_order = get(
            self.xpaths["api"] + "get_last_message_order",
            params = {
                "device_id": self.device_id,
                "contact_phone_number": contact_phone_number
            }
        )
        if last_message_order.status_code == 200:
            return last_message_order.text
        else:
            self.log.error("Last message not found")
            return None

    def getChatMessages(self, contact_phone_number, order):
        self.log.info("Getting chat messages...")
        messages = {
            'readedsAt': [],
            'bodies': [],
            'times': [],
            'types': [],
            'mimetypes': [],
            'extensions': [],
            'filenames': [],
            'captions': [],
            'order': [],
            'ids': []
        }
        id = self.getLastMessageID(contact_phone_number, order) if order > 0 else None
        try:
            self.scrollUpMessages(id)
        except:
            pass
        all_ids = self.getReturnMessagesID(contact_phone_number) if order > 0 else []
        messagesIn = self.getMessagesIn(all_ids)
        for i in messagesIn:
            if isinstance(i, str):
                if i == 'SÁBADO':
                    day = (datetime.now() + timedelta(days=-2)).strftime(f"%Y-%m-%d ")
                elif i == 'ONTEM':
                    day = (datetime.now() + timedelta(days=-1)).strftime(f"%Y-%m-%d ")
                else:
                    day = datetime.now().strftime(f"%Y-%m-%d ")
                continue
            order += 1
            if self.elementExistsInElement(i, self.xpaths['mediaDownload']):
                i.find_element(By.XPATH, self.xpaths['btnMediaDownload']).click()
                sleep(3)
            if self.elementExistsInElement(i, self.xpaths['textMessages']):
                body, time, c_id, readedAt = self.getTextMessage(i)
                body = sub(r'\s+\d{1,2}:\d{2}\s*(?:AM|PM)?$', '', body).strip()
                messages['readedsAt'].append(readedAt)
                messages['bodies'].append(body)
                messages['times'].append(day + time)
                messages['types'].append("text")
                messages['mimetypes'].append(None)
                messages['extensions'].append(None)
                messages['filenames'].append(None)
                messages['captions'].append(None)
                messages['order'].append(order)
                messages['ids'].append(c_id)
            elif self.elementExistsInElement(i, self.xpaths['comboImageMessages']):
                combo_image = self.getComboImageMessage(i)
                for k, v in combo_image.items():
                    messages['readedsAt'].append(v['readedAt'])
                    messages['bodies'].append(v['body'])
                    messages['times'].append(day + v['time'])
                    messages['types'].append(v['type_'])
                    messages['mimetypes'].append(v['mimetype'])
                    messages['extensions'].append(v['extension'])
                    messages['filenames'].append(v['filename'])
                    messages['captions'].append(None)
                    messages['order'].append(order)
                    messages['ids'].append(k)
            elif self.elementExistsInElement(i, self.xpaths['imageFlagMessages']):
                body, mimetype, type_, extension, filename, caption, time, c_id, readedAt = self.getImageMessage(i)
                messages['readedsAt'].append(readedAt)
                messages['bodies'].append(body)
                messages['times'].append(day + time)
                messages['types'].append(type_)
                messages['mimetypes'].append(mimetype)
                messages['extensions'].append(extension)
                messages['filenames'].append(filename)
                messages['captions'].append(caption)
                messages['order'].append(order)
                messages['ids'].append(c_id)
            elif self.elementExistsInElement(i, self.xpaths['documentMessages']):
                body, mimetype, type_, extension, filename, caption, time, c_id, readedAt = self.getDocumentMessage(i)
                messages['readedsAt'].append(readedAt)
                messages['bodies'].append(body)
                messages['times'].append(day + time)
                messages['types'].append(type_)
                messages['mimetypes'].append(mimetype)
                messages['extensions'].append(extension)
                messages['filenames'].append(filename)
                messages['captions'].append(caption)
                messages['order'].append(order)
                messages['ids'].append(c_id)
            elif self.elementExistsInElement(i, self.xpaths['audioMessages']):
                isavailable, body, mimetype, type_, extension, filename, time, c_id, readedAt = self.getAudioMessage(i)
                if isavailable:
                    messages['readedsAt'].append(readedAt)
                    messages['bodies'].append(body)
                    messages['times'].append(day + time)
                    messages['types'].append(type_)
                    messages['mimetypes'].append(mimetype)
                    messages['extensions'].append(extension)
                    messages['filenames'].append(filename)
                    messages['captions'].append(None)
                    messages['order'].append(order)
                    messages['ids'].append(c_id)
            elif self.elementExistsInElement(i, self.xpaths['contactMessages']):
                body, time, c_id, readedAt = self.getContactMessage(i)
                body = sub(r'\s+\d{1,2}:\d{2}\s*(?:AM|PM)?$', '', body).strip()
                messages['readedsAt'].append(readedAt)
                messages['bodies'].append(body)
                messages['times'].append(day + time)
                messages['types'].append("text")
                messages['mimetypes'].append(None)
                messages['extensions'].append(None)
                messages['filenames'].append(None)
                messages['captions'].append(None)
                messages['order'].append(order)
                messages['ids'].append(c_id)
            else:
                time, c_id, readedAt = self.getIgnoredMessage(i)
                messages['readedsAt'].append(readedAt)
                messages['bodies'].append("_")
                messages['times'].append(day + time)
                messages['types'].append("ignored")
                messages['mimetypes'].append(None)
                messages['extensions'].append(None)
                messages['filenames'].append(None)
                messages['captions'].append(None)
                messages['order'].append(order)
                messages['ids'].append(c_id)
        self.log.info("Messages collected.")
        return messages

    def getReturnMessagesID(self, contact_phone_number):
        messages_id = get(
            self.xpaths["api"] + "get_return_messages_id",
            params = {
                "device_id": self.device_id,
                "contact_phone_number": contact_phone_number
            }
        )
        if messages_id.status_code == 200:
            return messages_id.json()
        else:
            self.log.error(f"{self.device} - Error on getting return messages id")
            return None

    def getLastMessageID(self, contact_phone_number, order):
        last_message_id = get(
            self.xpaths["api"] + "get_last_id",
            params = {
                "device_id": self.device_id,
                "contact_phone_number": contact_phone_number,
                "order": order
            }
        )
        if last_message_id.status_code == 200:
            return last_message_id.text
        else:
            self.log.error("Last ID not found")
            return None

    def getMessagesIn(self, ids):
        try:
            while not self.elementExistsInDriver(self.xpaths['messagesChat']):
                sleep(1)
            all_chat = self.driver.find_element(By.XPATH, self.xpaths['messagesChat'])
            all_messages = all_chat.find_elements(By.XPATH, "./child::*")

            messages = []
            for i in all_messages:
                try:
                    j = i.find_element(By.XPATH, "./child::*")
                    if (
                        self.xpaths['messageDateAttr1'] in i.get_attribute('class') or 
                        self.xpaths['messageDateAttr2'] in i.get_attribute('class') or 
                        self.xpaths['messageDateAttr3'] in i.get_attribute('class') or
                        self.xpaths['messageDateAttr4'] in i.get_attribute('class') or
                        self.xpaths['messageDateAttr5'] in i.get_attribute('class') or
                        self.xpaths['messageDateAttr6'] in i.get_attribute('class') or
                        self.xpaths['messageDateAttr7'] in i.get_attribute('class')
                    ):
                        messages.append(i.text)
                        continue
                    if "NÃO LIDA" in j.text:
                        continue
                    elif self.xpaths['messageOutAttr'] in j.get_attribute('class'):
                        continue

                    messages_id_list = self.extract_data_id_if_message_in_exists(i.get_attribute("innerHTML"))
                    if messages_id_list:
                        if len(messages_id_list) == 1:
                            messageid = messages_id_list[0]
                            messageid = messageid.split("_")[-1]
                            messageid = messageid if len(messageid) <= 36 else id[:35]
                            if messageid in ids:
                                continue
                            else:
                                messages.append(j)
                                continue
                        else:
                            j = i.find_elements(By.XPATH, "./child::*")
                            c = 0
                            for k in j:
                                messageid = messages_id_list[c]
                                messageid = messageid.split("_")[-1]
                                messageid = messageid if len(messageid) <= 36 else id[:35]
                                c += 1
                                if messageid in ids:
                                    continue
                                else:
                                    messages.append(k)
                                    continue
                except:
                    continue

            idx = None
            for i in messages:
                if isinstance(i, str):
                    if i == self.day_flag:
                        idx = messages.index(i)
            if not idx:
                if self.day_flag == 'SÁBADO':
                    for i in messages:
                        if isinstance(i, str):
                            if i == 'ONTEM':
                                idx = messages.index(i)
            if not idx:
                for i in messages:
                    if isinstance(i, str):
                        if i == 'HOJE':
                            idx = messages.index(i)
            return messages[idx:]
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": "Error getMessagesIn function: " + str(e),
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error getMessagesIn function: " + str(e))
            self.close()

    # def extract_data_id_if_message_in_exists(self, html_string):
    #     """
    #     Retorna o valor do atributo data-id se houver um <div> com a classe 'message-in' no HTML.
    #     Caso contrário, retorna None.
    #     """
    #     # Verifica se existe uma div com a classe 'message-in'
    #     if 'class="message-in' in html_string:
    #         # Extrai o valor de data-id
    #         match = search(r'data-id="([^"]+)"', html_string)
    #         if match:
    #             return match.group(1)
    #     return None

    def extract_data_id_if_message_in_exists(self, html_string: str) -> Union[str, list[str], None]:
        """
        Retorna uma lista com todos os atributos data-id das <div> que contêm
        uma <div class="message-in"> em seu conteúdo.
        """
        soup = BeautifulSoup(html_string, 'html.parser')
        data_ids = []

        # Encontrar todos os elementos com classe 'message-in'
        for msg_div in soup.find_all('div', class_='message-in'):
            parent = msg_div.find_parent('div', attrs={'data-id': True})
            if parent:
                data_ids.append(parent['data-id'])

        return data_ids


    def getIgnoredMessage(self, el):
        time = el.find_element(By.XPATH, self.xpaths['messagesTime']).text
        id = el.get_attribute(self.xpaths['messagesIdAttr'])
        if id is None:
            id = self.extract_data_id_from_html(el.get_attribute("innerHTML"))
        id = id.split("_")[-1]
        id = id if len(id) <= 36 else id[:35]
        return time, id, datetime.now().strftime(f"%Y-%m-%d %H:%M:%S")

    def getContactMessage(self, el):
        el.find_element(By.XPATH, self.xpaths['contactMessages']).click()
        while not self.elementExistsInDriver(self.xpaths['contactNumberMessages']):
            sleep(1)
        WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, self.xpaths['contactNumberMessages'])))
        body = 'Compartilhamento de contatos\nNome do contato: '
        body += self.driver.find_element(By.XPATH, self.xpaths['contactNameMessages']).text
        body += '\nNúmero do contato: '
        number = self.driver.find_element(By.XPATH, self.xpaths['contactNumberMessages']).text
        number.split('+')[-1]
        body += number
        time = el.find_element(By.XPATH, self.xpaths['messagesTime']).text
        id = el.get_attribute(self.xpaths['messagesIdAttr'])
        if id is None:
            id = self.extract_data_id_from_html(el.get_attribute("innerHTML"))
        id = id.split("_")[-1]
        id = id if len(id) <= 36 else id[:35]
        self.ac.send_keys(Keys.ESCAPE).perform()
        return body, time, id, datetime.now().strftime(f"%Y-%m-%d %H:%M:%S")

    def getAudioMessage(self, el):
        start_time = time()
        max_time = 20
        audio_is_downloadable = True
        while self.elementExistsInElement(el, self.xpaths['audioLoading']):
            end_time = time()
            if end_time - start_time > max_time:
                audio_is_downloadable = False
                break
            else:
                sleep(1)
        if audio_is_downloadable:
            downloads_before = listdir(self.downloads_path)
            for i in downloads_before:
                remove(self.downloads_path + i)
            downloads_before = listdir(self.downloads_path)
            c_id = el.get_attribute(self.xpaths['messagesIdAttr'])
            if c_id is None:
                c_id = self.extract_data_id_from_html(el.get_attribute("innerHTML"))       
            c_id = c_id.split("_")[-1]
            c_id = c_id if len(c_id) <= 36 else c_id[:35]
            chat_panel = self.driver.find_element(By.XPATH, self.xpaths['chatPanel'])
            el_position = self.driver.execute_script("return arguments[0].getBoundingClientRect();", el)
            el_position = el_position['top'] - 33
            while el_position > self.down_of_screen or el_position < 0:
                if self.middle_of_screen < el_position:
                    self.driver.execute_script("arguments[0].scrollBy(0, 20);", chat_panel)
                else:
                    self.driver.execute_script("arguments[0].scrollBy(0, -20);", chat_panel)
                try:
                    el_position = self.driver.execute_script("return arguments[0].getBoundingClientRect();", el)
                    el_position = el_position['top'] - 33
                except:
                    els = self.driver.find_elements(By.XPATH, self.xpaths['messagesIn'])
                    for i in els:
                        id = el.get_attribute(self.xpaths['messagesIdAttr'])
                        if id is None:
                            id = self.extract_data_id_from_html(el.get_attribute("innerHTML"))
                        id = id.split("_")[-1]
                        id = c_id if len(c_id) <= 36 else c_id[:35]
                        if id == c_id:
                            el = i
                            break
                    el_position = self.driver.execute_script("return arguments[0].getBoundingClientRect();", el)
                    el_position = el_position['top'] - 33
            while not self.elementExistsInDriver(self.xpaths['audioMenuDownload']):
                self.ac.move_to_element(
                    el.find_element(By.XPATH, self.xpaths['audioElement'])
                ).perform()
                sleep(0.2)
                try:
                    self.driver.find_element(By.XPATH, self.xpaths['audioDropButton']).click()
                    sleep(0.3)
                except:
                    pass
            sleep(0.3)
            self.driver.find_element(By.XPATH, self.xpaths['audioMenuDownload']).click()
            while len(listdir(self.downloads_path)) == len(downloads_before):
                sleep(1)
            downloads_after = listdir(self.downloads_path)
            file_downloaded = list(set(downloads_after) - set(downloads_before))[0]
            while file_downloaded.split(".")[-1] == "crdownload":
                sleep(1)
                downloads_after = listdir(self.downloads_path)
                file_downloaded = list(set(downloads_after) - set(downloads_before))[0]
            mimetype = guess_type(self.downloads_path + file_downloaded)[0]
            type_ = mimetype.split('/')[0] if mimetype is not None else 'audio'
            extension = file_downloaded.split(".")[-1]
            filename = c_id + "." + extension
            with open(self.downloads_path + file_downloaded, "rb") as f:
                base64_body = b64encode(f.read()).decode("utf-8")
            for i in downloads_after:
                remove(self.downloads_path + i)
            time_ = el.find_element(By.XPATH, self.xpaths['messagesTime']).text
        else:
            base64_body = None
            mimetype = None
            type_ = None
            extension = None
            filename = None
            c_id = None
            time_ = None
        return audio_is_downloadable, base64_body, mimetype, type_, extension, filename, time_, c_id, datetime.now().strftime(f"%Y-%m-%d %H:%M:%S")

    def getDocumentMessage(self, el):
        downloads_before = listdir(self.downloads_path)
        for i in downloads_before:
            remove(self.downloads_path + i)
        downloads_before = listdir(self.downloads_path)
        el.find_element(By.XPATH, self.xpaths['documentDownload']).click()
        time = el.find_element(By.XPATH, self.xpaths['messagesTime']).text
        if self.elementExistsInElement(el, self.xpaths['documentCaption']):
            caption = self.getTextWithEmojis(el, self.xpaths['documentCaption'])
        else:
            caption = None
        c_id = el.get_attribute(self.xpaths['messagesIdAttr'])
        if c_id is None:
            c_id = self.extract_data_id_from_html(el.get_attribute("innerHTML"))
        c_id = c_id.split("_")[-1]
        c_id = c_id if len(c_id) <= 36 else c_id[:35]
        while len(listdir(self.downloads_path)) == len(downloads_before):
            sleep(1)
        downloads_after = listdir(self.downloads_path)
        file_downloaded = list(set(downloads_after) - set(downloads_before))[0]
        while file_downloaded.split(".")[-1] == "crdownload":
            sleep(1)
            downloads_after = listdir(self.downloads_path)
            file_downloaded = list(set(downloads_after) - set(downloads_before))[0]
        mimetype = guess_type(self.downloads_path + file_downloaded)[0]
        mimetype = mimetype if mimetype else "application/octet-stream"
        type_ = mimetype.split('/')[0] if mimetype is not None else 'application'
        if type_ == 'text':
            type_ = 'application'
        extension = file_downloaded.split(".")[-1] if len(file_downloaded.split(".")) > 1 else ".bin"
        filename = c_id + "." + extension
        with open(self.downloads_path + file_downloaded, "rb") as f:
            base64_body = b64encode(f.read()).decode("utf-8")
        for i in downloads_after:
            remove(self.downloads_path + i)
        return base64_body, mimetype, type_, extension, filename, caption, time, c_id, datetime.now().strftime(f"%Y-%m-%d %H:%M:%S")

    def getComboImageMessage(self, el):
        time = el.find_element(By.XPATH, self.xpaths['messagesTime']).text
        c_id = el.get_attribute(self.xpaths['messagesIdAttr'])
        if c_id is None:
            c_id = self.extract_data_id_from_html(el.get_attribute("innerHTML"))
        c_id = c_id.split("_")[-1]
        c_id = c_id if len(c_id) <= 32 else c_id[:32]
        el.find_element(By.XPATH, self.xpaths['imageClick']).click()
        WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, self.xpaths['imageListCombo'])))
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, self.xpaths['imageListCombo'])))
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, self.xpaths['imageListCombo'])))
        image_list = self.driver.find_elements(By.XPATH, self.xpaths['imageListCombo'])
        combo = {}
        counter = 1
        for i in image_list:
            if self.elementExistsInElement(i, self.xpaths['videoInCombo']):
                continue
            i.click()
            downloads_before = listdir(self.downloads_path)
            for i in downloads_before:
                remove(self.downloads_path + i)
            downloads_before = listdir(self.downloads_path)
            WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, self.xpaths['comboMenuDownload6'])))
            if 'mais' in self.driver.find_element(By.XPATH, self.xpaths['comboMenuDownload6']).get_attribute('title').lower():
                image_download_xpath = 'comboMenuDownload6'
            else:
                image_download_xpath = 'comboMenuDownload7'
            self.driver.find_element(By.XPATH, self.xpaths[image_download_xpath]).click()
            WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, self.xpaths['downloadButtonCombo'])))
            self.driver.find_element(By.XPATH, self.xpaths['downloadButtonCombo']).click()
            while len(listdir(self.downloads_path)) == len(downloads_before):
                sleep(1)
            downloads_after = listdir(self.downloads_path)
            file_downloaded = list(set(downloads_after) - set(downloads_before))[0]
            while file_downloaded.split(".")[-1] == "crdownload":
                sleep(1)
                downloads_after = listdir(self.downloads_path)
                file_downloaded = list(set(downloads_after) - set(downloads_before))[0]
            mimetype = guess_type(self.downloads_path + file_downloaded)[0]
            mimetype = mimetype if mimetype else "image/jpeg"
            type_ = mimetype.split('/')[0] if mimetype is not None else 'image'
            extension = file_downloaded.split(".")[-1] if len(file_downloaded.split(".")) > 1 else ".jpeg"
            filename = c_id + "." + extension
            with open(self.downloads_path + file_downloaded, "rb") as f:
                base64_body = b64encode(f.read()).decode("utf-8")
            for i in downloads_after:
                remove(self.downloads_path + i)
            if counter == 1:
                combo[c_id] = {
                    'readedAt': datetime.now().strftime(f"%Y-%m-%d %H:%M:%S"),
                    'body': base64_body,
                    'time': time,
                    'type_': type_,
                    'mimetype': mimetype,
                    'extension': extension,
                    'filename': filename
                }
            else:
                combo[f"{c_id}{counter:03d}"] = {
                    'readedAt': datetime.now().strftime(f"%Y-%m-%d %H:%M:%S"),
                    'body': base64_body,
                    'time': time,
                    'type_': type_,
                    'mimetype': mimetype,
                    'extension': extension,
                    'filename': filename
                }
            counter += 1
        self.ac.send_keys(Keys.ESCAPE).perform()
        sleep(.3)
        return combo

    def getImageMessage(self, el):
        downloads_before = listdir(self.downloads_path)
        for i in downloads_before:
            remove(self.downloads_path + i)
        downloads_before = listdir(self.downloads_path)
        time_text = el.find_element(By.XPATH, self.xpaths['messagesTime']).text
        if self.elementExistsInElement(el, self.xpaths['imageCaption']):
            caption = self.getTextWithEmojis(el, self.xpaths['imageCaption'])
        else:
            caption = None
        c_id = el.get_attribute(self.xpaths['messagesIdAttr'])
        if c_id is None:
            c_id = self.extract_data_id_from_html(el.get_attribute("innerHTML"))
        c_id = c_id.split("_")[-1]
        c_id = c_id if len(c_id) <= 36 else c_id[:35]
        if self.elementExistsInElement(el, self.xpaths['btnMediaDownload']):
            el.find_element(By.XPATH, self.xpaths['btnMediaDownload']).click()
            sleep(1.5)
        if self.elementExistsInElement(el, self.xpaths['imageClick']):
            el.find_element(By.XPATH, self.xpaths['imageClick']).click()
            sleep(1.5)
        max_time = 5
        start_time = time()
        while not self.elementExistsInDriver(self.xpaths['imageDownloadDiv']):
            sleep(1)
            if time() - start_time > max_time:
                break
        if not self.elementExistsInDriver(self.xpaths['imageDownloadDiv']):
            try:
                el.find_element(By.XPATH, self.xpaths['imageClick']).click()
            except:
                pass
        WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, self.xpaths['imageDownloadDiv'])))
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, self.xpaths['imageDownloadDiv'])))
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, self.xpaths['imageDownloadDiv'])))
        if self.driver.find_element(By.XPATH, self.xpaths['imageDownload5']).get_attribute('title').lower() == 'baixar':
            image_download_xpath = 'imageDownload5'
        else:
            image_download_xpath = 'imageDownload6'
        
        download_button_el = self.driver.find_element(By.XPATH, self.xpaths[image_download_xpath])
        download_button_el.click()
        self.ac.send_keys(Keys.ESCAPE).perform()
        while len(listdir(self.downloads_path)) == len(downloads_before):
            sleep(1)
        downloads_after = listdir(self.downloads_path)
        file_downloaded = list(set(downloads_after) - set(downloads_before))[0]
        while file_downloaded.split(".")[-1] == "crdownload":
            sleep(1)
            downloads_after = listdir(self.downloads_path)
            file_downloaded = list(set(downloads_after) - set(downloads_before))[0]
        mimetype = guess_type(self.downloads_path + file_downloaded)[0]
        mimetype = mimetype if mimetype else "image/jpeg"
        type_ = mimetype.split('/')[0] if mimetype is not None else 'image'
        extension = file_downloaded.split(".")[-1] if len(file_downloaded.split(".")) > 1 else ".jpeg"
        filename = c_id + "." + extension
        with open(self.downloads_path + file_downloaded, "rb") as f:
            base64_body = b64encode(f.read()).decode("utf-8")
        for i in downloads_after:
            remove(self.downloads_path + i)
        return base64_body, mimetype, type_, extension, filename, caption, time_text, c_id, datetime.now().strftime(f"%Y-%m-%d %H:%M:%S")
    
    def extract_data_id_from_html(self, html_string):
        match = search(r'data-id="([^"]+)"', html_string)
        if match:
            return match.group(1)
        return None

    def extrair_mensagens(self, html):
        soup = BeautifulSoup(html, "html.parser")
        mensagem_final = ""

        for div in soup.select("div.copyable-text"):
            # Remove spans com horário
            for span in div.find_all("span"):
                texto = span.get_text()
                if ":" in texto and len(texto.strip()) <= 5 and texto.replace(":", "").isdigit():
                    span.decompose()

            # Substitui emojis e links
            for tag in div.find_all(True):
                if tag.has_attr("data-plain-text"):
                    tag.replace_with(tag["data-plain-text"])
                elif tag.name == "a" and tag.has_attr("href"):
                    tag.replace_with(tag["href"])

            # Captura o texto com espaços mínimos
            mensagem = div.get_text(separator=" ")

            # Normaliza múltiplos espaços e espaços antes de pontuação
            mensagem = sub(r'\s+', ' ', mensagem)                     # múltiplos espaços => um espaço
            mensagem = sub(r'\s+([.,;:!?])', r'\1', mensagem)         # remove espaço antes de pontuação

            if mensagem.strip():
                mensagem_final += mensagem.strip() + "\n"

        return mensagem_final.strip()

    def getTextMessage(self, el):
        body = self.extrair_mensagens(el.get_attribute("innerHTML"))
        time = el.find_element(By.XPATH, self.xpaths['messagesTime']).text
        id = el.get_attribute(self.xpaths['messagesIdAttr'])
        if id is None:
            id = self.extract_data_id_from_html(el.get_attribute("innerHTML"))
        id = id.split("_")[-1]
        id = id if len(id) <= 36 else id[:35]
        return body, time, id, datetime.now().strftime(f"%Y-%m-%d %H:%M:%S")

    def getTextWithEmojis(self, el, caption_xpath):
        innerHTML = el.find_element(By.XPATH, caption_xpath).get_attribute("innerHTML")
        innerHTML = self.re_inn_html.split(innerHTML)
        body = ''
        for i in innerHTML:
            if i == '':
                continue
            elif not 'data-plain-text=' in i:
                body += i
            else:
                body += i.split('data-plain-text="')[1].split('"')[0]
        return body

    def getBase64String(self, uri):
        sleep(1)
        base64Content = self.driver.execute_async_script("""
            var uri = arguments[0];
            var callback = arguments[1];
            var toBase64 = function(buffer){for(var r,n=new Uint8Array(buffer),t=n.length,a=new Uint8Array(4*Math.ceil(t/3)),i=new Uint8Array(64),o=0,c=0;64>c;++c)i[c]="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charCodeAt(c);for(c=0;t-t%3>c;c+=3,o+=4)r=n[c]<<16|n[c+1]<<8|n[c+2],a[o]=i[r>>18],a[o+1]=i[r>>12&63],a[o+2]=i[r>>6&63],a[o+3]=i[63&r];return t%3===1?(r=n[t-1],a[o]=i[r>>2],a[o+1]=i[r<<4&63],a[o+2]=61,a[o+3]=61):t%3===2&&(r=(n[t-2]<<8)+n[t-1],a[o]=i[r>>10],a[o+1]=i[r>>4&63],a[o+2]=i[r<<2&63],a[o+3]=61),new TextDecoder("ascii").decode(a)};
            var xhr = new XMLHttpRequest();
            xhr.responseType = 'arraybuffer';
            xhr.onload = function(){ callback(toBase64(xhr.response)) };
            xhr.onerror = function(){ callback(xhr.status) };
            xhr.open('GET', uri);
            xhr.send();
        """, uri)
        if type(base64Content) == int :
            self.log.error(f"{self.device} - Error getting file content")
            return None
        else:
            return base64Content

    def getOrdenedChats(self):
        try:
            count = 0
            while not self.elementExistsInDriver(self.xpaths['chatsList']):
                sleep(.1)
                count += 1
                if count > 10:
                    return []
            chatElements = self.driver.find_elements(By.XPATH, self.xpaths['chatsList'])
            ChatElementsDict = {}
            sortingKeys = []
            for i in chatElements:
                try:
                    idx = int(i.get_attribute(self.xpaths['chatsIndexAttr']).split("translateY(")[-1].split("px")[0])
                    sortingKeys.append(idx)
                    ChatElementsDict[idx] = i
                except:
                    continue
            sortingKeys.sort()
            chatElements = []
            for i in sortingKeys:
                chatElements.append(ChatElementsDict[i])
            return chatElements
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": f"Error getOrdenedChats function: {e}",
                    "contact": ''
                }
            )
            self.log.error(f"Error getOrdenedChats function: {e}")
            self.close()

    def scrollUpMessages(self, last_readed_id, n_scrolls=0):
        start_time = time()
        max_time = 5
        if last_readed_id:
            while not self.elementExistsInDriver(self.xpaths['messagesOut']) and not self.elementExistsInDriver(self.xpaths['messagesIn']):
                end_time = time()
                if end_time - start_time > max_time:
                    break
                else:
                    sleep(1)
            msgs = self.driver.find_elements(By.XPATH, self.xpaths['messagesIn'])
            reading_ids = []
            for i in msgs:
                id = i.get_attribute(self.xpaths['messagesIdAttr'])
                if id is None:
                    id = self.extract_data_id_from_html(i.get_attribute("innerHTML"))
                if id:
                    id = id.split("_")[-1]
                    id = id if len(id) <= 36 else id[:35]
                else:
                    id = i.find_element(By.XPATH, "./..")
                    id = id.get_attribute(self.xpaths['messagesIdAttr']).split("_")[-1]
                    id = id if len(id) <= 36 else id[:35]
                reading_ids.append(id)
            if not last_readed_id in reading_ids:
                try:
                    self.driver.find_element(By.XPATH, self.xpaths['chatPanel']).send_keys(Keys.PAGE_UP)
                except:
                    pass
                if n_scrolls < 10:
                    return self.scrollUpMessages(last_readed_id, n_scrolls+1)
                else:
                    return True
            else:
                return True
        else:
            while not self.elementExistsInDriver(self.xpaths['messagesOut']) and not self.elementExistsInDriver(self.xpaths['messagesIn']):
                end_time = time()
                if end_time - start_time > max_time:
                    break
                else:
                    sleep(1)
            count = 0
            while not self.elementExistsInDriver(self.xpaths['topOfChat']):
                if count < 10:
                    self.driver.find_element(By.XPATH, self.xpaths['chatPanel']).send_keys(Keys.PAGE_UP)
                    count += 1
                else:
                    break
            return True

    def getChatPhone(self):
        while not self.elementExistsInDriver(self.xpaths['chatPhoneNumber']):
            sleep(1)
        WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, self.xpaths['chatPhoneNumber'])))
        phone_name = self.driver.find_element(By.XPATH, self.xpaths['chatPhoneNumber']).text
        try:
            phone_number = phone_name.split(" ")
            nine = "9" if int(phone_number[2][0]) > 5 and len(phone_number[2]) == 9 else ""
            phone_number = phone_number[0][1:] + phone_number[1] + nine + phone_number[2].replace("-", "")
        except:
            phone_number = phone_name
        return phone_name, phone_number

    def identifyChat(self, contact):
        try:
            chatOk = False
            while not chatOk:
                self.verifyArchiveChats()
                chats = self.getOrdenedChats()
                numbers = []
                c = 0
                for i in chats:
                    try:
                        phone_number = i.find_element(By.XPATH, self.xpaths['chatsListNames']).text.split(" ")
                        nine = "9" if int(phone_number[2][0]) > 5 and len(phone_number[2]) == 9 else ""
                        phone_number = phone_number[0][1:] + phone_number[1] + nine + phone_number[2].replace("-", "")
                        numbers.append((phone_number, c))
                    except:
                        numbers.append((None, c))
                    c += 1
                c = 0
                idx = -1
                for i in numbers:
                    if i[0] is not None:
                        if contact[2:4] in i[0] and contact[-8:] in i[0]:
                            idx = c
                            break
                    c += 1
                if idx != -1:
                    chats[idx].click()
                    _, chat_phone = self.getChatPhone()
                    if contact == chat_phone or (contact[2:4] in chat_phone and contact[-8:] in chat_phone):
                        chatOk = True
                else:
                    break
            return chatOk
        except:
            return False

    def sendWritingMessage(self, message):
        WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, self.xpaths['sendTextBox'])))
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, self.xpaths['sendTextBox'])))
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, self.xpaths['sendTextBox'])))
        text_box = self.driver.find_element(By.XPATH, self.xpaths['sendTextBox'])
        text_box.click()
        re_split = message.split('\\r\\n')
        message_list = []
        for i in re_split:
            j = i.split('\\n')
            for k in j:
                final_message = k.split('<br />')
                for msg in final_message:
                    m = msg.replace('\t', '   ')
                    message_list.append(m)
        need_final = False
        final_message_list = []
        for i in message_list:
            if '\r\n' in i:
                need_final = True
            j = i.split('\r\n')
            for k in j:
                if '\n' in k:
                    need_final = True
                l = k.split('\n')
                for m in l:
                    final_message_list.append(m)
        if need_final:
            list_to_send = final_message_list
        else:
            list_to_send = message_list
        char_multiplier = self.getAPIConfig(int(self.xpaths["charMultiplier"]))
        time_divisor = self.getAPIConfig(int(self.xpaths["timeDivisor"]))
        for i in list_to_send:
            ilength = len(i)
            if ilength > 300:
                mintime = 0.03 / time_divisor
                maxtime = 0.10 / time_divisor
                jlength = 10 * char_multiplier
            elif ilength > 200:
                mintime = 0.05 / time_divisor
                maxtime = 0.15 / time_divisor
                jlength = 7 * char_multiplier
            elif ilength > 100:
                mintime = 0.07 / time_divisor
                maxtime = 0.17 / time_divisor
                jlength = 5 * char_multiplier
            elif ilength > 50:
                mintime = 0.10 / time_divisor
                maxtime = 0.20 / time_divisor
                jlength = 3 * char_multiplier
            elif ilength > 25:
                mintime = 0.15 / time_divisor
                maxtime = 0.22 / time_divisor
                jlength = 2 * char_multiplier
            elif ilength > 10:
                mintime = 0.20 / time_divisor
                maxtime = 0.25 / time_divisor
                jlength = 2 * char_multiplier
            else:
                mintime = 0.65
                maxtime = 0.95
                jlength = 1
            for j in range(0, ilength, jlength):
                text_box.send_keys(i[j:j+jlength])
                sleep(round(uniform(mintime, maxtime), 2))
            text_box.send_keys(Keys.SHIFT, Keys.ENTER)
        sleep(round(uniform(0, 1), 2))
        for i in range(5):
            try:
                text_box.send_keys(Keys.ENTER)
            except:
                pass
        sleep(round(uniform(0, 1), 2))

    def tryEnterInChat(self, contact):
        try:
            chats = self.getOrdenedChats()
            for i in chats:
                phone_number = i.find_element(By.XPATH, self.xpaths['chatsListNames']).text.split(" ")
                ddd = phone_number[1]
                phone_number = phone_number[-1].split("-")
                if ddd in contact and phone_number[0][1:] in contact and phone_number[1] in contact:
                    i.click()
                    return
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": f"Error tryEnterInChat function: {e}",
                    "contact": ''
                }
            )
            self.log.error(f"Error tryEnterInChat function: {e}")
            self.close()

    def sendMessageText(self, msg_id, contact, message):
        try:
            self.log.info("Sending text message...")
            if self.driver.execute_script("return typeof(whatsgw)") == 'undefined':
                self.injectClientJS()
                for _ in range(70):
                    sleep(.1)
                # self.driver.implicitly_wait(15)
            chatOk = self.identifyChat(contact)
            n_emojis = emoji_count(message)
            if (self.last_contact == contact or chatOk) and n_emojis == 0:
                self.sendWritingMessage(message)
                self.last_contact = contact
            else:
                send_msg = False
                def_contact = int(contact[2])
                pref = contact[:4]
                suff = contact[4:]
                if len(pref) == 4 and len(suff) >= 8:
                    if def_contact == 2 or def_contact == 1:
                        if len(suff) == 8:
                            if int(suff[0]) > 5:
                                contact = pref + '9' + suff
                            send_msg = True
                        elif len(suff) == 9:
                            contact = pref + suff
                            send_msg = True
                        else:
                            self.log.warning(f"Contact phone number is invalid {contact}")
                            self.updateContactPhoneNumber(contact, False)
                    else:
                        if len(suff) == 9:
                            contact = pref + suff[1:]
                            send_msg = True
                        elif len(suff) == 8:
                            contact = pref + suff
                            send_msg = True
                        else:
                            self.log.warning(f"Contact phone number is invalid {contact}")
                            self.updateContactPhoneNumber(contact, False)
                else:
                    self.log.warning(f"Contact phone number is invalid {contact}")
                    self.updateContactPhoneNumber(contact, False)
                if send_msg:
                    self.log.info(f"Sending message from {self.device}")
                    message_body = message.encode('unicode-escape').decode()
                    message_body = message_body.replace('"', '\\"')
                    emojis_found = self.re_emoji.findall(message_body)
                    for emoji in emojis_found:
                        message_body = message_body.replace(emoji, '" + String.fromCodePoint(parseInt (' + f"'{emoji[2:]}'" + ', 16)) + "')
                    msg_str_var = '{"type":"_wabc_","msg":{"cmd":"chat","msg":{"to":"' + contact + '","chat_type":"1","custom_uid":"100000000","body":{"title":"","desc":"","url":null,"base64":null,"mime_types":null,"filename":null,"thumb":"","text":"' + message_body + '","w_mensagem_tipo":1}},"w_telefone_id":0,"instancia_id":0,"data":null,"data2":null,"footer":null,"buttonText":null,"headerType":0,"buttons":null,"templateButtons":null,"sections":null,"poll":null}}'
                    sleep(round(uniform(1.5, 2), 2))
                    self.driver.execute_script(f'let message = {msg_str_var}; window.postMessage(message, "*");')
                    sleep(round(uniform(1, 2), 2))
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'message',
                    "message": message,
                    "contact": contact
                }
            )
            if contact == self.greeting_number and self.greetings_panel == 1:
                self.sendGreetingsAPI(message)
            if type(msg_id) == int:
                self.updateSendMessage(msg_id)
            else:
                for i in msg_id:
                    self.updateSendMessage(i)
            self.setDeviceInTitle()
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": "Error sendMessageText function: " + str(e),
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error sendMessageText function: " + str(e))
            self.close()

    def injectGreetingImage(self):
        try:
            with open('sendImageJS.js') as f:
                sendTextScript = f.read().rstrip()
            self.driver.execute_script(sendTextScript)
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": f"Error in injectGreetingImage function: {e}",
                    "contact": ''
                }
            )
            self.log.error(f"Error in injectGreetingImage function: {e}")
            self.close()

    def sendGreetingFakeImage(self, msg_id, contact):
        try:
            self.log.info("Sending greeting image message...")
            def_contact = int(contact[2])
            pref = contact[:4]
            suff = contact[4:]
            if len(pref) == 4 and len(suff) >= 8:
                if def_contact == 2 or def_contact == 1:
                    if len(suff) == 8:
                        if int(suff[0]) > 5:
                            contact = pref + '9' + suff
                    elif len(suff) == 9:
                        contact = pref + suff
                    else:
                        self.log.warning(f"Contact phone number is invalid {contact}")
                        self.updateContactPhoneNumber(contact, False)
                else:
                    if len(suff) == 9:
                        contact = pref + suff[1:]
                    elif len(suff) == 8:
                        contact = pref + suff
                    else:
                        self.log.warning(f"Contact phone number is invalid {contact}")
                        self.updateContactPhoneNumber(contact, False)
            else:
                self.log.warning(f"Contact phone number is invalid {contact}")
                self.updateContactPhoneNumber(contact, False)
            if self.driver.execute_script("return typeof(cda2msg)") == 'undefined':
                self.injectGreetingImage()
                sleep(6)
            self.log.info(f"Sending message from {self.device}")
            # ☉¡ σ¡ ð¡ ○¡ ○¡ ○i Ｏ¡ ◯◴◵◶◷❍ₒ॰°৹๐º𐤏Ｏ⦿⊕⊗⨷ ◯¡  --  ○¡  -- ○¡ - ○¡
            # messages_list = ['○ ¡', '❍ ¡'] # ['◯¡', '○¡', '❍¡'] # , 'ₒ¡', '๐¡', '𐤏¡',]
            msg_str_var = '{"msg":{"to":"","url":"○¡","desc":"○¡","thumb":""}}'
            if datetime.now().hour < 12:
                thumb = "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"
            elif datetime.now().hour < 18:
                thumb = "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"
            else:
                thumb = "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"
            message_choice = choice(self.setGreetings())
            script_str = f'let message = {msg_str_var}; message.msg.desc = "{message_choice}"; message.msg.url = "{message_choice}"; message.msg.to = "{contact}"; message.msg.thumb = "{thumb}"; cda2msg.onScriptMessage(message);'
            sleep(round(uniform(1.5, 2), 2))
            self.driver.execute_script(script_str)
            self.updateSendMessage(msg_id)
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'greeting',
                    "message": f"{message_choice} [ Fake Image ]",
                    "contact": contact
                }
            )
            sleep(round(uniform(1, 2), 2))
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": "Error sendGreetingFakeImage function: " + str(e),
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error sendGreetingFakeImage function: " + str(e))
            self.close()

    def sendMessageWithLink(self, contact, message): 
        url = CDACob.__sendURL + contact + "&text=" + message
        self.driver.get(url)
        # sleep(1)
        try:
            c = 0
            while not self.pageLoaded():
                sleep(1)
                c += 1
                if c > 15:
                    break
        except:
            pass
        c = 0
        for i in range(100):
            sleep(.1)
        while not self.elementExistsInDriver(self.xpaths['attachButton']) and not self.elementExistsInDriver(self.xpaths['popUpError']):
            sleep(1)
            c += 1
            if c > 20:
                break
        sleep(0.5)
        try:
            WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.XPATH, self.xpaths['sendMessageButton'])))
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, self.xpaths['sendMessageButton'])))
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, self.xpaths['sendMessageButton'])))
        except:
            pass
        if self.elementExistsInDriver(self.xpaths['sendMessageButton']):
            try:
                while self.elementExistsInDriver(self.xpaths['sendMessageButton']):
                    self.driver.find_element(By.XPATH, self.xpaths['sendMessageButton']).click()
            except:
                pass
        elif self.elementExistsInDriver(self.xpaths['popUpError']):
            self.ac.send_keys(Keys.ESCAPE).perform()
        else:
            self.ac.send_keys(Keys.ESCAPE).perform()

    def getEnviaCorpoSaudacao(self, msg_id):
        message_body = get(
            self.xpaths["api"] + "envia_corpo_saudacao",
            params = { "message_id": msg_id }
        )
        if message_body.status_code == 200:
            texto = message_body.text
            return texto if "'NoneType'" not in texto else ""
        else:
            self.log.error("Last ID not found")
            return None

    def sendMessageGreeting(self, msg_id, contact, message_body):
        try:
            self.log.info("Sending greeting message...")
            update = True
            if contact == self.greeting_number and self.greetings_panel == 1:
                self.sendMessageText(msg_id, contact, message_body)
                update = False
            message = self.getEnviaCorpoSaudacao(msg_id)
            message = message if message else choice(self.setGreetings())
            if self.send_with_link:
                self.sendMessageWithLink(contact, message)
            elif contact != self.greeting_number and self.greetings_panel == 0:
                if self.driver.execute_script("return typeof(whatsgw)") == 'undefined':
                    self.injectClientJS()
                    for _ in range(70):
                        sleep(.1)
                    # self.driver.implicitly_wait(15)
                def_contact = int(contact[2])
                pref = contact[:4]
                suff = contact[4:]
                if len(pref) == 4 and len(suff) >= 8:
                    if def_contact == 2 or def_contact == 1:
                        if len(suff) == 8:
                            if int(suff[0]) > 5:
                                contact = pref + '9' + suff
                        elif len(suff) == 9:
                            contact = pref + suff
                        else:
                            self.log.warning(f"Contact phone number is invalid {contact}")
                            self.updateContactPhoneNumber(contact, False)
                    else:
                        if len(suff) == 9:
                            contact = pref + suff[1:]
                        elif len(suff) == 8:
                            contact = pref + suff
                        else:
                            self.log.warning(f"Contact phone number is invalid {contact}")
                            self.updateContactPhoneNumber(contact, False)
                else:
                    self.log.warning(f"Contact phone number is invalid {contact}")
                    self.updateContactPhoneNumber(contact, False)
                msg_str_var = '{"type":"_wabc_","msg":{"cmd":"chat","msg":{"to":"' + contact + '","chat_type":"1","custom_uid":"100000000","body":{"title":"","desc":"","url":null,"base64":null,"mime_types":null,"filename":null,"thumb":"","text":"' + message + '","w_mensagem_tipo":1}},"w_telefone_id":0,"instancia_id":0,"data":null,"data2":null,"footer":null,"buttonText":null,"headerType":0,"buttons":null,"templateButtons":null,"sections":null,"poll":null}}'
                for _ in range(randint(15, 20)):
                    sleep(.1)
                self.driver.execute_script(f'let message = {msg_str_var}; window.postMessage(message, "*");')

                for _ in range(70):
                    sleep(.1)

                self.log.info(f"######## SAUDAÇÃO -- {self.device} ({message}) CLIENTE: {contact}")
            if update:
                self.updateSendMessage(msg_id)
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'greeting',
                    "message": f"{message}",
                    "contact": contact
                }
            )
            sleep(round(uniform(1, 2), 2))
            self.setDeviceInTitle()
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": "Error sendMessageGreeting function: " + str(e),
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error sendMessageGreeting function: " + str(e))
            self.close()
        
    def checkChats(self):
        try:
            list_changed = True
            while list_changed:
                list_changed = False
                chats = self.getOrdenedChats()[:int(self.xpaths['verifyArchive'])]
                chat_list = []
                for i in chats:
                    chat_name = i.find_element(By.XPATH, self.xpaths['chatsListNames']).text.strip()
                    chat_list.append(chat_name.replace(' ', '').replace('+', '').replace('-','').strip())
            return chat_list
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": "Error on checkChats function: " + str(e),
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error on checkChats function: " + str(e))
            self.close()

    def injectClientJS(self):
        try:
            with open('clientJS.js') as f:
                sendTextScript = f.read().rstrip()
            self.driver.execute_script(sendTextScript)
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": f"Error in injectClientJS function: {e}",
                    "contact": ''
                }
            )
            self.log.error(f"Error in injectClientJS function: {e}")
            self.close()

    def sendMessageImage(self, msg_id, contact):
        try:
            if self.driver.execute_script("return typeof(whatsgw)") == 'undefined':
                self.injectClientJS()
                for _ in range(70):
                    sleep(.1)
                # self.driver.implicitly_wait(15)
            self.log.info("Sending greeting image message...")
            def_contact = int(contact[2])
            pref = contact[:4]
            suff = contact[4:]
            if len(pref) == 4 and len(suff) >= 8:
                if def_contact == 2 or def_contact == 1:
                    if len(suff) == 8:
                        if int(suff[0]) > 5:
                            contact = pref + '9' + suff
                    elif len(suff) == 9:
                        contact = pref + suff
                    else:
                        self.log.warning(f"Contact phone number is invalid {contact}")
                        self.updateContactPhoneNumber(contact, False)
                else:
                    if len(suff) == 9:
                        contact = pref + suff[1:]
                    elif len(suff) == 8:
                        contact = pref + suff
                    else:
                        self.log.warning(f"Contact phone number is invalid {contact}")
                        self.updateContactPhoneNumber(contact, False)
            else:
                self.log.warning(f"Contact phone number is invalid {contact}")
                self.updateContactPhoneNumber(contact, False)
            self.log.info(f"Sending message from {self.device}")
            msg_str_var = '{"type":"_wabc_","msg":{"cmd":"media","msg":{"to":"","chat_type":"1","custom_uid":"100000000","body":{"title":"","desc":"","url":null,"base64":"","mime_types":"image/png","filename":"","thumb":"","text":"","w_mensagem_tipo":2}},"w_telefone_id":0,"instancia_id":0,"data":null,"data2":null,"footer":null,"buttonText":null,"headerType":0,"buttons":null,"templateButtons":null,"sections":null,"poll":null}}'
            if datetime.now().hour < 12:
                thumb = "data:image/png;base64,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AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA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AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAR/x+OodXCR/b6NAAAAABJRU5ErkJggg=="
            elif datetime.now().hour < 18:
                thumb = "data:image/png;base64,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AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA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AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAg4v8BwuU2Z4GqVhcAAAAASUVORK5CYII="
            else:
                thumb = "data:image/png;base64,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AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA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AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACO9hm1AAABdElEQVQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABH/D3FCyqNF1/TtAAAAAElFTkSuQmCC"
            sleep(round(uniform(1.5, 2), 2))
            self.driver.execute_script(f'let message = {msg_str_var}; message.msg.msg.to = "{contact}"; message.msg.msg.body.base64 = "{thumb}"; message.msg.msg.body.filename = "{choice(self.filename_list)}.png"; window.postMessage(message, "*");')
            self.updateSendMessage(msg_id)
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'greeting',
                    "message": "Imagem",
                    "contact": contact
                }
            )
            sleep(round(uniform(1, 2), 2))
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": "Error sendMessageImage function: " + str(e),
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error sendMessageImage function: " + str(e))
            self.close()

    def sendGreetingsAPI(self, message):
        try:
            post_greeting_api = post(
                "http://192.168.7.100:8080/api_msg",
                data = {
                    "device_id": self.device_id,
                    "device": self.device,
                    "data": message
                }
            )
            if post_greeting_api.status_code == 200:
                self.log.info("Inserted on Greetings API")
            else:
                self.log.error(f"{self.device} - Error on sendGreetingsAPI")
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": "Error on sendGreetingsAPI function: " + str(e),
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error on sendGreetingsAPI function: " + str(e))
            self.close()

    def sendAttachedMessage(self, id, contact, b64_body, caption, flname, custom_id, mimetype):
        try:
            self.log.info("Sending attached message...")
            error_counter_bfr = len(self.driver.find_elements(By.XPATH, self.xpaths['attachSendError']))
            file_path = self.downloads_path + custom_id + "." + mimetype.split("/")[-1]
            with open(file_path, "wb") as new_file:
                new_file.write(b64decode(b64_body))
            if caption == None or caption == "" or caption == " ":
                caption = contact + "_" + flname
            chatOk = self.identifyChat(contact)
            if chatOk or self.last_contact == contact:
                caption = caption.replace('\\r\\n', '\n')
                self.driver.find_element(By.XPATH, self.xpaths['sendTextBox']).send_keys(caption)
            else:
                caption = caption.replace('\\r\\n', '%0D%0A')
                caption = caption.replace('\\n', '%0D%0A')
                url = CDACob.__sendURL + contact + "&text=" + caption
                self.driver.get(url)
                # sleep(1)
            try:
                c = 0
                while not self.pageLoaded():
                    sleep(1)
                    c += 1
                    if c > 15:
                        break
            except:
                pass
            c = 0
            for i in range(100):
                sleep(.1)
            for i in range(30):
                sleep(.1)
            while not self.elementExistsInDriver(self.xpaths['attachButton']) and not self.elementExistsInDriver(self.xpaths['popUpError']):
                sleep(1)
                c += 1
                if c > 20:
                    break
            for i in range(30):
                sleep(.1)
            if self.elementExistsInDriver(self.xpaths['attachButton']):
                self.log.info("Contact phone number is valid")
                WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, self.xpaths['attachButton'])))
                WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, self.xpaths['attachButton'])))
                WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, self.xpaths['attachButton'])))
                self.driver.find_element(By.XPATH, self.xpaths['attachButton']).click()
                mime_type = mimetype.split("/")[0]
                if mime_type == 'image' or mime_type == 'video':
                    attach = self.xpaths['attachStream']
                else:
                    attach = self.xpaths['attachFile']
                while not self.CSSExistsInDriver(attach):
                    sleep(1)
                self.driver.find_element(By.CSS_SELECTOR, attach).send_keys(file_path)
                while not self.elementExistsInDriver(self.xpaths['attachSendButton']):
                    sleep(1)
                WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, self.xpaths['attachSendButton'])))
                WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, self.xpaths['attachSendButton'])))
                WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, self.xpaths['attachSendButton'])))
                if 0.1 * len(caption) > 3:
                    sleep(3)
                else:
                    sleep(0.1 * len(caption))
                for _ in range(30):
                    try:
                        self.driver.find_element(By.XPATH, self.xpaths['attachSendButton']).click()
                    except:
                        pass
                while self.elementExistsInDriver(self.xpaths['attachUploading']):
                    sleep(1)
                sleep(3)
                error_counter_atr = len(self.driver.find_elements(By.XPATH, self.xpaths['attachSendError']))
                if error_counter_bfr != error_counter_atr:
                    sleep(.5)
                    resend_buttons = self.driver.find_elements(By.XPATH, self.xpaths['attachResend'])
                    for i in resend_buttons:
                        sleep(.3)
                        i.click()
                        sleep(1)
                        while self.elementExistsInDriver(self.xpaths['attachUploading']):
                            sleep(1)
                        sleep(3)
                self.updateContactPhoneNumber(contact, True)
            elif self.elementExistsInDriver(self.xpaths['popUpError']):
                self.log.warning("Contact phone number is invalid")
                self.updateContactPhoneNumber(contact, False)
                self.ac.send_keys(Keys.ESCAPE).perform()
            else:
                self.close()
            self.updateSendMessage(id)
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'message',
                    "message": mimetype,
                    "contact": contact
                }
            )
            self.okToSpam()
            self.setDeviceInTitle()
            sleep(round(uniform(0.3, 0.7), 2))
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": "Error sendAttachedMessage function: " + str(e),
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error sendAttachedMessage function: " + str(e))
            self.close()

    def okToSpam(self):
        try:
            if self.elementExistsInDriver(self.xpaths['spamBanner']):
                WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, self.xpaths['okNotSpam'])))
                self.driver.find_element(By.XPATH, self.xpaths['okNotSpam']).click()
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": "Error okToSpam function: " + str(e),
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error okToSpam function: " + str(e))
            self.close()

    def pageLoaded(self):
        try:
            # while self.driver.execute_script("return document.readyState;").lower() != "complete":
            for _ in range(10):
                try:
                    WebDriverWait(self.driver, 2).until(EC.alert_is_present())
                    alt_clk = self.driver.switch_to.alert
                    alt_clk.accept()
                except:
                    break
                WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located((By.ID, self.xpaths['paneSideID']))
                )
            return True
        except TimeoutException:
            return False
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": "Error on pageLoaded function: " + str(e),
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error on pageLoaded function: " + str(e))
            self.close()

    def updateContactPhoneNumber(self, number, isvalid):
        try:
            if isvalid:
                route = "valid_contact_phone"
            else:
                route = "invalid_contact_phone"
            send_contact_isvalid = post(
                self.xpaths["api"] + route,
                params = {
                    "number": number
                }
            )
            if send_contact_isvalid.status_code == 200:
                self.log.info("Contact phone number updated")
            else:
                self.log.error(f"{self.device} - Error on update contact phone number")
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": "Error on updateContactPhoneNumber function: " + str(e),
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error on updateContactPhoneNumber function: " + str(e))
            self.close()

    def updateSendMessage(self, id):
        try:
            send_message = get(
                self.xpaths["api"] + "update_send_message",
                params = {
                    "id": id,
                    "sended_at": datetime.now()
                }
            )
            if send_message.status_code == 200:
                self.log.info("Message sent")
            else:
                self.log.error(f"{self.device} - Error on send message or not updated in database")
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": "Error on updateSendMessage function: " + str(e),
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error on updateSendMessage function: " + str(e))
            self.close()

    def sendPrankMessage(self, message_id, contact, message_body) -> None:
        try:
            chat_type = '1'
            if self.send_with_link:
                self.sendMessageWithLink(contact, message_body)
            else:
                if self.driver.execute_script("return typeof(whatsgw)") == 'undefined':
                    self.injectClientJS()
                    for _ in range(70):
                        sleep(.1)
                    # self.driver.implicitly_wait(15)
                self.log.info("Sending prank message...")
                def_contact = int(contact[2])
                pref = contact[:4]
                suff = contact[4:]
                if len(pref) == 4 and len(suff) >= 8:
                    if def_contact == 2 or def_contact == 1:
                        if len(suff) == 8:
                            if int(suff[0]) > 5:
                                contact = pref + '9' + suff
                        elif len(suff) == 9:
                            contact = pref + suff
                        else:
                            self.log.warning(f"Contact phone number is invalid {contact}")
                            self.updateContactPhoneNumber(contact, False)
                    else:
                        if len(suff) == 9:
                            contact = pref + suff[1:]
                        elif len(suff) == 8:
                            contact = pref + suff
                        else:
                            self.log.warning(f"Contact phone number is invalid {contact}")
                            self.updateContactPhoneNumber(contact, False)
                else:
                    self.log.warning(f"Contact phone number is invalid {contact}")
                    self.updateContactPhoneNumber(contact, False)
                self.log.info(f"Sending prank message from {self.device}")
                if self.prank_send_media:
                    chat_type = '1'

                    ratio_weights = [
                        (self.prank_image_ratio, 'image'),
                        (self.prank_document_ratio, 'document'),
                        (self.prank_video_ratio, 'video'),
                        (self.prank_audio_ratio, 'audio')
                    ]
                    ratio_weights.sort(key=lambda x: x[0])
                    random_value = round(uniform(0, 1), 2)

                    msgtype_test = False
                    for ratio, msgtype in ratio_weights:
                        if random_value < ratio:
                            msgtype_test = True
                            break
                    
                    if msgtype_test:
                        chat_type = '2'
                        if msgtype == 'image':
                            mimetype = 'image/png'
                            extension = '.png'
                        elif msgtype == 'document':
                            mimetype = 'application/pdf'
                            extension = '.pdf'
                        elif msgtype == 'video':
                            mimetype = 'video/mp4'
                            extension = '.mp4'
                        elif msgtype == 'audio':
                            mimetype = 'audio/ogg; codecs=opus'
                            extension = '.ogg'
                            chat_type = '8'

                if chat_type == '1':
                    msg_str_var = '{"type":"_wabc_","msg":{"cmd":"chat","msg":{"to":"' + contact + '","chat_type":"1","custom_uid":"100000000","body":{"title":"","desc":"","url":null,"base64":null,"mime_types":null,"filename":null,"thumb":"","text":"' + message_body + '","w_mensagem_tipo":' + chat_type + '}},"w_telefone_id":0,"instancia_id":0,"data":null,"data2":null,"footer":null,"buttonText":null,"headerType":0,"buttons":null,"templateButtons":null,"sections":null,"poll":null}}'
                else:
                    if round(uniform(0, 1), 2) < 0.2 and chat_type == '2':
                        message_body = message_body
                    else:
                        message_body = ''
                    msg_str_var = '{"type":"_wabc_","msg":{"cmd":"media","msg":{"to":"' + contact + '","chat_type":"1","custom_uid":"100000000","body":{"title":"' + message_body + '","desc":"","url":null,"base64":"' + self.getPrankBase64(msgtype) + '","mime_types":"' + mimetype + '","filename":"' + choice(self.filename_list) + extension + '","thumb":"","text":"","w_mensagem_tipo":' + chat_type + '}},"w_telefone_id":0,"instancia_id":0,"data":null,"data2":null,"footer":null,"buttonText":null,"headerType":0,"buttons":null,"templateButtons":null,"sections":null,"poll":null}}'
                sleep(round(uniform(self.min_prank_time, self.max_prank_time), 2))
                self.driver.execute_script(f'let message = {msg_str_var}; window.postMessage(message, "*");')
                sleep(10)
            self.updateSendMessage(message_id)
            if chat_type != '1':
                message_body = msgtype
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'prank',
                    "message": message_body,
                    "contact": contact
                }
            )
            sleep(round(uniform(self.min_prank_time, self.max_prank_time), 2))
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": "Error on sendPrankMessage function: " + str(e),
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error on sendPrankMessage function: " + str(e))
            self.close()

    def sendGreetingAudio(self, message_id, contact) -> None:
        try:
            if self.driver.execute_script("return typeof(whatsgw)") == 'undefined':
                self.injectClientJS()
                for _ in range(70):
                    sleep(.1)
                # self.driver.implicitly_wait(15)
            self.log.info("Sending prank message...")
            def_contact = int(contact[2])
            pref = contact[:4]
            suff = contact[4:]
            if len(pref) == 4 and len(suff) >= 8:
                if def_contact == 2 or def_contact == 1:
                    if len(suff) == 8:
                        if int(suff[0]) > 5:
                            contact = pref + '9' + suff
                    elif len(suff) == 9:
                        contact = pref + suff
                    else:
                        self.log.warning(f"Contact phone number is invalid {contact}")
                        self.updateContactPhoneNumber(contact, False)
                else:
                    if len(suff) == 9:
                        contact = pref + suff[1:]
                    elif len(suff) == 8:
                        contact = pref + suff
                    else:
                        self.log.warning(f"Contact phone number is invalid {contact}")
                        self.updateContactPhoneNumber(contact, False)
            else:
                self.log.warning(f"Contact phone number is invalid {contact}")
                self.updateContactPhoneNumber(contact, False)
            self.log.info(f"Sending prank message from {self.device}")
            msg_str_var = '{"type":"_wabc_","msg":{"cmd":"media","msg":{"to":"' + contact + '","chat_type":"1","custom_uid":"100000000","body":{"title":"","desc":"","url":null,"base64":"' + self.getPrankBase64('audio', True) + '","mime_types":"audio/ogg; codecs=opus","filename":"' + choice(self.filename_list) + '.ogg","thumb":"","text":"","w_mensagem_tipo":8}},"w_telefone_id":0,"instancia_id":0,"data":null,"data2":null,"footer":null,"buttonText":null,"headerType":0,"buttons":null,"templateButtons":null,"sections":null,"poll":null}}'
            sleep(round(uniform(self.min_prank_time, self.max_prank_time), 2))
            self.driver.execute_script(f'let message = {msg_str_var}; window.postMessage(message, "*");')
            self.updateSendMessage(message_id)
            sleep(10)
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'greeting',
                    "message": 'audio',
                    "contact": contact
                }
            )
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": "Error on sendGreetingAudio function: " + str(e),
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error on sendGreetingAudio function: " + str(e))
            self.close()

    def getPrankBase64(self, msgtype, greeting=False):
        try:
            filefolder = self.xpaths['localPath'] + '\\guicob\\' + msgtype
            if greeting:
                file = ['greeting1.ogg', 'greeting2.ogg']
            else:
                file = self.getListFilenameFromFolder(filefolder)
            return self.getBase64FromFile(filefolder + '\\' + choice(file))
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": "Error on getPrankBase64 function: " + str(e),
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error on getPrankBase64 function: " + str(e))
            self.close()

    def getListFilenameFromFolder(self, folder):
        try:
            return [f for f in listdir(folder) if isfile(join(folder, f))]
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": "Error on getListFilenameFromFolder function: " + str(e),
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error on getListFilenameFromFolder function: " + str(e))
            self.close()

    def getBase64FromFile(self, file):
        mime = guess_type(file)[0]
        mime = mime if mime else file.split('.')[-1]
        if '/' not in mime:
            if 'mp4' in mime:
                mime = 'video/mp4'
            elif 'png' in mime:
                mime = 'image/png'
            elif 'jpg' in mime or 'jpeg' in mime:
                mime = 'image/jpeg'
            elif 'pdf' in mime:
                mime = 'application/pdf'
        with open(file, 'rb') as f:
            if 'ogg' in mime:
                return f'data:audio/ogg;+codecs=opus;base64,{b64encode(f.read()).decode("utf-8")}'
            return f'data:{mime};base64,{b64encode(f.read()).decode("utf-8")}'

    def getLastGreetingTime(self):
        try:
            last_job = get(
                self.xpaths["api"] + "get_last_greeting_time",
                params = {
                    "device_id": self.device_id
                }
            )
            if last_job.status_code == 200:
                return last_job.text
            else:
                self.log.error("Last job not found")
                return None
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": "Error getLastGreetingTime function: " + str(e),
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error getLastGreetingTime function: " + str(e))
            self.close()

    def updateGreetingTime(self):
        try:
            last_job = post(
                self.xpaths["api"] + "update_greeting_time",
                params = {
                    "device_id": self.device_id
                }
            )
            if last_job.status_code == 200:
                self.log.info("Greeting time updated")
            else:
                self.log.error(f"{self.device} - Error on update Greeting time")
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": "Error updateGreetingTime function: " + str(e),
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error updateGreetingTime function: " + str(e))
            self.close()

    def sendMediaMessages(self, messages):
        try:
            self.log.info("Sending sendMediaMessages...")
            prank_messages = {
                'id': [],
                'contact_phone_number': [],
                'message_body': []
            }
            oth_messages = self.messageStructure()
            oth_messages['check_status'] = []
            sing_messages = self.messageStructure()
            sing_messages['check_status'] = []
            c = 0
            for i in messages['check_status']:
                if i == 99:
                    prank_messages['id'].append(messages['id'][c])
                    prank_messages['contact_phone_number'].append(messages['contact_phone_number'][c])
                    prank_messages['message_body'].append(messages['message_body'][c])
                elif i == 7:
                    sing_messages['id'].append(messages['id'][c])
                    sing_messages['contact_phone_number'].append(messages['contact_phone_number'][c])
                    sing_messages['message_body'].append(messages['message_body'][c])
                    sing_messages['message_type'].append(messages['message_type'][c])
                    sing_messages['message_body_filename'].append(messages['message_body_filename'][c])
                    sing_messages['message_caption'].append(messages['message_caption'][c])
                    sing_messages['message_custom_id'].append(messages['message_custom_id'][c])
                    sing_messages['message_body_mimetype'].append(messages['message_body_mimetype'][c])
                    sing_messages['check_status'].append(messages['check_status'][c])
                elif i != 50:
                    oth_messages['id'].append(messages['id'][c])
                    oth_messages['contact_phone_number'].append(messages['contact_phone_number'][c])
                    oth_messages['message_body'].append(messages['message_body'][c])
                    oth_messages['message_type'].append(messages['message_type'][c])
                    oth_messages['message_body_filename'].append(messages['message_body_filename'][c])
                    oth_messages['message_caption'].append(messages['message_caption'][c])
                    oth_messages['message_custom_id'].append(messages['message_custom_id'][c])
                    oth_messages['message_body_mimetype'].append(messages['message_body_mimetype'][c])
                    oth_messages['check_status'].append(messages['check_status'][c])
                c += 1
            c = 0
            for i in oth_messages['message_type']:
                if self.send_gen_messages and (i == "image" or i == "document" or i == "video" or i == "audio" or i == "application"):
                    self.sendAttachedMessage(
                        oth_messages['id'][c],
                        oth_messages['contact_phone_number'][c],
                        oth_messages['message_body'][c],
                        oth_messages['message_caption'][c],
                        oth_messages['message_body_filename'][c],
                        oth_messages['message_custom_id'][c],
                        oth_messages['message_body_mimetype'][c]
                    )
                elif self.send_single_messages and (i == "image" or i == "document" or i == "video" or i == "audio" or i == "application"):
                    self.sendAttachedMessage(
                        sing_messages['id'][c],
                        sing_messages['contact_phone_number'][c],
                        sing_messages['message_body'][c],
                        sing_messages['message_caption'][c],
                        sing_messages['message_body_filename'][c],
                        sing_messages['message_custom_id'][c],
                        sing_messages['message_body_mimetype'][c]
                    )
                else:
                    self.log.warning("Robô bloqueado para enviar saudação ou message type not found")
                c += 1
                sleep(round(uniform(2, 2.5), 2))
            sleep(round(uniform(0, .75), 2))
            self.ac.send_keys(Keys.ESCAPE).perform()
            self.log.info("Messages has been sent")
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": "Error on sendMediaMessages function: " + str(e),
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error on sendMediaMessages function: " + str(e))
            self.close()

    def sendMessages(self, messages):
        try:
            self.log.info("Sending messages...")
            prank_messages = {
                'id': [],
                'contact_phone_number': [],
                'message_body': []
            }
            oth_messages = self.messageStructure()
            oth_messages['check_status'] = []
            sing_messages = self.messageStructure()
            sing_messages['check_status'] = []
            c = 0
            for i in messages['check_status']:
                if i == 99:
                    prank_messages['id'].append(messages['id'][c])
                    prank_messages['contact_phone_number'].append(messages['contact_phone_number'][c])
                    prank_messages['message_body'].append(messages['message_body'][c])
                elif i == 7:
                    sing_messages['id'].append(messages['id'][c])
                    sing_messages['contact_phone_number'].append(messages['contact_phone_number'][c])
                    sing_messages['message_body'].append(messages['message_body'][c])
                    sing_messages['message_type'].append(messages['message_type'][c])
                    sing_messages['message_body_filename'].append(messages['message_body_filename'][c])
                    sing_messages['message_caption'].append(messages['message_caption'][c])
                    sing_messages['message_custom_id'].append(messages['message_custom_id'][c])
                    sing_messages['message_body_mimetype'].append(messages['message_body_mimetype'][c])
                    sing_messages['check_status'].append(messages['check_status'][c])
                elif i != 50:
                    oth_messages['id'].append(messages['id'][c])
                    oth_messages['contact_phone_number'].append(messages['contact_phone_number'][c])
                    oth_messages['message_body'].append(messages['message_body'][c])
                    oth_messages['message_type'].append(messages['message_type'][c])
                    oth_messages['message_body_filename'].append(messages['message_body_filename'][c])
                    oth_messages['message_caption'].append(messages['message_caption'][c])
                    oth_messages['message_custom_id'].append(messages['message_custom_id'][c])
                    oth_messages['message_body_mimetype'].append(messages['message_body_mimetype'][c])
                    oth_messages['check_status'].append(messages['check_status'][c])
                c += 1
            if self.send_pranks:
                c = 0
                for i in prank_messages['id']:
                    self.sendPrankMessage(
                        prank_messages['id'][c],
                        prank_messages['contact_phone_number'][c],
                        prank_messages['message_body'][c]
                    )
                    sleep(round(uniform(1.5, 2), 2))
                    c += 1
            if self.send_single_messages:
                c = 0
                for i in sing_messages['message_type']:
                    if i == "image" or i == "document" or i == "video" or i == "audio" or i == "application":
                        self.sendAttachedMessage(
                            sing_messages['id'][c],
                            sing_messages['contact_phone_number'][c],
                            sing_messages['message_body'][c],
                            sing_messages['message_caption'][c],
                            sing_messages['message_body_filename'][c],
                            sing_messages['message_custom_id'][c],
                            sing_messages['message_body_mimetype'][c]
                        )
                    else:
                        self.sendMessageText(
                            sing_messages['id'][c],
                            sing_messages['contact_phone_number'][c],
                            sing_messages['message_body'][c]
                        )
                    sleep(round(uniform(1.5, 2), 2))
                    c += 1
            c = 0 
            for i in oth_messages['message_type']:
                if oth_messages['check_status'][c] == 1 and self.send_greetings and self.server_is_active:
                    last_time_str = self.getLastGreetingTime()
                    send_greeting_ok = False
                    if last_time_str:
                        last_time = datetime.strptime(last_time_str.split('.')[0], "%Y-%m-%d %H:%M:%S")
                        if last_time + timedelta(minutes=self.min_greeting_time) < datetime.now():
                            send_greeting_ok = True
                    else:
                        send_greeting_ok = True
                    if send_greeting_ok:
                        self.sendMessageGreeting(
                            oth_messages['id'][c],
                            oth_messages['contact_phone_number'][c],
                            choice(self.setGreetings()),
                        )
                        self.update_greeting_time = True
                    else:
                        self.log.warning("Robô bloqueado para enviar saudação devido a tempo configurado, {} minutos".format(self.min_greeting_time))
                elif i == "text" and oth_messages['check_status'][c] != 1 and self.send_gen_messages:
                    self.sendMessageText(
                        oth_messages['id'][c],
                        oth_messages['contact_phone_number'][c],
                        oth_messages['message_body'][c]
                    )
                elif self.send_gen_messages and (i == "image" or i == "document" or i == "video" or i == "audio" or i == "application"):
                    self.sendAttachedMessage(
                        oth_messages['id'][c],
                        oth_messages['contact_phone_number'][c],
                        oth_messages['message_body'][c],
                        oth_messages['message_caption'][c],
                        oth_messages['message_body_filename'][c],
                        oth_messages['message_custom_id'][c],
                        oth_messages['message_body_mimetype'][c]
                    )
                else:
                    self.log.warning("Robô bloqueado para enviar saudação ou message type not found")
                c += 1
                sleep(round(uniform(2, 2.5), 2))
            sleep(round(uniform(0, .75), 2))
            self.ac.send_keys(Keys.ESCAPE).perform()
            self.log.info("Messages has been sent")
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": "Error on sendMessages function: " + str(e),
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error on sendMessages function: " + str(e))
            self.close()

    def getMinutesFDatetime(self, date_str):
        date_str = date_str.split(' ')
        date_str = date_str[4].split(':')
        return date_str[1]

    def messageStructure(self):
        return {
            'id': [],
            'contact_phone_number': [],
            'message_type': [],
            'message_body': [],
            'message_body_filename': [],
            'message_caption': [],
            'message_custom_id': [],
            'message_body_mimetype': []
        }

    def concatenateMessages(self, messages):
        max_concatenate = self.getAPIConfig(int(self.xpaths["qMessages2Conc"]))
        max_minutes = self.getAPIConfig(int(self.xpaths["minutes2Conc"]))
        max_length = self.getAPIConfig(int(self.xpaths["length2Conc"]))
        contacts_list = []
        for i in messages:
            if i[1] not in contacts_list:
                contacts_list.append(i[1])
        messages_structure = {}
        for i in contacts_list:
            messages_structure[i] = self.messageStructure()
            messages_structure[i]['schedule'] = []
            messages_structure[i]['body_lenght'] = []
        for i in messages:
            if i[6] != 'prankCDA' and i[2] == 'text':
                messages_structure[i[1]]['id'].append(i[0])
                messages_structure[i[1]]['message_body'].append(i[3])
                messages_structure[i[1]]['schedule'].append(i[8])
                messages_structure[i[1]]['body_lenght'].append(len(i[3]))
        ids_2concatenate = []
        for i in contacts_list:
            sorted_schedules = []
            for j, k, l in zip(
                    messages_structure[i]['schedule'],
                    messages_structure[i]['id'],
                    messages_structure[i]['body_lenght']
                ):
                sorted_schedules.append((j, k, l))
            sorted_schedules.sort(key=lambda a: a[1])
            count_concatenate = 0
            ids = []
            for j in range(len(sorted_schedules)-1):
                minute_j_msg = int(self.getMinutesFDatetime(sorted_schedules[j][0]))
                minute_jp_msg = int(self.getMinutesFDatetime(sorted_schedules[j+1][0]))
                if (abs(minute_jp_msg - minute_j_msg) <= max_minutes and
                    sorted_schedules[j][2] <= max_length and sorted_schedules[j+1][2] <= max_length):
                    if count_concatenate <= max_concatenate-1:
                        if sorted_schedules[j][1] not in ids:
                            ids.append(sorted_schedules[j][1])
                        ids.append(sorted_schedules[j+1][1])
                    else:
                        ids_2concatenate.append((ids, i))
                        count_concatenate = 0
                        ids = []
                    count_concatenate += 1
            if ids:
                ids_2concatenate.append((ids, i))
        conc_messages = self.messageStructure()
        for i in ids_2concatenate:
            body = ''
            for j in i[0]:
                body += messages_structure[i[1]]['message_body'][messages_structure[i[1]]['id'].index(j)] + '\r\n'
            conc_messages['id'].append(i[0])
            conc_messages['contact_phone_number'].append(i[1])
            conc_messages['message_body'].append(body)
        final_messages = self.messageStructure()
        ids_concatenated = []
        for i in conc_messages['id']:
            if isinstance(i, list):
                for j in i:
                    ids_concatenated.append(j)
            else:
                ids_concatenated.append(i)
        final_messages['check_status'] = []
        for i in messages:
            if i[0] not in ids_concatenated:
                final_messages['id'].append(i[0])
                final_messages['contact_phone_number'].append(i[1])
                final_messages['message_type'].append(i[2])
                final_messages['message_body'].append(i[3])
                final_messages['message_body_filename'].append(i[4])
                final_messages['message_caption'].append(i[5])
                final_messages['message_custom_id'].append(i[6])
                final_messages['message_body_mimetype'].append(i[7])
                final_messages['check_status'].append(i[9])
        for i in range(len(conc_messages['id'])):
            final_messages['id'].append(conc_messages['id'][i])
            final_messages['contact_phone_number'].append(conc_messages['contact_phone_number'][i])
            final_messages['message_type'].append('text')
            final_messages['message_body'].append(conc_messages['message_body'][i])
            final_messages['message_body_filename'].append('')
            final_messages['message_caption'].append('')
            final_messages['message_custom_id'].append('nP')
            final_messages['message_body_mimetype'].append('')
            final_messages['check_status'].append(0)
        sorted_messages = self.messageStructure()
        sorted_ids = []
        for i in final_messages['id']:
            if type(i) == list:
                sorted_ids.append((min(i), i))
            else:
                sorted_ids.append((i, i))
        sorted_ids.sort(key=lambda a: a[0])
        sorted_messages['check_status'] = []
        for i in sorted_ids:
            sorted_messages['id'].append(i[1])
            sorted_messages['contact_phone_number'].append(final_messages['contact_phone_number'][final_messages['id'].index(i[1])])
            sorted_messages['message_type'].append(final_messages['message_type'][final_messages['id'].index(i[1])])
            sorted_messages['message_body'].append(final_messages['message_body'][final_messages['id'].index(i[1])])
            sorted_messages['message_body_filename'].append(final_messages['message_body_filename'][final_messages['id'].index(i[1])])
            sorted_messages['message_caption'].append(final_messages['message_caption'][final_messages['id'].index(i[1])])
            sorted_messages['message_custom_id'].append(final_messages['message_custom_id'][final_messages['id'].index(i[1])])
            sorted_messages['message_body_mimetype'].append(final_messages['message_body_mimetype'][final_messages['id'].index(i[1])])
            sorted_messages['check_status'].append(final_messages['check_status'][final_messages['id'].index(i[1])])
        return sorted_messages

    def checkMessages(self, messages, self_number = False):
        try:
            for i in messages:
                if i[9] == 1:
                    if self_number:
                        i[3] = '+' + i[1]
                        i[1] = self.getPhoneNumber()
                    else:
                        i[3] = i[1]
                        i[1] = self.greeting_number
            return messages
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": "Error on checkMessages function: " + str(e),
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error on checkMessages function: " + str(e))
            self.close()

    def sendPointGreetings(self, messages):
        try:
            self.log.info("Sending point greetings...")
            for i in messages:
                if i[9] == 1:
                    self.sendPointGreeting(i[0], i[1])
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": "Error on sendPointGreetings function: " + str(e),
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error on sendPointGreetings function: " + str(e))
            self.close()

    def sendPointGreeting(self, id, contact_phone_number):
        try:
            self.log.info("Sending point greeting...")
            send_msg = False
            def_contact = int(contact_phone_number[2])
            pref = contact_phone_number[:4]
            suff = contact_phone_number[4:]
            if len(pref) == 4 and len(suff) >= 8:
                if def_contact == 2 or def_contact == 1:
                    if len(suff) == 8:
                        if int(suff[0]) > 5:
                            contact_phone_number = pref + '9' + suff
                        send_msg = True
                    elif len(suff) == 9:
                        contact_phone_number = pref + suff
                        send_msg = True
                    else:
                        self.log.warning(f"Contact phone number is invalid {contact_phone_number}")
                        self.updateContactPhoneNumber(contact_phone_number, False)
                else:
                    if len(suff) == 9:
                        contact_phone_number = pref + suff[1:]
                        send_msg = True
                    elif len(suff) == 8:
                        contact_phone_number = pref + suff
                        send_msg = True
                    else:
                        self.log.warning(f"Contact phone number is invalid {contact_phone_number}")
                        self.updateContactPhoneNumber(contact_phone_number, False)
            else:
                self.log.warning(f"Contact phone number is invalid {contact_phone_number}")
                self.updateContactPhoneNumber(contact_phone_number, False)
            if send_msg:
                if self.driver.execute_script("return typeof(whatsgw)") == 'undefined':
                    self.injectClientJS()
                    for _ in range(70):
                        sleep(.1)
                    # self.driver.implicitly_wait(15)
                self.log.info(f"Sending message from {self.device}")
                message_body = choice(self.point_greeting).encode('unicode-escape').decode()
                msg_str_var = '{"type":"_wabc_","msg":{"cmd":"chat","msg":{"to":"' + contact_phone_number + '","chat_type":"1","custom_uid":"100000000","body":{"title":"","desc":"","url":null,"base64":null,"mime_types":null,"filename":null,"thumb":"","text":"' + message_body + '","w_mensagem_tipo":1}},"w_telefone_id":0,"instancia_id":0,"data":null,"data2":null,"footer":null,"buttonText":null,"headerType":0,"buttons":null,"templateButtons":null,"sections":null,"poll":null}}'
                sleep(round(uniform(1.5, 2), 2))
                self.driver.execute_script(f'let message = {msg_str_var}; window.postMessage(message, "*");')
            sleep(round(uniform(1, 2), 2))
            self.updateSendMessage(id)
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": "Error on sendPointGreeting function: " + str(e),
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error on sendPointGreeting function: " + str(e))
            self.close()

    def collectMessagesToSend(self, only_desktop = False):
        try:
            self.log.info("Collecting messages...")
            if only_desktop:
                get_from_db = self.getPrankMessages()
            elif self.xpaths['sendGreetings'] == '1':
                get_from_db = self.getSendMessages()
            else:
                get_from_db = self.getSendMessagesNotGreetings()
            if self.greetings_panel == 1:
                get_from_db = self.checkMessages(get_from_db)
            elif self.xpaths["greetingToMe"] == '1':
                get_from_db = self.checkMessages(get_from_db, True)
            if self.xpaths['pointGreeting'] == '1' and self.greetings_panel == 0:
                self.sendPointGreetings(get_from_db)
            max_messages = self.getAPIConfig(int(self.xpaths["qMessages2Send"]))
            max_greetings = self.getAPIConfig(int(self.xpaths["qGreetings2Send"]))
            max_pranks = randint(1, self.getAPIConfig(int(self.xpaths["qPranks2Send"])))
            max_single_messages = self.getAPIConfig(int(self.xpaths["qSingleMessages2Send"]))
            cleaned_messages = self.concatenateMessages(get_from_db)
            count_pranks = 0
            count_messages = 0
            count_greetings = 0
            count_single = 0
            messages = self.messageStructure()
            messages['schedule'] = []
            messages['check_status'] = []
            for i in range(len(cleaned_messages['id'])):
                if int(cleaned_messages['check_status'][i]) == 99:
                    count_pranks += 1
                elif int(cleaned_messages['check_status'][i]) == 7:
                    count_single += 1
                elif int(cleaned_messages['check_status'][i]) == 2:
                    count_messages += 1
                elif int(cleaned_messages['check_status'][i]) == 1:
                    count_greetings += 1
                if count_messages > max_messages and int(cleaned_messages['check_status'][i]) == 2:
                    continue
                elif count_single > max_single_messages and int(cleaned_messages['check_status'][i]) == 7:
                    continue
                elif count_greetings > max_greetings and int(cleaned_messages['check_status'][i]) == 1:
                    continue
                elif count_pranks > max_pranks and cleaned_messages['check_status'][i] == 99:
                    continue
                elif count_pranks > max_pranks and count_messages > max_messages and count_greetings > max_greetings:
                    break
                else:
                    messages['id'].append(cleaned_messages['id'][i])
                    messages['contact_phone_number'].append(cleaned_messages['contact_phone_number'][i])
                    messages['message_type'].append(cleaned_messages['message_type'][i])
                    messages['message_body'].append(cleaned_messages['message_body'][i])
                    messages['message_body_filename'].append(cleaned_messages['message_body_filename'][i])
                    messages['message_caption'].append(cleaned_messages['message_caption'][i])
                    messages['message_custom_id'].append(cleaned_messages['message_custom_id'][i])
                    messages['message_body_mimetype'].append(cleaned_messages['message_body_mimetype'][i])
                    messages['check_status'].append(cleaned_messages['check_status'][i])
            return messages
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": f"Error on collecting messages: {e}",
                    "contact": ''
                }
            )
            self.log.error(f"Error on collecting messages: {e}")
            self.close()

    def getAPIConfig(self, config_id):
        try:
            get_config = get(
                self.xpaths["api"] + "get_config",
                params = {
                    "config_id": config_id
                }
            )
            if get_config.status_code == 200:
                return int(get_config.text)
            else:
                self.log.error(f"{self.device} - Error on getting config")
                return None
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": f"Error on getting config: {e}",
                    "contact": ''
                }
            )
            self.log.error(f"Error on getting config: {e}")
            self.close()

    def getSendMessages(self):
        try:
            messages_id = get(
                self.xpaths["api"] + "get_send_messages",
                params = {
                    "device_id": self.device_id
                }
            )
            if messages_id.status_code == 200:
                return messages_id.json()
            else:
                self.log.error(f"{self.device} - Error on getting messages to send")
                return None
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": f"Error on getting messages to send: {e}",
                    "contact": ''
                }
            )
            self.log.error(f"Error on getting messages to send: {e}")
            self.close()

    def getPrankMessages(self):
        try:
            messages_id = get(
                self.xpaths["api"] + "get_prank_messages",
                params = {
                    "device_id": self.device_id
                }
            )
            if messages_id.status_code == 200:
                return messages_id.json()
            else:
                self.log.error(f"{self.device} - Error on getting prank messages to send")
                return None
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": f"Error on getting prank messages to send: {e}",
                    "contact": ''
                }
            )
            self.log.error(f"Error on getting prank messages to send: {e}")
            self.close()

    def getSendMessagesNotGreetings(self):
        try:
            messages_id = get(
                self.xpaths["api"] + "get_send_messages_not_greetings",
                params = {
                    "device_id": self.device_id
                }
            )
            if messages_id.status_code == 200:
                return messages_id.json()
            else:
                self.log.error(f"{self.device} - Error on getting messages to send")
                return None
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": f"Error on getting messages to send: {e}",
                    "contact": ''
                }
            )
            self.log.error(f"Error on getting messages to send: {e}")
            self.close()

    def setStatusDevice(self, status):
        try:
            if status:
                route = "set_qrcode_true"
            else:
                route = "set_qrcode_false"
            set_qrcode_status = post(
                self.xpaths["api"] + route,
                params = {
                    "device_id": self.device_id
                }
            )
            if set_qrcode_status.status_code == 200:
                self.log.info("QRCode status updated")
            else:
                self.log.error(f"{self.device} - Error on update QRCode status")
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": "Error on setStatusDevice function: " + str(e),
                    "contact": ''
                }
            )
            self.log.error(f"{self.device} - Error on setStatusDevice function: " + str(e))
            self.close()

    def sincronizeWhatsApp(self):
        try:
            sleep(round(uniform(0.5, 1), 2))
            self.openWhatsApp()
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'connecting',
                    "message": '',
                    "contact": ''
                }
            )
            while not self.isWhatsAppAvailable():
                self.log.info("Waiting sincronism...")
                if not self.elementExistsInDriver(self.xpaths["whatsLoadingBody"]) and not self.elementExistsInDriver(self.xpaths["whatsHeader"]):
                    if not self.elementExistsInDriver(self.xpaths["connectingWhatsApp"]) and not self.elementExistsInDriver(self.xpaths["isAvailable"]):
                        self.openWhatsApp()
                        for _ in range(50):
                            sleep(0.1)
                    for _ in range(10):
                        sleep(0.1)
                    if not 'whats' in self.driver.title.lower() and not self.device in self.driver.title:
                        self.openWhatsApp()
                    for _ in range(50):
                        sleep(0.1)
                    else:
                        for _ in range(10):
                            sleep(0.1)
            else:
                self.log.info("WhatsApp is available")
                self.setDeviceInTitle()
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": f"Error on sincronize WhatsApp: {e}",
                    "contact": ''
                }
            )
            self.log.error(f"Error on sincronize WhatsApp: {e}")
            self.close()

    def isWhatsAppAvailable(self):
        try:
            if self.elementExistsInDriver(self.xpaths["isAvailable"]) or self.elementExistsInDriver(self.xpaths["whatsBody"]):
                return True
            else:
                if not self.isQRCodePresent(time()):
                    self.log.info("WhatsApp is not available, waiting sincronism...")
                    if self.elementExistsInDriver(self.xpaths["popUpError"]) or self.elementExistsInDriver(self.xpaths["disconnectedPC"]):
                        self.openWhatsApp()
                        for _ in range(70):
                            sleep(0.1)
                    for _ in range(50):
                        sleep(0.1)
                return False
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": f"Error on check if WhatsApp is available: {e}",
                    "contact": ''
                }
            )
            self.log.error(f"Error on check if WhatsApp is available: {e}")
            self.close()

    def openWhatsApp(self):
        try:
            self.driver.get(self.__waLink)
            self.log.info("Starting WhatsApp...")
            for _ in range(20):
                sleep(0.1)
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": f"Error in openWhatsApp function: {e}",
                    "contact": ''
                }
            )
            self.log.error(f"Error in openWhatsApp function: {e}")
            self.close()

    def postQRCodeAPI(self, qrcode = None):
        try:
            if qrcode:
                data = {
                    "device_id": self.device_id,
                    "device": self.device,
                    "data": qrcode
                }
            else:
                data = {
                    "device_id": self.device_id,
                    "device": self.device
                }
            get_qrcode = post(
                "http://192.168.7.100:8080/api",
                data = data
            )
            if get_qrcode.status_code == 200:
                self.log.info(get_qrcode.text)
                return True
            else:
                self.log.error(f"{self.device} - Error on postQRCodeAPI")
                return False
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": f"Error on postQRCodeAPI: {e}",
                    "contact": ''
                }
            )
            self.log.error(f"Error on postQRCodeAPI: {e}")
            self.close()

    def isQRCodePresent(self, start_time):
        max_time = 60
        while self.isQRCodeNeeded():
            QRCodePresent = True
            self.setStatusDevice(False)
            self.setDeviceInTitle()
            if self.driver.find_elements(By.XPATH, self.xpaths["QRCodePresent"]):
                qr_element = self.driver.find_element(By.XPATH, self.xpaths["QRCodePresent"])
                self.driver.execute_script('arguments[0].scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});', qr_element)
                self.log.info("QRCode is present, waiting sincronism...")
                if self.driver.find_elements(By.XPATH, self.xpaths["whatsQRBanner"]):
                    qr_banner = self.driver.find_element(By.XPATH, self.xpaths["whatsQRBanner"])
                    self.driver.execute_script("arguments[0].remove();", qr_banner)
                filename = self.qrcode_path + self.device.replace(" ", "_") + self.datetimeName() + ".png"
                self.driver.save_screenshot(filename)
                for _ in range(10):
                    sleep(0.1)
                qrcode_filename = self.getQRCodeFromPath(filename)
                if isfile(qrcode_filename):
                    with open(qrcode_filename, "rb") as f:
                        qrcode = b64encode(f.read()).decode("utf-8")
                    self.postQRCodeAPI(qrcode)
                    post(
                        self.xpaths["api_log"],
                        params = {
                            "number": self.getPhoneNumber(),
                            "event": 'disconnected',
                            "message": '',
                            "contact": ''
                        }
                    )
                remove(filename)
                if time()-start_time > max_time:
                    self.close()
            elif self.driver.find_elements(By.XPATH, self.xpaths["QRCodeLoading"]):
                self.log.info("QRCode is loading")
                for _ in range(10):
                    sleep(0.1)
            elif self.driver.find_elements(By.XPATH, self.xpaths["QRCodeRefresh"]):
                self.log.info("QRCode is refreshing")
                for _ in range(10):
                    sleep(0.1)
            else:
                QRCodePresent = False
        if self.isQRCodeNeeded():
            QRCodePresent = True
        else:
            QRCodePresent = False
        if QRCodePresent:
            if time()-start_time > max_time:
                self.close()
            self.isQRCodePresent(start_time)
        else:
            ssToRemove = listdir(self.qrcode_path)
            for i in ssToRemove:
                remove(self.qrcode_path + i)
            return False

    def isQRCodeNeeded(self):
        if self.driver.find_elements(By.XPATH, self.xpaths["QRCodePresent"]):
            return True
        if self.driver.find_elements(By.XPATH, self.xpaths["QRCodeLoading"]):
            return True
        if self.driver.find_elements(By.XPATH, self.xpaths["QRCodeRefresh"]):
            self.log.info("QRCode is refreshing")
            element = self.driver.find_element(By.XPATH, self.xpaths["QRCodeRefresh"])
            element.click()
            for _ in range(20):
                sleep(0.1)
            return True
        else:
            return False

    def getQRCodeFromPath(self, filename):
        image = imread(filename)
        original = image.copy()
        gray = cvtColor(image, COLOR_BGR2GRAY)
        blur = GaussianBlur(gray, (9,9), 0)
        thresh = threshold(blur, 0, 255, THRESH_BINARY_INV + THRESH_OTSU)[1]
        kernel = getStructuringElement(MORPH_RECT, (5,5))
        close = morphologyEx(thresh, MORPH_CLOSE, kernel, iterations=2)
        cnts = findContours(close, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        filename = self.qrcode_path + "qrcode" + self.datetimeName() + ".png"
        for c in cnts:
            peri = arcLength(c, True)
            approx = approxPolyDP(c, 0.04 * peri, True)
            x,y,w,h = boundingRect(approx)
            area = contourArea(c)
            ar = w / float(h)
            if len(approx) == 4 and area > 1000 and (ar > .85 and ar < 1.3):
                rectangle(image, (x, y), (x + w, y + h), (36,255,12), 3)
                ROI = original[y:y+h, x:x+w] # type: ignore
                imwrite(filename, ROI)
        return filename

    def setDeviceInTitle(self):
        try:
            self.driver.execute_script(f'document.title = "{self.device}"')
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": f"Error in setDeviceInTitle function: {e}",
                    "contact": ''
                }
            )
            self.log.error(f"Error in setDeviceInTitle function: {e}")
            self.close()

    def injectSendTextJS(self):
        try:
            with open('sendTextJS.js') as f:
                sendTextScript = f.read().rstrip()
            self.driver.execute_script(sendTextScript)
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": f"Error in injectSendTextJS function: {e}",
                    "contact": ''
                }
            )
            self.log.error(f"Error in injectSendTextJS function: {e}")
            self.close()

    def postDriverArguments(self):
        try:
            self.driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
            params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': self.downloads_path}}
            self.driver.execute("send_command", params)
            stealth(self.driver,
                languages=["pt-BR", "pt"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                user_agent=self.xpaths["userAgent"]
            )
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": f"Error in postDriverArguments: {e}",
                    "contact": ''
                }
            )
            self.log.error(f"Error in postDriverArguments: {e}")
            self.close()

    def runChromeDriver(self):
        try:
            # https://groups.google.com/a/chromium.org/g/headless-dev/c/qqbZVZ2IwEw/m/qOoNb73gAwAJ
            self.log.info(f"Starting ChromeDriver... {self.device}")
            chromeService = ChromeService(executable_path = self.xpaths["chromeDriver"] + f"{self.driver_number}\\chromedriver.exe")
            chromeOptions = ChromeOptions()
            chromeOptions.binary_location = self.xpaths["path"] + self.device + self.xpaths["chromeBinary"]
            chromeOptions.add_argument("no-sandbox")
            chromeOptions.add_argument("start-maximized")
            chromeOptions.add_argument("disable-gpu")
            chromeOptions.add_argument("single-process")
            chromeOptions.add_argument("disable-quic")
            chromeOptions.add_argument("disable-blink-features")
            chromeOptions.add_argument("disable-blink-features=AutomationControlled")
            chromeOptions.add_argument("disable-dev-shm-usage")
            chromeOptions.add_argument("disable-infobars")
            # chromeOptions.add_argument("disable-extensions")
            chromeOptions.add_argument("disable-notifications")
            chromeOptions.add_argument("disable-web-security")
            chromeOptions.add_argument("remote-debugging-port=" + self.port)
            chromeOptions.add_argument("disable-default-apps")
            chromeOptions.add_argument("allow-running-insecure-content")
            chromeOptions.add_argument("allow-insecure-localhost")
            chromeOptions.add_argument("allow-file-access")
            chromeOptions.add_argument("allow-universal-access-from-files")
            chromeOptions.add_argument("enable-parallel-downloading")
            chromeOptions.add_argument("profile-directory=" + self.device)
            prefs = {
                "profile.default_content_settings.popups": 0,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                # "extensions_to_open": "",
                "safebrowsing_for_trusted_sources_enabled": False,
                "safebrowsing.disable_download_protection": True,
                "disable-client-side-phishing-detection": True,
                "safebrowsing.enabled": False
            }
            chromeOptions.add_experimental_option("prefs", prefs)
            chromeOptions.add_experimental_option("detach", True)
            chromeOptions.add_experimental_option(
                "excludeSwitches", [
                    "enable-automation",
                    "enable-logging",
                    "disable-popup-blocking"
                ]
            )
            chromeOptions.add_experimental_option('useAutomationExtension', False)
            self.log.info("Chrome options and services up, starting Chrome...")
            sleep(round(uniform(0.5, 1), 2))
            return webdriver.Chrome(service=chromeService, options=chromeOptions)
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": f"Error starting ChromeDriver: {e}",
                    "contact": ''
                }
            )
            self.log.error(f"Error starting ChromeDriver: {e}")
            exit()

    def logger(self, name):
        logger = getLogger(name)
        basicConfig(
            filename = self.logs_path + datetime.now().strftime("%Y-%m-%d") + ".log",
            encoding = 'utf-8', level = INFO
        )
        logger.handlers = [h for h in logger.handlers if not isinstance(h, StreamHandler)]
        ch = StreamHandler()
        ch.setLevel(INFO)
        formatter = Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger

    def datetimeName(self):
        return (datetime.now().strftime("_%d%m%Y_%H%M%S"))

    def CSSExistsInDriver(self, xpath):
        try:
            self.driver.find_element(By.CSS_SELECTOR, xpath)
        except NoSuchElementException:
            return False
        return True

    def elementExistsInDriver(self, xpath):
        try:
             self.driver.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            return False
        except UnexpectedAlertPresentException:
            return False
        return True

    def elementExistsInElement(self, element, xpath):
        try:
            element.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            return False
        return True

    def createPath(self):
        try:
            if not isdir(self.xpaths["path"] + self.device):
                makedirs(self.xpaths["path"] + self.device)
                copytree(
                    self.xpaths["chromeNew"],
                    self.xpaths["path"] + self.device + "\\chrome\\"
                )
            if not isdir(self.downloads_path):
                makedirs(self.downloads_path)
            if not isdir(self.logs_path):
                makedirs(self.logs_path)
            if not isdir(self.qrcode_path):
                makedirs(self.qrcode_path)
            chmod(self.xpaths["path"] + self.device + "\\chrome\\", 0o777)
            chmod(self.xpaths["path"] + self.device, 0o777)
            chmod(self.downloads_path, 0o777)
            chmod(self.qrcode_path, 0o777)
            chmod(self.logs_path, 0o777)
        except Exception as e:
            post(
                self.xpaths["api_log"],
                params = {
                    "number": self.getPhoneNumber(),
                    "event": 'error',
                    "message": "Error createPath function: " + str(e),
                    "contact": ''
                }
            )
            exit()

    # @pyqtSignal()
    def close(self):
        self.log.info(f"Closing ChromeDriver... {self.device}")
        self.driver.close()
        self.driver.quit()
        collect_gc()
        # self.is_eternal(self.xpaths['eternalConn'] == '1')
        exit()