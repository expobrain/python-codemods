from libcst.codemod import CodemodTest

from codemods.wx_python_2_to_4.colour_to_color import ColourToColorCommand


class ColourToColorCommandTests(CodemodTest):

    TRANSFORM = ColourToColorCommand

    def test_no_op(self) -> None:
        before = "wx.Colur(255, 255, 255)"
        after = "wx.Colur(255, 255, 255)"

        self.assertCodemod(before, after)

    def test_substitution(self) -> None:
        before = "wx.Colour(255, 255, 255)"
        after = "wx.Color(255, 255, 255)"

        self.assertCodemod(before, after)
