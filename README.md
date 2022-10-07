# 🗃 UUID World Converter

[![license](https://img.shields.io/github/license/skuzow/uuid-world-converter.svg)](https://github.com/skuzow/uuid-world-converter/blob/master/LICENSE)

Minecraft world data server converter from online to offline and reverse.

## 🗿 Usage

- `python uuidworldconverter.pyz` Display available options
- `python uuidworldconverter.pyz offline` Offline Mode
- `python uuidworldconverter.pyz online` Online Mode

## 💾 Config

Location: `uuidworldconverter.pyz directory`

```yaml
# Config file for uuid-world-converter
# https://github.com/skuzow/uuid-world-converter

# Server Directory
server_directory: server

# World Directory
world_directory: world

# Changing /server uuids
# IMPORTANT: used for getting player names for obtaining uuids
files:
  - name: usercache.json
    enable: true
  - name: whitelist.json
    enable: true
  - name: ops.json
    enable: true
  - name: banned-players.json
    enable: true

# Changing /world uuids
folders:
  - name: playerdata
    enable: true
  - name: stats
    enable: true
  - name: advancements
    enable: true
```

## 🗂️ Required Python libraries

- [colorama](https://pypi.org/project/colorama)
- [requests](https://pypi.org/project/requests)
- [ruamel.yaml](https://pypi.org/project/ruamel.yaml)

To install them execute:

```bash
  pip install -r requirements.txt
```
