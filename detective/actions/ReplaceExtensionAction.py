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

from detective.actions.BaseAction import BaseAction

class ReplaceExtensionAction(BaseAction):
    """Replace the extension of the given URL.

    Attributes:
        __old (str): The old extension (to replace)
        __new (str): The new extension

    """

    def __init__(self, old, new):
        """Constructs a ReplaceExtensionAction instance.

        Args:
            old (str): The old extension (to replace)
            new (str): The new extension

        """

        BaseAction.__init__(self)
        self.__old = old
        self.__new = new

    def get_action_items_derived(self):
        """Get new queue items based on this action.

        Returns:
            list(:class:`nyawc.QueueItem`): A list of possibly vulnerable queue items.

        """

        items = []

        extension = self.get_extension()

        if extension == self.__old:
            queue_item = self.get_item_copy()
            old_url = queue_item.request.url
            new_url = self.replace_extension(old_url, self.__new)
            queue_item.request.url = new_url
            items.append(queue_item)

        return items
