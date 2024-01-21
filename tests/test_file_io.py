from reqflow import Client, given
import os


def test_file_upload():
    client = Client(base_url="https://ps.uci.edu/~franklin")
    given(client).file_upload("userfile", "img/test.png").when("POST", "/doc/file_upload.html").then().status_code(200)


def test_file_download():
    client = Client(base_url=
                    "https://file-examples.com/storage/fe793dd9be65a9b389251ea/2017/10/file_example_PNG_1MB.png")

    given(client).when("GET").then().status_code(200).save_response_to_file("img/download.png")
    os.remove("img/download.png")

