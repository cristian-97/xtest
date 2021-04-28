import logging
import traceback_mail
import threading
import json
import requests
from collections import namedtuple
from global_xraid import xraid
import os
import re

logger = logging.getLogger("xraid.rfid_manager")


class RfIDManager:
    def __init__(self):
        self.rfid_list = {}

    def insert_or_update(self, rfid):
        if rfid.code not in self.rfid_list.keys():
            self.rfid_list[rfid.code] = rfid
            logger.debug("RfID %s added to rfid list %d" % (str(rfid), len(self.rfid_list.keys())))
        else:
            logger.debug("RfID %s update - rfid list %d" % (str(rfid), len(self.rfid_list.keys())))

        self.rfid_list[rfid.code].get_character()
        return self.rfid_list[rfid.code]


class RfID:
    __template = {'username': '',
                  'nickname': '',
                  'rfid': '',
                  'user_email': '',
                  'user_registered': '',
                  'avatarlinks': {'thumbnail': '',
                                  'medium': '',
                                  'large': '',
                                  'full': ''
                                  },
                  'globalranklevel': ''}

    Character = namedtuple('Character', __template.keys())

    error_codes = ['get_user_by_rfid', 'No-Authorised-Rfid', 'No-User-by-Rfid']

    rfid_pattern = r'^\d{10}$'

    def __init__(self, code: str = ''):
        self.code = str(code)
        self.character = None
        self.error = ''
        self.__thread = threading.Thread()

    def get_character(self, threaded=True):
        if self.code != '':
            if threaded and not self.__thread.is_alive():
                self.__thread = threading.Thread(target=self.__get_character)
                self.__thread.start()

            elif not threaded:
                self.__get_character()
                return self.character

        return None

    def __get_character(self):
        try:
            logger.info('Try to get player %s character...' % self.__str__())

            api_url = xraid.server_config.get('web_portal', 'api_url')
            r = requests.get(api_url + '/user/%s' % self.__str__())
            logger.debug('GET %s - %s' % (str(r.url), str(r.status_code)))

            if r.status_code == 200:
                data = json.loads(r.text)

                if data['code'] == self.error_codes[0]:

                    user = data['data']['user']
                    try:
                        self.character = RfID.Character(**user)
                    except TypeError as e:
                        logger.debug('Required Character data:' + str(self.__template))
                        logger.debug('User data:' + str(data))
                        raise e

                    logger.debug('Character %s username: %s' % (self.__str__(), self.character.username))
                    print(self.character)

                else:
                    self.character = None
                    self.error = data['code']
            #else:
            #    logger.error(r.status_code)

        except requests.RequestException as e:
            logger.error(e)
            self.error = str(e)

        except Exception as e:
            traceback_mail.traceback_error(logger, e)

    def __eq__(self, c):
        return self.code == c.code

    def __hash__(self):
        return hash(self.code)

    def __str__(self):
        if re.match(self.rfid_pattern, self.code):
            return self.code
        else:
            return '0000000000'

    def str(self):
        return self.__str__()

    def get_avatar(self):

        image_url = self.character.avatarlinks['thumbnail']
        #ora vado a prendere il percorso in cui memorizzerò il file
        image_path = '/tmp/%s' % os.path.basename(image_url)

        # controllo estensione del file
        imge_filename, image_extension = os.path.splitext(image_path)
        if image_extension.upper() not in ['.PNG', '.GIF', '.JPG', '.JPEG']:
            raise Exception('Extension not allowed "%s"' % str(image_extension))

        if image_url != "" and image_path != "":
            img_data = requests.get(image_url).content
            with open(image_path, 'wb') as handler:
                handler.write(img_data)
        return image_path