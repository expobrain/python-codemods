# Python codemods

This is a collection of codemods for Python packages basedon on [LibCST](https://github.com/Instagram/LibCST/).

- [Installation](#Installation)
- [Run the codemods](#Run_the_codemods)
- [Run the tests](#Run_the_tests)
- [wxPython 2.x to 4.x migrations](#wxPython)
  - [ColorToColourCommand](#ColorToColourCommand)
  - [ConstantsRenameCommand](#ConstantsRenameCommand)
  - [FixImportFromAdvCommand](#FixImportFromAdvCommand)
  - [FlexGridSizerCommand](#FlexGridSizerCommand)
  - [MenuAppendCommand](#MenuAppendCommand)
  - [ToolbarAddToolCommand](#ToolbarAddToolCommand)
  - [SizerAddCommand](#SizerAddCommand)
  - [ListCtrlInsertColumnCommand](#ListCtrlInsertColumnCommand)
  - [DeprecationWarningsCommand](#DeprecationWarningsCommand)
  - [MakeModalCommand](#MakeModalCommand)

## Installation

Codemods are based on [LibCST](https://github.com/Instagram/LibCST/), it will be installed by running:

```shell
pip install -r requirements.txt
```

## Run the codemods

To run the codemods a small shell script `mod` is provided for convenience:

```shell
./mod wxpython.ColorToColourCommand [<source_code_path>, ...]
```

## Run the tests

Tests are executed using [Pytest](https://docs.pytest.org/) which will be installed as dev requirements:

```shell
pip install -r requirements_dev.txt
pytest
```

## wxPython 2.x to 4.x migrations

These are codemods available to migrate from wxPython 2.8 to 4.x

### ColorToColourCommand

Converts calls to `wx.Color` into `wx.Colour`, i.e.:

```python
wx.Color(255, 255, 255)
```

into:

```python
wx.Colour(255, 255, 255)
```

### ConstantsRenameCommand

Renames constants not available anymore into their equivalent in wxPython 4.x, i.e.:

```python
wx.WXK_PRIOR
wx.WXK_NUMPAD_NEXT
wx.FILE_MUST_EXIST
```

into:

```python
wx.WXK_PAGEUP
wx.WXK_NUMPAD_PAGEDOWN
wx.FD_FILE_MUST_EXIST
```

### FixImportFromAdvCommand

Fix imports of symbols moved into the `wx.adv` package, i.e.:

```python
import wx

wx.DatePickerCtrl(...)
```

into:

```python
import wx.adv

wx.adv.DatePickerCtrl(...)
```

### FlexGridSizerCommand

`wx.FlexgridSizer` needs now at least 3 arguments and this codemod add the third one with the default value, i.e.:

```python
wx.FlexGridSizer(1, 0)
```

into:

```python
wx.FlexGridSizer(1, 0, 0)
```

### MenuAppendCommand

Renames keywords, like `help` into `helpString`, and renames the `wx.Menu.AppendItem` method into `wx.Menu.Append` if called with a single argument, i.e.:

```python
menu.AppendItem(menu_item)
menu.Append(
    help="",
    id=1,
    kind=wx.ITEM_NORMAL,
    text="Menu item",
)
```

into :

```python
menu.Append(menu_item)
menu.Append(
    helpString="",
    id=1,
    kind=wx.ITEM_NORMAL,
    item="Menu item",
)
```

### ToolbarAddToolCommand

Renames calls to `wx.Toolbar.DoAddTool` into `wx.Toolbar.AddTool`, i.e.:

```python
toolbar.DoAddTool(
    bitmap=my_bitmap,
    id=1,
    label="Toolbar tool"
)
```

into:

```python
toolbar.AddTool(
    bitmap=my_bitmap,
    toolId=1,
    label="Toolbar tool"
)
```

### SizerAddCommand

Renames calls to `wx.Sizer.AddWindow` into `wx.Sizer.Add`, i.e.:

```python
sizer.AddWindow(panel, 0, border=0, flag=wx.EXPAND)
```

into:

```python
sizer.Add(panel, 0, border=0, flag=wx.EXPAND)
```

### ListCtrlInsertColumnCommand

Renames calls to `wx.ListCtrl.InsertColumnInfo` into `wx.ListCtrl.InsertColumn`, i.e.:

```python
list_ctrl.InsertColumnInfo(0, info)
```

into:

```python
list_ctrl.InsertColumn(0, info)
```

### DeprecationWarningsCommand

Replaces all the deprecated symbols and methods with the eqivalent in wxPython 4.x, i.e.:

```python
wx.BitmapFromImage()
wx.DateTimeFromDMY(*args)
```

into :

```python
wx.Bitmap()
wx.DateTime.FromDMY(*args)
```

### MakeModalCommand

The `wx.Frame.MakeModal` method has been removed and wxPython 4.x suggest to use a modal dialog instead, however for previous code to continue to work this codemod adds an artigicial `MakeModal` method to any class which calls `self.MakeModal()` in the code, i.e.:

```python
class MyModal(wx.Frame):
    def __init__(self):
        super().__init__()

        self.MakeModal()
```

into:

```python
class MyModal(wx.Frame):
    def __init__(self):
        super().__init__()

        self.MakeModal()

    def MakeModal(self, modal=True):
        if modal and not hasattr(self, '_disabler'):
            self._disabler = wx.WindowDisabler(self)
        if not modal and hasattr(self, '_disabler'):
            del self._disabler
```
