import time

from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By


IMAGES: list[Path] = [
    Path("images_out/stamp_2.jpg").absolute(),
    Path("images_out/stamp_22.jpg").absolute(),
]
GOOGLE_LENS_URL = "https://lens.google.com"


def search_image(image_path: Path) -> None:
    driver.get(GOOGLE_LENS_URL)
    time.sleep(1)

    send_file_button = driver.find_element(By.XPATH, "//span[text()='prześlij plik']")
    send_file_button.click()
    time.sleep(1)

    input_element = driver.find_element(By.NAME, "encoded_image")
    input_element.send_keys(str(image_path))
    time.sleep(5)

    find_prize()


def find_prize() -> str | None:
    # Inject JavaScript to get elements based on visual order
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
    
    if prize_values:
        print(f"Returning most probable prize value for stamp: {prize_values[0]}")
        return prize_values[0]
    
    print("No prize values found for stamp")


if __name__ == "__main__":
    driver = webdriver.Firefox()
    driver.get(GOOGLE_LENS_URL)
    reject_button = driver.find_element(By.XPATH, "//span[text()='Odrzuć wszystko']")
    reject_button.click()
    time.sleep(1)
    
    for image in IMAGES:
        search_image(image)
        time.sleep(10)

    driver.close()
