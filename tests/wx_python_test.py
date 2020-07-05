from libcst.codemod import CodemodTest

from codemods.wx_python import ColorToColourCommand


class ColorToColourCommandTests(CodemodTest):

    TRANSFORM = ColorToColourCommand

    def test_call_substitution(self) -> None:
        before = "wx.Color(255, 255, 255)"
        after = "wx.Colour(255, 255, 255)"

        self.assertCodemod(before, after)

    def test_reference_substitution(self) -> None:
        before = "isinstance(a, wx.Color)"
        after = "isinstance(a, wx.Colour)"

        self.assertCodemod(before, after)
