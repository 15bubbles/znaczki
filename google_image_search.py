import time

from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

IMAGES: list[Path] = [
    Path("images_out/stamp_2.jpg").absolute(),
    Path("images_out/stamp_22.jpg").absolute(),
]

GOOGLE_LENS_URL = "https://lens.google.com"

REJECT_BUTTON_XPATH = "//span[text()='Odrzuć wszystko']"

SEND_FILE_BUTTON_XPATH = "//span[text()='prześlij plik']"
IMAGE_INPUT_XPATH = "//input[@name='encoded_image']"

PRIZE_LABEL_CSS_SELECTOR = "span[alt='Tag etykiety produktu'] + span"


def search_image(driver: WebDriver, image_path: Path) -> None:
    driver.get(GOOGLE_LENS_URL)
    time.sleep(1)

    # search and click `Send file` button
    send_file_button = driver.find_element(By.XPATH, SEND_FILE_BUTTON_XPATH)
    send_file_button.click()
    time.sleep(1)

    # imitate uploading a file by providing path to an image directly to form's input element
    input_element = driver.find_element(By.XPATH, IMAGE_INPUT_XPATH)
    input_element.send_keys(str(image_path))
    time.sleep(5)

    # find prizes
    prizes = find_image_prizes(driver)

    if prizes:
        print(
            f"Most probable prize value for stamp (that appears on top of results): {prizes[0]}"
        )

    print("No prize values found for stamp")


def find_image_prizes(driver: WebDriver) -> list[str]:
    # inject JavaScript to get elements based on visual order
    # because Google renders results in a Grid, which means that first element
    # found from HTML might not exactly be the first element that has highest
    # probability to be a direct match
    # we are interested in element that is displayed as one of first results
    script = """
    let items = Array.from(document.querySelectorAll("span[alt='Tag etykiety produktu'] + span"));

    return items
    .map((el, index) => {
        let rect = el.getBoundingClientRect();
        return { index: index, top: rect.top, left: rect.left, value: el.outerText };
    })
    .sort((a, b) => a.top - b.top || a.left - b.left) // Sort by visual order
    .map((el) => el.value);
    """
    prize_values = driver.execute_script(script)
    return prize_values


def reject_consents(driver: WebDriver) -> None:
    reject_button = driver.find_element(By.XPATH, REJECT_BUTTON_XPATH)
    reject_button.click()


if __name__ == "__main__":
    driver = webdriver.Firefox()
    driver.get(GOOGLE_LENS_URL)
    reject_consents(driver)
    time.sleep(1)

    for image in IMAGES:
        search_image(driver, image)
        time.sleep(3)

    driver.close()
