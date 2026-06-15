import subprocess
import time
import socket
import pathlib
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from pages.bank_page import BankPage


def wait_for_server(port=8000, timeout=10):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with socket.create_connection(("localhost", port), timeout=1):
                return
        except OSError:
            time.sleep(0.2)
    raise RuntimeError(f"Сервер не запустился на порту {port}")


@pytest.fixture(scope="session")
def http_server():
    dist_path = str(
        (pathlib.Path(__file__).parent.parent / "dist").resolve()
    )
    proc = subprocess.Popen(
        ["python3", "-m", "http.server", "8000"],
        cwd=dist_path,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    wait_for_server(8000)
    yield "http://localhost:8000"
    proc.terminate()
    proc.wait()


@pytest.fixture(scope="session")
def driver():
    opts = Options()
    opts.add_argument("--headless")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1280,800")

    try:
        from webdriver_manager.chrome import ChromeDriverManager
        svc = Service(ChromeDriverManager().install())
        dr = webdriver.Chrome(service=svc, options=opts)
    except Exception:
        dr = webdriver.Chrome(options=opts)

    yield dr
    dr.quit()


@pytest.fixture
def page(driver, http_server):
    return BankPage(driver, base_url=http_server)
