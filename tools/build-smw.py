#!/usr/bin/env python3
"""Empacota o RetroArch Tizen existente com Snes9x e a ROM local do usuário."""

import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import urllib.request
import zipfile


ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".work/offline-assets"
BASE = "https://sype0.github.io/retroarch-tizen/"
CORE = "snes9x2010"


def asset(name):
    path = CACHE / name
    if not path.exists():
        with urllib.request.urlopen(BASE + name, timeout=30) as response:
            data = response.read(40_000_000)
        if len(data) >= 40_000_000:
            raise ValueError(f"Recurso excede o limite: {name}")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    return path.read_bytes()


def replace_once(text, old, new):
    if text.count(old) != 1:
        raise ValueError(f"Fonte upstream diferente do esperado: {old[:70]}")
    return text.replace(old, new, 1)


def smaller_initial_memory(data):
    """Reduz só o mínimo da memória WASM; preserva crescimento e código."""
    result = bytearray(data)

    def unsigned(position):
        value = shift = 0
        while True:
            byte = result[position]
            position += 1
            value |= (byte & 127) << shift
            if not byte & 128:
                return value, position
            shift += 7
            if shift > 35:
                raise ValueError("Inteiro WASM inválido")

    if result[:8] != b"\0asm\x01\0\0\0":
        raise ValueError("Formato WASM inesperado")
    position = 8
    while position < len(result):
        section = result[position]
        size, position = unsigned(position + 1)
        end = position + size
        if section == 5:
            count, position = unsigned(position)
            flags, position = unsigned(position)
            start = position
            minimum, position = unsigned(position)
            if count != 1 or flags != 1 or minimum != 2048 or position - start != 2:
                raise ValueError("Layout de memória do core mudou")
            # 2048 páginas = 128 MiB; 512 páginas = 32 MiB. Mesmo tamanho LEB128.
            result[start:position] = b"\x80\x04"
            return bytes(result)
        position = end
    raise ValueError("Memória WASM não encontrada")


def main():
    global CORE
    parser = argparse.ArgumentParser(description="Empacota uma ROM SNES local; assinatura opcional.")
    parser.add_argument("--rom", type=Path, default=ROOT / "roms/SMW-PTBR-2.0.sfc")
    parser.add_argument("--name", default="Meu jogo SNES")
    parser.add_argument("--core", choices=["snes9x", "snes9x2010", "snes9x2005"], default=CORE)
    parser.add_argument("--initial-memory", type=int, choices=[32, 128], default=32)
    parser.add_argument("--unsigned", action="store_true", help="Não executa assinador externo")
    parser.add_argument("--output", type=Path, default=ROOT / "artifacts/SuperNintendo-SMW-PTBR.wgt")
    args = parser.parse_args()
    CORE = args.core
    rom = args.rom.expanduser()
    if not args.unsigned and not all(os.environ.get(key) for key in ("TIZEN_CERT_DIR", "TIZEN_SDB")):
        parser.error("Configure TIZEN_CERT_DIR e TIZEN_SDB ou use --unsigned para assinar por outra ferramenta.")
    if not rom.is_file():
        raise SystemExit(f"ROM não encontrada: {rom}")
    if rom.suffix.lower() not in {".sfc", ".smc"} or not rom.stat().st_size:
        parser.error("Use uma ROM SNES extraída, não vazia, com extensão .sfc ou .smc.")
    rom_data = rom.read_bytes()
    rom_filename = "game-" + hashlib.sha256(rom_data).hexdigest()[:12] + ".sfc"
    original = ROOT / "artifacts/RetroArch-v0.3.2.wgt"
    original.parent.mkdir(parents=True, exist_ok=True)
    if not original.exists():
        url = "https://github.com/Sype0/retroarch-tizen/releases/download/v0.3.2/RetroArch.wgt"
        with urllib.request.urlopen(url, timeout=60) as response:
            original.write_bytes(response.read())
    with zipfile.ZipFile(original) as source:
        files = {name: source.read(name) for name in source.namelist()
                 if not name.endswith("/") and not name.endswith("signature.xml")}

    script = files["app.js"].decode()
    script = replace_once(script, "return REMOTE_BASE;", 'return "./";')
    script = replace_once(script, "this.EmscriptenSendCommand(msg);", 'this.EmscriptenSendCommand(msg + "\\n");')
    script = replace_once(script, "   initPhoneLink();", "   // Aplicativo local: sem servidor ou descoberta de telefone.")
    script = replace_once(script, "t.onclick = function () { openSource(c); };", """t.onclick = function () {
            selectedCore = c;
            download("roms/SMW-PTBR-2.0.sfc", "Carregando SMW PT-BR").then(function (data) {
               playRom("SMW-PTBR-2.0.sfc", new Uint8Array(data));
            }).catch(function (error) { fail("Não foi possível abrir o jogo", error); });
         };""")
    script = replace_once(script, "'config_save_on_exit = \"true\"',", """'config_save_on_exit = "true"',
       'savefile_directory = "' + RA_HOME + '/userdata/saves"',
       'savestate_directory = "' + RA_HOME + '/userdata/states"',""")
    script = replace_once(script, 'mkdirp(FS, RA_HOME + "/userdata");', """mkdirp(FS, RA_HOME + "/userdata");
         mkdirp(FS, RA_HOME + "/userdata/saves");
         mkdirp(FS, RA_HOME + "/userdata/states");""")
    files["app.js"] = script.replace("SMW-PTBR-2.0.sfc", rom_filename).replace("Carregando SMW PT-BR", "Carregando jogo").encode()
    files["cores.js"] = ("var RA_CORES = " + json.dumps([
        {"id": CORE, "name": args.name, "emu": "Super Nintendo",
         "ext": ["sfc", "smc"]}], ensure_ascii=False) + ";\n").encode()
    files["config.xml"] = files["config.xml"].replace(b'version="0.3.2"', b'version="0.3.4"').replace(b"<name>RetroArch</name>", b"<name>Super Nintendo</name>")
    files["index.html"] = files["index.html"].replace(b"RetroArch for Tizen", b"Super Nintendo").replace(b"<h1>RetroArch</h1>", b"<h1>Super Nintendo</h1>").replace(b"Choose a system", b"Escolha o jogo").replace(b"Remote keys", b"Controles")
    files["style.css"] += b"\n#canvas{width:1280px!important;height:720px!important;transform:scale(1.5);transform-origin:0 0;}\n"
    files["roms/" + rom_filename] = rom_data
    for name in [f"cores/{CORE}_libretro.wasm", f"cores/{CORE}_libretro.js"]:
        files[name] = asset(name)
    if args.initial_memory == 32:
        files[f"cores/{CORE}_libretro.wasm"] = smaller_initial_memory(files[f"cores/{CORE}_libretro.wasm"])

    # RGUI, fontes, controles e informação do único core; nenhum shader ou filtro.
    bundle = io.BytesIO()
    with zipfile.ZipFile(io.BytesIO(asset("assets/frontend/bundle.zip"))) as source:
        with zipfile.ZipFile(bundle, "w", zipfile.ZIP_DEFLATED) as target:
            for item in source.infolist():
                name = item.filename
                if (name.startswith(("bundle/assets/rgui/", "bundle/autoconfig/"))
                        or name in {"bundle/assets/pkg/osd-font.ttf", "bundle/assets/pkg/fallback-font.ttf",
                                    f"bundle/info/{CORE}_libretro.info"}):
                    target.writestr(name, source.read(name))
    files["assets/frontend/bundle.zip"] = bundle.getvalue()
    output = args.output.expanduser()
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as package:
        for name, data in files.items():
            package.writestr(name, data)
    if args.unsigned:
        print(f"Gerado SEM assinatura: {output}. Assine antes de instalar.")
        return
    cert = Path(os.environ["TIZEN_CERT_DIR"]).expanduser()
    password = (cert / "password.txt").read_text().strip()
    sdb = Path(os.environ["TIZEN_SDB"]).expanduser()
    result = subprocess.run([str(sdb), "resign", str(output),
                             str(cert / "author.p12"), str(cert / "distributor.p12"), password],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if result.returncode:
        raise RuntimeError(result.stdout.replace(password, "[REDACTED]"))
    print(f"Gerado e assinado: {output.name} ({output.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
