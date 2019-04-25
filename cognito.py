import logging
import telnetlib
import time

log = logging.getLogger(__name__)

class TelnetController:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.connect(host, port)

    def connect(self, host, port):
        try:
            self.link = telnetlib.Telnet(host, port)
        except:
            log.error('Unable to connect to the host', exc_info = 1)
            return
        self.host = host
        self.port = port
        self.check()

        self.noprompt()
        self.noecho()

    def _send(self, msg):
        msg += '\r\n'
        bytestring = msg.encode('utf-8')
        try:
            self.link.write(bytestring)
        except OSError:
            log.error('Command not sent: telnet connection is not available!', exc_info = 1)
        
        self.check()

    def check(self):
        time.sleep(0.2)
        b_message = b''
        try:
            queue = self.link.read_eager()
            while queue != b'':
                b_message += queue
                queue = self.link.read_eager()
                time.sleep(0.1)
        except EOFError as e:
            b_message += b'\r\n<CONNECTION CLOSED>'
        except Exception as e:
            print(e)

        message = b_message.decode('utf-8')

        print(message)

    # noecho
    def noecho(self):
        self._send('noecho')
    
    # noprompt
    def noprompt(self):
        self._send('noprompt')
    
    # API.AttributeFade(fixture[,attribute_name],value [,time])
    def attribute_fade(self, fixture, value, attribute=None, time=None):
        if attribute:
            attribute = f"'{attribute}'"
        if time:
            time = str(time)
        args = filter(None, [str(fixture), attribute, str(value), time])
        self._send(f'API.AttributeFade({", ".join(args)})')
    
    # API.AttributeFadeCapture(fixture[,attribute_name],value [,time])
    def attribute_fade_capture(self, fixture, value, attribute=None, time=None):
        if attribute:
            attribute = f"'{attribute}'"
        if time:
            time = str(time)
        args = filter(None, [fixture, attribute, value, time])
        self._send(f'API.AttributeFadeCapture({", ".join(args)})')
    
    # API.Bump('page_name' | page_index , memory_number, is_down )
    def bump(self, page, memory_number, is_down):
        if isinstance(page, str): page = "'" + page + "'"
        self._send(f'API.Bump({page}, {memory_number}, {str(is_down).lower()})')
    
    # API.ButtonPress('page','name' or order)
    def button_press(self, page, button):
        if isinstance(button, str): button = "'" + button + "'"
        self._send(f"API.ButtonPress('{page}', {button})")
    
    # API.MemoryFade('page',memorynumber,value[,seconds])
    def memory_fade(self, page, memory_number, value, *, time=None):
        page = f"'{page}'"
        args = filter(None, [page, memory_number, value, time])
        self._send(f"API.MemoryFade({', '.join(args)})")
    
    # API.MemoryFadeRate('page',memorynumber,value[,seconds full scale])
    
    # API.MemoryFadeStop('page',memorynumber)
    
    # API.MemoryGetValue('page',memorynumber)
    
    # API.MidiNoteOff(channel_1_to_16,key_1_to_128[,velocity_0_to127])
    
    # API.MidiNoteOn(channel_1_to_16,key_1_to_128[,velocity_0_to127])
    
    # API.MidiWrite(midi_byte[,midi_byte ...])
    
    # API.PlayListAssert('playlist')
    
    # API.PlayListGo('playlist')
    
    # API.PlayListGotoAndExecuteFollows('playlist', cue)
    
    # API.PlayListGotoAndHalt('playlist', cue)
    
    # API.PlayListHalt('playlist')
    
    # API.PlayListHaltBack('playlist')
    
    # API.PlayListRelease('playlist'[,release_time])
    
    # API.ReleaseAll()
    
    # API.SerialClose()
    
    # API.SerialOpen(['script'])
    
    # API.SerialRead()
    
    # API.SerialWrite('output string' or binary_byte or table [,...])
    
    # API.SetLevel('fixture_string', 'level_string' [,fade_time_seconds])
    
    # API.SystemRestart([<maintain state>true|false])
    
    # API.SystemShutdown()
    
    # API.WriteLogMessage('message', 'category', severity_1_to_10)