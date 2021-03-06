"""
test code for html_render.py

This is just a start -- you will need more tests!
"""

import io
import pytest

# import * is often bad form, but makes it easier to test everything in a module.
from html_render import *


# utility function for testing render methods
# needs to be used in multiple tests, so we write it once here.
def render_result(element, ind=""):
    """
    calls the element's render method, and returns what got rendered as a
    string
    """
    # the StringIO object is a "file-like" object -- something that
    # provides the methods of a file, but keeps everything in memory
    # so it can be used to test code that writes to a file, without
    # having to actually write to disk.
    outfile = io.StringIO()
    # this so the tests will work before we tackle indentation
    if ind:
        element.render(outfile, ind)
    else:
        element.render(outfile)
    return outfile.getvalue()

########
# Step 1
########

def test_init():
    """
    This only tests that it can be initialized with and without
    some content -- but it's a start
    """
    e = Element()

    e = Element("this is some text")


def test_append():
    """
    This tests that you can append text

    It doesn't test if it works --
    that will be covered by the render test later
    """
    e = Element("this is some text")
    e.append("some more text")


def test_render_element():
    """
    Tests whether the Element can render two pieces of text
    So it is also testing that the append method works correctly.

    It is not testing whether indentation or line feeds are correct.
    """
    e = Element("this is some text")
    e.append("and this is some more text")

    # This uses the render_results utility above
    file_contents = render_result(e).strip()

    # making sure the content got in there.
    assert("this is some text") in file_contents
    assert("and this is some more text") in file_contents

    # make sure it's in the right order
    assert file_contents.index("this is") < file_contents.index("and this")

    # making sure the opening and closing tags are right.
    assert file_contents.startswith("<html>")
    assert file_contents.endswith("</html>")


# Uncomment this one after you get the one above to pass
# Does it pass right away?
def test_render_element2():
    """
    Tests whether the Element can render two pieces of text
    So it is also testing that the append method works correctly.

    It is not testing whether indentation or line feeds are correct.
     """
    e = Element()
    e.append("this is some text")
    e.append("and this is some more text")

    # This uses the render_results utility above
    file_contents = render_result(e).strip()

    # making sure the content got in there.
    assert("this is some text") in file_contents
    assert("and this is some more text") in file_contents

    # make sure it's in the right order
    assert file_contents.index("this is") < file_contents.index("and this")

    # making sure the opening and closing tags are right.
    assert file_contents.startswith("<html>")
    assert file_contents.endswith("</html>")


# ########
# # Step 2
# ########

# tests for the new tags
def test_html():
    e = Html("this is some text")
    e.append("and this is some more text")

    file_contents = render_result(e).strip()

    assert("this is some text") in file_contents
    assert("and this is some more text") in file_contents
    print(file_contents)
    assert file_contents.endswith("</html>")


def test_body():
    e = Body("this is some text")
    e.append("and this is some more text")

    file_contents = render_result(e).strip()

    assert("this is some text") in file_contents
    assert("and this is some more text") in file_contents

    assert file_contents.startswith("<body>")
    assert file_contents.endswith("</body>")


def test_p():
    e = P("this is some text")
    e.append("and this is some more text")

    file_contents = render_result(e).strip()

    assert("this is some text") in file_contents
    assert("and this is some more text") in file_contents

    assert file_contents.startswith("<p>")
    assert file_contents.endswith("</p>")


def test_sub_element():
    """
    tests that you can add another element and still render properly
    """
    page = Html()
    page.append("some plain text.")
    page.append(P("A simple paragraph of text"))
    page.append("Some more plain text.")

    file_contents = render_result(page)
    print(file_contents) # so we can see it if the test fails

    # note: The previous tests should make sure that the tags are getting
    #       properly rendered, so we don't need to test that here.
    assert "some plain text" in file_contents
    assert "A simple paragraph of text" in file_contents
    assert "Some more plain text." in file_contents
    assert "some plain text" in file_contents
    # but make sure the embedded element's tags get rendered!
    assert "<p>" in file_contents
    assert "</p>" in file_contents

########
# Step 3
########

# test for new tags
def test_head():
    e = Head("this is some text")
    e.append("and this is some more text")

    file_contents = render_result(e).strip()

    assert("this is some text") in file_contents
    assert("and this is some more text") in file_contents

    assert file_contents.startswith("<head>")
    assert file_contents.endswith("</head>")


def test_OneLineTag():
    e = OneLineTag("this is some text")
    e.append("and this is some more text")

    file_contents = render_result(e).strip()

    assert("this is some text") in file_contents
    assert("and this is some more text") in file_contents

    assert file_contents.startswith("<OneLineTag>")
    assert file_contents.endswith("</OneLineTag>")


def test_title():
    e = Title("this is some text")
    e.append("and this is some more text")

    file_contents = render_result(e).strip()

    assert("this is some text") in file_contents
    assert("and this is some more text") in file_contents

    assert file_contents.startswith("<title>")
    assert file_contents.endswith("</title>")


# test overriden render method
def test_render_OneLineTag():
    e = OneLineTag("Render on one line please")

    file_contents = render_result(e).strip()
    print(file_contents)

    assert file_contents == ('<OneLineTag>Render on one line please</OneLineTag>')


# test new subclass structure
def test_title_sub_element():
    """
    tests that you can add another element for title and still render properly
    """
    page = Html()

    page_head = Head()
    page_head.append(Title("Python Class Sample Page"))

    page.append(page_head)
    page.append("some plain text.")
    page.append(P("A simple paragraph of text"))
    page.append("Some more plain text.")

    file_contents = render_result(page)
    print(file_contents)  # so we can see it if the test fails

    # note: The previous tests should make sure that the tags are getting
    #       properly rendered, so we don't need to test that here.
    assert "<title>Python Class Sample Page</title>" in file_contents
    assert "some plain text" in file_contents
    assert "A simple paragraph of text" in file_contents
    assert "Some more plain text." in file_contents
    assert "some plain text" in file_contents
    # but make sure the embedded element's tags get rendered!
    assert "<title>" in file_contents
    assert "</title>" in file_contents
    assert "<p>" in file_contents
    assert "</p>" in file_contents


########
# Step 4
########

# test adding attributes to render classes
def test_render_element_attr():
    """
    Tests whether the Element can render two pieces of text
    So it is also testing that the append method works correctly.

    Tests whether the attributes are added to the opening line

    It is not testing whether indentation or line feeds are correct.
    """
    e = P("Here is a paragraph of text -- there could be more of them, "
          "but this is enough  to show that we can do some text",
          style="text-align: center; font-style: oblique;")
    e.append(P('more and more text for fun'))

    # This uses the render_results utility above
    file_contents = render_result(e).strip()

    # make sure the properties are in the opening tag
    assert '<p style="text-align: center; font-style: oblique;">' in file_contents
    assert '</p>' in file_contents

    # make sure extra text did not get the attributes
    assert '<p>' in file_contents
    assert 'more and more text for fun' in file_contents

    # making sure the opening and closing tags are right.
    assert file_contents.endswith("</p>")


def test_multiple_attributes():
    e = P('some text', width=400, id="Boys", style="text-align:center")

    file_contents = render_result(e).strip()

    print(file_contents)

    # check all attributes in file
    assert 'width="400"' in file_contents
    assert 'id="Boys"' in file_contents
    assert 'style="text-align:center"' in file_contents

    # check for attribute order
    assert file_contents.index('width="400"') < file_contents.index('id="Boys"')


def test_render_OneLineTag_attr():
    e = Html('parent level')
    body_title = Title('Testing one line tag attributes', style="text-align: center")
    e.append(body_title)

    file_contents = render_result(e).strip()

    # in case the test fails
    print(file_contents)

    # test that attributes are there all in one line
    assert '<title style="text-align: center">Testing one line tag attributes</title>' in file_contents

    # test start and ending tags
    assert file_contents.startswith("<!DOCTYPE html>")
    assert file_contents.endswith("</html>")


########
# Step 5
########

def test_render_SelfClosingTag():
    e = SelfClosingTag(width=400)

    file_contents = render_result(e).strip()

    assert 'width="400"' in file_contents
    assert '<SelfClosingTag width="400" />' in file_contents

def test_Hr_class():
    e = Hr(width=400)

    file_contents = render_result(e).strip()

    assert e.tag == 'Hr'
    assert '<Hr width="400" />' in file_contents

########
# Step 6
########

# test anchor element

def test_initialization_type_A():
    e = A("http://google.com", "link to google")

    print(e.attributes)

    assert e.tag == 'a'
    assert e.attributes == {'href': "http://google.com"}
    assert "link to google" in e.content_list

    file_contents = render_result(e).strip()

    print(file_contents)

    assert '<a href="http://google.com">link to google</a>' in file_contents

########
# Step 7
########

# test Unorder list Ul
def test_ul_li_tags():
    e = Ul('Unordered list')

    el = Li('List element')

    # routine tag check
    assert e.tag == 'Ul'
    assert el.tag == 'Li'

    file_contents = render_result(e).strip()

    # routine content check
    assert 'Unordered list' in file_contents

    file_contents = render_result(el).strip()

    assert 'List element' in file_contents

# test header class
def test_header():
    e = H(2, 'test header class')

    # routine checks
    assert e.tag == 'h2'

    file_contents = render_result(e).strip()

    assert 'test header class' in file_contents


########
# Step 8
########

# test doctype tag
def test_doctype():
    e = Html('testing doctype')

    file_contents = render_result(e).strip()

    assert file_contents.startswith('<!DOCTYPE html>')
    assert file_contents.endswith('</html>')
    assert '<html>' in file_contents
    assert file_contents.index('<html>') < file_contents.index('testing doctype')


# test meta clas
def test_meta():
    e = Meta(charset="UTF-8")

    assert e.tag == 'meta'

    file_contents = render_result(e).strip()

    assert 'charset="UTF-8"' in file_contents


#####################
# indentation testing
#  Uncomment for Step 9 -- adding indentation
#####################


def test_indent():
    """
    Tests that the indentation gets passed through to the renderer
    """
    html = Html("some content")
    file_contents = render_result(html, ind="   ").rstrip()  #remove the end newline

    print(file_contents)
    lines = file_contents.split("\n")
    assert lines[0].startswith("   <")
    print(repr(lines[-1]))
    assert lines[-1].startswith("   <")


def test_indent_contents():
    """
    The contents in a element should be indented more than the tag
    by the amount in the indent class attribute
    """
    html = Element("some content")
    file_contents = render_result(html, ind="")

    print(file_contents)
    lines = file_contents.split("\n")
    assert lines[1].startswith(Element.indent)


def test_multiple_indent():
    """
    make sure multiple levels get indented fully
    """
    body = Body()
    body.append(P("some text"))
    html = Html(body)

    file_contents = render_result(html)

    print(file_contents)
    lines = file_contents.split("\n")
    for i in range(3):  # this needed to be adapted to the <DOCTYPE> tag
        assert lines[i + 1].startswith(i * Element.indent + "<")

    assert lines[4].startswith(3 * Element.indent + "some")


def test_element_indent1():
    """
    Tests whether the Element indents at least simple content

    we are expecting to to look like this:

    <html>
        this is some text
    </html>

    More complex indentation should be tested later.
    """
    e = Element("this is some text")

    # This uses the render_results utility above
    file_contents = render_result(e).strip()

    # making sure the content got in there.
    assert("this is some text") in file_contents

    # break into lines to check indentation
    lines = file_contents.split('\n')
    # making sure the opening and closing tags are right.
    assert lines[0] == "<html>"
    # this line should be indented by the amount specified
    # by the class attribute: "indent"
    assert lines[1].startswith(Element.indent + "thi")
    assert lines[2] == "</html>"
    assert file_contents.endswith("</html>")
