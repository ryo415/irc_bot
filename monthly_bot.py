#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import socket
import os
import datetime
import time
import threading
import requests
import re
import random
import json
import schedule
from bs4 import BeautifulSoup

TARGET = ""
PORT = 
CHANNEL = ""

BUF_SIZE = 1024

USER = ""


def irc_connect(irc_socket, target, port):
    irc_socket.connect((target, port))


# IRCサーバへのログイン
def login(irc_server, nickname, username, realname, hostname="hostname", servername="*"):
    nick_message = "NICK " + nickname + "\n"
    user_message = "USER %s %s %s :%s\n" % (username, hostname, servername, realname)

    irc_server.send(nick_message.encode('utf-8'))
    irc_server.send(user_message.encode('utf-8'))


# チャンネルへの参加
def join(irc_server, channel):
    join_message = "JOIN " + channel + "\n"

    irc_server.send(join_message.encode('utf-8'))


# PINGへの返答
def pong(irc_server, daemon, daemon2=None):
    pong_message = "PONG :%s %s" % (daemon, daemon2)
    pong_message += "\n"

    irc_server.send(pong_message.encode('utf-8'))


# メッセージの送信
def privmsg(irc_server, channel, text):
    privmsg_message = "PRIVMSG %s :%s\n" % (channel, text)

    irc_server.send(privmsg_message.encode('iso2022_jp'))


# NOTICEメッセージの送信
def noticemsg(irc_server, channel, text):
    notice_message = "NOTICE %s :%s\n" % (channel, text)

    irc_server.send(notice_message.encode('iso2022_jp'))


# ログファイルの書き込み
def write_log(text):
    d = datetime.datetime.today()
    filename = 'log/' + str(d.month) + str(d.day) + '.log'
    output = str(d.hour) + ':' + str(d.minute) + ':' + str(d.second) + ' ' + text + '\n'
    f = open(filename, 'a')
    f.write(output)
    f.close()

# member配列からランダムに文字列を返す
def random_func(irc_server, channel):
    member = []
    random_member = random.choice(member)

    noticemsg(irc_server, channel, random_member)


def return_month_name(month):
    month_name = ["January", "Feburary", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    return month_name[month-1]

def priv_response(irc_server, channel, text, d):
    global do_flag, error_flag
    global curry_flag, ramen_flag, shime_flag, asakai_flag, task_flag

    if text == "print help":
        # ヘルプを記載

# 様々なメッセージの送信
def send_msg(irc_server, channel, command, text):
    global error_flag
    global do_flag
    d = datetime.datetime.today()

    if command == "PING":
        pong(irc_server, text)

    elif command == "PRIVMSG":
        priv_response(irc_server, channel, text, d)

    elif command == "ERROR":
        # write_log('ERROR:' + text)
        error_flag = 1


# IRCメッセージの受信
def wait_message(irc_server, channel):
    while(True):
        global error_flag
        global do_flag
        msg_buf = irc_server.recv(BUF_SIZE)
        msg_buf = msg_buf.decode('utf-8')
        msg_buf = msg_buf.strip()
        text = msg_buf
        if error_flag == 1:
            break
        else:
            prefix = None
            if msg_buf[0] == ":":
                p = msg_buf.find(" ")
                prefix = msg_buf[1:p]
                msg_buf = msg_buf[(p + 1):]
            p = msg_buf.find(":")
            if p != -1:  # has last param which starts with ":"
                last_param = msg_buf[(p + 1):]
                msg_buf = msg_buf[:p]
                msg_buf = msg_buf.strip()

            messages = msg_buf.split()
            command = messages[0]

            send_msg(irc_server, channel, command, last_param)

        time.sleep(1)

# 通知
def notice_schedule(irc_server, channel):
    while(True):
        global do_flag
        global curry_flag, ramen_flag, shime_flag, asakai_flag, task_flag

        d = datetime.datetime.today()
        if error_flag == 1:
            break
# .day: 日にち
# .hour: 時
# .minute: 分
# .second: 秒
# 10 o'clock
        elif d.hour == 9 and d.minute == 0 and d.second == 0:
            if d.day == 1:
                privmsg(irc_server, channel, "月初め")

        time.sleep(1.0)

def main():
    while(True):
        nickname = "bot"
        username = "bot"
        realname = "bot"
        channel = CHANNEL
        error_flag = 0

        irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        irc_connect(irc, TARGET, PORT)

        login(irc, nickname, username, realname)

        join(irc, channel)

        thread_wait = threading.Thread(target=wait_message, kwargs={'irc_server': irc, 'channel': channel})
        thread_wait.setDaemon(True)
        thread_wait.start()
        notice_schedule(irc, channel)
        time.sleep(5)


if __name__ == "__main__":
    main()
