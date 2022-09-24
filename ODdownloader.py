import requests
import logging as logger
import time
import base64
import os

class Odownloader:
    """
    Create one drive downloader class.
    """
    def __init__(self, download_path=''):
        # super(Odownloader, self).__init__(file_data, download_path)
        """
        initializing classes
        """
        if not download_path:
            self.download_path = os.path.join(os.getcwd(), 'downloads')

    def set_base_download_path(self, path):
        """Change downloads path locations"""
        self.download_path = path

    def get_db(self, file_data):
        """
        get database from file
        """
        data = {
            'no': [],
            'name': [],
            'link': [],
            'file-size': []
        }
        with open(file_data, 'r') as f:
            for line in f:
                temp = line.replace('\n', '').split(",")
                data['no'].append(temp[0])
                data['name'].append(temp[1])
                data['link'].append(temp[2])
                data['file-size'].append(temp[3])
        # self.db = data
        return data

    def create_onedrive_direct_download(onedrive_link):
        """
        create onedrive direct download link from shared links.
        """
        data_bytes64 = base64.b64encode(bytes(onedrive_link, 'utf-8'))
        data_bytes64_String = data_bytes64.decode('utf-8').replace('/', '_').replace('+', '-').rstrip("=")
        resultUrl = f"https://api.onedrive.com/v1.0/shares/u!{data_bytes64_String}/root/content"
        return resultUrl

    def download(self, url: str, file2dl, file_name='', attempts=2):
        """Downloads a URL content into a file (with large file support by streaming)

        :param url: URL to download
        :param file_path: Local file name to contain the data downloaded
        :param attempts: Number of attempts
        :return: New file path. Empty string if the download failed
        """
        if file_name:
            file_path = os.path.join(self.download_path, file_name)
        else:
            file_path = os.path.join(self.download_path, file2dl[1])

        logger.info(f'Downloading {url} content to {file_path}')

        for attempt in range(1, attempts + 1):
            try:
                if attempt > 1:
                    time.sleep(10)  # 10 seconds wait time between downloads
                # print(requests.head(urls).headers['content-length'])
                with requests.get(url, stream=True) as response:
                    response.raise_for_status()
                    filesize = float(file2dl[3])

                    with open(file_path, 'wb') as out_file:
                        ctr = 0
                        for chunk in response.iter_content(chunk_size=8192):
                            out_file.write(chunk)
                            ctr += 1
                            downloaded = ctr * 8192 / 1024 / 1024
                            if int(downloaded * 100 / filesize) % 20 == 0:
                                print(
                                    f"downloading files {'%.2f' % downloaded}-MB from {filesize}-MB --> {int(downloaded/filesize*100)}% "
                                )
                    logger.info('Download finished successfully')
                    return file_path
            except Exception as ex:
                logger.error(f'Attempt #{attempt} failed with error: {ex}')
        return ''
