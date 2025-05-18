WORKING_DIR = "/Users/jackychung/Documents/python/maimai_viewer"

EDGE_DRIVER_PATH = f"{WORKING_DIR}/driver/msedgedriver"
MAIMAI_DATA_PATHS = {
    "INTL": f"{WORKING_DIR}/data/raw/maimai_intl_data.json",
    "JP": f"{WORKING_DIR}/data/raw/maimai_jp_data.json",
}
SONG_CONST_CSV_PATHS = {
    "INTL": f"{WORKING_DIR}/data/chart_const/maimai_chart_const_intl.csv",
    "JP": f"{WORKING_DIR}/data/chart_const/maimai_chart_const_jp.csv",
}
MAIMAI_VERSION_DATA_PATH = f"{WORKING_DIR}/data/raw/maimai_version_data.json"
PLAYER_DATA_DIR = f"{WORKING_DIR}/data/player_data/xxxxxxxx/ssss"

SCORE_ICON_DIR = f"/static/score_icon"
RATING_BASE_ICON_DIR = f"/static/rating_base"

CURRENT_VERSION = {
    "INTL": "PRiSM",
    "JP": "PRiSM PLUS"
}

MAIMAI_NET_LOGIN_URL = "https://lng-tgk-aime-gw.am-all.net/common_auth/login?site_id=maimaidxex&redirect_url=https://maimaidx-eng.com/maimai-mobile/&back_url=https://maimai.sega.com/"
SONG_SCORE_URL = "https://maimaidx-eng.com/maimai-mobile/record/musicGenre/search/?genre=99&diff="
RECENT_SCORE_URL = "https://maimaidx-eng.com/maimai-mobile/record/"

SONG_JACKET_URL = "https://maimaidx-eng.com/maimai-mobile/img/Music/"

DX_CHART_ICON_URL = "https://maimaidx-eng.com/maimai-mobile/img/music_dx.png"
STD_CHART_ICON_URL = "https://maimaidx-eng.com/maimai-mobile/img/music_standard.png"

EMPTY_ICON_URL = "https://maimaidx-eng.com/maimai-mobile/img/music_icon_back.png?ver=1.50"
FC_ICON_URL = "https://maimaidx-eng.com/maimai-mobile/img/music_icon_fc.png?ver=1.50"
FCP_ICON_URL = "https://maimaidx-eng.com/maimai-mobile/img/music_icon_fcp.png?ver=1.50"
AP_ICON_URL = "https://maimaidx-eng.com/maimai-mobile/img/music_icon_ap.png?ver=1.50"
APP_ICON_URL = "https://maimaidx-eng.com/maimai-mobile/img/music_icon_app.png?ver=1.50"

SYNC_ICON_URL_DICT = {
    "https://maimaidx-eng.com/maimai-mobile/img/music_icon_back.png?ver=1.50": "",
    "https://maimaidx-eng.com/maimai-mobile/img/music_icon_sync.png?ver=1.50": "SP",
    "https://maimaidx-eng.com/maimai-mobile/img/music_icon_fs.png?ver=1.50": "FS",
    "https://maimaidx-eng.com/maimai-mobile/img/music_icon_fsp.png?ver=1.50": "FS+",
    "https://maimaidx-eng.com/maimai-mobile/img/music_icon_fdx.png?ver=1.50": "FDX",
    "https://maimaidx-eng.com/maimai-mobile/img/music_icon_fdxp.png?ver=1.50": "FDX+",
}
FCAP_ICON_URL_DICT = {
    "https://maimaidx-eng.com/maimai-mobile/img/music_icon_back.png?ver=1.50": "",
    "https://maimaidx-eng.com/maimai-mobile/img/music_icon_fc.png?ver=1.50": "FC",
    "https://maimaidx-eng.com/maimai-mobile/img/music_icon_fcp.png?ver=1.50": "FC+",
    "https://maimaidx-eng.com/maimai-mobile/img/music_icon_ap.png?ver=1.50": "AP",
    "https://maimaidx-eng.com/maimai-mobile/img/music_icon_app.png?ver=1.50": "AP+",
}
SYNC_PLAYLOG_ICON_URL_DICT = {
    "https://maimaidx-eng.com/maimai-mobile/img/playlog/sync_dummy.png?ver=1.50": "",
    "https://maimaidx-eng.com/maimai-mobile/img/playlog/sync.png?ver=1.50": "SP",
    "https://maimaidx-eng.com/maimai-mobile/img/playlog/fs.png?ver=1.50": "FS",
    "https://maimaidx-eng.com/maimai-mobile/img/playlog/fsplus.png?ver=1.50": "FS+",
    "https://maimaidx-eng.com/maimai-mobile/img/playlog/fsd.png?ver=1.50": "FDX",
    "https://maimaidx-eng.com/maimai-mobile/img/playlog/fsdplus.png?ver=1.50": "FDX+",
}
FCAP_PLAYLOG_ICON_URL_DICT = {
    "https://maimaidx-eng.com/maimai-mobile/img/playlog/fc_dummy.png?ver=1.50": "",
    "https://maimaidx-eng.com/maimai-mobile/img/playlog/fc.png?ver=1.50": "FC",
    "https://maimaidx-eng.com/maimai-mobile/img/playlog/fcplus.png?ver=1.50": "FC+",
    "https://maimaidx-eng.com/maimai-mobile/img/playlog/ap.png?ver=1.50": "AP",
    "https://maimaidx-eng.com/maimai-mobile/img/playlog/applus.png?ver=1.50": "AP+",
}
DIFFICULTY_ICON_URL_DICT = {
    "https://maimaidx-eng.com/maimai-mobile/img/diff_basic.png": "BASIC",
    "https://maimaidx-eng.com/maimai-mobile/img/diff_advanced.png": "ADVANCED",
    "https://maimaidx-eng.com/maimai-mobile/img/diff_expert.png": "EXPERT",
    "https://maimaidx-eng.com/maimai-mobile/img/diff_master.png": "MASTER",
    "https://maimaidx-eng.com/maimai-mobile/img/diff_remaster.png": "REMASTER"
}

DIFFICULTY_DICT = {
    "BASIC": 0,
    "ADVANCED": 1,
    "EXPERT": 2,
    "MASTER": 3,
    "REMASTER": 4
}
DATA_JSON_DIFFICULTY_KEYS = {
    "BASIC": "bas",
    "ADVANCED": "adv",
    "EXPERT": "exp",
    "MASTER": "mas",
    "REMASTER": "remas"
}
RANK_CONSTANT_DICT = {
    0: [0.0000, 9.9999],
    0.016: [10.0000, 19.9999],
    0.032: [20.0000, 29.9999],
    0.048: [30.0000, 39.9999],
    0.064: [40.0000, 49.9999],
    0.080: [50.0000, 59.9999],
    0.096: [60.0000, 69.9999],
    0.112: [70.0000, 74.9999],
    0.120: [75.0000, 79.9998],
    0.128: [79.9999, 79.9999],
    0.136: [80.0000, 89.9999],
    0.152: [90.0000, 93.9999],
    0.168: [94.0000, 96.9998],
    0.176: [96.9999, 96.9999],
    0.200: [97.0000, 97.9999],
    0.203: [98.0000, 98.9998],
    0.206: [98.9999, 98.9999],
    0.208: [99.0000, 99.4999],
    0.211: [99.5000, 99.9998],
    0.214: [99.9999, 99.9999],
    0.216: [100.0000, 100.4998],
    0.222: [100.4999, 100.4999],
    0.224: [100.5000, 101.0000]
}
RANK_DICT = {
    "D": [0.0000, 49.9999],
    "C": [50.0000, 59.9999],
    "B": [60.0000, 69.9999],
    "BB": [70.0000, 74.9999],
    "BBB": [75.0000, 79.9999],
    "A": [80.0000, 89.9999],
    "AA": [90.0000, 93.9999],
    "AAA": [94.0000, 96.9999],
    "S": [97.0000, 97.9999],
    "S+": [98.0000, 98.9999],
    "SS": [99.0000, 99.4999],
    "SS+": [99.5000, 99.9999],
    "SSS": [100.0000, 100.4999],
    "SSS+": [100.5000, 101.0000]
}
RATING_BASE_COLOR_DICT = {
    "white": [0, 999],
    "blue": [1000, 1999],
    "green": [20000, 3999],
    "orange": [4000, 6999],
    "red": [7000, 9999],
    "purple": [10000, 11999],
    "bronze": [12000, 12999],
    "silver": [13000, 13999],
    "gold": [14000, 14499],
    "platinum": [14500, 14999],
    "rainbow": [15000, 99999],
}

TABLE_STYLE_SETTING = '''
    <style>
        .song-table th {
            padding: 4px 8px;
        }
        .song-table td {
            padding: 2px 4px;
        }
        .q-table__sort-icon {
            display: none !important;
        }
    </style>
'''
B50_SONG_NAME_SLOT_SETTING = '''
    <q-td key="song_name" :props="props">
        <q-badge 
            :style="
                props.row.song_difficulty === 'BASIC' ? 'background-color: #6ed43e; color: white; max-width: 255px; word-wrap: break-word; white-space: normal;' :
                props.row.song_difficulty === 'ADVANCED' ? 'background-color: #f7b807; color: white; max-width: 255px; word-wrap: break-word; white-space: normal;' :
                props.row.song_difficulty === 'EXPERT' ? 'background-color: #ff828d; color: white; max-width: 255px; word-wrap: break-word; white-space: normal;' :
                props.row.song_difficulty === 'MASTER' ? 'background-color: #a051dc; color: white; max-width: 255px; word-wrap: break-word; white-space: normal;' :
                props.row.song_difficulty === 'REMASTER' ? 'background-color: #ee82ee; color: white; max-width: 255px; word-wrap: break-word; white-space: normal;' : 
                ''">
            {{ props.row.song_name }}
        </q-badge>
    </q-td>
'''
PLAYLOG_SONG_NAME_SLOT_SETTING = '''
    <q-td key="song_name" :props="props">
        <q-badge 
            :style="
                props.row.song_difficulty === 'BASIC' ? 'background-color: #6ed43e; color: white; max-width: 495px; word-wrap: break-word; white-space: normal;' :
                props.row.song_difficulty === 'ADVANCED' ? 'background-color: #f7b807; color: white; max-width: 495px; word-wrap: break-word; white-space: normal;' :
                props.row.song_difficulty === 'EXPERT' ? 'background-color: #ff828d; color: white; max-width: 495px; word-wrap: break-word; white-space: normal;' :
                props.row.song_difficulty === 'MASTER' ? 'background-color: #a051dc; color: white; max-width: 495px; word-wrap: break-word; white-space: normal;' :
                props.row.song_difficulty === 'REMASTER' ? 'background-color: #ee82ee; color: white; max-width: 495px; word-wrap: break-word; white-space: normal;' : 
                ''">
            {{ props.row.song_name }}
        </q-badge>
    </q-td>
'''
JACKET_SLOT_SETTING = '''
    <q-td :props="props">
        <img :src="props.value" alt="Image" style="height: 50px; min-width: 50px;">
    </q-td>
'''
RANK_SLOT_SETTING = '''
    <q-td :props="props">
        <img :src="props.value" alt="Image" style="height: 25px; min-width: 54px;">
    </q-td>
'''
FCAP_SLOT_SETTING = '''
    <q-td :props="props">
        <img :src="props.value" alt="Image" style="height: 30px; min-width: 25px;">
    </q-td>
'''
SYNC_SLOT_SETTING = '''
    <q-td :props="props">
        <img :src="props.value" alt="Image" style="height: 30px; min-width: 25px;">
    </q-td>
'''
FAVORITE_SLOT_SETTING = '''
<q-td :props="props">
    <q-btn 
        @click="$parent.$emit('favorite', props)" 
        :icon="props.value === 'True' ? 'delete' : 'add'" 
        :color="props.value === 'True' ? 'red' : 'green'" 
        flat dense
    />
</q-td>
'''
SCORE_RANK_DISPLAY_SOLT_SETTING = '''
    <q-td :props="props" v-html="props.value" style="text-align: center;">
'''

