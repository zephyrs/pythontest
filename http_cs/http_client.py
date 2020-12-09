import http.client

DEF_HEADER_IMAGE_NAME = "YH-Image-Name"
DEF_HEADER_RESULT = "YH-Result"

conn = http.client.HTTPConnection("192.168.70.161", 9012)
with open("c:/code/cur.png", "rb") as f:
    headers = {DEF_HEADER_IMAGE_NAME: "image.png", "Content-Type": "BMP-Image"}
    conn.request("POST", "/image", f.read(), headers)
    response = conn.getresponse()
    print(
        response.headers[DEF_HEADER_IMAGE_NAME]
        + " : "
        + response.headers[DEF_HEADER_RESULT]
    )
    print(response.read().decode())
