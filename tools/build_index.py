#!/usr/bin/env python3
"""stories/*.json dosyalarını doğrulayıp index.json üretir.

Uygulama yalnızca index.json'u çeker; bu dosya elle düzenlenmez, push'ta
GitHub Action tarafından yeniden üretilir.
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CATEGORIES = {"kuran-kissalari", "siyer", "sahabe", "ahlak"}
REQUIRED = ("slug", "title", "category", "body", "attribution")
COVER_EXTS = (".webp", ".jpg", ".jpeg", ".png")


def main() -> int:
    errors = []
    stories = []
    for path in sorted((ROOT / "stories").glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as e:  # noqa: BLE001
            errors.append(f"{path.name}: geçersiz JSON ({e})")
            continue

        missing = [k for k in REQUIRED if not str(data.get(k, "")).strip()]
        if missing:
            errors.append(f"{path.name}: eksik alan {missing}")
            continue
        if data["slug"] != path.stem:
            errors.append(f"{path.name}: slug dosya adıyla aynı olmalı ({data['slug']})")
            continue
        if data["category"] not in CATEGORIES:
            errors.append(f"{path.name}: geçersiz category '{data['category']}'")
            continue

        refs = data.get("references", [])
        if not isinstance(refs, list) or not all(isinstance(r, str) for r in refs):
            errors.append(f"{path.name}: references string listesi olmalı")
            continue

        cover = next(
            (f"covers/{path.stem}{ext}" for ext in COVER_EXTS if (ROOT / "covers" / f"{path.stem}{ext}").exists()),
            "",
        )
        if not cover:
            errors.append(f"{path.name}: covers/{path.stem}.webp (veya jpg/png) bulunamadı")
            continue

        stories.append(
            {
                "slug": data["slug"],
                "title": data["title"],
                "category": data["category"],
                "body": data["body"],
                "attribution": data["attribution"],
                "references": refs,
                "cover": cover,
            }
        )

    if errors:
        print("HATA:\n  " + "\n  ".join(errors))
        return 1

    out = {"schema": 1, "stories": stories}
    (ROOT / "index.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
    )
    print(f"index.json: {len(stories)} hikaye")
    return 0


if __name__ == "__main__":
    sys.exit(main())
