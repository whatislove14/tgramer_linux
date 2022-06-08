import os.path
import pandas as pd
from os import path
from time import sleep

from telethon.sync import TelegramClient

# для корректного переноса времени сообщений в json
from datetime import datetime

# классы для работы с каналами
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch, UserStatusOnline, UserStatusOffline, UserStatusRecently, UserStatusLastWeek, ChannelParticipantsAdmins

from PyQt5.QtCore import pyqtSignal, QObject, QEventLoop

class ClientSig(QObject):
    code_request = pyqtSignal(list)

signals = ClientSig()

class Parser:
    def __init__(self, client:TelegramClient, filters:dict, window) -> None:
        self.filters = filters # фильтры для парсера
        self.chat = None # текущий чат для парсинга
        self.client = client # клиент, с которого работаем
        self.window = window
    
    def dump_all_participants(self) -> None:
        '''Сбор участников группы по фильтрам'''
        offset_user = 0    # номер участника, с которого начинается считывание
        limit_user = 100   # максимальное число записей, передаваемых за один раз

        if self.filters["participants"] or (not(self.filters["participants"]) and not(self.filters["admins"])):
            all_participants = []   # список всех участников канала
            filter_user = ChannelParticipantsSearch('')
            while True:
                print("part")
                self.window.process_parsing()
                participants = self.client(GetParticipantsRequest(self.chat,
                                                                filter_user, offset_user, limit_user, hash=0))
                if not participants.users:
                    break
                all_participants.extend(participants.users)
                offset_user += len(participants.users)
                self.window.process_parsing()
                sleep(1)

            offset_user += len(participants.users)

        if (not(self.filters["admins"]) and self.filters["participants"]) or (self.filters["admins"] and not(self.filters["participants"])):
            print("adm")
            offset_user = 0    # номер участника, с которого начинается считывание
            limit_user = 100
            filter_user = ChannelParticipantsAdmins()
            admin_participants = []
            while True:
                self.window.process_parsing()
                participants = self.client(GetParticipantsRequest(self.chat,
                                                                filter_user, offset_user, limit_user, hash=0))
                if not participants.users:
                    break
                admin_participants.extend(participants.users)
                offset_user += len(participants.users)

        all_users = []   # список словарей с интересующими параметрами участников канала

        # исключаем админов из списка, если парсим только участников
        if self.filters["participants"] and not(self.filters["admins"]):
            new_all_participants = []
            all_admins_id = [adm.id for adm in admin_participants]
            self.window.process_parsing()
            for participant in all_participants:
                if participant.id not in all_admins_id:
                    new_all_participants.append(participant)
            all_participants = new_all_participants.copy()
        # если парсим только админов
        if self.filters["admins"] and not self.filters["participants"]:
            all_participants = admin_participants.copy()

        # прогоняем по всем остальным фильтрам
        # фильтр по сообщениям
        if self.filters["chatting"]:
            in_chat = set([message.sender_id for message in self.client.iter_messages(self.chat, 2000)])
            new_all_participants = []
            self.window.process_parsing()
            for part in all_participants:
                if part.id in in_chat:
                    new_all_participants.append(part)
            all_participants = new_all_participants.copy()


        # фильтр по аватарке
        if self.filters["photo"]:
            new_all_participants = []
            self.window.process_parsing()
            for participant in all_participants:
                if participant.photo != None:
                    new_all_participants.append(participant)
            all_participants = new_all_participants.copy()

        # фильтр по онлайну
        if self.filters["online"]:
            print("ONLINE")
            self.window.process_parsing()
            for participant in all_participants:
                if isinstance(participant.status, UserStatusOnline):
                    all_users.append([participant.id, participant.username, participant.first_name, participant.last_name, participant.phone])
                elif isinstance(participant.status, UserStatusOffline):
                    online_data = participant.status.was_online.replace(tzinfo=None)
                    if self.filters["online"] == 1:
                        if (datetime.utcnow() - online_data).days == 0 and (datetime.utcnow() - online_data).total_seconds()/3600 <= 1:
                            all_users.append([participant.id, participant.username, participant.first_name, participant.last_name, participant.phone])
                    elif self.filters["online"] == 2:
                        if (datetime.utcnow() - online_data).days == 0 and (datetime.utcnow() - online_data).total_seconds()/3600 <= 3:
                            all_users.append([participant.id, participant.username, participant.first_name, participant.last_name, participant.phone])
                    elif self.filters["online"] == 3:
                        if (datetime.utcnow() - online_data).days <= 1:
                            all_users.append([participant.id, participant.username, participant.first_name, participant.last_name, participant.phone])
                    elif self.filters["online"] == 4:
                        if (datetime.utcnow() - online_data).days <= 3:
                            all_users.append([participant.id, participant.username, participant.first_name, participant.last_name, participant.phone])
                    elif self.filters["online"] == 5:
                        if (datetime.utcnow() - online_data).days <= 7:
                            all_users.append([participant.id, participant.username, participant.first_name, participant.last_name, participant.phone])
                elif isinstance(participant.status, UserStatusRecently) and self.filters["online"] != 6:
                    all_users.append([participant.id, participant.username, participant.first_name, participant.last_name, participant.phone])
                elif isinstance(participant.status, UserStatusLastWeek):
                    if self.filters["online"] == 5:
                        all_users.append([participant.id, participant.username, participant.first_name, participant.last_name, participant.phone])
        else:
            self.window.process_parsing()
            x = 0
            for participant in all_participants:
                x += 1
                if x == 1000:
                    print("end")
                    self.window.process_parsing()
                    x = 0
                all_users.append([participant.id, participant.username, participant.first_name, participant.last_name, participant.phone])  
        self.window.process_load_file()
        data = pd.DataFrame(all_users, columns=["telegram id", "username", "first name", "last name", "phone"])
        data.to_excel("result\\{}.xlsx".format(self.chat.username))
        self.window.end_parsing()
        self.client.disconnect()

    def pars(self, chats:list) -> None:
        '''Парсинг списка чатов'''
        for chat in chats:
            self.chat = chat
            self.dump_all_participants()

def parsing(window):
    api_id = 3429312
    api_hash = '1ad0f9e1aed206dc0b9caa654221b1fe'
    f = open("accounts.txt")
    phone = f.readline().strip()
    f.close()
    client = TelegramClient(phone, api_id, api_hash)
    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(phone)
        print("sended")
        signals.code_request.emit([client, window, phone])
    else:
        client_sign_in(False, client, window, phone)

def client_sign_in(code, client, window, phone):
    if code:
        client.sign_in(phone, code)
    print(window.group_link_zone.text())
    window.process_parsing()
    sleep(1)
    channel = client.get_entity(window.group_link_zone.text())
    print({"participants": window.check_memb.checkState(),
    "admins": window.check_amd.checkState(),
    "online": window.active.currentIndex(), 
    "photo": window.check_photo.checkState(),
    "chatting": window.check_chatting.checkState()
    })
    now_parser = Parser(client, {"participants": window.check_memb.checkState(),
    "admins": window.check_amd.checkState(),
    "online": window.active.currentIndex(), 
    "photo": window.check_photo.checkState(),
    "chatting": window.check_chatting.checkState()
    }, window)
    now_parser.pars([channel])