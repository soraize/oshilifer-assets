#!/usr/bin/env python3
"""推し検索用の一覧 data/search_index.json を作る。

data/agency.json に載っている事務所のJSONから、グループとメンバーの名前だけを集める。
data/ の JSON を直したら、このスクリプトを実行する（GitHub Actions が自動でも実行する）。
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")


def main():
    with open(os.path.join(DATA, "agency.json"), encoding="utf-8") as f:
        categories = json.load(f)

    entries = []
    for cat in categories:
        for ag in cat.get("agencies", []):
            path = os.path.join(DATA, os.path.basename(ag["detailURL"]))
            if not os.path.exists(path):
                print(f"skip (no file): {path}", file=sys.stderr)
                continue
            with open(path, encoding="utf-8") as f:
                detail = json.load(f)
            for g in detail.get("groups", []):
                gname = g.get("name") or ""
                if not gname:
                    continue
                base = {"c": cat["categoryId"], "a": ag.get("agencyId") or "", "g": gname}
                gid = g.get("masterId") or ""
                entries.append({**base, "k": "g", "n": gname, "gid": gid})
                for m in g.get("members", []):
                    mname = m.get("name") or ""
                    if not mname:
                        continue
                    e = {**base, "k": "m", "n": mname, "gid": gid, "mid": m.get("masterId") or ""}
                    if m.get("isGraduated"):
                        e["x"] = 1
                    entries.append(e)

    out = os.path.join(DATA, "search_index.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
        f.write("\n")
    print(f"{len(entries)} entries -> {out}")


if __name__ == "__main__":
    main()
