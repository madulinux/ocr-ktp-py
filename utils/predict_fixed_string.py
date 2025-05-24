from utils.string_helper import StringHelper


class PredictFixedString:
    @staticmethod
    def spell_kecamatan() -> list:
        return ["keca", "ecam", "cama", "amata", "matan"]

    @staticmethod
    def spell_tempat_tanggal_lahir() -> list:
        return ["temp", "mpat", "tgl", "lahi", "ahir"]

    @staticmethod
    def spell_jenis_kelamin() -> list:
        return ["jeni", "enis", "kela", "lami", "amin"]

    @staticmethod
    def spell_status_kawin() -> list:
        return ["stat", "tatu", "atus", "kawi", "awin"]

    @staticmethod
    def spell_pekerjaan() -> list:
        return ["peke", "eker", "kerj", "erja", "rjaa", "jaan"]

    @staticmethod
    def spell_kewarganegaraan() -> list:
        return ["kewa", "ewar", "warg", "rgan", "negar", "egaraa", "araan"]

    @staticmethod
    def spell_desa_kelurahan() -> list:
        return ["desa", "kelu", "elur", "lura", "urah", "rahan"]

    @staticmethod
    def spell_berlaku_hingga() -> list:
        return ["berl", "erla", "erla", "rlak", "laku", "hingg", "ingga"]

    @staticmethod
    def spell_provinsi() -> list:
        return ["prov", "rovi", "ovin", "vins", "insi"]

    @staticmethod
    def is_list_in_string(content: str, search_list: list):
        return any(search in content for search in search_list)

    @staticmethod
    def jenis_kelamin_from_nik(nik: str) -> str:
        if len(nik) != 16:
            return ""
        t = nik[6:8]
        return "PEREMPUAN" if int(t) > 31 else "LAKI-LAKI"

    @staticmethod
    def tanggal_lahir_from_nik(nik: str) -> str:
        print("CHECK TANGGAL LAHIR")
        if len(nik) != 16:
            return ""
        
        print(nik)
        dob = nik[6:12]
        d = dob[:2]
        m = dob[2:4]
        y = dob[4:]
        yr = f"19{y}"
        print(dob)
        print(f"d: {d}, m: {m}, y: {y}, yr: {yr}")
        if int(d) > 31:
            d = str(int(d) - 40)

        if int(y) < 40:
            yr = f"20{y}"
        print(f"{d}-{m}-{yr}")
        return f"{d}-{m}-{yr}"

    def get_pekerjaan(self, key) -> str:
        pekerjaans = self.dict_pekerjaan
        return pekerjaans.get(key, "") if key else ""

    @property
    def dict_pekerjaan(self):
        return {
            "belumtidakbekerja": "BELUM/TIDAK BEKERJA",
            "pegawainegerisipil": "PEGAWAI NEGERI SIPIL",
            "pegawainegerisipilpns": "PEGAWAI NEGERI SIPIL (PNS)",
            "tentaranasionalindonesia": "TENTARA NASIONAL INDONESIA",
            "tentaranasionalindonesiatni": "TENTARA NASIONAL INDONESIA (TNI)",
            "kepolisianri": "KEPOLISIAN RI",
            "pelajarmahasiswa": "PELAJAR/MAHASISWA",
            "pensiunan": "PENSIUNAN",
            "buruhharianlepas": "BURUH HARIAN LEPAS",
            "buruhtaniperkebunan": "BURUH TANI/PERKEBUNAN",
            "buruhpeternakan": "BURUH PETERNAKAN",
            "buruhnelayanperikanan": "BURUH NELAYAN/PERIKANAN",
            "peternak": "PETERNAK",
            "nelayanperikanan": "NELAYAN/PERIKANAN",
            "petanipekebun": "PETANI/PEKEBUN",
            "dosen": "DOSEN",
            "pedagang": "PEDAGANG",
            "perdagangan": "PERDAGANGAN",
            "mengurusrumahtangga": "MENGURUS RUMAH TANGGA",
            "guru": "GURU",
            "karyawanbumn": "KARYAWAN BUMN",
            "karyawanbumd": "KARYAWAN BUMD",
            "karyawanswasta": "KARYAWAN SWASTA",
            "karyawanhonorer": "KARYAWAN HONORER",
            "wartawan": "WARTAWAN",
            "anggotadprri": "ANGGOTA DPR-RI",
            "anggotadpd": "ANGGOTA DPD",
            "anggotabpk": "ANGGOTA BPK",
            "anggotadprdprovinsi": "ANGGOTA DPRD PROVINSI",
            "anggotadprdkabupatenkota": "ANGGOTA DPRD KABUPATEN/KOTA",
            "anggotamahkamahkonstitusi": "ANGGOTA MAHKAMAH KONSTITUSI",
            "anggotakabinetkementerian": "ANGGOTA KABINET/KEMENTERIAN",
            "perangkatdesa": "PERANGKAT DESA",
            "kepaladesa": "KEPALA DESA",
            "pembanturumahtangga": "PEMBANTU RUMAH TANGGA",
            "tukangcukur": "TUKANG CUKUR",
            "tukanglistrik": "TUKANG LISTRIK",
            "tukangbatu": "TUKANG BATU",
            "tukangkayu": "TUKANG KAYU",
            "tukangsolsepatu": "TUKANG SOL SEPATU",
            "tukanglaspandaibesi": "TUKANG LAS/PANDAI BESI",
            "tukangjahit": "TUKANG JAHIT",
            "tukanggigi": "TUKANG GIGI",
            "wiraswasta": "WIRASWASTA",
            "presiden": "PRESIDEN",
            "wakilpresiden": "WAKIL PRESIDEN",
            "dutabesar": "DUTA BESAR",
            "gubernur": "GUBERNUR",
            "wakilgubernur": "WAKIL GUBERNUR",
            "bupati": "BUPATI",
            "wakilbupati": "WAKIL BUPATI",
            "walikota": "WALIKOTA",
            "wakilwalikota": "WAKIL WALIKOTA",
            "pengacara": "PENGACARA",
            "notaris": "NOTARIS",
            "peneliti": "PENELITI",
            "industri": "INDUSTRI",
            "konstruksi": "KONSTRUKSI",
            "transportasi": "TRANSPORTASI",
            "penatarias": "PENATA RIAS",
            "penatabusana": "PENATA BUSANA",
            "penatarambut": "PENATA RAMBUT",
            "mekanik": "MEKANIK",
            "seniman": "SENIMAN",
            "tabib": "TABIB",
            "paraji": "PARAJI",
            "perancangbusana": "PERANCANG BUSANA",
            "penterjemah": "PENTERJEMAH",
            "jurumasak": "JURU MASAK",
            "promotoracara": "PROMOTOR ACARA",
            "pilot": "PILOT",
            "arsitek": "ARSITEK",
            "akuntan": "AKUNTAN",
            "konsultan": "KONSULTAN",
            "penyiartelevisi": "PENYIAR TELEVISI",
            "penyiarradio": "PENYIAR RADIO",
            "pelaut": "PELAUT",
            "sopir": "SOPIR",
            "pialang": "PIALANG",
            "paranormal": "PARANORMAL",
            "imammesjid": "IMAM MESJID",
            "pendeta": "PENDETA",
            "pastor": "PASTOR",
            "ustadzmubaligh": "USTADZ/MUBALIGH",
            "biarawati": "BIARAWATI",
            "dokter": "DOKTER",
            "bidan": "BIDAN",
            "perawat": "PERAWAT",
            "apoteker": "APOTEKER",
            "psikiaterpsikolog": "PSIKIATER/PSIKOLOG",
            "lainnya": "LAINNYA",
        }

    def check_pekerjaan_buruh(self, content: str) -> str:
        if PredictFixedString.is_list_in_string(content, ["har", "rian", "lep", "pas"]):
            return PredictFixedString().get_pekerjaan("buruhharianlepas")

        if PredictFixedString.is_list_in_string(content, ["tan", "per", "keb", "bun"]):
            return PredictFixedString().get_pekerjaan("buruhtaniperkebunan")

        if PredictFixedString.is_list_in_string(content, ["pet", "ter", "nak"]):

            return PredictFixedString().get_pekerjaan("buruhpeternakan")

        if PredictFixedString.is_list_in_string(
            content, ["nel", "aya", "ikan", "peri", "kana"]
        ):
            return PredictFixedString().get_pekerjaan("buruhnelayanperikanan")

        return StringHelper().letter_sentences(content.upper)

    def check_pekerjaan_tukang(self, content: str) -> str:
        if "bat" in content:
            return PredictFixedString().get_pekerjaan("tukangbatu")
        if PredictFixedString.is_list_in_string(content, ["ay", "yu"]):
            return PredictFixedString().get_pekerjaan("tukangkayu")
        if PredictFixedString.is_list_in_string(content, ["sol", "sep", "epa", "pat"]):
            return PredictFixedString().get_pekerjaan("tukangsolsepatu")
        if PredictFixedString.is_list_in_string(content, ["las", "dai", "bes"]):
            return PredictFixedString().get_pekerjaan("tukanglaspandaibesi")
        if PredictFixedString.is_list_in_string(content, ["jah", "ahi", "hit"]):
            return PredictFixedString().get_pekerjaan("tukangjahit")
        if PredictFixedString.is_list_in_string(content, ["gi", "ig"]):
            return PredictFixedString().get_pekerjaan("tukanggigi")

        return StringHelper().letter_sentences(content.upper())

    def check_pekerjaan_desa(self, content: str) -> str:
        if PredictFixedString.is_list_in_string(content, ["kep", "epa", "pal", "ala"]):
            return PredictFixedString().get_pekerjaan("kepaladesa")
        if PredictFixedString.is_list_in_string(
            content, ["per", "era", "ran", "ang", "ngk", "gka", "kat"]
        ):
            return PredictFixedString().get_pekerjaan("perangkatdesa")

        return (
            PredictFixedString().get_pekerjaan("perangkatdesa")
            if "desa" in content
            else StringHelper().letter_sentences(content.upper())
        )

    def check_pekerjaan_karyawan(self, content: str) -> str:
        if PredictFixedString.is_list_in_string(content, ["sw", "as", "ta"]):
            return PredictFixedString().get_pekerjaan("karyawanswasta")
        if "mn" in content:
            return PredictFixedString().get_pekerjaan("karyawanbumn")

        if PredictFixedString.is_list_in_string(
            content, ["hon", "ono", "nor", "ore", "rer"]
        ):
            return PredictFixedString().get_pekerjaan("karyawanhonorer")
        return (
            PredictFixedString().get_pekerjaan("karyawanbumd")
            if "md" in content
            else StringHelper().letter_sentences(content.upper())
        )

    def check_pekerjaan_anggota(self, content: str) -> str:
        if "dp" in content:
            if "pd" in content:
                return self.get_pekerjaan("anggotadpd")

            if "ri" in content:
                return self.get_pekerjaan("anggotadprri")

            if PredictFixedString.is_list_in_string(
                content,
                ["kab", "abu", "bup", "upa", "pat", "ate", "ten", "kot"],
            ):
                return self.get_pekerjaan("anggotadprdkabupatenkota")

            if PredictFixedString.is_list_in_string(
                content, ["pro", "rov", "ovi", "vin", "nsi"]
            ):
                return self.get_pekerjaan("anggotadprdprovinsi")

        if PredictFixedString.is_list_in_string(content, ["bp", "pk"]):
            return self.get_pekerjaan("anggotabpk")

        if PredictFixedString.is_list_in_string(
            content, ["kon", "ons", "nst", "stit", "titu", "tusi"]
        ):
            return self.get_pekerjaan("anggotamahkamahkonstitusi")

        if PredictFixedString.is_list_in_string(
            content,
            ["kem", "emen", "ment", "ente", "nter", "teri", "eria", "rian"],
        ):
            return self.get_pekerjaan("anggotakabinetkementerian")

        return StringHelper().letter_sentences(content.upper())

    @staticmethod
    def pekerjaan(content):
        pekerjaans = PredictFixedString().dict_pekerjaan

        content_letter = StringHelper().letter_only(content).lower()

        if content_letter in list(pekerjaans.keys()):
            return PredictFixedString().get_pekerjaan(content_letter)

        content_lower = content.lower()
        if PredictFixedString.is_list_in_string(content_lower, ["belum", "tidak"]):
            return pekerjaans["belumtidakbekerja"]

        if PredictFixedString.is_list_in_string(
            content_lower, ["pens", "nsiu", "siun"]
        ):
            return pekerjaans["pensiunan"]

        if PredictFixedString.is_list_in_string(
            content_lower, ["elaj", "maha", "hasi", "sisw"]
        ):
            return pekerjaans["pelajarmahasiswa"]

        if PredictFixedString.is_list_in_string(
            content_lower, ["pns", "nege", "geri", "negr", "sipi", "ipil"]
        ):
            return pekerjaans["pegawainegerisipilpns"]

        if PredictFixedString.is_list_in_string(content_lower, ["buru", "uruh"]):
            PredictFixedString().check_pekerjaan_buruh(content_lower)

        buruh2_list = ["bu", "ur", "ru", "uh"]
        if PredictFixedString.is_list_in_string(
            content_lower, ["nela", "ayan", "ikan", "peri", "kanan"]
        ):
            if PredictFixedString.is_list_in_string(content_lower, buruh2_list):
                return pekerjaans["buruhnelayanperikanan"]
            return pekerjaans["nelayanperikanan"]

        if PredictFixedString.is_list_in_string(
            content_lower, ["tani", "perke", "kebun", "bunan"]
        ):
            if PredictFixedString.is_list_in_string(content_lower, buruh2_list):
                return pekerjaans["buruhtaniperkebunan"]
            return pekerjaans["petanipekebun"]

        if PredictFixedString.is_list_in_string(
            content_lower, ["peter", "terna", "rnak"]
        ):
            if PredictFixedString.is_list_in_string(content_lower, buruh2_list):
                return pekerjaans["buruhpeternakan"]
            return pekerjaans["peternak"]

        if PredictFixedString.is_list_in_string(content_lower, ["dose", "osen"]):
            return pekerjaans["dosen"]

        if PredictFixedString.is_list_in_string(content_lower, ["bida", "idan"]):
            return pekerjaans["bidan"]

        if PredictFixedString.is_list_in_string(
            content_lower, ["tni", "tent", "tara", "nasio", "ional"]
        ):
            return pekerjaans["tentaranasionalindonesiatni"]

        if PredictFixedString.is_list_in_string(
            content_lower, ["kepo", "polis", "polr"]
        ):
            return pekerjaans["kepolisianri"]

        if PredictFixedString.is_list_in_string(
            content_lower, ["bel", "elu", "lum", "idak", "rja"]
        ):
            return pekerjaans["belumtidakbekerja"]

        if PredictFixedString.is_list_in_string(content_lower, ["daga", "gang"]):
            if PredictFixedString.is_list_in_string(content_lower, ["er"]):
                return pekerjaans["perdagangan"]
            return pekerjaans["pedagang"]

        if "gur" in content_lower:
            if len(content_lower) < 6:
                return pekerjaans["guru"]

            if PredictFixedString.is_list_in_string(
                content_lower, ["pem", "ban", "ntu"]
            ):
                return pekerjaans["pembanturumahtangga"]
            return pekerjaans["mengurusrumahtangga"]

        if PredictFixedString.is_list_in_string(
            content_lower, ["wart", "arta", "tawa"]
        ):
            return pekerjaans["wartawan"]

        if PredictFixedString.is_list_in_string(
            content_lower, ["wira", "iras", "rasw", "aswa"]
        ):
            return PredictFixedString().get_pekerjaan("wiraswasta")

        if PredictFixedString.is_list_in_string(content_lower, ["ary", "rya", "yaw"]):
            return PredictFixedString().check_pekerjaan_karyawan(content_lower)

        if PredictFixedString.is_list_in_string(content_lower, ["nggot", "gota"]):
            return PredictFixedString().check_pekerjaan_anggota(content_lower)

        if "des" in content_lower:
            return PredictFixedString().check_pekerjaan_desa(content_lower)

        if PredictFixedString.is_list_in_string(content_lower, ["tukan", "ukang"]):
            return PredictFixedString().check_pekerjaan_tukang(content_lower)

        return StringHelper().letter_sentences(content)

    @staticmethod
    def golongan_darah(content: str) -> str:
        list_gol = content.split(" ")
        golongan_darah = list_gol[-1]
        golongan_darah = golongan_darah.upper()
        if "8" in golongan_darah:
            golongan_darah = golongan_darah.replace("8", "B")

        if "0" in golongan_darah:
            golongan_darah = golongan_darah.replace("0", "O")

        if "4" in golongan_darah:
            golongan_darah = golongan_darah.replace("4", "A")

        if "*" in golongan_darah:
            golongan_darah = golongan_darah.replace("*", "+")
        if golongan_darah in (
            "A",
            "A+",
            "A-",
            "B",
            "B+",
            "B-",
            "O",
            "O+",
            "O-",
            "AB",
            "AB+",
            "AB-",
        ):
            return golongan_darah

        else:
            return ""

    @staticmethod
    def agama(content):
        if content in (
            "ISLAM",
            "KRISTEN",
            "KATOLIK",
            "BUDHA",
            "BUDDHA",
            "HINDU",
            "KONGHUCU",
            "KONGHUCHU",
            "KEPERCAYAAN",
        ):
            return content
        content_lower = content.lower()

        islam_list = ["isl", "sla", "lam"]
        if any(islam in content_lower for islam in islam_list):
            return "ISLAM"

        kristen_list = [
            "kri",
            "ris",
            "ten",
        ]
        if any(kristen in content_lower for kristen in kristen_list):
            return "KRISTEN"

        katolik_list = [
            "kat",
            "tol",
            "lik",
        ]
        if any(katolik in content_lower for katolik in katolik_list):
            return "KATOLIK"

        budha_list = [
            "bud",
            "udh",
            "dha",
        ]
        if any(budha in content_lower for budha in budha_list):
            return "BUDDHA"

        konghucu_list = ["kon", "ngh", "huc", "ucu"]
        if any(konghucu in content_lower for konghucu in konghucu_list):
            return "KONGHUCU"

        kepercayaan_list = ["kep", "per", "cay", "aan"]
        if any(kepercayaan in content_lower for kepercayaan in kepercayaan_list):
            return "KEPERCAYAAN"

        return ""

    @staticmethod
    def jenis_kelamin(content):

        if PredictFixedString.is_list_in_string(
            content, ["PE", "ER", "RE", "EM", "MP", "PU", "UA", "AN"]
        ):
            return "PEREMPUAN"

        if PredictFixedString.is_list_in_string(
            content, ["LA", "AK", "KI", "I-", "-L"]
        ):
            return "LAKI-LAKI"

        return ""

    @staticmethod
    def tanggal_berlaku(content: str) -> str:
        tanggal_berlaku = StringHelper().get_date_from_string(content)

        if tanggal_berlaku:
            tanggal_berlaku = tanggal_berlaku.strftime("%d-%m-%Y")
        elif PredictFixedString.is_list_in_string(
            content.lower(), ["seum", "umur", "hidu", "idup"]
        ):
            tanggal_berlaku = "SEUMUR HIDUP"
        else:
            tanggal_berlaku = ""

        return tanggal_berlaku

    @staticmethod
    def status_kawin(content: str) -> str:
        list_status = content.split(" ")
        new_list_status = []
        pernah_list = ["per", "rna", "nah"]
        belum_list = ["bel", "elu", "lum"]
        kawin_list = ["kaw", "awi", "win"]
        for status in list_status:
            status_lower = status.lower()
            if any(pernah in status_lower for pernah in pernah_list):
                new_list_status.append("PERNAH")
            elif any(belum in status_lower for belum in belum_list):
                new_list_status.append("BELUM")
            elif any(kawin in status_lower for kawin in kawin_list):
                new_list_status.append("KAWIN")

        new_status = " ".join(new_list_status)

        if "PERNAH" in new_status:
            return "PERNAH KAWIN"
        if "BELUM" in new_status:
            return "BELUM KAWIN"

        return "KAWIN" if "KAWIN" in new_status else ""

    @staticmethod
    def provinsi(content: str) -> str:
        result = ""
        content = content.upper()
        if "DKI" in content:
            return "DKI JAKARTA"
        provinsi_arr = content.strip().split(" ")
        len_provinsi_arr = len(provinsi_arr)
        if len_provinsi_arr < 1:
            return result

        for i in range(len_provinsi_arr - 1):
            has_prov = PredictFixedString.is_list_in_string(
                provinsi_arr[i].lower(), PredictFixedString.spell_provinsi()
            )
            if has_prov:
                result = " ".join(provinsi_arr[i + 1 :])
                break
        return result

    @staticmethod
    def kabupaten(content: str) -> str:

        content = content.upper().strip()
        if "JAKARTA" in content:
            return content

        if PredictFixedString.is_list_in_string(content, ["KABUPATEN", "KOTA"]):
            return content.replace("KABUPATEN", "").strip()

        arr_content = content.split(" ")
        len_arr_content = len(arr_content)
        result = content
        for i in range(len_arr_content - 1):
            is_found = PredictFixedString.is_list_in_string(
                arr_content[i], ["abupa", "bupat", "upate", "paten"]
            )
            if is_found:
                result = " ".join(arr_content[i + 1 :])
                break
        return result
