from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import threading
import configparser
from pathlib import Path

DEF_HEADER_IMAGE_NAME = 'YH-Image-Name'
DEF_HEADER_RESULT = 'YH-Result'

class stopThread (threading.Thread):
    def __init__(self, server):
        threading.Thread.__init__(self)
        self._server = server

    def run(self):
        self._server.shutdown()

class ImageReqHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        '''will call GET "/stop_server" to stop server'''
        if self.path.startswith('/stop_server'):
            print(time.asctime(), 'Server is going down!')
            stopThread(httpd).start()
            self.send_error(500)
            return
        
        '''only for GET test'''
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'SHOULD USE POST')

    def do_POST(self):
        '''read image name or id in header "YH-Image-Name"'''
        image_id = self.headers.get(DEF_HEADER_IMAGE_NAME)
        if image_id == '':
            self.return_result(400, '', 'NO_ID')
            return

        '''check if POST path is "/image". otherwise return 404'''
        if self.path.lower() != '/image':
            self.return_result(404, image_id, 'UNKNOWN_API')
            return

        '''check if content type is "BMP-Image". otherwise return 404'''
        if self.headers['Content-Type'].lower() != 'bmp-image':
            self.return_result(406, image_id, 'TYPE_INVALID')
            return
        
        content_length = int(self.headers.get('Content-Length', '0'))
        if content_length <= 0:
            self.return_result(406, image_id, 'LENGTH_INVALID')
            return

        '''read all image content'''
        body = self.rfile.read(content_length)
        
        '''do image process here, for example, save it'''
        with open(DUMP_PATH + image_id, 'wb') as f:
            f.write(body)

        '''write result in "Result" header'''
        result = 'OK'   #or return NG
        self.return_result(200, image_id, result)
    
    def return_result(self, code, id, reason):
        self.send_response(code)
        self.send_header(DEF_HEADER_IMAGE_NAME, id)
        self.send_header(DEF_HEADER_RESULT, reason)        
        self.end_headers()

if __name__ == '__main__':
    '''read config file for params'''
    config = configparser.ConfigParser()
    config.read(Path(__file__).parent.joinpath('config.ini'))
    HOST_NAME = config.get('CONFIG', 'host')
    PORT_NUMBER = int(config.get('CONFIG', 'port'))
    DUMP_PATH = config.get('CONFIG', 'dump_path')

    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), ImageReqHandler)
    print(time.asctime(), 'Server Starts - %s:%s' % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), 'Server Stops - %s:%s' % (HOST_NAME, PORT_NUMBER))