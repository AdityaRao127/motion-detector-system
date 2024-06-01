import network
import ussl
import ubinascii
import machine
import time
from m5stack import *
from m5ui import *
from uiflow import *
import utime

setScreenColor(0xCCCCCC)  # Set screen color to blue

# Define the PIR sensor pin
pir_sensor = machine.Pin(36, machine.Pin.IN)


motion_count = 0

# Display motion count on the screen
label = M5TextBox(10, 10, "Motion: 0", lcd.FONT_DejaVu40, 0xCCCCCC, rotate=0)


# Define SMTP class directly in the same file
DEFAULT_TIMEOUT = 10  # sec
LOCAL_DOMAIN = '127.0.0.1'
CMD_EHLO = 'EHLO'
CMD_STARTTLS = 'STARTTLS'
CMD_AUTH = 'AUTH'
CMD_MAIL = 'MAIL'
AUTH_PLAIN = 'PLAIN'
AUTH_LOGIN = 'LOGIN'

class SMTP:
    def cmd(self, cmd_str):
        sock = self._sock
        sock.write(('%s\r\n' % cmd_str).encode())
        resp = []
        next = True
        while next:
            code = sock.read(3).decode()
            next = sock.read(1) == b'-'
            resp.append(sock.readline().strip().decode())
        return int(code), resp

    def __init__(self, host, port, ssl=False, username=None, password=None):
        import usocket
        self.username = username
        addr = usocket.getaddrinfo(host, port)[0][-1]
        sock = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
        sock.settimeout(DEFAULT_TIMEOUT)
        sock.connect(addr)
        if ssl:
            sock = ussl.wrap_socket(sock)
        code = int(sock.read(3).decode())
        sock.readline()
        assert code == 220, 'cant connect to server %d' % code
        self._sock = sock

        code, resp = self.cmd(CMD_EHLO + ' ' + LOCAL_DOMAIN)
        assert code == 250, '%d' % code
        if not ssl and CMD_STARTTLS in resp:
            code, resp = self.cmd(CMD_STARTTLS)
            assert code == 220, 'start tls failed %d, %s' % (code, resp)
            self._sock = ussl.wrap_socket(sock)

        if username and password:
            self.login(username, password)

    def login(self, username, password):
        self.username = username
        code, resp = self.cmd(CMD_EHLO + ' ' + LOCAL_DOMAIN)
        assert code == 250, '%d, %s' % (code, resp)

        auths = None
        for feature in resp:
            if feature[:4].upper() == CMD_AUTH:
                auths = feature[4:].strip('=').upper().split()
        assert auths != None, "no auth method"

        from ubinascii import b2a_base64 as b64
        if AUTH_PLAIN in auths:
            cren = b64(("\0%s\0%s" % (username, password)).encode())[:-1].decode()
            code, resp = self.cmd('%s %s %s' % (CMD_AUTH, AUTH_PLAIN, cren))
        elif AUTH_LOGIN in auths:
            code, resp = self.cmd("%s %s %s" % (CMD_AUTH, AUTH_LOGIN, b64(username.encode())[:-1].decode()))
            assert code == 334, 'wrong username %d, %s' % (code, resp)
            code, resp = self.cmd(b64(password.encode())[:-1].decode())
        else:
            raise Exception("auth(%s) not supported " % ', '.join(auths))

        assert code == 235 or code == 503, 'auth error %d, %s' % (code, resp)
        return code, resp

    def to(self, addrs, mail_from=None):
        mail_from = self.username if mail_from == None else mail_from
        code, resp = self.cmd(CMD_EHLO + ' ' + LOCAL_DOMAIN)
        assert code == 250, '%d' % code
        code, resp = self.cmd('MAIL FROM: <%s>' % mail_from)
        assert code == 250, 'sender refused %d, %s' % (code, resp)

        if isinstance(addrs, str):
            addrs = [addrs]
        count = 0
        for addr in addrs:
            code, resp = self.cmd('RCPT TO: <%s>' % addr)
            if code != 250 and code != 251:
                print('%s refused, %s' % (addr, resp))
                count += 1
        assert count != len(addrs), 'recipient refused, %d, %s' % (code, resp)

        code, resp = self.cmd('DATA')
        assert code == 354, 'data refused, %d, %s' % (code, resp)
        return code, resp

    def write(self, content):
        self._sock.write(content.encode())

    def send(self, content=''):
        if content:
            self.write(content)
        self._sock.write(b'\r\n.\r\n')  
        line = self._sock.readline()
        return (int(line[:3]), line[4:].strip().decode())

    def quit(self):
        self.cmd("QUIT")
        self._sock.close()


ssid = ''
password = ''


sender_email = ''
sender_name = 'M5GO'  # sender name
sender_app_password = ''  # Replace this with your actual app password
recipient_email = ''
email_subject = '' 

def connect_wifi(ssid, password):
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid, password)
    while not station.isconnected():
        pass
    print('Connection successful')
    print(station.ifconfig())

def get_formatted_time():
    tm = utime.localtime()
    return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(tm[0], tm[1], tm[2], tm[3], tm[4], tm[5])

def send_email():
    current_time = get_formatted_time()
    
    # Send the email
    smtp = SMTP('smtp.gmail.com', 587, ssl=False)  # Gmail's STARTTLS port
    smtp.login(sender_email, sender_app_password)
    smtp.to(recipient_email)
    smtp.write("From:" + sender_name + "<" + sender_email + ">\n")
    smtp.write("To:" + recipient_email + "\n")
    smtp.write("Subject:" + email_subject + "\n")
<<<<<<< HEAD
    smtp.write("Motion was detected at front door!")
=======
    smtp.write("Motion detected!")
>>>>>>> ca3eb8bcab6c01a5de85b5a92f49180fbadf273d
    smtp.send()
    smtp.quit()
    print("Email sent successfully at " + current_time) # debugging purposes


connect_wifi(ssid, password)

while True:
    # Read PIR sensor value
    motion_detected = pir_sensor.value()
    
    # Display motion status on the screen
    if motion_detected:
        label.setText("Motion: 1")
        send_email()
        
        # Wait for 10 seconds before checking again
        time.sleep(18)
    else:
        label.setText("Motion: 0")
        
        # Wait for 1 second before checking again
    time.sleep(0.6)
