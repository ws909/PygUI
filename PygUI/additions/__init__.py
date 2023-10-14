# import threading as _threading
import multiprocessing as _processing
import subprocess as _subprocess
import platform as _platform
import warnings as _warnings


class _Notificator:

    @staticmethod
    def command(cmd: str): pass

    @staticmethod
    def write(text: str, title: str = None) -> str: pass

    @staticmethod
    def speak(text: str, title: str = None) -> str: pass

    @staticmethod
    def beep(count: int) -> str: pass

    @staticmethod
    def decode(commands: [str]) -> {str: {str: str}}: pass

    @staticmethod
    def encode(commands: {str: {str: str}}) -> [str]: pass


class _NoOS(_Notificator):

    @staticmethod
    def command(cmd: str):
        _warnings.warn("Notifications are not supported in this OS")
        return False

    @staticmethod
    def write(text: str, title: str = None) -> str:
        return ""

    @staticmethod
    def speak(text: str, title: str = None) -> str:
        return ""

    @staticmethod
    def beep(count: int) -> str:
        return ""

    @staticmethod
    def decode(commands: [str]) -> {str: {str: str}}:
        return [{}]

    @staticmethod
    def encode(commands: {str: {str: str}}) -> [str]:
        return []


class _MacOS(_Notificator):

    @staticmethod
    def command(cmd: str) -> bool:
        try:
            _subprocess.run("""osascript -e '{}'""".format(cmd), shell=True)
            return True
        except (IOError, SyntaxError):
            _warnings.warn("Notifying has failed")
        return False

    @staticmethod
    def write(text: str, title: str = None) -> str:
        return '''display notification "{}" with title "{}"'''.format(text, title) if title is not None \
            else '''display notification "{}"'''.format(text)

    @staticmethod
    def speak(text: str, title: str = None) -> str:
        return '''say "{}" using "Samantha"'''.format(text) if title is None \
            else '''say "{}" using "Samantha" \ndelay 0.4 \nsay "{}" using "Samantha"'''.format(title,
                                                                                                text)

    @staticmethod
    def beep(count: int) -> str:
        return '''beep {}'''.format(count)

    @staticmethod
    def decode(commands: [str]) -> {str: {str: str}}:

        decoded_commands: {str: {str: str}} = {}

        for command in commands:
            if command is None:
                continue

            decoded: {str: str} = {}

            # write
            if command.startswith('display notification '):
                start = command.find('"')
                end = command.find('"', start + 1)
                decoded["text"] = command[start + 1: end]

                if command.startswith(' with title ', end + 1):
                    start = command.find('"', end + 1)
                    end = command.rfind('"')
                    decoded["title"] = command[start + 1: end]

                if len(commands) > end + 1:
                    decoded["error"] = "command out of range. Cannot encode further"

                decoded_commands["write"] = decoded

            # speak
            elif command.startswith('say '):

                indexes: [int] = []
                for i in range(0, len(command)):
                    if command[i] == '"':
                        indexes.append(i)

                texts: [str] = []
                voices: [str] = []

                for i in range(0, int(len(indexes) / 2)):
                    start = indexes[i * 2]
                    end = indexes[i * 2 + 1]

                    if command.startswith('say ', start - 4):
                        texts.append(command[start + 1: end])

                    elif command.startswith('using ', start - 6):
                        voices.append(command[start + 1: end])

                if len(texts) > 1:
                    decoded["title"] = texts[0]
                    texts.pop(0)

                    text = ''
                    for txt in texts:
                        text += txt + '"'
                    text = text[:-1]

                    decoded["text"] = text

                else:
                    decoded["text"] = texts[0]

                decoded_commands["speak"] = decoded

            # beep
            elif command.startswith('beep '):
                decoded["beep"] = command[5:]
                decoded_commands["beep"] = decoded

            else:
                decoded["error"] = "Unknown command"
                decoded_commands["error"] = decoded

        return decoded_commands

    @staticmethod  # TODO: add checks that'll remove steps that try to damage the computer
    def encode(commands: {str: {str: str}}) -> [str]:

        encoded: [str] = []

        for command, parameters in commands.items():

            if command == 'write':
                text = parameters['text']

                if text is None:
                    continue

                text = text.replace('"', '\n')

                encoded.append(_MacOS.write(text, parameters['title']))

            elif command == 'speak':
                title = parameters['title']

                if title is not None and len(parameters) > 2 or len(parameters) > 1 and title is None:
                    text = ''

                    for key, value in parameters.items():
                        if key == 'text':
                            text += value + '. '

                else:
                    text = parameters['text']

                if text is None:
                    continue

                encoded.append(_MacOS.speak(text, parameters['title']))

            elif command == 'beep':
                count = parameters['count']

                if count is not None:
                    try:
                        count = int(count)
                        if count < 1:
                            continue
                    except ValueError:
                        continue

                encoded.append(_MacOS.beep(count))

        return encoded


class _Windows(_Notificator):

    @staticmethod
    def command(cmd: str): pass

    @staticmethod
    def write(text: str, title: str = None) -> str: pass

    @staticmethod
    def speak(text: str, title: str = None) -> str: pass

    @staticmethod
    def beep(count: int) -> str: pass

    @staticmethod
    def decode(commands: [str]) -> {str: {str: str}}: pass

    @staticmethod
    def encode(commands: {str: {str: str}}) -> [str]: pass


class _Linux(_Notificator):

    @staticmethod
    def command(cmd: str): pass

    @staticmethod
    def write(text: str, title: str = None) -> str: pass

    @staticmethod
    def speak(text: str, title: str = None) -> str: pass

    @staticmethod
    def beep(count: int) -> str: pass

    @staticmethod
    def decode(commands: [str]) -> {str: {str: str}}: pass

    @staticmethod
    def encode(commands: {str: {str: str}}) -> [str]: pass


class Notifications:
    """
    This class holds methods to notify the user, either through the OS or the app itself.
    It also stores all notifications in raw string command format, and holds methods to decode these.
    These notifications can be resent, and the dates and time will also be registered.
    Notification saving can be turned off
    """

    _notificator: _Notificator
    _processes: [_processing.Process]

    notifications: [str]
    save_notifications: bool

    @staticmethod
    def init():
        platform = _platform.uname()
        release = platform.__getattribute__("release").split(".")

        # MacOS
        if platform.__getattribute__("system") == "Darwin":
            if int(release[0]) >= 13:
                Notifications._notificator = _MacOS

        # Windows
        elif platform.__getattribute__("system") == "Windows":
            print("Notifications not implemented for Windows")
            Notifications._notificator = _Windows

        # Linux
        elif platform.__getattribute__("system") == "Linux":
            print("Notifications not implemented for Linux")
            Notifications._notificator = _Linux

        # None
        else:
            Notifications._notificator = None

        del platform
        del release

        Notifications.notifications = [str]
        Notifications.save_notifications = True
        Notifications._processes = []

    @staticmethod
    def _run(cmd: str):
        Notifications._notificator.command(cmd)

        # Notifications._processes.get() # TODO: No idea how to solve this.

        # Count number of processes running, of each type.

    @staticmethod
    def run(*commands: str):

        for command in commands:
            if command is not None:
                process = _processing.Process(target=Notifications._run, args=[command])
                process.name = "PygUI notification"

                Notifications._processes.append(process)
                process.start()
                process.terminate()

        # Save notification
        if Notifications.save_notifications:
            notification = commands
            Notifications.notifications.append(notification)

    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def notify(title: str, text: str, speech: bool = False, beeps: int = 0):

        write = Notifications._notificator.write(text, title)
        beep = Notifications._notificator.beep(beeps) if beeps > 0 else None
        speak = Notifications._notificator.speak(text, title) if speech is True else None

        Notifications.run(write, beep, speak)

    @staticmethod
    def write(text: str or [], title: str = None):
        """Sends a notification handled by the OS"""
        write = Notifications._notificator.write(title, text)
        Notifications.run(write)

    @staticmethod
    def speak(text: str or [], title: str = None):
        """Plays a voice telling 'text', starting with 'title', if set"""
        speak = Notifications._notificator.speak(text, title)
        Notifications.run(speak)

    @staticmethod
    def beep(count: int = 1):
        """Plays beep sounds with count"""
        if count < 1:
            raise ValueError("count must range from 1")
        beep = Notifications._notificator.beep(count)
        Notifications.run(beep)

    # ------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def decode(commands: [str], os: str = None) -> {str: str}:

        if os is None:
            return Notifications._notificator.decode(commands)

        elif os.lower() == "macos" or "darwin":
            return _MacOS.decode(commands)

        elif os.lower() == "windows":
            return _Windows.decode(commands)

        elif os.lower() == "linux":
            return _Linux.decode(commands)

        else:
            return _NoOS.decode(commands)

    @staticmethod
    def encode(commands: {str: {str: str}}, os: str = None) -> [str]:

        if os is None:
            return Notifications._notificator.encode(commands)

        elif os.lower() == "macos" or "darwin":
            return _MacOS.encode(commands)

        elif os.lower() == "windows":
            return _Windows.encode(commands)

        elif os.lower() == "linux":
            return _Linux.encode(commands)

        else:
            return _NoOS.encode(commands)

    # ------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def flush():
        for process in Notifications._processes:
            process.terminate()

        del Notifications._notificator
        del Notifications.notifications
