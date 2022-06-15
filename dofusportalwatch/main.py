import threading
import requests

import rumps
from lxml import html


UNKNOWN = "UNKNOWN"
DOFUS_PORTAL_APP_URL = "https://dofus-portals.fr/portails/2"

ENUTROSOR_XPATH_POSITION = "//*[@id='dim_list']/div[3]/div[2]/div/div/h3[1]/b/text()"
ENUTROSOR_XPATH_LEFT_ENTRIES = "//*[@id='dim_list']/div[3]/div[2]/div/div/h3[2]/b/font/text()"
ENUTROSOR_XPATH_LAST_UPDATE = "//*[@id='dim_list']/div[3]/div[5]/div/div/h3/text()"

ECAFLIPUS_XPATH_POSITION = "//*[@id='dim_list']/div[2]/div[2]/div/div/h3[1]/b/text()"
ECAFLIPUS_XPATH_LEFT_ENTRIES = "//*[@id='dim_list']/div[2]/div[2]/div/div/h3[2]/b/font/text()"
ECAFLIPUS_XPATH_LAST_UPDATE = "//*[@id='dim_list']/div[2]/div[5]/div/div/h3/text()"

SRAMBAD_XPATH_POSITION = "//*[@id='dim_list']/div[4]/div[2]/div/div/h3[1]/b/text()"
SRAMBAD_XPATH_LEFT_ENTRIES = "//*[@id='dim_list']/div[4]/div[2]/div/div/h3[2]/b/font/text()"
SRAMBAD_XPATH_LAST_UPDATE = "//*[@id='dim_list']/div[4]/div[5]/div/div/h3/text()"


class DofusPortalApp(rumps.App):
    def __init__(self) -> None:
        super(DofusPortalApp, self).__init__(name="Portal app", icon="icon/dofusportalwatch.jpg")

        self.enutrosor_item = rumps.MenuItem(
            "Enutrosor portal position: UNKNOWN, remaining entries: UNKNOWN, last update: UNKNOWN",
            icon="icon/enu.jpeg",
            callback=self.print_something
        )

        self.srambad_item = rumps.MenuItem(
            "Srambad portal position: UNKNOWN, remaining entries: UNKNOWN, last update: UNKNOWN",
            icon="icon/sram.jpeg",
            callback=self.print_something
        )

        self.ecaflipus_item = rumps.MenuItem(
            "Ecaflipus portal position: UNKNOWN, remaining entries: UNKNOWN, last update: UNKNOWN",
            icon="icon/eca.jpeg",
            callback=self.print_something
        )

        self.menu = [
            self.enutrosor_item,
            rumps.separator,
            self.srambad_item,
            rumps.separator,
            self.ecaflipus_item,
            rumps.separator
        ]

    def print_something(self):
        return ""

    @staticmethod
    def _get_dofus_portal_page_content() -> str:
        return requests.get(DOFUS_PORTAL_APP_URL).content

    @staticmethod
    def _transfrom_page_content_to_html_element_object(page_content: bytes) -> html.HtmlElement:
        return html.fromstring(page_content)

    @staticmethod
    def _get_position(parsed_html: html.HtmlElement, xpath_position: str) -> str:
        position = parsed_html.xpath(xpath_position)
        if position:
            return position[0]
        return UNKNOWN

    @staticmethod
    def _get_remaining_entries(parsed_html: html.HtmlElement, xpath_remaining_entries: str) -> str:
        remaining_entries = parsed_html.xpath(xpath_remaining_entries)
        if remaining_entries:
            return remaining_entries[0]
        return UNKNOWN

    @staticmethod
    def _get_last_update(parsed_html: html.HtmlElement, xpath_last_update: str) -> str:
        last_update = parsed_html.xpath(xpath_last_update)
        if last_update:
            return last_update[0]
        return UNKNOWN

    @staticmethod
    def render_enutrosor_title(enutrosor_position: str, enutrosor_left_entries: int, enutrosor_last_update: str) -> str:
        return f"Enutrosor pos {enutrosor_position}, left entries: {enutrosor_left_entries}, last update: {enutrosor_last_update}"

    @staticmethod
    def render_srambad_title(srambad_position: str, srambad_left_entries: int, srambad_last_update: str) -> str:
        return f"Srambad pos {srambad_position}, left entries: {srambad_left_entries}, last update: {srambad_last_update}"

    @staticmethod
    def render_ecaflipus_title(ecaflipus_position: str, ecaflipus_left_entries: int, ecaflipus_last_update: str) -> str:
        return f"Ecaflipus pos {ecaflipus_position}, left entries: {ecaflipus_left_entries}, last update: {ecaflipus_last_update}"

    def _update_enutrosor_title(self, html_element: html.HtmlElement) -> str:
        pos = self._get_position(html_element, ENUTROSOR_XPATH_POSITION)
        remaining_entries = self._get_remaining_entries(html_element, ENUTROSOR_XPATH_LEFT_ENTRIES)
        last_update = self._get_last_update(html_element, ENUTROSOR_XPATH_LAST_UPDATE)
        return self.render_enutrosor_title(pos, remaining_entries, last_update)

    def _update_srambad_title(self, html_element: html.HtmlElement) -> str:
        pos = self._get_position(html_element, SRAMBAD_XPATH_POSITION)
        remaining_entries = self._get_remaining_entries(html_element, SRAMBAD_XPATH_LEFT_ENTRIES)
        last_update = self._get_last_update(html_element, SRAMBAD_XPATH_LAST_UPDATE)
        return self.render_srambad_title(pos, remaining_entries, last_update)

    def _update_ecaflipus_title(self, html_element: html.HtmlElement) -> str:
        pos = self._get_position(html_element, ECAFLIPUS_XPATH_POSITION)
        remaining_entries = self._get_position(html_element, ECAFLIPUS_XPATH_LEFT_ENTRIES)
        last_update = self._get_last_update(html_element, ECAFLIPUS_XPATH_LAST_UPDATE)
        return self.render_ecaflipus_title(pos, remaining_entries, last_update)

    def _update(self) -> None:
        html_page_content = self._get_dofus_portal_page_content()
        parsed_html_body = self._transfrom_page_content_to_html_element_object(html_page_content)
        self.enutrosor_item.title = self._update_enutrosor_title(parsed_html_body)
        self.srambad_item.title = self._update_srambad_title(parsed_html_body)
        self.ecaflipus_item.title = self._update_ecaflipus_title(parsed_html_body)

    @rumps.clicked("Update now")
    def _update_now(self, _):
        self._update()

    @rumps.timer(600)
    def _update_async_portal(self, _):
        thread = threading.Thread(target=self._update)
        thread.start()


if __name__ == "__main__":
    app = DofusPortalApp()
    app.run()
