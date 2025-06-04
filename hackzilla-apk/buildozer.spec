[app]

# Uygulama adı, paket adı falan
title = Hackzilla
package.name = hackzilla
package.domain = org.unknown

source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy,requests

# Python kodunun ana girişi
source.dir = .
source.main = main.py

# Android ayarları
orientation = portrait
fullscreen = 1
android.permissions = INTERNET, SYSTEM_ALERT_WINDOW
android.minapi = 21
android.sdk = 20
android.ndk = 19b

# İkon eklemek istersen buraya yaz: icon.filename = %(source.dir)s/icon.png

[buildozer]

log_level = 2
warn_on_root = 1
