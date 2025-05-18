import json
import pandas as pd

import config as cfg

def main(server_version: str):
    maimai_data_path = cfg.MAIMAI_DATA_PATHS[server_version]
    with open(maimai_data_path, "r") as f:
        maimai_data = json.load(f)

    version_data_path = cfg.MAIMAI_VERSION_DATA_PATH
    with open(version_data_path, "r") as f:
        version_data = json.load(f)
    
    version_data = version_data["songs"]

    song_data_list = []

    for song_data in maimai_data:
        song_keys = song_data.keys()
        song_name = song_data["title"]
        song_jacket_url = song_data["image_url"]

        try:
            for version_data_song in version_data:
                if version_data_song["title"] == song_name:
                    matched_song = True
                    for sheets in version_data_song["sheets"]:
                        if sheets["type"] == "dx":
                            DX_chart_version = sheets["version"]
                            if server_version == "INTL" and "version" in list(sheets["regionOverrides"]["intl"].keys()):
                                DX_chart_version = sheets["regionOverrides"]["intl"]["version"]
                        if sheets["type"] == "std":
                            STD_chart_version = sheets["version"]
                            if server_version == "INTL" and "version" in list(sheets["regionOverrides"]["intl"].keys()):
                                STD_chart_version = sheets["regionOverrides"]["intl"]["version"]

            if not matched_song:
                raise ValueError
        except:
            print(song_name)
            DX_chart_version = ""
            STD_chart_version = ""

        if "lev_bas" in song_keys:
            song_const_list = []
            song_chart_version = "STD"
            
            for difficulty in list(cfg.DATA_JSON_DIFFICULTY_KEYS.keys()):
                song_detail_const_key = f"lev_{cfg.DATA_JSON_DIFFICULTY_KEYS[difficulty]}_i"
                song_display_const_key = f"lev_{cfg.DATA_JSON_DIFFICULTY_KEYS[difficulty]}"
                if song_detail_const_key in song_keys and song_data[song_detail_const_key] != "":
                    song_const = song_data[song_detail_const_key]
                    song_const_list.append(song_const)
                elif song_display_const_key in song_keys:
                    song_const = song_data[song_display_const_key]
                    if "+" in song_const:
                        song_const = song_const.replace("+", ".6~")
                    else:
                        song_const = song_const + ".0~"
                    song_const_list.append(song_const)
                else:
                    song_const_list.append("")
            
            song_data_row = [song_name, song_chart_version, song_jacket_url, STD_chart_version] + song_const_list
            song_data_list.append(song_data_row)
        
        if "dx_lev_bas" in song_keys:
            song_const_list = []
            song_chart_version = "DX"
            
            for difficulty in list(cfg.DATA_JSON_DIFFICULTY_KEYS.keys()):
                song_detail_const_key = f"dx_lev_{cfg.DATA_JSON_DIFFICULTY_KEYS[difficulty]}_i"
                song_display_const_key = f"dx_lev_{cfg.DATA_JSON_DIFFICULTY_KEYS[difficulty]}"
                if song_detail_const_key in song_keys and song_data[song_detail_const_key] != "":
                    song_const = song_data[song_detail_const_key]
                    song_const_list.append(song_const)
                elif song_display_const_key in song_keys:
                    song_const = song_data[song_display_const_key]
                    if "+" in song_const:
                        song_const = song_const.replace("+", ".6~")
                    else:
                        song_const = song_const + ".0~"
                    song_const_list.append(song_const)
                else:
                    song_const_list.append("")
            
            song_data_row = [song_name, song_chart_version, song_jacket_url, DX_chart_version] + song_const_list
            song_data_list.append(song_data_row)
                
    song_df = pd.DataFrame(song_data_list, columns=["Song Name", "Chart Version", "Image URL", "Version", "BASIC", "ADVANCED", "EXPERT", "MASTER", "REMASTER"])
    song_df.to_csv(cfg.SONG_CONST_CSV_PATHS[server_version], index=False)


if __name__ == "__main__":
    main("JP")