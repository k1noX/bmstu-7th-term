import argparse
import logging
import os
import typing as _t

from hdfs import InsecureClient

APP_LOGGING_LEVEL = 31
URL = "http://localhost:9870"
logging.addLevelName(APP_LOGGING_LEVEL, "APP")


class NotFileException(BaseException):
    def __init__(self, path: str, type_name: str, *args):
        self.path = path
        self.type_name = type_name
        BaseException.__init__(self, args)


def check_hdfs_file(filename: str) -> _t.Optional[_t.Dict]:
    client = InsecureClient(URL, user="hadoop")
    status = client.status(filename, strict=False)
    if (
            isinstance(status, dict)
            and "type" in status
            and status["type"] != "FILE"
    ):
        raise NotFileException(path=filename, type_name=status["type"])
    return status


def check_local_file(filename: str) -> _t.Optional[os.stat_result]:
    if os.path.isfile(filename):
        return os.stat(filename)
    if os.path.exists(filename):
        raise NotFileException(
            path=filename, type_name=str(os.stat(filename).st_mode)
        )
    return None


def send_file_to_hdfs(from_path: str, to_path: str):
    client = InsecureClient(URL, user="hadoop")
    if check_hdfs_file(to_path) is not None:
        client.delete(to_path)
    client.upload(to_path, from_path)


def send_file_from_hdfs(from_path: str, to_path: str):
    client = InsecureClient(URL, user="hadoop")
    client.download(from_path, to_path, overwrite=True)


def send_file(local_file, hdfs_file):
    try:
        hdfs_file_status = check_hdfs_file(hdfs_file)
        local_file_status = check_local_file(local_file)
        hdfs_file_timestamp: int = 0
        local_file_timestamp: int = 0
        if not hdfs_file_status:
            logging.log(APP_LOGGING_LEVEL, "\tHDFS file doesn't exist")
        else:
            hdfs_file_timestamp = hdfs_file_status["modificationTime"] / 1000
        if not local_file_status:
            logging.log(APP_LOGGING_LEVEL, "\tLocal file doesn't exist")
        else:
            local_file_timestamp = int(local_file_status.st_mtime)
        if not (hdfs_file_status or local_file_status):
            return logging.error("\tCan't locate any of the files, exiting...")
        logging.log(
            APP_LOGGING_LEVEL, "\tHDFS\tm_time=%d.", hdfs_file_timestamp
        )
        logging.log(
            APP_LOGGING_LEVEL, "\tLocal\tm_time=%d.", local_file_timestamp
        )
        if hdfs_file_timestamp > local_file_timestamp:
            send_file_from_hdfs(hdfs_file, local_file)
            logging.log(
                APP_LOGGING_LEVEL,
                "\tFile %s received from HDFS %s.",
                local_file,
                hdfs_file,
            )
        else:
            send_file_to_hdfs(local_file, hdfs_file)
            logging.log(
                APP_LOGGING_LEVEL,
                "\tFile %s sent to HDFS %s.",
                local_file,
                hdfs_file,
            )


    except NotFileException as exc:
        return logging.error(
            "\tFilepath %s already exists, type: %s (is not a file)",
            exc.path,
            exc.type_name,
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-local", help="Local filepath")
    parser.add_argument("-hdfs", help="HDFS filepath")
    args = parser.parse_args()
    send_file(args.local, args.hdfs)
