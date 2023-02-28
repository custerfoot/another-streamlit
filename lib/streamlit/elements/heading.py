# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import TYPE_CHECKING, Optional, Union, cast

from typing_extensions import Literal

from streamlit.errors import StreamlitAPIException
from streamlit.proto.Heading_pb2 import Heading as HeadingProto
from streamlit.runtime.metrics_util import gather_metrics
from streamlit.string_util import clean_text
from streamlit.type_util import SupportsStr

if TYPE_CHECKING:
    from streamlit.delta_generator import DeltaGenerator

TITLE_TAG = "h1"
HEADER_TAG = "h2"
SUBHEADER_TAG = "h3"

Anchor = Optional[Union[str, Literal[False]]]


class HeadingMixin:
    @gather_metrics("header")
    def header(self, body: SupportsStr, anchor: Anchor = None) -> "DeltaGenerator":
        """Display text in header formatting.

        Parameters
        ----------
        body : str
            The text to display as Github-flavored Markdown. Syntax
            information can be found at: https://github.github.com/gfm.

            This also supports:

            * Emoji shortcodes, such as ``:+1:``  and ``:sunglasses:``.
              For a list of all supported codes,
              see https://share.streamlit.io/streamlit/emoji-shortcodes.

            * LaTeX expressions, by wrapping them in "$" or "$$" (the "$$"
              must be on their own lines). Supported LaTeX functions are listed
              at https://katex.org/docs/supported.html.

            * Colored text, using the syntax ``:color[text to be colored]``,
              where ``color`` needs to be replaced with any of the following
              supported colors: blue, green, orange, red, violet.

        anchor : str or False
            The anchor name of the header that can be accessed with #anchor
            in the URL. If omitted, it generates an anchor using the body.
            If False, the anchor is not shown in the UI.

        Examples
        --------
        >>> import streamlit as st
        >>>
        >>> st.header('This is a header')
        >>> st.header('A header with _italics_ :blue[colors] and emojis :sunglasses:')

        """
        header_proto = HeadingProto()
        marshall(header_proto, body=body, anchor=anchor, tag=HEADER_TAG)
        return self.dg._enqueue("heading", header_proto)

    @gather_metrics("subheader")
    def subheader(self, body: SupportsStr, anchor: Anchor = None) -> "DeltaGenerator":
        """Display text in subheader formatting.

        Parameters
        ----------
        body : str
            The text to display as Github-flavored Markdown. Syntax
            information can be found at: https://github.github.com/gfm.

            This also supports:

            * Emoji shortcodes, such as ``:+1:``  and ``:sunglasses:``.
              For a list of all supported codes,
              see https://share.streamlit.io/streamlit/emoji-shortcodes.

            * LaTeX expressions, by wrapping them in "$" or "$$" (the "$$"
              must be on their own lines). Supported LaTeX functions are listed
              at https://katex.org/docs/supported.html.

            * Colored text, using the syntax ``:color[text to be colored]``,
              where ``color`` needs to be replaced with any of the following
              supported colors: blue, green, orange, red, violet.

        anchor : str or False
            The anchor name of the header that can be accessed with #anchor
            in the URL. If omitted, it generates an anchor using the body.
            If False, the anchor is not shown in the UI.

        Examples
        --------
        >>> import streamlit as st
        >>>
        >>> st.subheader('This is a subheader')
        >>> st.subheader('A subheader with _italics_ :blue[colors] and emojis :sunglasses:')

        """
        subheader_proto = HeadingProto()
        marshall(subheader_proto, body=body, anchor=anchor, tag=SUBHEADER_TAG)
        return self.dg._enqueue("heading", subheader_proto)

    @gather_metrics("title")
    def title(self, body: SupportsStr, anchor: Anchor = None) -> "DeltaGenerator":
        """Display text in title formatting.

        Each document should have a single `st.title()`, although this is not
        enforced.

        Parameters
        ----------
        body : str
            The text to display as Github-flavored Markdown. Syntax
            information can be found at: https://github.github.com/gfm.

            This also supports:

            * Emoji shortcodes, such as ``:+1:``  and ``:sunglasses:``.
              For a list of all supported codes,
              see https://share.streamlit.io/streamlit/emoji-shortcodes.

            * LaTeX expressions, by wrapping them in "$" or "$$" (the "$$"
              must be on their own lines). Supported LaTeX functions are listed
              at https://katex.org/docs/supported.html.

            * Colored text, using the syntax ``:color[text to be colored]``,
              where ``color`` needs to be replaced with any of the following
              supported colors: blue, green, orange, red, violet.

        anchor : str or False
            The anchor name of the header that can be accessed with #anchor
            in the URL. If omitted, it generates an anchor using the body.
            If False, the anchor is not shown in the UI.

        Examples
        --------
        >>> import streamlit as st
        >>>
        >>> st.title('This is a title')
        >>> st.title('A title with _italics_ :blue[colors] and emojis :sunglasses:')

        """
        title_proto = HeadingProto()
        marshall(title_proto, body=body, anchor=anchor, tag=TITLE_TAG)
        return self.dg._enqueue("heading", title_proto)

    @property
    def dg(self) -> "DeltaGenerator":
        """Get our DeltaGenerator."""
        return cast("DeltaGenerator", self)


def marshall(
    heading_proto: HeadingProto,
    *,
    body,
    anchor: Union[None, str, Literal[False]],
    tag: str,
):
    """Marshall heading's data into proto."""
    if anchor is not None:
        if anchor is False:
            heading_proto.hide_anchor = True
        elif isinstance(anchor, str):
            heading_proto.anchor = anchor
        elif anchor is True:  # type: ignore
            raise StreamlitAPIException(
                "Anchor parameter has invalid value: %s. "
                "Supported values: None, any string or False" % anchor
            )
        else:
            raise StreamlitAPIException(
                "Anchor parameter has invalid type: %s. "
                "Supported values: None, any string or False" % type(anchor).__name__
            )

    heading_proto.body = clean_text(body)
    heading_proto.tag = tag
