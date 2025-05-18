import math


import config as cfg


def rating_calculation(song_constant: str, song_score: float):
    for const, (lower_bound, upper_bound) in list(cfg.RANK_CONSTANT_DICT.items()):
        if lower_bound <= song_score <= upper_bound:
            song_rank_const = const
            break
    
    if song_score >= 100.5:
        DX_rating = float(song_constant.replace("~", "")) * song_rank_const * 100.5
    else:
        DX_rating = float(song_constant.replace("~", "")) * song_rank_const * song_score
    
    rating = math.floor(DX_rating)

    return rating


def rank_calculation(score: float):
    for rank, (lower_bound, upper_bound) in list(cfg.RANK_DICT.items()):
        if lower_bound <= score <= upper_bound:
            song_rank = rank
            break

    return song_rank


def get_rating_base_image(DX_rating: int):
    for color, (lower_bound, upper_bound) in list(cfg.RATING_BASE_COLOR_DICT.items()):
        if lower_bound <= DX_rating <= upper_bound:
            rating_base_color = color
            break

    rating_base_image_path = cfg.RATING_BASE_ICON_DIR + f"/rating_base_{rating_base_color}.png"

    return rating_base_image_path


def song_data_process(song_data_list: list):
    for song_data in song_data_list:
        song_data["song_jacket_url"] = cfg.SONG_JACKET_URL + song_data["song_jacket_url"]
        song_data["song_rank"] = rank_calculation(song_data["song_score"])
        song_data["song_rank"] = cfg.SCORE_ICON_DIR + "/music_icon_" + song_data["song_rank"].lower().replace("+", "p") + ".png"
        song_data["song_score"] = f"{song_data["song_score"]:.4f}%"

        if song_data["fcap"] == "":
            song_data["fcap"] = cfg.SCORE_ICON_DIR + "/music_icon_back.png"
        else:
            song_data["fcap"] = cfg.SCORE_ICON_DIR + "/music_icon_" + song_data["fcap"].lower().replace("+", "p") + ".png"

        if song_data["sync"] == "":
            song_data["sync"] = cfg.SCORE_ICON_DIR + "/music_icon_back.png"
        elif song_data["sync"] == "SP":
            song_data["sync"] = cfg.SCORE_ICON_DIR + "/music_icon_sync.png"
        else:
            song_data["sync"] = cfg.SCORE_ICON_DIR + "/music_icon_" + song_data["sync"].lower().replace("+", "p") + ".png"
    return song_data_list


def song_recommend_process(song_data_list: list, list_type: str):
    rank_list = list(cfg.RANK_DICT.keys())
    song_recommend_list = []

    if list_type == "N15":
        best_song_list = song_data_list[:15]
        min_rating = best_song_list[-1]["rating"]
    elif list_type == "P35":
        best_song_list = song_data_list[:35]
        min_rating = best_song_list[-1]["rating"]



    for song_data in song_data_list:
        drop_data = True
        song_data["song_jacket_url"] = cfg.SONG_JACKET_URL + song_data["song_jacket_url"]
        song_data["song_rank"] = rank_calculation(song_data["song_score"])

        if song_data["song_rank"] == "SSS+":
            continue

        if song_data in best_song_list:
            song_data["song_target_rank"] = rank_list[rank_list.index(song_data["song_rank"]) + 1]
            song_data["song_target_score"] = cfg.RANK_DICT[song_data["song_target_rank"]][0]
            song_data["target_rating"] = rating_calculation(song_data["song_constant"], song_data["song_target_score"])
            song_data["rating_increment"] = song_data["target_rating"] - song_data["rating"]

            drop_data = False
        else:
            for rank in rank_list:
                target_score = cfg.RANK_DICT[rank][0]
                target_rating = rating_calculation(song_data["song_constant"], target_score)
                if target_rating > min_rating:
                    song_data["song_target_rank"] = rank
                    song_data["song_target_score"] = target_score
                    song_data["target_rating"] = target_rating
                    song_data["rating_increment"] = song_data["target_rating"] - min_rating

                    drop_data = False
                    break

        if not drop_data:
            song_data["sort_alg"] = int(song_data["rating_increment"] / ((song_data["song_target_score"] - song_data["song_score"])))

            song_data["song_score"] = f"{song_data["song_score"]:.4f}%<br>{song_data["song_rank"]}"
            song_data["song_target_score"] = f"{song_data["song_target_score"]}%<br>{song_data["song_target_rank"]}"
            song_data["target_rating"] = f"{song_data["rating"]} → {song_data["target_rating"]}"
            song_data["rating_increment"] = f"(+{song_data["rating_increment"]})"

            song_recommend_list.append(song_data)

    return song_recommend_list

