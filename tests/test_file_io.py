from reqflow import Client, given
import os


def test_file_upload():
    client = Client(base_url="https://ps.uci.edu/~franklin")
    given(client).file_upload("userfile", "data/test.png").when("POST", "/doc/file_upload.html").then().status_code(200)


def test_file_download_png():
    client = Client(base_url=
                    "https://download.samplelib.com/png/sample-boat-400x300.png")

    given(client).when("GET").then().status_code(200).save_response_to_file("data/download.png")
    os.remove("data/download.png")


def test_file_download_pdf():
    client = Client(base_url=
                    "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf")

    given(client).when("GET").then().status_code(200).save_response_to_file("data/download.pdf")
    os.remove("data/download.pdf")


def test_file_download_txt():
    client = Client(base_url=
                    "https://filesamples.com/samples/document/txt/sample3.txt")

    given(client).when("GET").then().status_code(200).save_response_to_file("data/download.txt")
    os.remove("data/download.txt")
