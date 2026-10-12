from locators import TicketPageLocators as tk_locators
import allure

class TicketPage:
    def __init__(self, page):
        self.page = page

    def _panel(self):
        return self.page.locator(tk_locators.PANEL)

    def _search_input(self):
        return self._panel().get_by_role("textbox", name=tk_locators.SEARCH_INPUT)

    @allure.step("Search ticket: {keyword}")
    def search_ticket(self, keyword):
        self._search_input().fill(keyword)
        self._panel().get_by_role("button", name=tk_locators.BUTTON_SEARCH).click()

    @allure.step("Search ticket by Enter: {keyword}")
    def search_ticket_by_enter(self, keyword):
        self._search_input().fill(keyword)
        self._search_input().press("Enter")

    @allure.step("Get ticket rows")
    def ticket_rows(self):
        return self.page.locator(tk_locators.TICKET_ROWS)

    @allure.step("Open new ticket drawer")
    def open_new_ticket_drawer(self):
        self._panel().get_by_role("button", name=tk_locators.BUTTON_NEW_TICKET).click()

    @allure.step("Get new ticket drawer")
    def new_ticket_drawer(self):
        return self.page.get_by_role("dialog", name=tk_locators.DRAWER_TITLE)

    @allure.step("Get drawer step 1")
    def drawer_step1(self):
        return self.new_ticket_drawer().get_by_text(tk_locators.STEP1)
    
    @allure.step("Open notification tab")
    def open_notification_tab(self):
        self.page.locator(tk_locators.NAV_NOTIFICATIONS).click()
    
    @allure.step("Select all visible tickets")
    def select_all_tickets(self):
        self._panel().get_by_role("checkbox", name=tk_locators.SELECT_ALL).check(force=True)

    @allure.step("Get row checkboxes")
    def row_checkboxes(self):
        return self.page.locator(tk_locators.ROW_CHECKBOX)

    @allure.step("Get bulk action bar")
    def bulk_action_bar(self):
        return self.page.locator(tk_locators.BULK_BAR)

    @allure.step("Filter priority: {value}")
    def filter_priority(self, value):
        self._panel().get_by_role("combobox", name=tk_locators.PRIORITY_FILTER).select_option(value)

    def _ticket_row(self, ticket_id):
        return self.ticket_rows().filter(has_text=ticket_id)

    @allure.step("Cancel delete ticket: {ticket_id}")
    def cancel_delete_ticket(self, ticket_id):
        self.page.once("dialog", lambda dialog: dialog.dismiss())
        self._ticket_row(ticket_id).get_by_role("button", name=tk_locators.BUTTON_DELETE).click()

    @allure.step("Hover created date help")
    def hover_created_date_help(self):
        self.page.locator(tk_locators.CREATED_DATE_HELP).hover()

    @allure.step("Get created date tooltip")
    def created_date_tooltip(self):
        return self.page.locator(tk_locators.CREATED_DATE_TOOLTIP)

    @allure.step("Open ticket detail: {ticket_id}")
    def open_ticket_detail(self, ticket_id):
        self._ticket_row(ticket_id).get_by_role("button", name=tk_locators.BUTTON_DETAIL).click()

    @allure.step("Get detail dialog")
    def detail_dialog(self):
        return self.page.get_by_role("dialog", name=tk_locators.DETAIL_TITLE)
        
    @allure.step("Upload attachment: {file_path}")
    def upload_attachment(self, file_path):
        self.page.locator(tk_locators.FILE_INPUT).set_input_files(file_path)

    @allure.step("Get uploaded file name")
    def uploaded_file_name(self):
        return self.detail_dialog().locator(tk_locators.FILE_NAME)

    @allure.step("Get remove file button")
    def remove_file_button(self):
        return self.detail_dialog().get_by_role("button", name=tk_locators.BUTTON_REMOVE_FILE)

    @allure.step("Close detail dialog")
    def close_detail(self):
        self.detail_dialog().locator(tk_locators.BUTTON_CLOSE_DETAIL).click()

    @allure.step("Open manual in new tab")
    def open_manual_tab(self):
        with self.page.expect_popup() as popup:
            self.page.get_by_role("button", name=tk_locators.BUTTON_MANUAL).click()
        return popup.value

    def _preview_frame(self):
        return self.page.frame_locator(tk_locators.PREVIEW_FRAME)

    @allure.step("Apply iframe status: {status}")
    def apply_iframe_status(self, status):
        frame = self._preview_frame()
        frame.locator(tk_locators.FRAME_STATUS).select_option(label=status)
        frame.get_by_role("button", name=tk_locators.BUTTON_APPLY).click()

    @allure.step("Get iframe result")
    def iframe_result(self):
        return self._preview_frame().locator(tk_locators.FRAME_RESULT)

    @allure.step("Set browser zoom")
    def set_browser_zoom(self):
        size = self.page.viewport_size
        self.page.set_viewport_size({
            "width": int(size["width"] / 1.5),
            "height": int(size["height"] / 1.5),
        })

    @allure.step("Get header")
    def header(self):
        return self.page.locator(tk_locators.HEADER)

    @allure.step("Get ticket table")
    def ticket_table(self):
        return self.page.locator(tk_locators.TICKET_TABLE)