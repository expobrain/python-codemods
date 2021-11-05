import libcst as cst
from libcst import matchers
from libcst.codemod import VisitorBasedCodemodCommand


class DefaultFunctionReturnTypeCommand(VisitorBasedCodemodCommand):

    DESCRIPTION = "Adds a default return type of None for functions without a return type"

    matcher = matchers.FunctionDef(returns=None)

    def leave_FunctionDef(
        self, original_node: cst.FunctionDef, updated_node: cst.FunctionDef
    ) -> cst.FunctionDef:
        if matchers.matches(updated_node, self.matcher):
            return updated_node.with_changes(returns=cst.Annotation(cst.Name(value="None")))

        return updated_node
