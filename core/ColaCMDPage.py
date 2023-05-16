from .ColaCMDMenu import MenuItemSet

class ColaCMDPage(MenuItemSet):
    def __init__(self, username="cola", is_page_dif_prefix=True) -> None:
        super().__init__(username, is_page_dif_prefix)

        self.meta_page = None


    def add_meta_page(self, name, **cmd_dict):
        if self.meta_page is None:
            self.meta_page = MenuItemSet("meta", is_page_dif_prefix=False)

        self.meta_page.add_menuAkeyfunc(name, **cmd_dict)
        self.add_menuAkeyfunc(
            "meta", 
            is_norm_show=False, 
            meta=["meta mode", self.meta_page.runloop]
        )


class PageTest(ColaCMDPage):
    def __init__(self, username="cola", is_page_dif_prefix=True) -> None:
        super().__init__(username, is_page_dif_prefix)

        self.add_menuAkeyfunc(
            "TEST1", 
            _1=["test1", self._keyfunc_none], 
            _2=["test2", self._keyfunc_none]
        )

        self.add_meta_page(
            "meta1", 
            _1=["meta1", self._keyfunc_none], 
        )

if __name__=="__main__":
    page = PageTest()
    page.runloop()

"""
python -m core.ColaCMDPage
"""