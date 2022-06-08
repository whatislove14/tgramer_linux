from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import PeerFloodError
import os
import time
import pandas as pd

from PyQt5.QtCore import pyqtSignal, QObject, QEventLoop, QTimer

from math import isnan


class ClientSig(QObject):
    code_request = pyqtSignal(list)
    next_client = False


signals = ClientSig()


class Sender:
    def __init__(self, clients: list, pause: int, users: list, message: str, send_file, total_users: int, each_users: int, window) -> None:
        self.clients = clients
        self.pause = pause
        self.users = users
        self.message = message
        self.send_file = send_file
        self.total_users = total_users
        self.each_users = each_users

        self.window = window

    def send_messages(self):
        num_client = 0
        now_total = 0
        now_each = 0
        if not self.clients:
            self.window.add_log_warn("Enter accounts to use")
            return

        client = self.clients[num_client]
        client.connect()
        self.window.add_log_inform("starting "+str(client.get_me().phone))

        for user in self.users:
            if now_total >= self.total_users:
                break

            if now_each >= self.each_users:
                client.disconnect()
                num_client += 1
                if num_client >= len(self.clients):
                    break

                client = self.clients[num_client]
                client.connect()
                self.window.add_log_inform("starting "+str(client.get_me().phone))
                now_each = 0
            try:
                self.window.add_log_inform("sending message to: " + user)

                receiver = client.get_entity(user)
                if self.send_file:
                    client.send_file(receiver, self.send_file,
                                     caption=self.message)
                else:
                    client.send_message(receiver, self.message)
                self.window.add_log_inform("waiting {} seconds".format(self.pause))

                loop = QEventLoop()
                QTimer.singleShot(self.pause*1000, loop.quit)
                loop.exec_()
            except PeerFloodError:
                self.window.add_log_warn("Достигли лимита запросов на аккаунт. Переключаемся")
                client.disconnect()

                num_client += 1
                if num_client >= len(self.clients):
                    break

                client = self.clients[num_client]
                client.connect()
                self.window.add_log_inform("starting "+str(client.get_me().phone))

            except Exception as e:
                self.window.add_log_warn(e)
                continue

            now_total += 1
            now_each += 1
        self.window.add_log_inform("end mailing")

def start_mailing(window):
    users_id = []
    for filename in os.listdir("result"):
        if ".xlsx" not in filename:
            continue
        f = os.path.join("result", filename)
        if os.path.isfile(f):
            all_users_info = pd.read_excel(f)
            for i in range(len(all_users_info["username"])):
                try:
                    if isnan(all_users_info["username"][i]):
                        continue
                except:
                    pass
                users_id.append(all_users_info["username"][i])
    image = window.file_to_send
    api_id = 3429312
    api_hash = '1ad0f9e1aed206dc0b9caa654221b1fe'

    all_clients = []
    message = window.mes_zone.toPlainText()
    total_append = int(window.mes_total.text())
    each_append = int(window.mes_each.text())
    min_pause = int(window.mes_pause.text())

    with open("accounts.txt") as f:
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
            all_clients.append(client)

    sender = Sender(all_clients, min_pause, users_id,
                    message, image, total_append, each_append, window)
    sender.send_messages()


def client_sign_in(code, client, window, phone):
    if code:
        client.sign_in(phone, code)
    client.disconnect()
