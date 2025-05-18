import os
import json
from asyncio import to_thread
from datetime import datetime as dt

from nicegui import ui, app
from PIL import Image

import config as cfg
from retrieve_maiNET_data import *
from utils import *

app.add_static_files("/static", "static")
username = ""
password = ""
server_version = ""
user_ID = ""
DX_rating = "0"
user_icon_url = ""


def login_page():
    async def on_submit():
        global username
        global password
        global server_version
        global user_ID
        global DX_rating
        global user_icon_url

        username = username_input.value
        password = password_input.value
        server_version = server_version_input.value

        noti = ui.notification(timeout=None)
        noti.spinner = True

        noti.message = "Logging in maiNET"
        driver = await to_thread(create_web_instance, cfg.EDGE_DRIVER_PATH)
        user_ID, DX_rating, user_icon_url = await to_thread(login_maimai_net, driver, username, password, server_version)
        if user_ID is None:
            raise ValueError("Login maiNET unsuccessful.")
        
        current_song_score_list, past_song_score_list = await to_thread(get_all_song_score, driver, username, server_version, noti)
        noti.message = "Retrieving Recent Play Data"
        recent_song_score_list = await to_thread(retrieve_recent_data, driver, server_version)
        
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
            
        driver.quit()
        # noti_message.clear()
        ui.navigate.to("/B50")

    with ui.card().style("width: 300px; margin: 100px auto"):
        ui.label("Login").classes("text-h5 text-center")
        username_input = ui.input("SEGA ID").classes("w-full")
        password_input = ui.input("Password").props("type=password").classes("w-full")
        server_version_input = ui.select(["INTL", "JP"], label="Server Version", value="INTL").classes("w-full")

        ui.button("Login", on_click=on_submit).classes("w-full")


def navigation_bar():
    def on_B50():
        ui.navigate.to("/B50")
    def on_song_recommend():
        ui.navigate.to("/song_recommend")
    def on_playlog():
        ui.navigate.to("/playlog")
    def on_friends_score():
        ui.navigate.to("/friends_score")
    def on_logout():
        ui.navigate.to("/")


    with ui.button_group():
        ui.button("B50 查詢", on_click=on_B50)
        ui.button("歌曲推薦", on_click=on_song_recommend)
        ui.button("遊玩歷史", on_click=on_playlog)
        ui.button("好友分數", on_click=on_friends_score)
        ui.button("登出", on_click=on_logout)


def B50_page():
    global username
    global password
    global server_version
    global user_ID
    global DX_rating
    global user_icon_url


    def read_B50_data(username: str, server_version: str):
        player_data_dir = cfg.PLAYER_DATA_DIR.replace("xxxxxxxx", username).replace("ssss", server_version)
        current_score_data_path = f"{player_data_dir}/current_score_data.json"
        past_score_data_path = f"{player_data_dir}/past_score_data.json"

        if os.path.exists(current_score_data_path):
            with open(current_score_data_path, "r") as f:
                current_score_data_list = json.load(f)
        else:
            raise FileNotFoundError       
        
        if os.path.exists(past_score_data_path):
            with open(past_score_data_path, "r") as f:
                past_score_data_list = json.load(f)
        else:
            raise FileNotFoundError
    
        N15_data = sorted(current_score_data_list, key=lambda x: x["rating"], reverse=True)[:15]
        P35_data = sorted(past_score_data_list, key=lambda x: x["rating"], reverse=True)[:35]

        N15_data = song_data_process(N15_data)
        P35_data = song_data_process(P35_data)

        return P35_data, N15_data

    P35_data, N15_data = read_B50_data(username, server_version)

    ui.add_head_html(cfg.TABLE_STYLE_SETTING)
    navigation_bar()

    top_info_container = ui.row().classes("w-full")
    with top_info_container:
        with ui.card().style("height: 120px; width: 310px;"):
            with ui.row():
                ui.image(user_icon_url).style("width: 90px")
                with ui.column():
                    ui.label(user_ID).style("font-size: 20px; font-weight: bold;")
                    ui.image(get_rating_base_image(int(DX_rating))).style("width: 150px;")
                    ui.label(" ".join(DX_rating)).style("position: absolute; top: 70px; right: 48px; color: white; font-size: 20px; text-align: left;")


    columns = [
        {"name": "song_jacket_url", "label": "", "field": "song_jacket_url"},
        {"name": "song_name", "label": "歌曲", "field": "song_name", "style": "width: 260px;"},
        {"name": "song_chart_version", "label": "", "field": "song_chart_version", "align": "center", "sortable": True, "style": "width: 32px;"},
        {"name": "song_constant", "label": "定數", "field": "song_constant", "align": "center", "sortable": True},
        {"name": "song_score", "label": "分數", "field": "song_score", "align": "center", "sortable": True},
        {"name": "song_rank", "label": "等級", "field": "song_rank", "align": "center", "sortable": True},
        {"name": "fcap", "label": "", "field": "fcap", "align": "center", "sortable": True},
        {"name": "sync", "label": "", "field": "sync", "align": "center", "sortable": True},
        {"name": "rating", "label": "Rating", "field": "rating", "align": "center", "sortable": True, "style": "font-weight: bold; font-size: 18px"},
    ]

    B50_container = ui.row().classes("w-full")
    with B50_container:
        with ui.column():
            columns[0]["label"] = "New-15"
            
            N15_table = ui.table(columns=columns, rows=N15_data, column_defaults={"align": "left"}).classes("song-table")
            N15_table.add_slot("body-cell-song_jacket_url", cfg.JACKET_SLOT_SETTING)
            N15_table.add_slot("body-cell-song_name", cfg.B50_SONG_NAME_SLOT_SETTING)
            N15_table.add_slot("body-cell-song_rank", cfg.RANK_SLOT_SETTING)
            N15_table.add_slot("body-cell-fcap", cfg.FCAP_SLOT_SETTING)
            N15_table.add_slot("body-cell-sync", cfg.SYNC_SLOT_SETTING)

        with ui.column():
            columns[0]["label"] = "Past-35"

            P35_table = ui.table(columns=columns, rows=P35_data, column_defaults={"align": "left"}).classes("song-table")
            P35_table.add_slot("body-cell-song_jacket_url", cfg.JACKET_SLOT_SETTING)
            P35_table.add_slot("body-cell-song_name", cfg.B50_SONG_NAME_SLOT_SETTING)
            P35_table.add_slot("body-cell-song_rank", cfg.RANK_SLOT_SETTING)
            P35_table.add_slot("body-cell-fcap", cfg.FCAP_SLOT_SETTING)
            P35_table.add_slot("body-cell-sync", cfg.SYNC_SLOT_SETTING)


def recommend_page():
    global username
    global password
    global server_version
    global user_ID
    global DX_rating
    global user_icon_url

    def read_B50_data(username: str, server_version: str):
        player_data_dir = cfg.PLAYER_DATA_DIR.replace("xxxxxxxx", username).replace("ssss", server_version)
        current_score_data_path = f"{player_data_dir}/current_score_data.json"
        past_score_data_path = f"{player_data_dir}/past_score_data.json"

        if os.path.exists(current_score_data_path):
            with open(current_score_data_path, "r") as f:
                current_score_data_list = json.load(f)
        else:
            raise FileNotFoundError       
        
        if os.path.exists(past_score_data_path):
            with open(past_score_data_path, "r") as f:
                past_score_data_list = json.load(f)
        else:
            raise FileNotFoundError
    
        N15_data = sorted(current_score_data_list, key=lambda x: x["rating"], reverse=True)
        P35_data = sorted(past_score_data_list, key=lambda x: x["rating"], reverse=True)

        N15_recommend = song_recommend_process(N15_data, "N15")
        P35_recommend = song_recommend_process(P35_data, "P35")

        N15_recommend = sorted(N15_recommend, key=lambda x: x["sort_alg"], reverse=True)
        P35_recommend = sorted(P35_recommend, key=lambda x: x["sort_alg"], reverse=True)

        return N15_recommend, P35_recommend

    N15_recommend, P35_recommend = read_B50_data(username, server_version)

    ui.add_head_html(cfg.TABLE_STYLE_SETTING)
    navigation_bar()

    top_info_container = ui.row().classes("w-full")
    with top_info_container:
        with ui.card().style("height: 120px; width: 310px;"):
            with ui.row():
                ui.image(user_icon_url).style("width: 90px")
                with ui.column():
                    ui.label(user_ID).style("font-size: 20px; font-weight: bold;")
                    ui.image(get_rating_base_image(int(DX_rating))).style("width: 150px;")
                    ui.label(" ".join(DX_rating)).style("position: absolute; top: 70px; right: 48px; color: white; font-size: 20px; text-align: left;")


    columns = [
        {"name": "song_jacket_url", "label": "", "field": "song_jacket_url"},
        {"name": "song_name", "label": "歌曲", "field": "song_name", "style": "width: 260px;"},
        {"name": "song_chart_version", "label": "", "field": "song_chart_version", "align": "center", "style": "width: 32px;"},
        {"name": "song_constant", "label": "定數", "field": "song_constant", "align": "center"},
        {"name": "song_score", "label": "分數", "field": "song_score", "align": "center"},
        {"name": "song_target_score", "label": "目標分數", "field": "song_target_score", "align": "center"},
        {"name": "target_rating", "label": "Rating", "field": "target_rating", "align": "center", "style": "font-weight: bold; font-size: 16px"},
        {"name": "rating_increment", "label": "", "field": "rating_increment"},
    ]

    B50_container = ui.row().classes("w-full")
    with B50_container:
        with ui.column():
            columns[0]["label"] = "新版本"
            
            N15_table = ui.table(columns=columns, rows=N15_recommend, column_defaults={"align": "left"}, pagination=25).classes("song-table")
            N15_table.add_slot("body-cell-song_jacket_url", cfg.JACKET_SLOT_SETTING)
            N15_table.add_slot("body-cell-song_name", cfg.B50_SONG_NAME_SLOT_SETTING)
            N15_table.add_slot("body-cell-song_score", cfg.SCORE_RANK_DISPLAY_SOLT_SETTING)
            N15_table.add_slot("body-cell-song_target_score", cfg.SCORE_RANK_DISPLAY_SOLT_SETTING)

        with ui.column():
            columns[0]["label"] = "舊版本"

            P35_table = ui.table(columns=columns, rows=P35_recommend, column_defaults={"align": "left"}, pagination=25).classes("song-table")
            P35_table.add_slot("body-cell-song_jacket_url", cfg.JACKET_SLOT_SETTING)
            P35_table.add_slot("body-cell-song_name", cfg.B50_SONG_NAME_SLOT_SETTING)
            P35_table.add_slot("body-cell-song_score", cfg.SCORE_RANK_DISPLAY_SOLT_SETTING)
            P35_table.add_slot("body-cell-song_target_score", cfg.SCORE_RANK_DISPLAY_SOLT_SETTING)


def playlog_page():
    global username
    global password
    global server_version
    global user_ID
    global DX_rating
    global user_icon_url

    def read_playlog_data(username: str, server_version: str):
        player_data_dir = cfg.PLAYER_DATA_DIR.replace("xxxxxxxx", username).replace("ssss", server_version)
        playlog_data_path = f"{player_data_dir}/hist_score_data.json"

        if os.path.exists(playlog_data_path):
            with open(playlog_data_path, "r") as f:
                playlog_data = json.load(f)
        else:
            raise FileNotFoundError       
    
        playlog_data = sorted(playlog_data, key=lambda x: dt.strptime(x["play_time"], "%Y/%m/%d %H:%M"), reverse=True)

        playlog_data = song_data_process(playlog_data)

        return playlog_data
    

    playlog_data = read_playlog_data(username, server_version)

    ui.add_head_html(cfg.TABLE_STYLE_SETTING)
    navigation_bar()

    top_info_container = ui.row().classes("w-full")
    with top_info_container:
        with ui.card().style("height: 120px; width: 310px;"):
            with ui.row():
                ui.image(user_icon_url).style("width: 90px")
                with ui.column():
                    ui.label(user_ID).style("font-size: 20px; font-weight: bold;")
                    ui.image(get_rating_base_image(int(DX_rating))).style("width: 150px;")
                    ui.label(" ".join(DX_rating)).style("position: absolute; top: 70px; right: 48px; color: white; font-size: 20px; text-align: left;")

    columns = [
        {"name": "play_time", "label": "遊玩紀錄", "field": "play_time", "sortable": True},
        {"name": "song_jacket_url", "label": "歌曲", "field": "song_jacket_url"},
        {"name": "song_name", "label": "", "field": "song_name", "style": "width: 500px;"},
        {"name": "song_chart_version", "label": "", "field": "song_chart_version", "align": "center", "sortable": True, "style": "width: 32px;"},
        {"name": "song_constant", "label": "定數", "field": "song_constant", "align": "center", "sortable": True},
        {"name": "song_score", "label": "分數", "field": "song_score", "align": "center", "sortable": True},
        {"name": "song_rank", "label": "等級", "field": "song_rank", "align": "center", "sortable": True},
        {"name": "fcap", "label": "", "field": "fcap", "align": "center", "sortable": True},
        {"name": "sync", "label": "", "field": "sync", "align": "center", "sortable": True},
        {"name": "rating", "label": "Rating", "field": "rating", "align": "center", "sortable": True, "style": "font-weight: bold; font-size: 18px"},
    ]

    playlog_container = ui.row().classes("w-full")
    with playlog_container:
        
        playlog_table = ui.table(columns=columns, rows=playlog_data, column_defaults={"align": "left"}, pagination=50).classes("song-table")
        playlog_table.add_slot("body-cell-song_jacket_url", cfg.JACKET_SLOT_SETTING)
        playlog_table.add_slot("body-cell-song_name", cfg.PLAYLOG_SONG_NAME_SLOT_SETTING)
        playlog_table.add_slot("body-cell-song_rank", cfg.RANK_SLOT_SETTING)
        playlog_table.add_slot("body-cell-fcap", cfg.FCAP_SLOT_SETTING)
        playlog_table.add_slot("body-cell-sync", cfg.SYNC_SLOT_SETTING)

 
@ui.page("/")
def index():
    login_page()


@ui.page("/B50")
def summary():
    B50_page()


@ui.page("/song_recommend")
def recommend():
    recommend_page()


@ui.page("/playlog")
def playlog():
    playlog_page()


ui.run(
    title="maimai Viewer",
    port=8080,
    reconnect_timeout=60
)