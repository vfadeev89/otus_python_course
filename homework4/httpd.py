import argparse
import logging
import os
import multiprocessing

from http_server.server import ThreadedServer


def parse_sys_args():
    parser = argparse.ArgumentParser(description="Simple http server")
    parser.add_argument("-i", "--host", dest="host", default="127.0.0.1")
    parser.add_argument("-p", "--port", dest="port", type=int, default=8080)
    parser.add_argument("-w", "--workers", dest="workers", type=int, default=10)
    parser.add_argument("-r", "--root", dest="document_root", default="")
    parser.add_argument("-l", "--log", dest="logging_file", default=None)
    return parser.parse_args()


def setup_logging(path_to_save=None):
    logging.basicConfig(format="[%(asctime)s] %(levelname).1s %(message)s",
                        datefmt="%Y.%m.%d %H:%M:%S",
                        filename=os.path.join(path_to_save),
                        filemode='a',
                        level=logging.INFO)
    return logging.getLogger(__name__)


def main(args):
    logger = setup_logging(args.logging_file)
    logger.info("Started with args: %s", args)

    processes = []
    try:
        for i in xrange(args.workers):
            server = ThreadedServer(args.host, args.port, os.path.realpath(args.document_root), logger)
            process = multiprocessing.Process(target=server.serve_forever)
            processes.append(process)
            process.start()
            logger.info("Server running on the process: {}, host: {}, port: {}".format(process.pid, args.host, args.port))
        for process in processes:
            process.join()
    except KeyboardInterrupt:
        for process in processes:
            if process:
                pid = process.pid
                logger.info("Trying to shutting down process {}".format(pid))
                process.terminate()
                logger.info("Process {} terminated".format(pid))


if __name__ == "__main__":
    main(parse_sys_args())
