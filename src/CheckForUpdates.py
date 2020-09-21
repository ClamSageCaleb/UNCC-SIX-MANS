import bot
import os
import requests
import sys
import wget


def updateBot() -> None:
    release_url = requests.get("https://github.com/ClamSageCaleb/UNCC-SIX-MANS/releases/latest").url
    split_url = release_url.split("/")
    release_version = split_url[len(split_url) - 1]

    if (release_version[1:] > bot.__version__):
        print("A new version is available")

        if os.name == 'nt':
            print("Getting new Windows binary...")

            newFile = wget.download(
                "https://github.com/ClamSageCaleb/UNCC-SIX-MANS/releases"
                "/download/{0}/Norm_the_6_Mans_Bot_{0}.exe".format(release_version),
                os.getcwd() + "/Norm_the_6_Mans_Bot_{0}.exe".format(release_version)
            )
            os.startfile(newFile)
            sys.exit()
