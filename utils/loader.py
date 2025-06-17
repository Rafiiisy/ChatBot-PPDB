import json

def load_jurusan():
    with open("data/data_jurusan.json", encoding='utf-8') as f:
        return json.load(f)

def load_jadwal():
    with open("data/data_jadwal_penerimaan_murid_baru_2025.json", encoding='utf-8') as f:
        return json.load(f)

def load_video_poster():
    with open("data/data_poster_dan_video.json", encoding='utf-8') as f:
        return json.load(f)
