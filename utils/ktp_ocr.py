import cv2
import os
import re
import json
from google.cloud import vision
from statistics import mean
import numpy as np
from utils.predict_fixed_string import PredictFixedString
from utils.string_helper import StringHelper

string_helper = StringHelper()


class OcrVision:
    def __init__(self, image) -> None:
        self.client = vision.ImageAnnotatorClient()
        self.img = image

    @property
    def vision_image(self):
        return vision.Image(content=self.get_img_bytes())

    def get_img_bytes(self):
        _, im_buf_arr = cv2.imencode(".jpg", self.img)
        return im_buf_arr.tobytes()

    def block_photo(self):
        image = self.img
        has_foto = False
        casc_path = os.path.join(
            cv2.data.haarcascades, "haarcascade_frontalface_default.xml"
        )
        face_cascade = cv2.CascadeClassifier(casc_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=4,
            minSize=(40, 60),
            flags=cv2.CASCADE_SCALE_IMAGE,
        )
        cv_height, cv_width, _ = image.shape

        list_x = []
        list_y = []
        list_w = []
        list_h = []
        x_cropper = 0
        y_cropper = 0
        w_cropper = cv_width
        h_cropper = cv_height

        face_count = 0
        for (x, y, w, h) in faces:
            face_count = face_count + 1
            list_y.append(y)
            list_w.append(w)
            list_h.append(h)
            list_x.append(x)

            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0, 50), 2)
            cv2.rectangle(
                image,
                (x - round(w * 0.1), y - round(h * 0.5)),
                (cv_width, cv_height),
                (0, 255, 0, 50),
                -1,
            )

        if len(faces) > 0:
            has_foto = True
            av_w = mean(list_w)
            av_h = mean(list_h)
            av_y = mean(list_y)
            av_x = mean(list_x)

            x_cropper = round(av_x - (av_w * 4.5))
            x_cropper = max(x_cropper, 0)
            y_cropper = round(av_y - (av_h * 1.5))
            y_cropper = max(y_cropper, 0)

            w_cropper = round(av_w * 6)
            h_cropper = round(av_h * 4)

            if w_cropper > cv_width:
                w_cropper = cv_width

            if h_cropper > cv_height:
                h_cropper = cv_height

        cv2.rectangle(
            image,
            (x_cropper, y_cropper),
            (w_cropper, h_cropper),
            (0, 255, 0, 50),
            2,
        )
        return has_foto, (x_cropper, y_cropper, w_cropper, h_cropper)

    def get_full_text_annotations(self):
        response = self.client.document_text_detection(image=self.vision_image)
        return response.full_text_annotation


class OcrVisionText(OcrVision):
    def __init__(self, image) -> None:
        OcrVision.__init__(self, image)

    def get_vertex_x_list(self, vertices):
        return [vertex.x for vertex in vertices]

    def get_vertex_y_list(self, vertices):
        return [vertex.y for vertex in vertices]

    def get_vertex_separate_list(self, vertices):
        vertex_x = []
        vertex_y = []
        for v in vertices:
            vertex_x.append(v.x)
            vertex_y.append(v.y)
        return (vertex_x, vertex_y)

    def get_text_list(self, text_annotations):
        list_text = []
        list_x = []
        list_y = []
        list_mean_y = []
        for i, text in enumerate(text_annotations):
            text_desc = text.description
            if text_desc.lower() != "kartu" or text_desc.lower() != "penduduk":
                # vertex_x = self.get_vertex_x_list(text.bounding_poly.vertices)
                # vertex_y = self.get_vertex_y_list(text.bounding_poly.vertices)
                vertex_x, vertex_y = self.get_vertex_separate_list(
                    text.bounding_poly.vertices
                )
                if i == 0:
                    self.min_x = np.min(vertex_x)
                    self.max_x = np.max(vertex_x)
                    self.min_y = np.min(vertex_y)
                    self.max_y = np.max(vertex_y)
                else:
                    list_x.append(vertex_x)
                    list_y.append(vertex_y)
                    list_text.append(text_desc)
                    list_mean_y.append(mean(vertex_y))

        return list_text, list_x, list_y, list_mean_y

    def get_text_annotations(self):
        response = self.client.text_detection(image=self.vision_image)
        return response.text_annotations


class KtpContentHelper:
    def __init__(self) -> None:
        self.predict = PredictFixedString()

    def validate_nik(self, content):
        content = content.replace(".", "").replace(" ", "")
        if len(content) > 14 and len(re.sub(r"[^0-9 ]", "", content)) > 12:
            if "$" in content:
                content = content.replace("$", "5")
            if "D" in content:
                content = content.replace("D", "0")
            if "h" in content:
                content = content.replace("h", "1")
            if "b" in content:
                content = content.replace("b", "6")
            if "?" in content:
                content = content.replace("?", "7")
            is_valid = bool(content.isnumeric())
        else:
            is_valid = False

        return is_valid, content

    def validate_tempat_lahir(self, content):
        found_number = re.findall(r"\d+", content)
        tempat_lahir = content.replace("Lahir", "")
        for fn in found_number:
            tempat_lahir = tempat_lahir.replace(fn, "")
        result = re.sub(r"[^a-z A-Z]+", "", tempat_lahir).strip()
        is_valid = result != ""
        result = result if is_valid else tempat_lahir
        return is_valid, result

    def validate_tanggal_lahir(self, content):
        is_valid = False
        result = content
        tanggal_lahir = string_helper.get_date_from_string(content)
        if tanggal_lahir:
            tanggal_lahir = tanggal_lahir.strftime("%d-%m-%Y")
            is_valid = True
            result = tanggal_lahir

        ttl = content.split(",")
        if len(ttl) == 2:
            date_in_string = re.findall(r"\d+", ttl[1])
            tanggal_lahir = string_helper.get_date_from_string("-".join(date_in_string))
            result = tanggal_lahir.strftime("%d-%m-%Y") if tanggal_lahir else ""
            is_valid = result != ""

        return is_valid, result

    def validate_golongan_darah(self, content) -> None:
        golongan_darah = self.predict.golongan_darah(content)
        is_valid = golongan_darah != ""
        result = golongan_darah if is_valid else content
        return is_valid, result

    def validate_jenis_kelamin(self, content):

        jenis_kelamin = self.predict.jenis_kelamin(
            string_helper.letter_sentences(content)
        )
        is_valid = jenis_kelamin != ""
        result = jenis_kelamin if is_valid else content
        return is_valid, result

    def validate_berlaku_hingga(self, content):
        berlaku_hingga = self.predict.tanggal_berlaku(content)
        return berlaku_hingga != "", berlaku_hingga

    def extract_rt_rw(self, content: str):
        content = (
            content.replace("o", "0")
            .replace("O", "0")
            .replace(".", "")
            .replace(",", "")
            .strip()
        )
        rt = ""
        rw = ""
        rt_rw = content.split("/")
        if len(rt_rw) == 2:
            rt = str(rt_rw[0])
            rw = str(rt_rw[1])
        else:
            rt_rw = re.findall(r"\d+", content)
            if len(rt_rw) == 2:
                rt = str(rt_rw[0])
                rw = str(rt_rw[1])
            else:
                rt_rw = string_helper.digits_only(content)
                if len(rt_rw) == 6:
                    rt = rt_rw[:3]
                    rw = rt_rw[4:]

        return rt, rw

    def validate_status_kawin(self, content):
        result = self.predict.status_kawin(self.clean_text_only_char(content))
        is_valid = result != ""
        return is_valid, result

    def validate_pekerjaan(self, content):
        result = self.predict.pekerjaan(string_helper.letter_sentences(content))
        is_valid = result != ""
        return is_valid, result

    def validate_kelurahan(self, content):
        result = self.clean_text_only_char(content)
        return result != "", result

    def validate_kecamatan(self, content):
        result = self.clean_text_only_char(content)
        return result != "", result

    def validate_agama(self, content):
        result = self.predict.agama(self.clean_text_only_char(content))
        is_valid = result != ""
        return is_valid, result

    def validate_alamat(self, content):
        result = string_helper.letter_sentences(content)
        is_valid = result != ""
        return is_valid, result

    def clean_text_only_char(self, content):
        return re.sub(r"[^a-zA-Z\s\-]+", "", content).strip()

    def clean_backgrund_text(self, content):
        possible_fix = ["KARTU", "PENDUDUK", ":"]
        for p in possible_fix:
            content = content.replace(p, "")
        return content.strip()


class KtpOcr(OcrVisionText, KtpContentHelper):
    def __init__(self, image):
        OcrVisionText.__init__(self, image)
        KtpContentHelper.__init__(self)
        self.min_x = 0
        self.max_x = 0
        self.min_y = 0
        self.max_y = 0
        self.score: float = 0
        self.setup(image)
        self.predict = PredictFixedString()

    def setup(self, image):
        self.tmp_result = {
            "provinsi": "",
            "kabupaten": "",
            "nik": "",
            "nama": "",
            "tempat_lahir": "",
            "tanggal_lahir": "",
            "jenis_kelamin": "",
            "alamat": "",
            "rt": "",
            "rw": "",
            "kelurahan": "",
            "kecamatan": "",
            "agama": "",
            "status_kawin": "",
            "pekerjaan": "",
            "kewarganegaraan": "",
            "berlaku_hingga": "",
            "golongan_darah": "",
        }

        self.result = {
            "nik": "",
            "nama": "",
            "tempat_lahir": "",
            "tanggal_lahir": "",
            "jenis_kelamin": "",
            "agama": "",
            "status_kawin": "",
            "pekerjaan": "",
            "alamat": "",
            "rt": "",
            "rw": "",
            "kelurahan": "",
            "kecamatan": "",
            "kabupaten": "",
            "provinsi": "",
            "kewarganegaraan": "",
            "berlaku_hingga": "",
            "golongan_darah": "",
        }
        self.client = vision.ImageAnnotatorClient()
        self.img = image
        self.text_annotations = self.get_text_annotations()

    def set_score(self):
        result_dict = self.result
        score_vals: dict[str:float] = {
            "nik": 9,
            "nama": 5,
            "tempat_lahir": 2.5,
            "tanggal_lahir": 2,
            "jenis_kelamin": 2,
            "agama": 1.25,
            "status_kawin": 1.5,
            "pekerjaan": 1.5,
            "alamat": 2.5,
            "rt": 1,
            "rw": 1,
            "kelurahan": 3,
            "kecamatan": 3,
            "kabupaten": 3,
            "provinsi": 3,
            "kewarganegaraan": 0.5,
            "berlaku_hingga": 0.75,
            "golongan_darah": 0.5,
        }
        max_score = sum(list(score_vals.values()))
        score = sum(
            score_vals.get(k, 0)
            for k in list(score_vals.keys())
            if result_dict.get(k, "") != ""
        )

        self.score = round((score / max_score) * 100, 2)

    def text_line_segmentation(self):
        list_text, list_x, list_y, list_mean_y = self.get_text_list(
            self.text_annotations
        )
        self.median_x = np.median(list_x)
        lines_dict = {}
        index_selected = []
        count_line_dict = 0
        sorted_y = np.array(list_mean_y)
        sort_index_y = np.argsort(sorted_y, axis=0)

        for i in sort_index_y:
            if i not in index_selected:
                mean_y = mean(list_y[i])
                new_line_text = [list_text[i]]
                new_line_x = [list_x[i]]
                new_line_y = [list_y[i]]
                font_height = round((list_y[i][3] - list_y[i][0]) * 0.65, 2)

                for j, y_compare in enumerate(list_y):
                    if (
                        j != i
                        and j not in index_selected
                        and (
                            mean_y == mean(y_compare)
                            or (
                                (mean_y - mean(y_compare)) < font_height
                                and (mean_y - mean(y_compare)) > (font_height * -1)
                            )
                        )
                    ):

                        new_line_text.append(list_text[j])
                        new_line_x.append(list_x[j])
                        new_line_y.append(list_y[j])

                        index_selected.append(j)
                lines_dict[count_line_dict] = self.sort_left_to_right_text_axis(
                    new_line_text, new_line_x, new_line_y
                )
                count_line_dict += 1

        return lines_dict

    def sort_left_to_right_text_axis(self, list_text, list_x, list_y):
        mean_x_list = [min(x) for x in list_x]
        sorted_x = np.array(mean_x_list)
        sort_index_x = np.argsort(sorted_x, axis=0)
        new_list_x = []
        new_list_y = []
        new_list_text = []
        for index_sorted in sort_index_x:
            new_list_text.append(list_text[index_sorted])
            new_list_x.append(list_x[index_sorted])
            new_list_y.append(list_y[index_sorted])
        return new_list_text, new_list_x, new_list_y

    def set_tmp_result(self, key, content):
        self.tmp_result[key] = content or ""

    def set_ktp_title(self, check_text):
        check_text = self.clean_text_only_char(check_text)
        if self.is_result_not_set("provinsi"):
            result = self.predict.provinsi(check_text)
            self.set_result("provinsi", result)
            return

        if self.is_result_not_set("kabupaten"):
            result = self.predict.kabupaten(check_text)
            self.set_result("kabupaten", result)
            return

    def is_result_not_set(self, key: str) -> bool:
        return self.result.get(key, "") == ""

    def get_result(self, key: str) -> str:
        return self.result.get(key, "")

    def set_result(self, key: str, content) -> None:
        if key not in list(self.result.keys()) or content is None or content == "":
            return
        rcontent = content
        is_valid = True
        if key == "jenis_kelamin":
            is_valid, rcontent = self.validate_jenis_kelamin(rcontent)
        elif key == "kewarganegaraan":
            rcontent = rcontent if rcontent in ("WNI", "WNA") else "WNI"
        elif key == "nama":
            rcontent = string_helper.letter_sentences(rcontent)
        elif key == "nik":
            is_valid, rcontent = self.validate_nik(rcontent)
        elif key == "pekerjaan":
            is_valid, rcontent = self.validate_pekerjaan(rcontent)
        elif key == "status_kawin":
            is_valid, rcontent = self.validate_status_kawin(rcontent)
        elif key == "tanggal_lahir":
            is_valid, rcontent = self.validate_tanggal_lahir(rcontent)
        elif key == "tempat_lahir":
            is_valid, rcontent = self.validate_tempat_lahir(rcontent)
        elif key == "agama":
            is_valid, rcontent = self.validate_agama(rcontent)
        elif key == "alamat":
            is_valid, rcontent = self.validate_alamat(rcontent)
        elif key == "kelurahan":
            is_valid, rcontent = self.validate_kelurahan(rcontent)
        elif key == "kecamatan":
            is_valid, rcontent = self.validate_kecamatan(rcontent)
        elif key == "berlaku_hingga":
            is_valid, rcontent = self.validate_berlaku_hingga(rcontent)
        elif key == "golongan_darah":
            is_valid, rcontent = self.validate_golongan_darah(rcontent)

        if is_valid:
            self.result[key] = rcontent
        self.tmp_result[key] = content

    def compose_result(self, left_content: str, right_content: str):
        if self.is_result_not_set("nik") and self.predict.is_list_in_string(
            left_content, ["νικ", "nik", "nlk"]
        ):
            self.set_result("nik", right_content)
            return

        if (
            self.is_result_not_set("tanggal_lahir")
            and self.is_result_not_set("tempat_lahir")
        ) and self.predict.is_list_in_string(
            left_content, self.predict.spell_tempat_tanggal_lahir()
        ):
            if self.is_result_not_set("tanggal_lahir"):
                self.set_result("tanggal_lahir", right_content)
            if self.is_result_not_set("tempat_lahir"):
                self.set_result("tempat_lahir", right_content)
            return

        if self.is_result_not_set("nama") and "nama" in left_content:
            self.set_result("nama", right_content)
            return

        if self.is_result_not_set("jenis_kelamin") and self.predict.is_list_in_string(
            left_content, self.predict.spell_jenis_kelamin()
        ):
            self.set_result("jenis_kelamin", right_content)
            if self.predict.is_list_in_string(
                right_content.lower(), ["gol", "dara", "arah"]
            ):
                self.set_result("golongan_darah", right_content)
            return

        if self.is_result_not_set("status_kawin") and self.predict.is_list_in_string(
            left_content, self.predict.spell_status_kawin()
        ):
            self.set_result("status_kawin", right_content)
            return

        if self.is_result_not_set("kewarganegaraan") and self.predict.is_list_in_string(
            left_content, self.predict.spell_kewarganegaraan()
        ):
            self.set_result("kewarganegaraan", right_content)
            return

        if self.is_result_not_set("pekerjaan") and self.predict.is_list_in_string(
            left_content, self.predict.spell_pekerjaan()
        ):
            self.set_result("pekerjaan", right_content)
            return

        if self.is_result_not_set("agama") and self.predict.is_list_in_string(
            left_content, ["agam", "gama"]
        ):
            self.set_result("agama", right_content)
            return

        if self.is_result_not_set("alamat") and self.predict.is_list_in_string(
            left_content, ["alama", "lamat"]
        ):
            self.set_result("alamat", right_content)
            return

        if self.is_result_not_set("rt") and self.predict.is_list_in_string(
            left_content, ["rt", "rw"]
        ):
            rt, rw = self.extract_rt_rw(right_content) if right_content else ("", "")
            self.set_result("rt", rt)
            self.set_result("rw", rw)
            return

        if self.is_result_not_set("kelurahan") and self.predict.is_list_in_string(
            left_content, self.predict.spell_desa_kelurahan()
        ):
            self.set_result("kelurahan", right_content)
            return

        if self.is_result_not_set("kecamatan") and self.predict.is_list_in_string(
            left_content, self.predict.spell_kecamatan()
        ):
            self.set_result("kecamatan", right_content)
            return

        if self.is_result_not_set("berlaku_hingga") and self.predict.is_list_in_string(
            left_content, self.predict.spell_berlaku_hingga()
        ):
            self.set_result("berlaku_hingga", right_content)
            return

    def find_nik_by_len(self, line_dict):
        for list_text, _, _ in line_dict.values():
            for text in list_text:
                if len(text) > 15 and self.result["nik"] == "":
                    self.set_result("nik", text)

    def get_index_by_key_name(self, key_name, line_dict):
        if self.tmp_result[key_name] == "":
            return None
        index_found = None
        for i, (list_text, _, _) in enumerate(line_dict.values()):
            for text in list_text:
                if len(text) > 2 and text in self.tmp_result[key_name]:
                    index_found = i
                    break

        return index_found

    def find_by_index(self, lines_dict, i):
        if i in lines_dict:
            text_found = [""]
            text_list, x_list, _ = lines_dict[i]

            for i, text in enumerate(text_list):
                if min(x_list[i]) > self.separate_point:
                    text_found.append(text)
                i += 1

            return " ".join(text_found)
        return None

    def get_by_prev_next_index(self, lines_dict, prev_name, next_name):
        prev_index = self.get_index_by_key_name(prev_name, line_dict=lines_dict)
        if prev_index:
            find_by_prev = self.find_by_index(lines_dict, prev_index + 1)
            if find_by_prev:
                return find_by_prev

        next_index = self.get_index_by_key_name(next_name, line_dict=lines_dict)
        return self.find_by_index(lines_dict, next_index - 1) if next_index else None

    def recheck_result(self, lines_dict, loop_i=3, prev_res_empy=0):

        if self.result["nik"] == "":
            self.find_nik_by_len(lines_dict)

        if self.result["nama"] == "":
            self.set_result(
                "nama", self.get_by_prev_next_index(lines_dict, "nik", "tempat_lahir")
            )

        if self.result["tempat_lahir"] == "":
            self.set_result(
                "tempat_lahir",
                self.get_by_prev_next_index(lines_dict, "nama", "jenis_kelamin"),
            )

        if self.is_result_not_set("tanggal_lahir"):
            tanggal_lahir = self.get_by_prev_next_index(
                lines_dict, "nama", "jenis_kelamin"
            )
            if tanggal_lahir:
                self.set_result("tanggal_lahir", tanggal_lahir)
            
            if not self.is_result_not_set("nik") and self.is_result_not_set("tanggal_lahir"):
                self.set_result(
                    "tanggal_lahir",
                    self.predict.tanggal_lahir_from_nik(self.get_result("nik")),
                )

        if self.result["jenis_kelamin"] == "":
            jenis_kelamin = self.get_by_prev_next_index(
                lines_dict, "tanggal_lahir", "alamat"
            )
            if jenis_kelamin:
                self.set_result("jenis_kelamin", jenis_kelamin)
                
            if not self.is_result_not_set("nik") and self.is_result_not_set("jenis_kelamin"):
                self.set_result(
                    "jenis_kelamin",
                    self.predict.jenis_kelamin_from_nik(self.get_result("nik")),
                )

        if self.result["alamat"] == "":
            self.set_result(
                "alamat", self.get_by_prev_next_index(lines_dict, "jenis_kelamin", "rt")
            )

        if self.result["rt"] == "" or self.result["rw"] == "":
            rt_rw = self.get_by_prev_next_index(lines_dict, "alamat", "kelurahan")
            rt, rw = self.extract_rt_rw(rt_rw) if rt_rw else ("", "")
            self.set_result("rt", rt)
            self.set_result("rw", rw)

        if self.result["kelurahan"] == "":
            kelurahan = self.get_by_prev_next_index(lines_dict, "rt", "kecamatan")
            if not kelurahan:
                kelurahan = self.get_by_prev_next_index(lines_dict, "rw", "kecamatan")
            self.set_result("kelurahan", kelurahan)

        if self.result["kecamatan"] == "":
            self.set_result(
                "kecamatan",
                self.get_by_prev_next_index(lines_dict, "kelurahan", "agama"),
            )

        if self.result["agama"] == "":
            self.set_result(
                "agama",
                self.get_by_prev_next_index(lines_dict, "kecamatan", "status_kawin"),
            )

        if self.result["status_kawin"] == "":
            self.set_result(
                "status_kawin",
                self.get_by_prev_next_index(lines_dict, "agama", "pekerjaan"),
            )

        if self.result["pekerjaan"] == "":
            self.set_result(
                "pekerjaan",
                self.get_by_prev_next_index(
                    lines_dict, "status_kawin", "kewarganegaraan"
                ),
            )

        result_list = list(self.result.values())
        empty_res = result_list.count("")

        if loop_i > 0 and prev_res_empy > empty_res and empty_res > 1:
            self.recheck_result(lines_dict, loop_i - 1, empty_res)

    def text_processing(self):
        lines_dict = self.text_line_segmentation()
        median_x = self.median_x
        min_x = self.min_x

        left_right_content = []
        self.separate_point = median_x * 0.6 + min_x

        for list_text, list_x, list_y in lines_dict.values():
            left_list = []
            right_list = []

            for i, x in enumerate(list_x):
                if min(x) < self.separate_point:
                    left_list.append(list_text[i])
                else:
                    right_list.append(list_text[i])

            left_right_content.append((" ".join(left_list), " ".join(right_list)))
            if not left_list:
                self.set_ktp_title(" ".join(right_list))

        for left_content, right_content in left_right_content:
            left_content = (
                left_content.lower().replace(" ", "").replace(":", "").strip()
            )
            right_content = right_content.replace("  ", " ").replace(":", "").strip()
            self.compose_result(left_content, right_content)

        result_list = list(self.result.values())
        empty_res = result_list.count("")
        if empty_res > 1 or self.result["nik"] == "":
            self.recheck_result(lines_dict, 3, empty_res)

        self.set_score()
        return self.result

    def get_dict(self):
        return self.text_processing() if self.text_annotations else self.result

    def run(self):
        result = self.text_processing() if self.text_annotations else self.result
        return self.score, result

    def get_json(self):
        res = self.text_processing()
        return json.dumps(res, skipkeys=True)
