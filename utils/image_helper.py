import cv2
import numpy as np
import os
from scipy.ndimage import rotate


class SkewCorrection:
    def determine_score(self, arr, angle):
        data = rotate(arr, angle, reshape=False, order=0)
        histogram = np.sum(data, axis=1, dtype=float)
        score = np.sum((histogram[1:] - histogram[:-1]) ** 2, dtype=float)
        return histogram, score

    def correct_skew(self, image, delta=1, limit=5):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        scores = []
        angles = np.arange(-limit, limit + delta, delta)
        for angle in angles:
            histogram, score = self.determine_score(thresh, angle)
            scores.append(score)

        best_angle = angles[scores.index(max(scores))]

        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, best_angle, 1.0)
        corrected = cv2.warpAffine(
            image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE
        )

        return best_angle, corrected


class ImageConvert:
    @staticmethod
    def decoding(img_request):
        return np.fromstring(img_request, np.uint8)

    @staticmethod
    def encoding(img_nd, ext: str):
        ext = ext.replace(".", "")
        if ext not in ("jpg", "jpeg", "png"):
            ext = "jpg"

        image_encode = cv2.imencode(ext=f".{ext}", img=img_nd)[1]
        print(f"CV 2 IMENCODE : {type(image_encode)}")
        data_encode = np.array(object=image_encode, dtype=np.uint8)
        print(f"NP ARRAY : {type(data_encode)}")
        result = data_encode.tobytes()
        print(f".TOBYTES() : {type(result)}")
        return result
        # img = Image.fromarray(img_nd, mode="BGR").convert("RGBA")
        # img.save("coba.png")
        # return img
        # return bts


class ImageProcess:
    def __init__(self, img):
        self.img = img

    def apply_morphological_operation(self, method):
        """Apply a morphological operation depending on method

        Opening: erosion followed by dilation and is useful for removing noise
        Closing: dilation followed by erosion and is useful for closing small holes

        Args:
            img: image as numpy array
            method: either 'open' for opening or 'close' for closing

        Returns:
            Image as numpy array

        """
        if method == "open":
            op = cv2.MORPH_OPEN
        elif method == "close":
            op = cv2.MORPH_CLOSE

        return cv2.morphologyEx(
            src=self.img,
            op=op,
            kernel=np.ones((5, 5), np.uint8),
        )

    def apply_gaussian_smoothing(self):
        """Apply Gaussian smoothing with 5x5 kernal size

        Useful for removing high frequency content (e.g. noise)

        Args:
            img: image as numpy array

        Returns:
            Image as numpy array
        """
        return cv2.GaussianBlur(
            src=self.img,
            ksize=(5, 5),
            sigmaX=0,
            sigmaY=0,
        )

    def apply_adaptive_thresholding(self, method):
        """Apply adaptive thresholding with a threshold value depending on method

        Threshold value is:
        Gaussian:  sum of neighborhood values where weights are a Gaussian window
        Mean: mean of neighborhood area

        Useful when the image has different lighting conditions in different areas

        Args:
            img: image as numpy array
            method: either 'gaussian' for 'mean'

        Returns:
            Image as numpy array
        """
        self.img = cv2.cvtColor(
            src=self.img,
            code=cv2.COLOR_RGB2GRAY,
        )

        if method == "gaussian":
            adaptive_method = cv2.ADAPTIVE_THRESH_GAUSSIAN_C

        elif method == "mean":
            adaptive_method = cv2.ADAPTIVE_THRESH_MEAN_C

        return cv2.adaptiveThreshold(
            src=self.img,
            maxValue=255,
            adaptiveMethod=adaptive_method,
            thresholdType=cv2.THRESH_BINARY,
            blockSize=11,
            C=2,
        )

    def apply_sobel_filter(self, direction):
        """
        Apply Sobel filter of first order (i.e. 1st derivative) along direction

        Direction could be along x (horizontally) or y (vertically)


        Useful to detect horizontal or vertical edges and are resistant to noise

        Args:
            img: image as numpy array
            direction: either 'h' or 'v'

        Returns:
            Image as numpy array
        """
        self.img = cv2.cvtColor(
            src=self.img,
            code=cv2.COLOR_RGB2GRAY,
        )

        if direction == "h":
            dx, dy = 0, 1

        elif direction == "v":
            dx, dy = 1, 0

        return cv2.Sobel(
            src=self.img,
            ddepth=cv2.CV_64F,
            dx=dx,
            dy=dy,
            ksize=3,
        )

    def apply_laplacian_filter(self):
        """
        Apply Laplacian filter of second order (i.e. 2nd derivative) along both x (horizontally) and y (vertically)

        Useful to detect edges

        Args:
            img: image as numpy array

        Returns:
            Image as numpy array
        """
        self.img = cv2.cvtColor(
            src=self.img,
            code=cv2.COLOR_RGB2GRAY,
        )

        return np.uint8(
            np.absolute(
                cv2.Laplacian(
                    src=self.img,
                    ddepth=cv2.CV_64F,
                )
            )
        )


class ImageVisualize:
    def __init__(self, img):
        self.img = img

    def crop_image(self, ymin, ymax, xmin, xmax):
        """Crop image with given size

        Args:
            img: image as numpy array
            ymin: start cropping position along height in pixels
            ymax: end cropping position along height in pixels
            xmin: end cropping position along width in pixels
            xmax: end cropping position along width in pixels

        Returns:
            Image as numpy array
        """
        return self.img[int(ymin) : int(ymax), int(xmin) : int(xmax), :]

    def add_white_boarder(self, width):
        """Add a white boarder to all sides of an image

        Args:
            img: image as numpy array
            width: boarder width in pixels

        Returns:
            Image as numpy array
        """
        return cv2.copyMakeBorder(
            src=self.img,
            top=width,
            bottom=width,
            left=width,
            right=width,
            borderType=cv2.BORDER_CONSTANT,
            value=(255, 255, 255),
        )

    def resize_image(self, direction, MAX_PIX):
        """
        Resize an image along the height or the width, and keep its aspect ratio

        Args:
            img: image as numpy array
            direction: either 'h' or 'v'
            MAX_PIX: required maximum number of pixels

        Returns:
            Image as numpy array
        """
        h, w, c = self.img.shape
        dsize = None

        if direction == "h":
            dsize = (int((MAX_PIX * w) / h), int(MAX_PIX))

        elif direction == "w":
            dsize = (int(MAX_PIX), int((MAX_PIX * h) / w))

        if not dsize:
            return self.img

        self.img = cv2.resize(
            src=self.img,
            dsize=dsize,
            interpolation=cv2.INTER_CUBIC,
        )

        h, w, c = self.img.shape

        return self.img


class KtpImageProcess:
    def __init__(self, image_request) -> None:
        self.image = self.open_image_fromstring(image_request)

    def open_image_fromstring(self, image_request):
        nparr = np.fromstring(string=image_request, dtype=np.uint8)
        return cv2.imdecode(nparr, flags=1)

    def open_image(self, image_request):
        return cv2.imread(image_request)

    def deskew(self):
        _, corrected = SkewCorrection().correct_skew(self.image)
        self.image = corrected

    def resize_image(self):
        self.image = ImageVisualize(self.image).resize_image("w", 640)

    def get_file_name(self, image_request):
        return os.path.basename(image_request)

    def save_as_image(self):
        return cv2.imwrite(self.image_request, self.image)

    def run(self):
        self.resize_image()
        self.deskew()
        self.resize_image()
        return self.image
