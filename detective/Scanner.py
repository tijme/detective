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

import requests

from nyawc.http.Handler import Handler as HttpHandler
from detective.actions.AppendToUrlAction import AppendToUrlAction
from detective.actions.TraverseInUrlAction import TraverseInUrlAction
from detective.actions.ReplaceExtensionAction import ReplaceExtensionAction

class Scanner:
    """The BaseAction can be used to create other actions.

    Attributes:
        actions list(:class:`detective.actions.BaseAction`): The actions to perform on the queue item.
        scanned_hashes list(str): A list of scanned queue item hashes.
        __queue_item (:class:`nyawc.QueueItem`): The queue item to perform actions on.

    """

    actions = [
        # Append to URL
        AppendToUrlAction(".DS_Store"),
        AppendToUrlAction("Thumbs.db"),
        AppendToUrlAction("error.log"),
        AppendToUrlAction("errors.log"),
        AppendToUrlAction("access.log"),
        AppendToUrlAction(".htaccess"),
        AppendToUrlAction(".htaccess.old"),
        AppendToUrlAction(".htaccess.bak"),
        AppendToUrlAction(".htpasswd"),
        AppendToUrlAction(".htpasswd.old"),
        AppendToUrlAction(".htpasswd.bak"),
        AppendToUrlAction("nginx.conf"),

        # Traverse in URL
        TraverseInUrlAction(".DS_Store"),
        TraverseInUrlAction("Thumbs.db"),
        TraverseInUrlAction("error.log"),
        TraverseInUrlAction("errors.log"),
        TraverseInUrlAction("access.log"),
        TraverseInUrlAction(".htaccess"),
        TraverseInUrlAction(".htaccess.old"),
        TraverseInUrlAction(".htaccess.bak"),
        TraverseInUrlAction(".htpasswd"),
        TraverseInUrlAction(".htpasswd.old"),
        TraverseInUrlAction(".htpasswd.bak"),
        TraverseInUrlAction("nginx.conf"),

        # Replace extension
        ReplaceExtensionAction(".jpg", ".jpg.old"),
        ReplaceExtensionAction(".php", ".php.old"),
        ReplaceExtensionAction(".php", ".php.bak"),
        ReplaceExtensionAction(".jsp", ".jsp.old"),
        ReplaceExtensionAction(".jsp", ".jsp.bak")
    ]

    scanned_hashes = []

    def __init__(self, queue_item):
        """Initialize a scanner for the given queue item.

        Args:
            queue_item (:class:`nyawc.QueueItem`): The queue item to scan.

        """

        self.__queue_item = queue_item

    def get_vulnerable_items(self):
        """Get a list of vulnerable queue items, if any.

        Returns:
            list(:class:`nyawc.QueueItem`): A list of vulnerable queue items.

        """

        results = []

        for action in self.actions:
            items = action.get_action_items(self.__queue_item)

            for item in items:
                if item.get_hash() in self.scanned_hashes:
                    continue

                self.scanned_hashes.append(item.get_hash())

                if self.is_item_vulnerable(item):
                    results.append(item)

        return results

    def is_item_vulnerable(self, queue_item):
        """Check if the given queue item is vulnerable by executing it using the HttpHandler.

        Args:
            queue_item (:class:`nyawc.QueueItem`): The queue item to check.

        Returns:
            bool: True if vulnerable, false otherwise.

        """

        try:
            handler = HttpHandler(None, queue_item)

            try:
                queue_item.response.raise_for_status()
            except Exception:
                return False

        except Exception:
            return False

        return True
