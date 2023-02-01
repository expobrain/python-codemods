from libcst.codemod import CodemodTest

from codemods.mypy import DefaultFunctionReturnTypeCommand


class ColorToColourCommandTests(CodemodTest):
    TRANSFORM = DefaultFunctionReturnTypeCommand

    def test_add_return_type_if_missing(self) -> None:
        before = "def f(): pass"
        after = "def f() -> None: pass"

        self.assertCodemod(before, after)

    def test_dont_add_return_type_if_present(self) -> None:
        before = "def f() -> None: pass"
        after = "def f() -> None: pass"

        self.assertCodemod(before, after)
