from platforms.identifier import iOSSession, AndroidSession, ExecutablePath

def init_config():
    # 在此处设置session/executable_path最为方便
    iOSSession.session = {
        "platformName": "iOS",
        "platformVersion": "13.3",
        # "platformVersion": "13.4",
        "deviceName": "Jackey",
        "bundleId": "com.bindo.bindo-pos-dev",
        "udid": "18b61a7bcd83c7d47a8e5a3d4c0202a6b2807c6f",
        # "udid": "d848f309487bd4c841b329f1d75fd3a30a356b5c",
        "noReset": "true",
        "clearSystemFiles": "true",
        "Connect Hardware Keyboard": "true",
    }

    AndroidSession.session = None

    ExecutablePath.executable_path = None