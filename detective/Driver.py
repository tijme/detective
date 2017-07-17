# -*- coding: utf-8 -*-

# MIT License
#
# Copyright (c) 2017 Tijme Gommers
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import colorlog

from requests_toolbelt import user_agent
from nyawc.QueueItem import QueueItem
from nyawc.Crawler import Crawler
from nyawc.CrawlerActions import CrawlerActions
from nyawc.http.Request import Request
from detective.helpers.PackageHelper import PackageHelper
from detective.Scanner import Scanner

class Driver:
    """The main Crawler class which handles the crawling recursion, queue and processes.

    Attributes:
        __args (:class:`argparse.Namespace`): A namespace with all the parsed CLI arguments.
        __options (:class:`nyawc.Options`): The options to use for the current crawling runtime.
        __vulnerable_items list(:class:`nyawc.http.Request`): A list of vulnerable items (if any).

    """

    def __init__(self, args, options):
        """Constructs a Driver instance. The driver instance manages the crawling proces.

        Args:
            args (:class:`argparse.Namespace`): A namespace with all the parsed CLI arguments.
            options (:class:`nyawc.Options`): The options to use for the current crawling runtime.

        """

        self.__args = args
        self.__options = options
        self.__vulnerable_items = []

        self.__options.callbacks.crawler_before_start = self.cb_crawler_before_start
        self.__options.callbacks.crawler_after_finish = self.cb_crawler_after_finish
        self.__options.callbacks.request_before_start = self.cb_request_before_start
        self.__options.callbacks.request_after_finish = self.cb_request_after_finish
        self.__options.callbacks.request_in_thread_after_finish = self.cb_request_in_thread_after_finish
        self.__options.callbacks.request_on_error = self.cb_request_on_error

        self.__options.identity.headers.update({
            "User-Agent": user_agent(PackageHelper.get_alias(), PackageHelper.get_version())
        })

    def start(self):
        """Start the crawler."""

        startpoint = Request(self.__args.domain)

        crawler = Crawler(self.__options)
        crawler.start_with(startpoint)

    def cb_crawler_before_start(self):
        """Called before the crawler starts crawling."""

        colorlog.getLogger().info("Detective scanner started.")

    def cb_crawler_after_finish(self, queue):
        """Crawler callback (called after the crawler finished).

        Args:
            queue (obj): The current crawling queue.

        """

        if queue.get_all(QueueItem.STATUS_CANCELLED):
            colorlog.getLogger().warning("Detective scanner finished (but some requests were cancelled).")
        else:
            colorlog.getLogger().info("Detective scanner finished.")

        if self.__vulnerable_items:
            colorlog.getLogger().success("Found " + str(len(self.__vulnerable_items)) + " endpoint(s) with interesting information.")
            colorlog.getLogger().success("Listing endpoint(s) with interesting information.")

            for vulnerable_item in self.__vulnerable_items:
                colorlog.getLogger().success(vulnerable_item.url)
        else:
            colorlog.getLogger().warning("Couldn't find any endpoints with interesting information.")


    def cb_request_before_start(self, queue, queue_item):
        """Crawler callback (called before a request starts).

        Args:
            queue (:class:`nyawc.Queue`): The current crawling queue.
            queue_item (:class:`nyawc.QueueItem`): The queue item that's about to start.

        Returns:
            str: A crawler action (either DO_SKIP_TO_NEXT, DO_STOP_CRAWLING or DO_CONTINUE_CRAWLING).

        """

        colorlog.getLogger().info("Investigating " + queue_item.request.url)

        if self.__vulnerable_items and self.__args.stop_if_vulnerable:
            return CrawlerActions.DO_STOP_CRAWLING

        return CrawlerActions.DO_CONTINUE_CRAWLING

    def cb_request_after_finish(self, queue, queue_item, new_queue_items):
        """Crawler callback (called after a request finished).

        Args:
            queue (:class:`nyawc.Queue`): The current crawling queue.
            queue_item (:class:`nyawc.QueueItem`): The queue item that was finished.
            new_queue_items list(:class:`nyawc.QueueItem`): The new queue items that were found in the one that finished.

        Returns:
            str: A crawler action (either DO_STOP_CRAWLING or DO_CONTINUE_CRAWLING).

        """

        self.__vulnerable_items.extend(queue_item.vulnerable_items)

        if self.__vulnerable_items and self.__args.stop_if_vulnerable:
            return CrawlerActions.DO_STOP_CRAWLING

        return CrawlerActions.DO_CONTINUE_CRAWLING

    def cb_request_on_error(self, queue_item, message):
        """Crawler callback (called when a request error occurs).

        Args:
            queue_item (:class:`nyawc.QueueItem`): The queue item that failed.
            message (str): The error message.

        """

        colorlog.getLogger().error(message)

    def cb_request_in_thread_after_finish(self, queue_item):
        """Crawler callback (called after a request finished).

        Args:
            queue_item (:class:`nyawc.QueueItem`): The queue item that's about to start.

        Note:
            This method gets called in the crawling thread and is therefore not thread safe.

        """

        queue_item.vulnerable_items = Scanner(queue_item).get_vulnerable_items()
