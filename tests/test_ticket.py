from pathlib import Path
from playwright.sync_api import expect
from ultis.messages import IFRAME_STATUS_UPDATED, TOOLTIP_CREATED_DATE
import allure

_SAMPLE_PNG = Path(__file__).parent.parent / "test-data" / "sample.png"

@allure.feature("Ticket Feature")
@allure.link("https://bsv-nhungnguyen.github.io/bai_tap_17082026.html", name="Ticket Page")

class TestTicket:
    @allure.title("GD02.3-005: Search")
    def test_gd02_3_005_search_ticket_by_keyword(self, open_ticket_page):
        open_ticket_page.search_ticket("ログインできない")
        expect(open_ticket_page.ticket_rows()).to_have_count(1)
        expect(open_ticket_page.ticket_rows()).to_contain_text("ログインできない")

    
    @allure.title("GD02.6-02: Search bằng Enter")
    def test_gd02_6_02_search_ticket_by_enter(self, open_ticket_page):
        open_ticket_page.search_ticket_by_enter("ログインできない")
        expect(open_ticket_page.ticket_rows()).to_have_count(1)
        expect(open_ticket_page.ticket_rows()).to_contain_text("ログインできない")

    @allure.title("GD02.1-21: Mở drawer")
    def test_gd02_1_21_open_new_ticket_drawer(self, open_ticket_page):
        open_ticket_page.open_new_ticket_drawer()
        drawer = open_ticket_page.new_ticket_drawer()
        expect(drawer).to_be_visible()
        expect(drawer).to_be_in_viewport()
        expect(open_ticket_page.drawer_step1()).to_be_visible()

    @allure.title("GD02.2-001: Checkbox")
    def test_gd02_2_001_select_all_checkbox(self, open_ticket_page):
        open_ticket_page.select_all_tickets()
        expect(open_ticket_page.row_checkboxes()).to_have_count(10)
        for checkbox in open_ticket_page.row_checkboxes().all():
            expect(checkbox).to_be_checked()
        expect(open_ticket_page.bulk_action_bar()).to_be_visible()

    @allure.title("GD02.4-02: Dropdown")
    def test_gd02_4_02_filter_priority_high(self, open_ticket_page):
        open_ticket_page.filter_priority("高")
        expect(open_ticket_page.ticket_rows()).to_have_count(5)

    @allure.title("GD03.1-03: Dialog")
    def test_gd03_1_03_cancel_delete_ticket(self, open_ticket_page):
        open_ticket_page.cancel_delete_ticket("T-1001")
        expect(open_ticket_page.ticket_rows()).to_have_count(10)
        expect(open_ticket_page.page.get_by_text("T-1001")).to_be_visible()

    @allure.title("GD02.5-001: Hover")
    def test_gd02_5_001_show_created_date_tooltip(self, open_ticket_page):
        open_ticket_page.hover_created_date_help()
        expect(open_ticket_page.created_date_tooltip()).to_be_visible()
        expect(open_ticket_page.created_date_tooltip()).to_have_text(TOOLTIP_CREATED_DATE)

    @allure.title("GD02.7-01: Upload")
    def test_gd02_7_01_upload_png_file(self, open_ticket_page):
        _SAMPLE_PNG.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * (1024 * 1024 - 8))
        open_ticket_page.open_ticket_detail("T-1001")
        open_ticket_page.upload_attachment(str(_SAMPLE_PNG))
        expect(open_ticket_page.uploaded_file_name()).to_have_text("sample.png（1024KB）")
        expect(open_ticket_page.remove_file_button()).to_be_visible()

    @allure.title("GD03.3-04: New tab")
    def test_gd03_3_04_open_manual_new_tab(self, open_ticket_page):
        manual_tab = open_ticket_page.open_manual_tab()
        expect(manual_tab).to_have_url("https://playwright.dev/")

    @allure.title("GD03.2-01: iframe")
    def test_gd03_2_01_update_status_in_iframe(self, open_ticket_page):
        open_ticket_page.apply_iframe_status("対応中")
        expect(open_ticket_page.iframe_result()).to_have_text(IFRAME_STATUS_UPDATED)
        expect(open_ticket_page.ticket_rows()).to_have_count(10)
        expect(open_ticket_page.page.locator("#ticket_tbody")).not_to_contain_text("画面外には反映されません")     

    @allure.title("Others_07: Browser zoom")
    def test_others_07_browser_zoom(self, open_ticket_page):
        open_ticket_page.set_browser_zoom()
        expect(open_ticket_page.header()).to_be_in_viewport()
        expect(open_ticket_page.ticket_table()).to_be_in_viewport()
        open_ticket_page.open_ticket_detail("T-1001")
        expect(open_ticket_page.detail_dialog()).to_be_in_viewport()
        open_ticket_page.close_detail()
        open_ticket_page.open_new_ticket_drawer()
        expect(open_ticket_page.new_ticket_drawer()).to_be_in_viewport()