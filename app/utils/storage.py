from __future__ import annotations
import json
import os
from typing import Any, Dict, List

def load_json_list(path: str) -> List[Dict[str, Any]]:
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("Storage file must contain a JSON list.")
    return data

def save_json_list(path: str, items: List[Dict[str, Any]]) -> None:
    # Ghi atomically để hạn chế hỏng file nếu đang ghi mà bị tắt
    tmp_path = f"{path}.tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    os.replace(tmp_path, path)


import sqlite3
from app.db_connect import *
TABLE ="thanhpho"
def load_database(path: str) -> List[Dict[str, Any]]:
    #conn = sqlite3.connect(path)
    conn = create_connection()
    #conn.row_factory = sqlite3.Row  # để fetch ra dạng dict-like

    cur = conn.cursor(dictionary=True)
    cur.execute(f"SELECT * FROM {TABLE}")
    rows = cur.fetchall()

    data = [dict(r) for r in rows]

    conn.close()
    return data
def update_database(path: str, city: dict[str, Any],id) -> None:
    #conn = sqlite3.connect(path)
    conn = create_connection()
    #conn.row_factory = sqlite3.Row  # để fetch ra dạng dict-like
    placeholders = ", ".join(["%s"] * len(city))
    cols = list(city.keys())
    set_clause = ", ".join([f"{c} = %s" for c in cols])
    cur = conn.cursor(dictionary=True)
    columns = list(city.keys())
    values = [city[c] for c in columns]
    cur.execute(f"UPDATE {TABLE}  SET {set_clause} WHERE id={id}",values)
    conn.commit()
    conn.close()
def delete_database(path: str,id) -> None:
    #conn = sqlite3.connect(path)
    conn = create_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute(f"DELETE FROM {TABLE} WHERE id={id}")
    conn.commit()
    conn.close()
def add_database(path: str,city: Dict[str,Any]) -> None:
    #conn = sqlite3.connect(path)
    conn = create_connection()
    cur = conn.cursor(dictionary=True)

    placeholders = ", ".join(["%s"] * len(city))
    columns = list(city.keys())
    values = [city[c] for c in columns]
    col_clause = ", ".join(city)
    sql = f"INSERT INTO {TABLE} ({col_clause}) VALUES ({placeholders})"
    cur.execute(sql, values)
    conn.commit()
    conn.close()
def next_id(path: str) -> int:
    conn = create_connection()
    #conn = sqlite3.connect(path)
    try:
        cur = conn.cursor()

        # 1) Ưu tiên lấy AUTO_INCREMENT (nếu có)
        cur.execute(
            """
            SELECT AUTO_INCREMENT
            FROM information_schema.TABLES
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = %s
            """,
            (TABLE,),
        )
        row = cur.fetchone()
        if row and row[0] is not None:
            return int(row[0])

        # 2) Fallback: MAX(id) + 1
        cur.execute(f"SELECT COALESCE(MAX(`id`), 0) + 1 FROM `{TABLE}`")
        (nid,) = cur.fetchone()
        return int(nid)

    finally:
        conn.close()
def find_id(id: int)-> Dict[str, Any] :

    conn = create_connection()

    cur = conn.cursor(dictionary=True)
    cur.execute(f"SELECT * FROM {TABLE} WHERE id={id}")
    rows = cur.fetchall()

    data = [dict(r) for r in rows]

    conn.close()
    return data[0]
