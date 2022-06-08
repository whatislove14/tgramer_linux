import os
import pandas as pd
from time import sleep
from random import randint
from datetime import datetime

from telethon.sync import TelegramClient
from telethon.tl.functions.messages import AddChatUserRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch, UserStatusOnline, UserStatusOffline, UserStatusRecently, UserStatusLastWeek, ChannelParticipantsAdmins
from telethon.errors.rpcerrorlist import UserAlreadyParticipantError, PeerFloodError, FloodWaitError, ChatIdInvalidError, UserNotMutualContactError
from telethon.tl.functions.channels import GetParticipantsRequest, InviteToChannelRequest, JoinChannelRequest
from telethon.tl.types import ChannelParticipantsSearch, UserStatusOnline, UserStatusOffline, UserStatusRecently, UserStatusLastWeek, ChannelParticipantsAdmins

from PyQt5.QtCore import pyqtSignal, QObject, QEventLoop, QTimer

from math import isnan


class ClientSig(QObject):
    code_request = pyqtSignal(list)
    next_client = False


signals = ClientSig()

class FullInvite:
    '''Класс для инвайтинга всего списка со всех аккаунтов'''

    def __init__(self, clients: list, chat: str, users: list, total_append: int, pause_interval: tuple, each_append: int, window) -> None:
        self.clients = clients  # список доступных аккаунтов
        self.chat = chat  # чат, куда добаляем
        self.users = users  # список пользователей для добаления
        self.pause_interval = pause_interval  # интервал паузы между каждым добалением
        self.len_clients = len(clients)  # количество рабочих аккаунтов
        self.working_client = list()  # список аккаунтов в работе
        self.total_append = total_append  # сколько нужно добавить пользователей
        self.each_append = each_append  # сколько добавлять с каждого
        self.window = window

    def invite_users(self):
        '''Функция для разделения аккаунтов'''

        # создаем инвайтеры для каждого аккаунта
        for client in self.clients:
            print(self.total_append)
            if self.total_append == 0:
                break
            now_invite = Inviter(client, self.chat, self.users,
                                 self.pause_interval, self.total_append, self.each_append, self.window)
            self.total_append, new_start_users = now_invite.invite_users()
            # убираем из списка уже добавленных юзеров
            users = self.users[self.each_append::]
            self.users = users.copy()
            client.disconnect()
        self.window.add_log_inform("end inviting")


class Inviter:
    '''Класс для инвайтинга опр. части юзеров с опр. аккаунта'''

    def __init__(self, client: TelegramClient, chat: str, users: list, pause_interval: tuple, total_append: int, each_append: int, window) -> None:
        self.client = client  # аккаунт, который используем
        self.chat = chat  # чат, куда добаляем
        self.users = users  # список пользователей для добаления
        self.pause_interval = pause_interval  # интервал паузы между каждым добалением
        self.pause = None  # текущая пауза
        self.total_append = total_append  # сколько осталось добавить
        self.each_append = each_append  # сколько добавлять с каждого
        self.window = window

        self.client.connect()

        self.window.add_log_inform(str(self.total_append)+" users left")
        self.window.add_log_inform("starting "+str(self.client.get_me().phone))


    def invite_users(self):
        '''Функция добавления пользователей и паузы'''
        total_now_appending = 0  # сколько уже добавили
        for user in self.users:
            if total_now_appending >= self.each_append or self.total_append == 0:
                return (self.total_append, total_now_appending)
            self.change_pause()
            try:
                self.client(AddChatUserRequest(self.chat, user, 0))
                self.window.add_log_inform("add "+ str(user))
                self.window.add_log_inform(f"waiting {str(self.pause)} seconds")
                loop = QEventLoop()
                QTimer.singleShot(self.pause*1000, loop.quit)
                loop.exec_()
            except PeerFloodError:
                self.window.add_log_warn("Достигли лимита запросов на аккаунт. Переключаемся")
                return (self.total_append, total_now_appending)
            except FloodWaitError:
                self.window.add_log_warn("Достигли лимита запросов на аккаунт. Переключаемся")
                return (self.total_append, total_now_appending)
            except UserAlreadyParticipantError:
                continue
            except ValueError:
                continue
            except ChatIdInvalidError:
                try:
                    self.client(InviteToChannelRequest(self.chat, [user]))
                    self.window.add_log_inform("add "+ str(user))
                    self.window.add_log_inform(f"waiting {str(self.pause)} seconds")
                    loop = QEventLoop()
                    QTimer.singleShot(self.pause*1000, loop.quit)
                    loop.exec_()
                except PeerFloodError:
                    self.window.add_log_warn("Достигли лимита запросов на аккаунт. Переключаемся")
                    return (self.total_append, total_now_appending)
                except FloodWaitError:
                    self.window.add_log_warn("Достигли лимита запросов на аккаунт. Переключаемся")
                    return (self.total_append, total_now_appending)
                except UserAlreadyParticipantError:
                    continue
                except UserNotMutualContactError:
                    continue
                except ValueError:
                    continue
                except Exception as e:
                    self.window.add_log_warn("Error while adding "+user)
                    self.window.add_log_warn(e)
                    continue
            except UserNotMutualContactError:
                continue
            except Exception as e:
                self.window.add_log_warn("Error while adding "+user)
                self.window.add_log_warn(e)
                continue

            self.total_append -= 1
            total_now_appending += 1
        return (0, total_now_appending)

    def change_pause(self):
        '''Функция рандомной смены паузы'''
        self.pause = randint(*self.pause_interval)

def start_inviting(window):
    api_id = 3429312
    api_hash = '1ad0f9e1aed206dc0b9caa654221b1fe'

    inp_chat = window.group_link_zone.text()
    chat = inp_chat.replace("+", "joinchat/")
    chat_id = 0
    total_append = int(window.group_add_zone.text())
    each_append = int(window.group_each_zone.text())
    min_pause = int(window.group_pausemin_zone.text())
    max_pause = int(window.group_pausemax_zone.text())

    users_id = []
    for filename in os.listdir("result"):
        if not ".xlsx" in filename:
            continue
        f = os.path.join("result", filename)
        if os.path.isfile(f):
            all_users_info = pd.read_excel(f)
            for i in range(len(all_users_info["username"])):
                if all_users_info["username"][i]:
                    try:
                        if isnan(all_users_info["username"][i]):
                            continue
                    except:
                        pass
                    users_id.append(all_users_info["username"][i])

    with open("accounts.txt") as f:
        all_clients = []
        for line in f:
            phone = line.strip()
            client = TelegramClient(phone, api_id, api_hash)
            window.add_log_inform("starting "+phone)
            client.connect()
            if not client.is_user_authorized():
                client.send_code_request(phone)
                print("sended")
                signals.code_request.emit([client, window, phone])
                while not client.is_user_authorized():
                    print(signals.next_client)
                    if signals.next_client:
                        break
                if signals.next_client:
                    signals.next_client = False
                    continue
            else:
                client_sign_in(False, client, window, phone)
            if not chat_id:
                client.connect()
                chat_id = client.get_entity(chat).id
                print(chat_id, type(chat_id))
            all_clients.append(client)
    print(all_clients)
    invite = FullInvite(all_clients, chat_id, users_id, total_append,
                    (min_pause, max_pause), each_append, window)
    invite.invite_users()

def client_sign_in(code, client, window, phone):
    if code:
        client.sign_in(phone, code)
    
    inp_chat = window.group_link_zone.text()
    try:
        client(JoinChannelRequest(inp_chat))
    except:
        pass
    try:
        client(ImportChatInviteRequest(
            inp_chat.replace("https://t.me/+", "")))
    except:
        pass
    client.disconnect()
