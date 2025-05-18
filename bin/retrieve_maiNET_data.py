import os
import json
import math
import requests

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from nicegui.ui import notification

import config as cfg
from utils import *


def main():
    username = "aaa"
    password = "bbb"
    server_version = "INTL"

    driver = create_web_instance(cfg.EDGE_DRIVER_PATH)

    print("Logging In maimaiNET")
    user_ID, DX_rating, user_icon_url = login_maimai_net(driver, username, password, server_version)
    if user_ID is None:
        raise ValueError("Login maiNET unsuccessful.")
    print(user_ID, DX_rating)

    current_song_score_list, past_song_score_list = get_all_song_score(driver, username, server_version)
    recent_song_score_list = retrieve_recent_data(driver, server_version)
    
    player_data_dir = cfg.PLAYER_DATA_DIR.replace("xxxxxxxx", username).replace("ssss", server_version)
    os.makedirs(player_data_dir, exist_ok=True)

    current_score_data_path = f"{player_data_dir}/current_score_data.json"
    past_score_data_path = f"{player_data_dir}/past_score_data.json"
    hist_score_data_path = f"{player_data_dir}/hist_score_data.json"


    if os.path.exists(hist_score_data_path):
        with open(hist_score_data_path, "r") as f:
            hist_score_data_list = json.load(f)
    else:
        hist_score_data_list = []
    
    for recent_score_data in recent_song_score_list:
        if recent_score_data not in hist_score_data_list:
            hist_score_data_list.append(recent_score_data)

    with open(current_score_data_path, "w") as f:
        json.dump(current_song_score_list, f, indent=4)
    with open(past_score_data_path, "w") as f:
        json.dump(past_song_score_list, f, indent=4)   
    with open(hist_score_data_path, "w") as f:
        json.dump(hist_score_data_list, f, indent=4)

def create_web_instance(web_driver_path: str):
    options = webdriver.EdgeOptions()
    options.add_argument("--window-size=100,100")
    cService = webdriver.EdgeService(executable_path=web_driver_path)
    driver = webdriver.Edge(service=cService, options=options)

    return driver

def login_maimai_net(driver: webdriver.Edge, username: str, password: str, server_version: str):
    driver.get(cfg.MAIMAI_NET_LOGIN_URL)

    SEGA_ID_button = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/main/article/section[2]/dl/dt/ul/li/span")
    username_input_box = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/main/article/section[2]/dl/dd/form/ul/li[1]/div[2]/input")
    password_input_box = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/main/article/section[2]/dl/dd/form/ul/li[2]/div[2]/input")
    login_button = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/main/article/section[2]/dl/dd/form/div/input")

    SEGA_ID_button.click()
    username_input_box.send_keys(username)
    password_input_box.send_keys(password)
    login_button.click()

    soup = BeautifulSoup(driver.page_source, "html.parser")
    user_ID = soup.find("div", attrs={"class": "name_block f_l f_16"}).contents[0]
    DX_rating = soup.find("div", attrs={"class": "rating_block"}).contents[0]
    user_icon_url = soup.find("div", attrs={"class": "basic_block p_10 f_0"}).contents[1].attrs["src"]

    return user_ID, DX_rating, user_icon_url


def get_all_song_score(driver: webdriver.Edge, username: str, server_version: str, noti: notification):
    current_song_score_list = []
    past_song_score_list = []
    for i, difficulty in enumerate(list(cfg.DIFFICULTY_DICT.keys())):
        noti.message = f"Retrieving {difficulty} Data"
        current_song_score_list_by_diff, past_song_score_list_by_diff = retrieve_song_data(driver, difficulty, server_version)
        current_song_score_list += current_song_score_list_by_diff
        past_song_score_list += past_song_score_list_by_diff

    current_song_score_list = calculate_rating(current_song_score_list)
    past_song_score_list = calculate_rating(past_song_score_list)
    current_song_score_list = sorted(current_song_score_list, key=lambda x: x["rating"], reverse=True)
    past_song_score_list = sorted(past_song_score_list, key=lambda x: x["rating"], reverse=True)

    return current_song_score_list, past_song_score_list


def retrieve_song_data(driver: webdriver.Edge, difficulty: str, server_version: str):
    difficulty_num = cfg.DIFFICULTY_DICT[difficulty]
    driver.get(cfg.SONG_SCORE_URL + str(difficulty_num))
    soup = BeautifulSoup(driver.page_source, "html.parser")

    maimai_data_path = cfg.SONG_CONST_CSV_PATHS[server_version]
    song_const_df = pd.read_csv(maimai_data_path)

    current_ver_song_score_list = []
    past_ver_song_score_list = []

    song_score_element_list = soup.find_all("div", attrs={"class": "w_450 m_15 p_r f_0"})
    for song_element in song_score_element_list:
        # Retrieve all elements
        song_name = song_element.find("div", attrs={"class": "music_name_block t_l f_13 break"}).contents[0]
        song_display_level = song_element.find("div", attrs={"class": "music_lv_block f_r t_c f_14"}).contents[0]
        song_score_element = song_element.find("div", attrs={"class": "music_score_block w_112 t_r f_l f_12"})
        song_dx_score_element = song_element.find("div", attrs={"class": "music_score_block w_190 t_r f_l f_12"})
        song_chart_version_url = song_element.find("img", attrs={"class": "music_kind_icon"}).attrs["src"]
        song_score_icons = song_element.find_all("img", attrs={"class": "h_30 f_r"})

        # Get song score, if not played, score = -1
        if song_score_element is not None and song_dx_score_element is not None:
            song_score_element = song_score_element.contents
            song_dx_score_element = song_dx_score_element.contents
            song_score = float(song_score_element[0][:-1])
            song_dx_score = int(song_dx_score_element[-1].strip().split(" / ")[0].replace(",", ""))
            song_full_dx_score = int(song_dx_score_element[-1].strip().split(" / ")[1].replace(",", ""))
        else:
            continue

        # Retrieve song chart version (DX or STD)
        if song_chart_version_url == cfg.DX_CHART_ICON_URL:
            song_chart_version = "DX"
        elif song_chart_version_url == cfg.STD_CHART_ICON_URL:
            song_chart_version = "STD"

        # Retrieve song progress (FC/AP, FS/FDX)
        sync_icon_url = song_score_icons[0].attrs["src"]
        sync = cfg.SYNC_ICON_URL_DICT[sync_icon_url]
        fcap_icon_url = song_score_icons[1].attrs["src"]
        fcap = cfg.FCAP_ICON_URL_DICT[fcap_icon_url]

        # Retrieve song constant
        song_const_data = song_const_df.loc[(song_const_df["Song Name"] == song_name) & (song_const_df["Chart Version"] == song_chart_version)]
        song_jacket_url = song_const_data["Image URL"].values[0]
        song_constant = song_const_data[difficulty].values[0]
        song_version = song_const_data["Version"].values[0]

        song_score_dict = {
            "song_name": song_name, 
            "song_jacket_url": song_jacket_url,
            "song_chart_version": song_chart_version,
            "song_version": song_version,
            "song_difficulty": difficulty,
            "song_display_level": song_display_level,
            "song_constant": str(song_constant),
            "song_score": song_score, 
            "song_dx_score": song_dx_score, 
            "song_full_dx_score": song_full_dx_score,
            "fcap": fcap, 
            "sync": sync 
        }
        if song_version == cfg.CURRENT_VERSION[server_version]:
            current_ver_song_score_list.append(song_score_dict)
        else:
            past_ver_song_score_list.append(song_score_dict)

    return current_ver_song_score_list, past_ver_song_score_list


def retrieve_recent_data(driver: webdriver.Edge, server_version: str):
    print(f"Retrieving Recent Data")
    
    driver.get(cfg.RECENT_SCORE_URL)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    maimai_data_path = cfg.SONG_CONST_CSV_PATHS[server_version]
    song_const_df = pd.read_csv(maimai_data_path)

    recent_song_score_list = []

    recent_score_element_list = soup.find_all("div", attrs={"class": "p_10 t_l f_0 v_b"})
    for recent_element in recent_score_element_list:
        play_time = recent_element.find("div", attrs={"class": "sub_title t_c f_r f_11"}).contents[3].contents[0]
        song_difficulty_url = recent_element.find("img", attrs={"class": "playlog_diff v_b"}).attrs["src"]
        song_name = recent_element.find("div", attrs={"class": "basic_block m_5 p_5 p_l_10 f_13 break"}).contents[-1]
        song_chart_version_url = recent_element.find("img", attrs={"class": "playlog_music_kind_icon"}).attrs["src"]
        song_score_element = recent_element.find("div", attrs={"class": "playlog_achievement_txt t_r"})
        song_dx_score_element = recent_element.find("div", attrs={"class": "white p_r_5 f_15 f_r"}).contents[0]
        song_score_icons = recent_element.find_all("img", attrs={"class": "h_35 m_5 f_l"})

        song_score = float(song_score_element.contents[0] + song_score_element.contents[1].contents[0][:-1])
        song_dx_score = int(song_dx_score_element.strip().split(" / ")[0].replace(",", ""))
        song_full_dx_score = int(song_dx_score_element.strip().split(" / ")[1].replace(",", ""))

        # Retrieve song difficulty
        difficulty = cfg.DIFFICULTY_ICON_URL_DICT[song_difficulty_url]

        # Retrieve song chart version (DX or STD)
        if song_chart_version_url == cfg.DX_CHART_ICON_URL:
            song_chart_version = "DX"
        elif song_chart_version_url == cfg.STD_CHART_ICON_URL:
            song_chart_version = "STD"

        # Retrieve song progress (FC/AP, FS/FDX)
        fcap_icon_url = song_score_icons[0].attrs["src"]
        fcap = cfg.FCAP_PLAYLOG_ICON_URL_DICT[fcap_icon_url] 
        sync_icon_url = song_score_icons[1].attrs["src"]
        sync = cfg.SYNC_PLAYLOG_ICON_URL_DICT[sync_icon_url]

        # Retrieve song constant
        song_const_data = song_const_df.loc[(song_const_df["Song Name"] == song_name) & (song_const_df["Chart Version"] == song_chart_version)]
        song_jacket_url = song_const_data["Image URL"].values[0]
        song_constant = str(song_const_data[difficulty].values[0])
        song_version = song_const_data["Version"].values[0]

        # Retrieve song display level
        song_level = song_constant.split(".")
        if song_level[1] in ["6~", "6", "7", "8", "9"]:
            song_display_level = song_level[0] + "+"
        else:
            song_display_level = song_level[0]

        recent_score_dict = {
            "play_time": play_time,
            "song_name": song_name, 
            "song_jacket_url": song_jacket_url,
            "song_chart_version": song_chart_version,
            "song_version": song_version,
            "song_difficulty": difficulty,
            "song_display_level": song_display_level,
            "song_constant": str(song_constant),
            "song_score": song_score, 
            "song_dx_score": song_dx_score, 
            "song_full_dx_score": song_full_dx_score,
            "fcap": fcap, 
            "sync": sync 
        }
        recent_song_score_list.append(recent_score_dict)

    recent_song_score_list = calculate_rating(recent_song_score_list)

    return recent_song_score_list


def calculate_rating(song_score_list: list):
    for song_score_info in song_score_list:
        song_score = song_score_info["song_score"]
        song_constant = song_score_info["song_constant"]
        song_score_info["rating"] = rating_calculation(song_constant, song_score)

    return song_score_list


if __name__ == "__main__":
    main()
    