"""Safe functional tests for DirX. Operates only under ./TEST. Does not touch Desktop/Downloads/Temp."""
from __future__ import annotations

import json
import os
import sys
import traceback
from os.path import splitext
from pathlib import Path

PROJECT = Path(__file__).resolve().parent
TEST = PROJECT / "TEST"
sys.path.insert(0, str(PROJECT))
os.chdir(PROJECT)

results = []


def rec(name, expected, actual, status, notes=""):
    results.append(
        {
            "Test": name,
            "Expected": expected,
            "Actual": str(actual),
            "Status": status,
            "Notes": notes,
        }
    )
    print(f"[{status}] {name}: {actual}")


def make_dir(p: Path) -> Path:
    p.mkdir(parents=True, exist_ok=True)
    return p


def write_files(folder: Path, names):
    import shutil

    if folder.exists():
        shutil.rmtree(folder)
    make_dir(folder)
    for n in names:
        (folder / n).write_bytes(b"sample-" + n.encode("utf-8", errors="replace"))


def main():
    import shutil

    if TEST.exists():
        shutil.rmtree(TEST)
    TEST.mkdir(parents=True, exist_ok=True)

    import tkinter as tk
    from tkinter import ttk
    from Frames import FileOrganizer, DirUnpack, BatchRename, ClearTemp, Encrypt
    from windowsdpi import set_dpi_awareness

    set_dpi_awareness()

    class DirX(tk.Tk):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.title("DirX")
            self.iconbitmap(PROJECT / "icons/dirx.ico")
            self.resizable(False, False)
            self.columnconfigure(0, weight=1)
            tabs = ttk.Notebook(self)
            self.organizer_tab = FileOrganizer(tabs)
            self.unpack_tab = DirUnpack(tabs)
            self.rename_tab = BatchRename(tabs)
            self.temp_tab = ClearTemp(tabs)
            self.encrypt_tab = Encrypt(tabs)
            tabs.add(self.organizer_tab, text="File Organizer")
            tabs.add(self.unpack_tab, text="Unpack")
            tabs.add(self.rename_tab, text="Batch Rename")
            tabs.add(self.encrypt_tab, text="Encrypt/Decrypt")
            tabs.add(self.temp_tab, text="Clear Temp")
            tabs.pack(expand=True, fill="both")
            self.tabs = tabs

    try:
        root = DirX()
        root.update_idletasks()
        tab_texts = [root.tabs.tab(i, "text") for i in root.tabs.tabs()]
        widgets_ok = all(
            [
                root.organizer_tab.select_button.winfo_exists(),
                root.organizer_tab.organize_button.winfo_exists(),
                root.organizer_tab.undo_button.winfo_exists(),
                root.rename_tab.rename_button.winfo_exists(),
                root.unpack_tab.unpack_button.winfo_exists(),
                root.encrypt_tab.encrypt_button.winfo_exists(),
                root.encrypt_tab.decrypt_button.winfo_exists(),
                root.temp_tab.clear_button.winfo_exists(),
            ]
        )
        rec(
            "TEST 01 Launch",
            "Window + 5 tabs + core buttons",
            f"tabs={tab_texts} widgets_ok={widgets_ok}",
            "PASS" if widgets_ok and len(tab_texts) == 5 else "FAIL",
        )
    except Exception as e:
        rec("TEST 01 Launch", "Window starts", e, "FAIL")
        traceback.print_exc()
        raise

    org_folder = TEST / "02_select"
    write_files(org_folder, ["a.txt"])
    root.organizer_tab.path.set(str(org_folder))
    root.update_idletasks()
    ok = root.organizer_tab.path.get() == str(org_folder)
    rec(
        "TEST 02 Select folder",
        "Path StringVar updates to TEST folder",
        root.organizer_tab.path.get(),
        "PASS" if ok else "FAIL",
        "filedialog.askdirectory not auto-clicked; path set the same way Select Folder does",
    )

    path = str(org_folder)
    cwd_ok = root.organizer_tab.cwd(path)
    listed = [f for f in os.listdir(path) if os.path.isfile(f)]
    rec(
        "TEST 03 Read files",
        "listdir files after cwd",
        listed,
        "PASS" if cwd_ok and "a.txt" in listed else "FAIL",
    )

    samples = [
        "sample.jpg",
        "sample.png",
        "document.pdf",
        "document.txt",
        "music.mp3",
        "video.mp4",
        "test.docx",
        "weird.xyz",
    ]
    exts = {n: splitext(n)[1].lower() for n in samples}
    fm = root.organizer_tab.FILE_FORMATS
    mapped = {n: fm.get(exts[n], "OTHER") for n in samples}
    ok4 = mapped["sample.jpg"] != "OTHER" and mapped["weird.xyz"] == "OTHER"
    rec(
        "TEST 04 Extensions",
        "Known ext -> category, unknown -> OTHER",
        mapped,
        "PASS" if ok4 else "FAIL",
        f"FILE_FORMATS count={len(fm)}",
    )

    f06 = TEST / "06_organize"
    write_files(
        f06,
        [
            "sample.jpg",
            "sample.png",
            "document.pdf",
            "document.txt",
            "music.mp3",
            "video.mp4",
            "test.docx",
        ],
    )
    root.organizer_tab.path.set(str(f06))
    root.organizer_tab.organize_options.current(0)
    root.organizer_tab.organize()
    root.update()
    created_dirs = [p.name for p in f06.iterdir() if p.is_dir()]
    remaining_files = [p.name for p in f06.iterdir() if p.is_file()]
    moved = []
    for d in f06.iterdir():
        if d.is_dir():
            moved.extend([f"{d.name}/{x.name}" for x in d.iterdir()])
    rec(
        "TEST 05 Create category folders",
        "Category folders created",
        sorted(created_dirs),
        "PASS" if created_dirs else "FAIL",
    )
    rec(
        "TEST 06 Organize files",
        "Files moved into category folders, none left at root",
        f"root_files={remaining_files} moved={moved}",
        "PASS" if (not remaining_files and created_dirs) else "FAIL",
    )

    root.organizer_tab.undo_organize()
    root.update()
    after_undo_files = sorted([p.name for p in f06.iterdir() if p.is_file()])
    after_undo_dirs = [p.name for p in f06.iterdir() if p.is_dir()]
    needed = {
        "sample.jpg",
        "sample.png",
        "document.pdf",
        "document.txt",
        "music.mp3",
        "video.mp4",
        "test.docx",
    }
    ok13 = needed.issubset(set(after_undo_files)) and not after_undo_dirs
    rec(
        "TEST 13 Undo",
        "Files back at parent, empty dirs removed",
        f"files={after_undo_files} dirs={after_undo_dirs}",
        "PASS" if ok13 else "FAIL",
    )

    f10 = TEST / "10_unknown"
    write_files(f10, ["mystery.xyz123"])
    root.organizer_tab.path.set(str(f10))
    root.organizer_tab.organize_by_type()
    root.update()
    other = list((f10 / "OTHER").glob("*")) if (f10 / "OTHER").exists() else []
    rec(
        "TEST 10 Unknown extension",
        "Goes to OTHER",
        [p.name for p in other],
        "PASS" if other else "FAIL",
    )

    f11 = TEST / "folder with spaces"
    write_files(f11, ["spaced file.txt"])
    root.organizer_tab.path.set(str(f11))
    root.organizer_tab.organize_by_type()
    root.update()
    moved11 = list((f11 / "PLAINTEXT").glob("*")) if (f11 / "PLAINTEXT").exists() else []
    rec(
        "TEST 11 Paths with spaces",
        "Organize works with spaces in path and filename",
        [p.name for p in moved11],
        "PASS" if moved11 else "FAIL",
    )

    f12 = TEST / "عربي"
    try:
        write_files(f12, ["ملف.txt"])
        root.organizer_tab.path.set(str(f12))
        root.organizer_tab.organize_by_type()
        root.update()
        moved12 = list((f12 / "PLAINTEXT").glob("*")) if (f12 / "PLAINTEXT").exists() else []
        rec(
            "TEST 12 Arabic names",
            "Arabic folder/file organize",
            [p.name for p in moved12],
            "PASS" if moved12 else "FAIL",
        )
    except Exception as e:
        rec("TEST 12 Arabic names", "Arabic folder/file organize", e, "FAIL")

    f07 = TEST / "07_rename"
    write_files(f07, ["alpha.txt", "beta.txt"])
    root.rename_tab.path.set(str(f07))
    root.rename_tab.add_prefix.set(True)
    root.rename_tab.change_fname.set(False)
    root.rename_tab.add_postfix.set(False)
    root.rename_tab.prefix_options.current(0)
    root.rename_tab.custom_prefix_text.set("NEW")
    root.rename_tab.rename_all()
    root.update()
    renamed07 = sorted([p.name for p in f07.iterdir() if p.is_file()])
    ok07 = "NEW alpha.txt" in renamed07 and "NEW beta.txt" in renamed07
    rec(
        "TEST 07 Rename",
        "Prefix Custom 'NEW ' + original name + ext",
        renamed07,
        "PASS" if ok07 else "FAIL",
    )

    f08 = TEST / "08_batch"
    write_files(f08, ["a.txt", "b.txt", "c.txt"])
    root.rename_tab.path.set(str(f08))
    root.rename_tab.add_prefix.set(True)
    root.rename_tab.change_fname.set(True)
    root.rename_tab.add_postfix.set(False)
    root.rename_tab.prefix_options.current(1)
    root.rename_tab.fname_options.current(0)
    root.rename_tab.custom_fname_text.set("SalesReport")
    root.rename_tab.rename_all()
    root.update()
    renamed08 = sorted([p.name for p in f08.iterdir() if p.is_file()])
    ok08 = len(renamed08) == 3 and all("SalesReport" in n and n.endswith(".txt") for n in renamed08)
    rec(
        "TEST 08 Batch Rename",
        "Numeric prefix + custom fname + original ext",
        renamed08,
        "PASS" if ok08 else "FAIL",
    )

    f09 = TEST / "09_dup"
    write_files(f09, ["one.txt", "two.txt"])
    root.rename_tab.path.set(str(f09))
    root.rename_tab.add_prefix.set(False)
    root.rename_tab.change_fname.set(True)
    root.rename_tab.add_postfix.set(False)
    root.rename_tab.fname_options.current(0)
    root.rename_tab.custom_fname_text.set("same")
    root.rename_tab.rename_all()
    root.update()
    renamed09 = sorted([p.name for p in f09.iterdir() if p.is_file()])
    has_same = "same.txt" in renamed09
    has_paren = any("(1)" in n or "(2)" in n for n in renamed09)
    rec(
        "TEST 09 Duplicate names",
        "FileExistsError -> dest with (i)",
        renamed09,
        "PASS" if has_same and has_paren and len(renamed09) == 2 else "FAIL",
    )

    root.organizer_tab.path.set(str(TEST / "does_not_exist_xyz"))
    root.organizer_tab.organize_by_type()
    root.update()
    err = root.organizer_tab.status.err_status.get()
    rec(
        "TEST 14 Invalid path",
        "Invalid Path! error status",
        repr(err),
        "PASS" if "Invalid Path" in err else "FAIL",
    )

    f_un = TEST / "unpack_src"
    write_files(f_un / "IMAGES", ["pic.jpg"])
    write_files(f_un / "PDF", ["x.pdf"])
    root.unpack_tab.path.set(str(f_un))
    root.unpack_tab.del_folders.set(True)
    root.unpack_tab.unpack_files()
    root.update()
    un_files = sorted([p.name for p in f_un.iterdir() if p.is_file()])
    un_dirs = [p.name for p in f_un.iterdir() if p.is_dir()]
    rec(
        "TEST extra Unpack",
        "Files moved to parent, emptied dirs deleted",
        f"files={un_files} dirs={un_dirs} status={root.unpack_tab.success_status.get()}",
        "PASS" if "pic.jpg" in un_files and "x.pdf" in un_files and not un_dirs else "FAIL",
    )

    f_ext = TEST / "by_ext"
    write_files(f_ext, ["a.jpg", "b.pdf"])
    root.organizer_tab.path.set(str(f_ext))
    root.organizer_tab.organize_by_ext()
    root.update()
    ext_dirs = sorted([p.name for p in f_ext.iterdir() if p.is_dir()])
    rec(
        "TEST extra Organize by extension",
        "Folders named jpg and pdf",
        ext_dirs,
        "PASS" if "jpg" in ext_dirs and "pdf" in ext_dirs else "FAIL",
    )

    enc_dir = TEST / "encrypt"
    write_files(enc_dir, ["secret.txt"])
    secret = enc_dir / "secret.txt"
    root.encrypt_tab.path.set(str(secret))
    key = root.encrypt_tab.getKey("testdevpassword")
    root.encrypt_tab.encrypt(key)
    enc_file = enc_dir / "secret.txt.enc"
    ok_enc = enc_file.exists()
    root.encrypt_tab.path.set(str(enc_file))
    root.encrypt_tab.decrypt(key)
    dec = enc_dir / "(decrypted)secret.txt"
    ok_dec = dec.exists() and dec.read_bytes().startswith(b"sample-")
    rec(
        "TEST extra Encrypt/Decrypt",
        "Creates .enc and (decrypted) copy in TEST",
        f"enc={ok_enc} dec={ok_dec}",
        "PASS" if ok_enc and ok_dec else "FAIL",
        "Clear Temp was not executed on real AppData",
    )

    f_ov = TEST / "overwrite"
    write_files(f_ov, ["dup.txt"])
    (f_ov / "PLAINTEXT").mkdir()
    (f_ov / "PLAINTEXT" / "dup.txt").write_bytes(b"already-here")
    root.organizer_tab.path.set(str(f_ov))
    root.organizer_tab.organize_by_type()
    root.update()
    src_still = (f_ov / "dup.txt").exists()
    dest = (f_ov / "PLAINTEXT" / "dup.txt").read_bytes()
    rec(
        "TEST extra duplicate dest / no overwrite",
        "Existing dest kept; source not silently destroyed",
        f"src_still={src_still} dest={dest}",
        "PASS" if dest == b"already-here" and src_still else "FAIL",
        "except: pass on FileExistsError",
    )

    rec(
        "TEST extra Clear Temp",
        "Must NOT run against real %TEMP%",
        "SKIPPED by design",
        "SKIP",
        r"cleartemp.py targets AppData\Local\Temp; not executed",
    )

    try:
        root.destroy()
        rec("TEST 15 Close", "destroy() without error", "closed", "PASS")
    except Exception as e:
        rec("TEST 15 Close", "destroy() without error", e, "FAIL")

    out = TEST / "results.json"
    out.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print("wrote", out)
    failed = [r for r in results if r["Status"] == "FAIL"]
    print("FAIL count:", len(failed))


if __name__ == "__main__":
    main()
