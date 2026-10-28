# HƯỚNG DẪN KIẾN TRÚC & TRIỂN KHAI HỆ THỐNG SOCIAL CRM (ĐA KÊNH FACEBOOK & TIKTOK)

Hệ thống trong ảnh là **Social Commerce CRM & Multi-Fanpage Engagement Tracker** (Giao diện Quản trị tương tác đa kênh tập trung).

---

## 1. PHÂN TÍCH CHỨC NĂNG CỦA HỆ THỐNG

### A. Màn hình "Tương tác mạng xã hội" (Đang hiển thị trong ảnh)
1. **Phân nhóm theo ngành hàng (Industry Tags)**:
   - Các nhãn trên cùng: `Tất cả (16)`, `Lọc nước (7)`, `AI (5)`, `Chưa gán ngành (4)`.
   - Giúp doanh nghiệp quản lý nhiều thương hiệu, nhiều ngành nghề hoặc nhiều chi nhánh trên cùng một bảng điều khiển.
2. **Theo dõi trạng thái đồng bộ thời gian thực (Real-time Sync Status)**:
   - Thông báo: *"Đang theo dõi 8 trang Facebook & TikTok · cập nhật 08:48"*.
   - Tiến trình: *"⏳ Đang đọc lần đầu 1 trang Facebook..."*.
   - Cơ chế: Tự động chạy nền mỗi 5 phút quét API kéo dữ liệu mới nhất.
3. **Bộ lọc nền tảng & thời gian**:
   - Nền tảng: `Tất cả (9)`, `Facebook (8)`, `TikTok (1)`.
   - Thời gian: `7 ngày`, `30 ngày`, `90 ngày`, `Hôm nay`, `Hôm qua`, `Tất cả`, `Chọn ngày`.
4. **Ma trận thẻ Fanpage (Page Cards Grid)**:
   - Hiển thị từng Fanpage với Avatar, tên Fanpage.
   - 4 chỉ số đo lường hiệu suất:
     - 📝 **Số bài đăng** (Posts count)
     - 👍 **Lượt thích & cảm xúc** (Reactions/Likes)
     - 💬 **Lượt bình luận** (Comments)
     - 🔁/👁️ **Lượt chia sẻ / Lượt xem** (Shares / Views)
   - Cảnh báo thời gian hoạt động gần nhất: *"Bình luận gần nhất 14 giờ"*, *"Bài gần nhất 09-09"*, hoặc *"Chưa có hoạt động"*.
   - Cho phép bấm vào từng thẻ để **xem riêng (Drill-down)** biểu đồ tăng trưởng và danh sách bài viết chi tiết.

### B. Các chức năng CRM toàn diện trên Sidebar trái
- **Tổng quan**: Dashboard tóm tắt doanh số, số khách mới, tỷ lệ phản hồi.
- **Cần chăm (Badge 12)**: Danh sách khách hàng tiềm năng vừa bình luận hỏi giá, tư vấn hoặc nhắn tin chưa được nhân viên chốt/chăm sóc.
- **Bắn lại (Retarget / Broadcast)**: Gửi tin nhắn tiếp thị hàng loạt đến tệp khách cũ theo thẻ phân loại.
- **Hâm nóng (Lead Nurturing)**: Chuỗi tin nhắn tự động (Drip Campaign) gửi theo ngày để kích hoạt nhu cầu mua lại hoặc gia hạn lõi lọc/phần mềm.
- **Hộp thư (Omnichannel Inbox - Badge 16)**: Gom toàn bộ chat Facebook Messenger, TikTok DM, Shopee chat về 1 cửa sổ tập trung.
- **Khách**: CRM quản lý thông tin khách (Họ tên, SĐT, địa chỉ, lịch sử đơn, tag sở thích).
- **Pipeline**: Phễu bán hàng dạng Kanban (Mới tiếp cận -> Đang tư vấn -> Đã báo giá -> Chốt đơn -> Hoàn tất).
- **Shopee & TikTok Shop**: Tích hợp đơn hàng và thông tin vận chuyển sàn TMĐT.
- **Cài đặt**: Quản lý API Token, Webhook Meta/TikTok, phân quyền nhân viên phụ trách trang.

---

## 2. CÁCH XÂY DỰNG HỆ THỐNG NÀY TỪ A - Z

### Bước 1: Công nghệ đề xuất (Tech Stack)
- **Frontend**: Next.js (React) / Tailwind CSS / Lucide Icons / Chart.js.
- **Backend API**: Node.js (NestJS / Express) hoặc Python (FastAPI).
- **Database**: PostgreSQL (hoặc Supabase) để lưu quan hệ dữ liệu chuẩn; Redis để làm hàng đợi (Queue) đồng bộ API.
- **Cron Jobs / Task Scheduler**: BullMQ (Node.js) hoặc Celery/APScheduler (Python) chạy job định kỳ 5 phút/lần.

### Bước 2: Đăng ký & Tích hợp API các nền tảng
1. **Facebook Graph API (Meta for Developers)**:
   - Tạo Facebook App loại *Business*.
   - Cấp các quyền: `pages_show_list`, `pages_read_engagement`, `pages_manage_posts`, `pages_read_user_content`.
   - Lấy **Page Access Token dài hạn (Never-expire token)**.
   - Endpoint quét dữ liệu:
     ```http
     GET /{page-id}/feed?fields=id,message,created_time,shares,reactions.summary(true),comments.summary(true)&limit=50
     ```
   - Cài đặt **Meta Webhooks** lắng nghe sự kiện `feed` (post mới, comment mới) để cập nhật ngay lập tức mà không phải đợi 5 phút.

2. **TikTok for Business API / TikTok Display API**:
   - Đăng ký tài khoản TikTok Developer.
   - Sử dụng endpoint `/v2/video/list/` để lấy danh sách video, lượt xem, lượt like, comment.

3. **YouTube Data API v3 (Google Cloud Console)**:
   - Vào Google Cloud Console (`console.cloud.google.com`), tạo Project và bật **YouTube Data API v3**.
   - Tạo **API Key** (dùng đọc thông tin công khai của kênh, video, views, likes, comments hoàn toàn miễn phí 10.000 quota units/ngày).
   - Nếu muốn đọc bình luận riêng tư hoặc trả lời bình luận YouTube từ CRM: Tạo thêm **OAuth 2.0 Client ID**.
   - Endpoint quét dữ liệu kênh & video:
     ```http
     GET https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id={CHANNEL_ID}&key={API_KEY}
     GET https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&id={VIDEO_IDS}&key={API_KEY}
     ```

### Bước 3: Thiết kế Database Schema
```sql
-- 1. Bảng trang / kênh
CREATE TABLE pages (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    platform VARCHAR(20) NOT NULL, -- 'facebook' | 'tiktok'
    industry_tag VARCHAR(50),      -- 'loc-nuoc' | 'ai' | 'unassigned'
    avatar_url TEXT,
    access_token TEXT NOT NULL,
    last_synced_at TIMESTAMP WITH TIME ZONE,
    status VARCHAR(20) DEFAULT 'active'
);

-- 2. Bảng bài đăng
CREATE TABLE posts (
    id VARCHAR(100) PRIMARY KEY,
    page_id VARCHAR(50) REFERENCES pages(id),
    content TEXT,
    post_url TEXT,
    published_at TIMESTAMP WITH TIME ZONE
);

-- 3. Bảng chỉ số tương tác theo thời gian
CREATE TABLE post_metrics (
    id SERIAL PRIMARY KEY,
    post_id VARCHAR(100) REFERENCES posts(id),
    likes_count INT DEFAULT 0,
    comments_count INT DEFAULT 0,
    shares_count INT DEFAULT 0,
    views_count INT DEFAULT 0,
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### Bước 4: Cron Job đồng bộ mỗi 5 phút (Node.js / Python)
```python
# Ví dụ cron job đơn giản bằng Python:
import schedule
import time
import requests

def sync_all_pages():
    pages = get_active_pages_from_db()
    for page in pages:
        if page['platform'] == 'facebook':
            url = f"https://graph.facebook.com/v19.0/{page['id']}/feed"
            params = {
                'fields': 'id,reactions.summary(true),comments.summary(true),shares',
                'access_token': page['access_token']
            }
            res = requests.get(url, params=params).json()
            # Cập nhật số liệu vào database...
    print("Đã hoàn tất đồng bộ lúc:", time.strftime("%H:%M:%S"))

schedule.every(5).minutes.do(sync_all_pages)
```

---

## 3. FILE GIAO DIỆN MẪU ĐÃ ĐƯỢC TẠO SẴN TRONG THƯ MỤC
- `index.html`: Giao diện Dashboard hoàn chỉnh giống 100% ảnh chụp, có sẵn hiệu ứng lọc, chuyển tab, đếm số liệu, xem chi tiết và biểu đồ.
- `server.py`: Script chạy máy chủ cục bộ nhanh.

**Cách mở xem ngay lập tức**:
1. Nhấp đúp vào file `d:\MCP\index.html` để mở trực tiếp trên trình duyệt.
2. Hoặc mở Terminal chạy lệnh:
   ```bash
   python server.py
   ```
   Sau đó truy cập: `http://localhost:3000/index.html`.
