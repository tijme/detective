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

from nyawc.QueueItem import QueueItem
from nyawc.Crawler import Crawler
from nyawc.CrawlerActions import CrawlerActions
from nyawc.http.Request import Request
from detective.helpers.PackageHelper import PackageHelper
from requests_toolbelt import user_agent

class Driver:

    def __init__(self, args, options):
        self.args = args
        self.options = options

        self.options.identity.headers.update({
            "User-Agent": user_agent(PackageHelper.get_alias(), PackageHelper.get_version())
        })

        self.options.callbacks.crawler_before_start = self.cb_crawler_before_start
        self.options.callbacks.crawler_after_finish = self.cb_crawler_after_finish
        self.options.callbacks.request_before_start = self.cb_request_before_start
        self.options.callbacks.request_after_finish = self.cb_request_after_finish

    def start(self):
        startpoint = Request(self.args.domain)

        crawler = Crawler(self.options)
        crawler.start_with(startpoint)

    def cb_crawler_before_start(self):
        colorlog.getLogger().info("Crawler started.")

    def cb_crawler_after_finish(self, queue):
        colorlog.getLogger().info("Crawler finished.")
        colorlog.getLogger().info("Found " + str(queue.count_finished) + " requests.")

    def cb_request_before_start(self, queue, queue_item):
        vulnerable = False

        if vulnerable:
            if self.args.stop_if_vulnerable:
                return CrawlerActions.DO_STOP_CRAWLING

        return CrawlerActions.DO_CONTINUE_CRAWLING

    def cb_request_after_finish(self, queue, queue_item, new_queue_items):

        return CrawlerActions.DO_CONTINUE_CRAWLING
