# Automation Framework — Sauce Demo (Playwright + POM)

Framework tự động hóa kiểm thử (Automation Test) cho website thương mại điện tử demo [Sauce Demo](https://www.saucedemo.com/).

Framework được xây dựng bằng **Python**, sử dụng **Playwright** để điều khiển trình duyệt, **Pytest** để chạy test, **Allure** để tạo báo cáo, và mô hình **Page Object Model (POM)** để tổ chức code.

---

## Mục lục

1. [Framework dùng để làm gì?](#1-framework-dùng-để-làm-gì)
2. [Cấu trúc thư mục](#2-cấu-trúc-thư-mục)
3. [Giải thích chi tiết từng file](#3-giải-thích-chi-tiết-từng-file)
4. [Page Object Model (POM) là gì?](#4-page-object-model-pom-là-gì)
5. [Danh sách Test Case](#5-danh-sách-test-case)
6. [Cài đặt môi trường](#6-cài-đặt-môi-trường)
7. [Cách chạy test](#7-cách-chạy-test)
8. [Cách xem báo cáo Allure](#8-cách-xem-báo-cáo-allure)
9. [Cách thêm Test Data](#9-cách-thêm-test-data)
10. [Best Practices đã áp dụng](#10-best-practices-đã-áp-dụng)
11. [Hướng dẫn mở rộng framework](#11-hướng-dẫn-mở-rộng-framework)

---

## 1. Framework dùng để làm gì?

Thay vì tester phải **mở trình duyệt → click → nhập liệu → kiểm tra kết quả** bằng tay mỗi lần, framework sẽ **tự động** thực hiện các thao tác đó và báo cáo Pass/Fail.

**Ví dụ thực tế:** Test "Login thành công" sẽ tự động:
1. Mở trình duyệt Chrome
2. Vào trang https://www.saucedemo.com/
3. Nhập username và password
4. Click nút Login
5. Kiểm tra có chuyển sang trang Products hay không
6. Chụp ảnh màn hình và ghi vào báo cáo

---

## 2. Cấu trúc thư mục

```
playwright-pom/
│
├── conftest.py              # Cấu hình chung: mở browser, fixture, screenshot Allure
├── locators.py              # Danh sách vị trí element trên website (selector)
├── pytest.ini               # Cấu hình Pytest (thư mục test, Allure output)
├── requirements.txt         # Danh sách thư viện Python cần cài
├── run_tests.sh             # Script chạy test nhanh (dành cho Linux/Mac)
├── .env                     # Biến môi trường (URL website — không commit lên git)
│
├── pages/                   # PAGE OBJECT — mỗi màn hình website = 1 file
│   ├── login_page.py        #   Hành vi trang Login
│   ├── product_page.py      #   Hành vi trang Product / Product Detail
│   └── cart_page.py         #   Hành vi trang Cart
│
├── tests/                   # TEST CASE — kịch bản kiểm thử
│   ├── test_login.py        #   4 test Login (đọc data từ JSON)
│   ├── test_login_csv.py    #   Test Login data-driven (đọc data từ CSV)
│   ├── test_product.py      #   2 test Product
│   └── test_cart.py         #   2 test Cart
│
├── test-data/               # DỮ LIỆU TEST — tách riêng khỏi code
│   ├── users.json           #   User login dạng JSON
│   └── users.csv            #   User login dạng CSV
│
├── ultis/                   # TIỆN ÍCH dùng chung
│   ├── data_reader.py       #   Hàm đọc file JSON / CSV
│   └── messages.py          #   Các thông báo lỗi trên website
│
├── allure-results/          # Kết quả test thô (tự sinh khi chạy pytest)
├── allure-report/           # Báo cáo HTML (tự sinh sau khi chạy allure generate)
└── venv/                    # Môi trường Python ảo (cài thư viện tại đây)
```

---

## 3. Giải thích chi tiết từng file

### 3.1. File cấu hình (ở thư mục gốc)

#### `conftest.py` — "Trợ lý" chuẩn bị trước mỗi test

| Thành phần | Ý nghĩa (dễ hiểu) |
|---|---|
| `load_dotenv('.env')` | Đọc file `.env` để lấy URL website |
| Fixture `page` | Tự mở trình duyệt Chrome trước mỗi test, tự đóng sau khi test xong |
| Fixture `open_login_page` | Mở browser + vào trang Login, trả về sẵn `LoginPage` cho test dùng |
| Fixture `open_product_page` | Mở browser + Login thành công + vào trang Products, trả về `ProductPage` |
| Hook `pytest_runtest_makereport` | Sau mỗi test, tự chụp screenshot gắn vào báo cáo Allure |

**Fixture là gì?** Giống như "combo chuẩn bị sẵn". Test không cần tự mở browser hay login — chỉ cần khai báo tên fixture là có sẵn màn hình tương ứng.

---

#### `locators.py` — "Bản đồ" vị trí element trên website

Lưu **selector** (địa chỉ element trên trang web). Khi website đổi giao diện, chỉ cần sửa ở đây.

| Class | Màn hình | Ví dụ locator |
|---|---|---|
| `LoginPageLocators` | Trang Login | `#user-name`, `#password`, `#login-button` |
| `ProductPageLocators` | Trang danh sách sản phẩm | `[data-test='inventory-item']` |
| `ProductDetailPageLocators` | Trang chi tiết sản phẩm | `[data-test='inventory-item-name']` |
| `CartPageLocators` | Trang giỏ hàng | `[data-test='shopping-cart-badge']` |

**Ví dụ dễ hiểu:** `#user-name` giống như "số nhà" của ô nhập Username trên website. Code cần biết "số nhà" mới tìm đúng ô để điền text.

---

#### `pytest.ini` — Cấu hình Pytest

```ini
[pytest]
addopts = --alluredir=allure-results --clean-alluredir
testpaths = tests
```

- `testpaths = tests` → Pytest chỉ tìm test trong folder `tests/`
- `--alluredir=allure-results` → Tự lưu kết quả cho Allure report
- `--clean-alluredir` → Xóa kết quả cũ trước mỗi lần chạy

---

#### `requirements.txt` — Thư viện cần cài

| Thư viện | Vai trò |
|---|---|
| `pytest` | Engine chạy test |
| `playwright` | Điều khiển trình duyệt (click, fill, navigate) |
| `pytest-playwright` | Tích hợp Playwright với Pytest |
| `allure-pytest` | Tạo báo cáo Allure |
| `python-dotenv` | Đọc file `.env` |

---

#### `.env` — Cấu hình môi trường

```
BASE_URL=https://www.saucedemo.com/
```

Chứa URL website cần test. **Không commit file này lên git** (đã nằm trong `.gitignore`).

> **Lưu ý:** Username/password login đã chuyển sang `test-data/users.json` thay vì lưu trong `.env`.

---

#### `run_tests.sh` — Script chạy test (Linux/Mac)

Chạy toàn bộ test → generate Allure report → mở report trong browser.

Trên **Windows**, dùng lệnh PowerShell ở [Mục 7](#7-cách-chạy-test).

---

### 3.2. Folder `pages/` — Page Object (hành vi từng màn hình)

Mỗi file = **1 màn hình** trên website. Chứa các **hành động** người dùng có thể làm trên màn hình đó.

#### `pages/login_page.py` — Trang Login

| Method | Hành động tương ứng |
|---|---|
| `input_username(username)` | Nhập username vào ô Username |
| `input_password(password)` | Nhập password vào ô Password |
| `click_login_button()` | Click nút Login |
| `login(username, password)` | Gộp 3 bước trên (nhập user → nhập pass → click Login) |
| `error_message()` | Lấy element hiển thị thông báo lỗi |

#### `pages/product_page.py` — Trang Product & Product Detail

| Method | Hành động tương ứng |
|---|---|
| `inventory_container()` | Lấy vùng chứa danh sách sản phẩm |
| `page_title()` | Lấy tiêu đề trang ("Products") |
| `product_items()` | Lấy danh sách tất cả sản phẩm |
| `open_backpack_detail()` | Click vào sản phẩm "Sauce Labs Backpack" |
| `detail_product_name()` | Lấy tên sản phẩm ở trang chi tiết |
| `add_backpack_to_cart()` | Click nút "Add to cart" cho Backpack |

#### `pages/cart_page.py` — Trang Cart

| Method | Hành động tương ứng |
|---|---|
| `cart_badge()` | Lấy số hiển thị trên icon giỏ hàng |
| `open_cart()` | Click icon giỏ hàng → vào trang Cart |
| `cart_items()` | Lấy danh sách sản phẩm trong giỏ |
| `remove_backpack()` | Click nút "Remove" để xóa Backpack khỏi giỏ |

---

### 3.3. Folder `tests/` — Test Case (kịch bản kiểm thử)

Mỗi file test = **1 module chức năng**. Test **không chứa locator** — chỉ gọi method từ Page Object và kiểm tra kết quả.

#### `tests/test_login.py` — Module Login (JSON)

| Test Case | Mô tả | Data key (JSON) |
|---|---|---|
| TC_LOGIN_001 | Login thành công → vào trang Products | `validUser` |
| TC_LOGIN_002 | Login sai password → hiện lỗi | `invalidPassword` |
| TC_LOGIN_003 | Login sai username → hiện lỗi | `invalidUsername` |
| TC_LOGIN_004 | Login để trống → hiện lỗi bắt buộc nhập | `emptyFields` |

#### `tests/test_login_csv.py` — Module Login (CSV, data-driven)

Chạy **9 kịch bản** tự động từ file `users.csv` — mỗi dòng CSV = 1 test.

#### `tests/test_product.py` — Module Product

| Test Case | Mô tả |
|---|---|
| TC_PRODUCT_001 | Hiển thị danh sách 6 sản phẩm |
| TC_PRODUCT_002 | Click sản phẩm → xem trang chi tiết |

#### `tests/test_cart.py` — Module Cart

| Test Case | Mô tả |
|---|---|
| TC_CART_001 | Add Backpack vào cart → badge hiện số "1" |
| TC_CART_002 | Remove Backpack khỏi cart → giỏ trống |

---

### 3.4. Folder `test-data/` — Dữ liệu test

Tách data ra khỏi code để:
- Sửa data **không cần sửa code test**
- QA/Business có thể chỉnh data bằng Excel (CSV) hoặc Notepad (JSON)

#### `test-data/users.json`

```json
{
  "validUser": {
    "username": "standard_user",
    "password": "secret_sauce"
  }
}
```

Mỗi key (ví dụ `validUser`) = 1 bộ username/password cho 1 kịch bản test.

#### `test-data/users.csv`

```csv
test_case,username,password,expected_result
validUser,standard_user,secret_sauce,success
invalidPassword,standard_user,wrong_password,login_failed
```

Mỗi **dòng** = 1 kịch bản test. Cột `expected_result` cho biết kết quả mong đợi.

---

### 3.5. Folder `ultis/` — Tiện ích dùng chung

#### `ultis/data_reader.py` — Đọc file JSON / CSV

| Hàm | Chức năng |
|---|---|
| `get_user_from_json("validUser")` | Lấy 1 user từ `users.json` theo tên key |
| `get_users_from_csv()` | Lấy toàn bộ danh sách user từ `users.csv` |

#### `ultis/messages.py` — Thông báo lỗi trên website

```python
ERROR_LOGIN_FAILED = "Epic sadface: Username and password do not match..."
ERROR_USERNAME_REQUIRED = "Epic sadface: Username is required"
```

Dùng để assert (kiểm tra) message lỗi hiển thị đúng — tránh hardcode text trực tiếp trong test.

---

## 4. Page Object Model (POM) là gì?

### 4.1. Vấn đề khi KHÔNG dùng POM

Tất cả code (selector, thao tác, kiểm tra) viết chung trong 1 file test:

```
Test file
├── "#user-name"          ← selector hardcode
├── page.fill(...)        ← thao tác UI
├── page.click(...)       ← thao tác UI
└── expect(...)           ← kiểm tra kết quả
```

**Hậu quả:** Website đổi 1 button → phải sửa **tất cả** test file có dùng button đó.

---

### 4.2. Giải pháp POM — tách thành 3 lớp

```
┌─────────────────────────────────────────────────────────┐
│  tests/test_login.py          ← Lớp TEST               │
│  "Login thành công → thấy trang Products"              │
│  Chỉ mô tả KỊCH BẢN, không biết selector               │
└──────────────────────┬──────────────────────────────────┘
                       │ gọi method
┌──────────────────────▼──────────────────────────────────┐
│  pages/login_page.py          ← Lớp PAGE OBJECT        │
│  login(username, password)                              │
│  Mô tả HÀNH VI trên màn hình                            │
└──────────────────────┬──────────────────────────────────┘
                       │ dùng locator
┌──────────────────────▼──────────────────────────────────┐
│  locators.py                  ← Lớp LOCATOR            │
│  INPUT_USERNAME = "#user-name"                          │
│  Mô tả VỊ TRÍ element trên website                      │
└─────────────────────────────────────────────────────────┘
```

### 4.3. Ví dụ cụ thể trong project

**Test (WHAT — kiểm tra cái gì):**
```python
user = get_user_from_json("validUser")
open_login_page.login(user["username"], user["password"])
expect(open_login_page.page).to_have_url(".../inventory.html")
```

**Page Object (HOW — làm thế nào):**
```python
def login(self, username, password):
    self.input_username(username)
    self.input_password(password)
    self.click_login_button()
```

**Locator (WHERE — ở đâu trên trang):**
```python
INPUT_USERNAME = "#user-name"
BUTTON_LOGIN = "#login-button"
```

### 4.4. Lợi ích POM

| Lợi ích | Giải thích |
|---|---|
| Dễ bảo trì | Website đổi selector → chỉ sửa `locators.py` |
| Tái sử dụng | `login()` dùng chung cho Login, Product, Cart test |
| Dễ đọc | Test đọc như kịch bản tiếng Việt/Anh, không lẫn code kỹ thuật |
| Tách biệt trách nhiệm | Dev sửa Page Object, QA viết Test Case |

### 4.5. Quy tắc POM trong project này

- Mỗi màn hình = 1 Page Object (`LoginPage`, `ProductPage`, `CartPage`)
- **Không viết locator trực tiếp trong test case**
- Test data tách ra `test-data/`, không hardcode trong test
- Mỗi test **độc lập** — tự login, tự chuẩn bị data, không phụ thuộc test khác

---

## 5. Danh sách Test Case

| Module | TC | Tên | File |
|---|---|---|---|
| Login | TC_LOGIN_001 | Login thành công | `test_login.py` |
| Login | TC_LOGIN_002 | Login sai password | `test_login.py` |
| Login | TC_LOGIN_003 | Login sai username | `test_login.py` |
| Login | TC_LOGIN_004 | Login để trống dữ liệu | `test_login.py` |
| Login | TC_LOGIN_CSV | Login data-driven (9 cases) | `test_login_csv.py` |
| Product | TC_PRODUCT_001 | Hiển thị danh sách sản phẩm | `test_product.py` |
| Product | TC_PRODUCT_002 | Xem chi tiết sản phẩm | `test_product.py` |
| Cart | TC_CART_001 | Add product vào cart | `test_cart.py` |
| Cart | TC_CART_002 | Remove product khỏi cart | `test_cart.py` |

**Tổng: 12 test cases** (8 test riêng lẻ + 9 test CSV data-driven)

---

## 6. Cài đặt môi trường

### Yêu cầu

- Python 3.10 trở lên
- Git
- Allure CLI (để xem báo cáo)

### Các bước cài đặt

```powershell
# 1. Clone project
git clone <repo-url>
cd playwright-pom

# 2. Tạo virtual environment
python -m venv venv

# 3. Kích hoạt venv (Windows)
.\venv\Scripts\activate

# 4. Cài thư viện Python
pip install -r requirements.txt

# 5. Cài trình duyệt cho Playwright
playwright install

# 6. Tạo file .env
# Tạo file .env trong thư mục gốc với nội dung:
# BASE_URL=https://www.saucedemo.com/
```

---

## 7. Cách chạy test

> Tất cả lệnh chạy trong thư mục `playwright-pom`, với venv đã activate.

### Chạy toàn bộ test

```powershell
pytest -v
```

### Chạy theo module

```powershell
pytest tests/test_login.py -v
pytest tests/test_product.py -v
pytest tests/test_cart.py -v
pytest tests/test_login_csv.py -v
```

### Chạy 1 test case cụ thể

```powershell
pytest tests/test_login.py::TestLogin::test_login_success -v
pytest tests/test_product.py::TestProduct::test_display_product_list -v
pytest tests/test_cart.py::TestCart::test_add_product_to_cart -v
```

### Chạy test theo tên (keyword)

```powershell
pytest -k "login_success" -v
pytest -k "cart" -v
```

---

## 8. Cách xem báo cáo Allure

### Bước 1: Chạy test (kết quả tự lưu vào `allure-results/`)

```powershell
pytest -v
```

### Bước 2: Mở báo cáo

```powershell
allure serve allure-results
```

Lệnh trên sẽ tự mở browser hiển thị report với:
- Tổng số Pass / Fail
- Screenshot từng test
- Các bước thực hiện (Allure Steps)
- Thời gian chạy từng test

### Hoặc generate file HTML tĩnh

```powershell
allure generate allure-results -o allure-report --clean
start allure-report\index.html
```

---

## 9. Cách thêm Test Data

### 9.1. Thêm user mới qua JSON

**Bước 1:** Mở `test-data/users.json`, thêm key mới:

```json
{
  "validUser": { "username": "standard_user", "password": "secret_sauce" },
  "myNewUser": { "username": "problem_user", "password": "secret_sauce" }
}
```

**Bước 2:** Dùng trong test:

```python
user = get_user_from_json("myNewUser")
open_login_page.login(user["username"], user["password"])
```

---

### 9.2. Thêm user mới qua CSV

**Bước 1:** Mở `test-data/users.csv`, thêm 1 dòng:

```csv
test_case,username,password,expected_result
myNewCase,problem_user,secret_sauce,success
```

**Bước 2:** Test CSV tự chạy thêm 1 case (không cần sửa code test) — vì `test_login_csv.py` dùng `@pytest.mark.parametrize` đọc toàn bộ file CSV.

**Bước 3:** Nếu `expected_result` mới, thêm nhánh xử lý trong `test_login_csv.py`:

```python
elif user["expected_result"] == "ten_ket_qua_moi":
    # assert tương ứng
```

---

### 9.3. Phân biệt JSON vs CSV — khi nào dùng gì?

| | JSON | CSV |
|---|---|---|
| Ai sửa | Developer / Automation Engineer | QA, Business Analyst |
| Công cụ sửa | VS Code, Notepad | Excel, Google Sheets |
| Dùng khi | Test case cố định, cấu trúc phức tạp | Nhiều data, data-driven test |
| Trong project | `test_login.py` | `test_login_csv.py` |

---

## 10. Best Practices đã áp dụng

### Test độc lập (Independent Tests)

Mỗi test **tự chuẩn bị** trạng thái ban đầu — không phụ thuộc test khác.

```
TC_LOGIN_002 không cần TC_LOGIN_001 chạy trước
TC_CART_002 tự login + add product + remove (không dùng kết quả TC_CART_001)
```

Fixture `open_product_page` tự login mỗi lần → Product/Cart test luôn bắt đầu từ trang Products sạch.

---

### Smart Wait (chờ thông minh)

| Không dùng | Dùng thay thế |
|---|---|
| `time.sleep(5)` — chờ cứng 5 giây | `expect(locator).to_be_visible()` — chờ đến khi element hiện |
| | `expect(page).to_have_url(...)` — chờ đến khi chuyển trang |

Playwright tự retry cho đến khi điều kiện đúng hoặc hết timeout — test **nhanh hơn và ổn định hơn** sleep cứng.

---

### Tách biệt trách nhiệm

| Thư mục / File | Trách nhiệm |
|---|---|
| `locators.py` | Biết element **ở đâu** |
| `pages/` | Biết **làm gì** trên màn hình |
| `tests/` | Biết **kiểm tra gì** |
| `test-data/` | Biết **dùng data nào** |
| `ultis/messages.py` | Biết **message nào** cần assert |
| `conftest.py` | Biết **chuẩn bị môi trường** thế nào |

---

## 11. Hướng dẫn mở rộng framework

### Thêm test case mới cho module có sẵn

**Ví dụ:** Thêm test login với `locked_out_user`

1. Thêm data vào `test-data/users.json`:
   ```json
   "lockedOutUser": { "username": "locked_out_user", "password": "secret_sauce" }
   ```
2. Thêm message vào `ultis/messages.py` (nếu cần)
3. Thêm test vào `tests/test_login.py`:
   ```python
   def test_login_locked_out_user(self, open_login_page):
       user = get_user_from_json("lockedOutUser")
       open_login_page.login(user["username"], user["password"])
       expect(open_login_page.error_message()).to_contain_text("locked out")
   ```

---

### Thêm module mới (ví dụ: Checkout)

1. Thêm locator vào `locators.py` → class `CheckoutPageLocators`
2. Tạo `pages/checkout_page.py` → class `CheckoutPage`
3. Thêm fixture vào `conftest.py` (nếu cần setup riêng)
4. Tạo `tests/test_checkout.py`
5. Thêm test data vào `test-data/` (nếu cần)

---

## Sơ đồ luồng chạy test (tổng quan)

```
pytest khởi chạy
    │
    ▼
conftest.py ──→ Mở browser (Chrome)
    │
    ▼
Fixture ──→ Vào trang / Login sẵn
    │
    ▼
test_login.py ──→ get_user_from_json("validUser")
    │                  │
    │                  ▼
    │             test-data/users.json
    │
    ▼
login_page.login() ──→ locators.py (#user-name, #password...)
    │
    ▼
expect(...) ──→ Kiểm tra kết quả Pass/Fail
    │
    ▼
Allure ──→ Screenshot + Báo cáo HTML
```

---

## Website được test

| Thông tin | Giá trị |
|---|---|
| URL | https://www.saucedemo.com/ |
| Username mặc định | `standard_user` |
| Password mặc định | `secret_sauce` |
| Các user khác | `locked_out_user`, `problem_user`, `performance_glitch_user`, `error_user`, `visual_user` |

---

## Công nghệ sử dụng

| Công nghệ | Phiên bản | Mục đích |
|---|---|---|
| Python | 3.10+ | Ngôn ngữ lập trình |
| Playwright | 1.60+ | Automation browser |
| Pytest | 9.1+ | Test runner |
| Allure | 2.16+ | Báo cáo test |
| python-dotenv | — | Đọc file .env |
