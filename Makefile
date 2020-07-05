fmt:
	isort -rc .
	black .
mod:
	python -m libcst.tool codemod constant_folding.ConvertConstantCommand --help
