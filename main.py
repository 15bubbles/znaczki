import cv2
from pathlib import Path


def save_image(path: Path | str, image: cv2.typing.MatLike) -> None:
    cv2.imwrite(str(path), image)


def extract_stamps(filename: Path | str, output_dir: Path | str) -> None:
    image = cv2.imread(Path(filename).as_posix())
    output_path = Path(output_dir)

    print("--- Saving grayscale image...")
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    save_image(output_path / "debug_grascale.jpg", image_gray)

    print("--- Saving binary image...")
    _, thresh = cv2.threshold(image_gray, 60, 255, cv2.THRESH_BINARY)
    save_image(output_path /"debug_binary.jpg", thresh)

    print("--- Saving original image with contours...")
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    image_countured = image.copy()
    cv2.drawContours(image_countured, contours, -1, (0, 255, 0), 2)
    save_image(output_path / "debug_contoured.jpg", image_countured)

    extracted_stamp_paths = []
    counter = 0

    for contour in contours:
        area = cv2.contourArea(contour)

        if area <= 100:
            continue

        x, y, width, height = cv2.boundingRect(contour)
        image_stamp = image[y:y+height, x:x+width]

        counter += 1
        image_stamp_path = output_path / f"stamp_{counter}.jpg"
        save_image(image_stamp_path, image_stamp)
        extracted_stamp_paths.append(image_stamp_path)

    print(f"--- Saved {len(extracted_stamp_paths)} extracted images")


if __name__ == "__main__":
    print("--- Starting script...")
    extract_stamps("images/example_znaczki.jpg", "images_out")
    print("--- Done")
