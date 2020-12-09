import math
import configparser
from pathlib import Path

if __name__ == "__main__":
    """read params"""
    SEC_NAME = "TMD"

    try:
        config = configparser.ConfigParser()
        config.read(str(Path(__file__).parent.joinpath("param.ini")))
        m_main = float(config.get(SEC_NAME, "mass_main"))
        f_main = float(config.get(SEC_NAME, "f_main"))
        m_tmd = float(config.get(SEC_NAME, "mass_tmd"))

        print("INPUT:")
        print("M_tower\t=\t%f kg" % m_main)
        print("m_tmd\t=\t%f kg" % m_tmd)
        print("f_tower\t=\t%f Hz" % f_main)

        print("\nRESULT:")
        mass_ratio = m_tmd / m_main
        print("mass_ratio\t=\t%f" % mass_ratio)

        f_tmd = f_main / (1.0 + mass_ratio)
        print("frequency_tmd\t=\t%f Hz" % f_tmd)

        len_pendulum = 9.8 / math.pow(2 * math.pi * f_tmd, 2)
        print("len_pendulum\t=\t%f m" % len_pendulum)

        zeta = math.sqrt(3.0 / 8.0 * mass_ratio / (1 + mass_ratio))
        print("zeta_opt\t=\t%f" % zeta)

        damping_coefficient = zeta * 2 * m_tmd * 1000 * 2 * math.pi * f_tmd
        print("damping_c\t=\t%f Ns/m" % damping_coefficient)

    except Exception as err:
        print("load param.ini failed, use defaut settings")
        print("error message: %s" % err)

