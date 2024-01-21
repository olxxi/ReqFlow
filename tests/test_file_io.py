from reqflow import Client, given
import os

client = Client(base_url="https://ps.uci.edu/~franklin")


def test_file_upload():
    given(client).file_upload("userfile", "img/test.png").when("POST", "/doc/file_upload.html").then().status_code(200)



