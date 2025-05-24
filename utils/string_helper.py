import re
import datefinder
from typing import Union
import string
import random
import uuid
from datetime import datetime


class StringHelper:
    @staticmethod
    def get_date_from_string(content: str) -> Union[str, None]:
        find_tanggal = None
        tanggals = datefinder.find_dates(content, first="day")
        for tanggal in tanggals:
            find_tanggal = tanggal

        return find_tanggal

    @staticmethod
    def letter_sentences(content):
        """Clean string, match only letters (a-z and A-Z), (. , - /) and space

        Args:
            content (string): sentences

        Returns:
            string: sentences
        """
        return re.sub(r"[^a-zA-Z\s\.\,\-\/]+", "", content).strip()

    @staticmethod
    def letter_only(content):
        """Match characters letters (a-z and A-Z) only

        Args:
            content (string): sentences

        Returns:
            string: sentences
        """
        return re.sub(r"[^a-zA-Z]+", "", content)

    @staticmethod
    def random_letters(length=8, case=None):
        if case == "lower":
            letters = string.ascii_lowercase
        elif case == "upper":
            letters = string.ascii_uppercase
        else:
            letters = string.ascii_letters
        return "".join(random.choice(letters) for _ in range(length))

    @staticmethod
    def digits_only(content):
        """Match characters digits (0-9) only

        Args:
            content (string): sentences input

        Returns:
            string: sentences output
        """
        return re.sub(r"[^0-9 ]", "", content)

    @staticmethod
    def get_safe_filename():
        uuid_name = str(uuid.uuid4())
        arr_uuid_name = uuid_name.split("-")
        now = datetime.now()
        s_now = now.strftime("%y-%m-%d")
        arr_now = s_now.split("-")
        arr_kode = arr_uuid_name + arr_now
        random.shuffle(arr_kode)
        return s_now, "".join(arr_kode)
