"""Script to build and validate Bonus Chunks, Questions, and Agent Cases for SGK Dia li 10.
Compliant with ADVANCED.md, RUBRIC.md, and starter/baseline.py validate().
"""
import json
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR / "starter"))
from baseline import validate

BONUS_DIR = ROOT_DIR / "data" / "bonus"
BONUS_DIR.mkdir(parents=True, exist_ok=True)

# ----------------- 32 CHUNKS -----------------
chunks_data = [
    # 1. Diagram Vỏ Trái Đất
    {
        "id": "sgk10_p17_diagram_votraidat",
        "source_id": "sgk-dia-li-10-kntt",
        "source": "assets/sgk-dia-li-10-kntt-17627059007551086575955.pdf",
        "page": 17,
        "text": "Sơ đồ cấu tạo vỏ Trái Đất (Trang 17):\n- Tầng trầm tích: Nằm ở trên cùng, do các vật liệu vụn, nhỏ bị nén chặt tạo thành; tầng này không liên tục và có độ dày không đều.\n- Tầng granit: Gồm các loại đá nhẹ (như đá granit và các loại đá có tính chất tương tự) tạo nên; lớp vỏ lục địa được cấu tạo chủ yếu bằng granit.\n- Tầng badan: Gồm các loại đá nặng hơn (như đá badan và các loại đá có tính chất tương tự) tạo nên; lớp vỏ đại dương cấu tạo chủ yếu bằng badan.\nVật liệu cấu tạo nên vỏ Trái Đất là khoáng vật và đá. Đá gồm ba nhóm theo nguồn gốc: đá macma (granit, badan), đá trầm tích (đá vôi, sa thạch) và đá biến chất (đá gơnai, đá hoa, đá phiến).",
        "metadata": {
            "type": "diagram",
            "title": "Sơ đồ cấu tạo vỏ Trái Đất",
            "chapter": "Chương 2",
            "lesson": "Bài 4",
            "pdf_page": 18,
            "crop_filename": "page_17_diagram_votraidat.png"
        }
    },
    # 2. Map Giờ Trái Đất
    {
        "id": "sgk10_p19_map_gio",
        "source_id": "sgk-dia-li-10-kntt",
        "source": "assets/sgk-dia-li-10-kntt-17627059007551086575955.pdf",
        "page": 19,
        "text": "Hình 5.2. Bản đồ giờ trên Trái Đất (Trang 19):\nNgười ta quy định lấy kinh tuyến 180 độ đi qua giữa múi giờ số 12 ở Thái Bình Dương làm đường chuyển ngày quốc tế. Nếu đi từ tây sang đông qua kinh tuyến 180 độ thì lùi lại một ngày lịch; nếu đi từ đông sang tây qua kinh tuyến 180 độ thì tăng thêm một ngày lịch. Bề mặt Trái Đất được chia làm 24 múi giờ, mỗi múi rộng 15 độ kinh tuyến. Giờ múi số 0 (giờ quốc tế GMT/UTC) đi qua đài thiên văn Grin-uých ở Luân Đôn (Vương quốc Anh).",
        "metadata": {
            "type": "map",
            "title": "Bản đồ giờ trên Trái Đất và Đường chuyển ngày quốc tế",
            "chapter": "Chương 2",
            "lesson": "Bài 5",
            "pdf_page": 20,
            "crop_filename": "page_19_map_gio.png"
        }
    },
    # 3. Map Mảng Kiến Tạo
    {
        "id": "sgk10_p23_map_kientao",
        "source_id": "sgk-dia-li-10-kntt",
        "source": "assets/sgk-dia-li-10-kntt-17627059007551086575955.pdf",
        "page": 23,
        "text": "Hình 6.2. Lược đồ các mảng kiến tạo của Trái Đất (Trang 23):\nThạch quyển được cấu tạo bởi 7 mảng kiến tạo lớn gồm: mảng Thái Bình Dương, mảng Ấn Độ - Ô-xtrây-li-a, mảng Âu - Á, mảng Bắc Mỹ, mảng Nam Mỹ, mảng Phi, mảng Nam Cực. Và một số mảng kiến tạo nhỏ như: mảng Ca-ri-bê, mảng Cô-cốt, mảng Na-dơ-ca, mảng Phi-líp-pin, mảng A-rập. Các mảng kiến tạo không đứng yên mà luôn dịch chuyển trên lớp quánh dẻo của manti trên.",
        "metadata": {
            "type": "map",
            "title": "Lược đồ các mảng kiến tạo của Trái Đất",
            "chapter": "Chương 3",
            "lesson": "Bài 6",
            "pdf_page": 24,
            "crop_filename": "page_23_map_kientao.png"
        }
    },
    # 4. Table 9 Nhiệt Độ Bán Cầu Bắc
    {
        "id": "sgk10_p30_table9_nhietdo",
        "source_id": "sgk-dia-li-10-kntt",
        "source": "assets/sgk-dia-li-10-kntt-17627059007551086575955.pdf",
        "page": 30,
        "text": "BẢNG 9. NHIỆT ĐỘ TRUNG BÌNH NĂM VÀ BIÊN ĐỘ NHIỆT ĐỘ NĂM THEO VĨ ĐỘ Ở BÁN CẦU BẮC (Trang 30):\n| Vĩ độ | Nhiệt độ trung bình năm (°C) | Biên độ nhiệt độ năm (°C) |\n|---|---|---|\n| 0° (Xích đạo) | 24,5 | 1,8 |\n| 20° | 25,0 | 7,4 |\n| 30° | 20,4 | 13,3 |\n| 40° | 14,0 | 17,7 |\n| 50° | 5,4 | 23,8 |\n| 60° | -0,6 | 29,0 |\n| 70° | -10,4 | 32,2 |\nNhận xét: Càng lên vĩ độ cao, nhiệt độ trung bình năm càng giảm (từ 24,5°C ở xích đạo xuống -10,4°C ở 70°B) và biên độ nhiệt độ năm càng tăng (từ 1,8°C ở xích đạo lên 32,2°C ở 70°B).",
        "metadata": {
            "type": "table",
            "title": "Bảng 9. Nhiệt độ trung bình năm và biên độ nhiệt độ năm theo vĩ độ ở bán cầu Bắc",
            "chapter": "Chương 4",
            "lesson": "Bài 9",
            "pdf_page": 31,
            "crop_filename": "page_30_table9_nhietdo.png"
        }
    },
    # 5. Chart 10 Khí Hậu
    {
        "id": "sgk10_p36_chart_bieudokhihau",
        "source_id": "sgk-dia-li-10-kntt",
        "source": "assets/sgk-dia-li-10-kntt-17627059007551086575955.pdf",
        "page": 36,
        "text": "Hình 10. Biểu đồ nhiệt độ và lượng mưa của một số trạm khí hậu trên Trái Đất (Trang 36):\n- Trạm I-cu-xcơ (Nga - Kiểu khí hậu ôn đới lục địa): Nhiệt độ tháng 7 cao nhất đạt khoảng 19°C, nhiệt độ tháng 1 thấp nhất xuống dưới -20°C (khoảng -21°C). Lượng mưa trung bình năm thấp (410 mm), mưa tập trung chủ yếu vào mùa hạ.\n- Trạm Pa-lec-mô (I-ta-li-a - Kiểu khí hậu cận nhiệt địa trung hải): Nhiệt độ tháng 7-8 cao nhất (25°C), tháng 1 ấm áp (11°C). Lượng mưa năm 650 mm, mùa hạ khô nóng ít mưa, mùa đông mưa nhiều.\n- Trạm Vơ-lanh (I-rơ-lan - Kiểu khí hậu ôn đới hải dương): Mưa quanh năm, lượng mưa 1016 mm, biên độ nhiệt năm nhỏ.",
        "metadata": {
            "type": "chart",
            "title": "Hình 10. Biểu đồ nhiệt độ và lượng mưa của một số trạm khí hậu trên Trái Đất",
            "chapter": "Chương 4",
            "lesson": "Bài 10",
            "pdf_page": 37,
            "crop_filename": "page_36_chart_bieudokhihau.png"
        }
    },
    # 6. Diagram Vòng tuần hoàn nước
    {
        "id": "sgk10_p41_diagram_tuanhoannuoc",
        "source_id": "sgk-dia-li-10-kntt",
        "source": "assets/sgk-dia-li-10-kntt-17627059007551086575955.pdf",
        "page": 41,
        "text": "Hình 12. Sơ đồ vòng tuần hoàn của nước (Trang 41):\nNước trong thuỷ quyển luôn vận động không ngừng và chuyển từ trạng thái này sang trạng thái khác theo hai vòng tuần hoàn:\n- Vòng tuần hoàn nhỏ: Nước biển và đại dương bốc hơi tạo thành mây, mây gặp lạnh ngưng tụ thành mưa rơi xuống biển.\n- Vòng tuần hoàn lớn: Nước biển bốc hơi tạo thành mây, gió đưa mây vào đất liền, ngưng tụ thành mưa hoặc tuyết rơi trên lục địa; nước mưa chảy tràn trên bề mặt thành sông suối hoặc ngấm xuống đất thành nước ngầm, rồi cuối cùng lại chảy ra biển và đại dương.",
        "metadata": {
            "type": "diagram",
            "title": "Hình 12. Sơ đồ vòng tuần hoàn của nước",
            "chapter": "Chương 5",
            "lesson": "Bài 12",
            "pdf_page": 42,
            "crop_filename": "page_41_diagram_tuanhoannuoc.png"
        }
    },
    # 7. Chart Sông Hồng
    {
        "id": "sgk10_p44_chart_songhong",
        "source_id": "sgk-dia-li-10-kntt",
        "source": "assets/sgk-dia-li-10-kntt-17627059007551086575955.pdf",
        "page": 44,
        "text": "Hình 13. Biểu đồ lưu lượng nước trung bình tháng của sông Hồng tại trạm Hà Nội (Trang 44):\nChế độ nước sông Hồng chia làm 2 mùa rõ rệt:\n- Mùa lũ kéo dài 5 tháng (từ tháng 6 đến tháng 10), lưu lượng nước tháng cao nhất là tháng 8 (đạt trên 9.000 m³/s, đỉnh lũ khoảng 9.200 m³/s). Mùa lũ chiếm khoảng 75% tổng lượng nước cả năm.\n- Mùa cạn kéo dài 7 tháng (từ tháng 11 đến tháng 5 năm sau), lưu lượng nước tháng thấp nhất là tháng 3 (xuống dưới 1.000 m³/s, khoảng 950 m³/s).",
        "metadata": {
            "type": "chart",
            "title": "Hình 13. Biểu đồ lưu lượng nước trung bình tháng của sông Hồng tại trạm Hà Nội",
            "chapter": "Chương 5",
            "lesson": "Bài 13",
            "pdf_page": 45,
            "crop_filename": "page_44_chart_songhong.png"
        }
    },
    # 8. Diagram Đai khí áp
    {
        "id": "sgk10_p50_diagram_daikhiap",
        "source_id": "sgk-dia-li-10-kntt",
        "source": "assets/sgk-dia-li-10-kntt-17627059007551086575955.pdf",
        "page": 50,
        "text": "Hình 15.1. Sơ đồ các đai khí áp và các đới gió trên Trái Đất (Trang 50):\nKhí áp được phân bố thành các đai xen kẽ nhau từ xích đạo về cực:\n- 1 đai áp thấp xích đạo (0°)\n- 2 đai áp cao cận nhiệt đới (ở khoảng 30° Bắc và 30° Nam)\n- 2 đai áp thấp ôn đới (ở khoảng 60° Bắc và 60° Nam)\n- 2 đai áp cao cực (ở 90° Bắc và 90° Nam)\nCác đới gió chính thổi từ đai áp cao về đai áp thấp:\n- Gió Mậu dịch (gió Tín phong): thổi từ áp cao cận nhiệt đới về áp thấp xích đạo.\n- Gió Tây ôn đới: thổi từ áp cao cận nhiệt đới về áp thấp ôn đới.\n- Gió Đông cực: thổi từ áp cao cực về áp thấp ôn đới.",
        "metadata": {
            "type": "diagram",
            "title": "Hình 15.1. Sơ đồ các đai khí áp và các đới gió trên Trái Đất",
            "chapter": "Chương 4",
            "lesson": "Bài 15",
            "pdf_page": 51,
            "crop_filename": "page_50_diagram_daikhiap.png"
        }
    },
    # 9. Text Quy luật địa đới & phi địa đới
    {
        "id": "sgk10_p51_text_quyluatdiadoi",
        "source_id": "sgk-dia-li-10-kntt",
        "source": "assets/sgk-dia-li-10-kntt-17627059007551086575955.pdf",
        "page": 51,
        "text": "Quy luật địa đới và Quy luật phi địa đới (Trang 51):\n1. Quy luật địa đới:\n- Là sự thay đổi có quy luật của tất cả các thành phần địa lí và cảnh quan địa lí theo vĩ độ (từ xích đạo về hai cực).\n- Nguyên nhân: Do dạng hình cầu của Trái Đất và góc chiếu của bức xạ mặt trời giảm dần từ xích đạo về hai cực, làm cho lượng bức xạ mặt trời phân bố không đều.\n- Biểu hiện: Các vòng đai nhiệt, các đai khí áp và đới gió, các đới khí hậu, các nhóm đất và thảm thực vật chính trên Trái Đất.\n2. Quy luật phi địa đới:\n- Là quy luật phân bố không phụ thuộc vào bức xạ mặt trời, gồm quy luật đai cao (thay đổi theo độ cao) và quy luật địa ô (thay đổi theo kinh độ từ bờ biển vào nội địa).",
        "metadata": {
            "type": "text",
            "title": "Quy luật địa đới và Quy luật phi địa đới",
            "chapter": "Chương 4",
            "lesson": "Bài 15",
            "pdf_page": 52,
            "crop_filename": "page_51_text_quyluatdiadoi.png"
        }
    },
    # 10. Chart Gia tăng dân số
    {
        "id": "sgk10_p54_chart_giatangdanso",
        "source_id": "sgk-dia-li-10-kntt",
        "source": "assets/sgk-dia-li-10-kntt-17627059007551086575955.pdf",
        "page": 54,
        "text": "Hình 18. Biểu đồ tỉ suất sinh thô, tỉ suất tử thô và tỉ suất gia tăng dân số tự nhiên thế giới giai đoạn 1950 - 2020 (Trang 54):\n- Năm 1950: Tỉ suất sinh thô là 36,9‰, tỉ suất tử thô là 19,1‰, tỉ suất gia tăng dân số tự nhiên là 1,78%.\n- Năm 1970: Tỉ suất sinh thô là 33,6‰, tỉ suất tử thô là 12,8‰, tỉ suất gia tăng tự nhiên là 2,08% (đỉnh điểm gia tăng).\n- Năm 2020: Tỉ suất sinh thô giảm còn 18,5‰, tỉ suất tử thô giảm xuống 7,6‰, tỉ suất gia tăng dân số tự nhiên giảm xuống 1,09%.\nNhận xét: Tỉ suất gia tăng dân số tự nhiên của thế giới có xu hướng giảm rõ rệt từ năm 1970 (2,08%) xuống còn 1,09% năm 2020.",
        "metadata": {
            "type": "chart",
            "title": "Hình 18. Biểu đồ tỉ suất sinh thô, tỉ suất tử thô và tỉ suất gia tăng dân số tự nhiên thế giới",
            "chapter": "Chương 8",
            "lesson": "Bài 18",
            "pdf_page": 55,
            "crop_filename": "page_54_chart_giatangdanso.png"
        }
    },
    # 11. Table 19.1 Dân số châu lục
    {
        "id": "sgk10_p56_table19_danso",
        "source_id": "sgk-dia-li-10-kntt",
        "source": "assets/sgk-dia-li-10-kntt-17627059007551086575955.pdf",
        "page": 56,
        "text": "BẢNG 19.1. QUY MÔ DÂN SỐ THẾ GIỚI VÀ CÁC CHÂU LỤC GIAI ĐOẠN 1950 - 2020 (Đơn vị: triệu người) (Trang 56):\n| Châu lục | Năm 1950 | Năm 1970 | Năm 1990 | Năm 2010 | Năm 2020 |\n|---|---|---|---|---|---|\n| Châu Á | 1.404 | 2.138 | 3.202 | 4.194 | 4.641 |\n| Châu Phi | 228 | 366 | 632 | 1.044 | 1.341 |\n| Châu Âu | 549 | 657 | 722 | 735 | 748 |\n| Châu Mỹ | 339 | 519 | 727 | 944 | 1.025 |\n| Châu Đại Dương | 13 | 20 | 27 | 37 | 43 |\n| Toàn thế giới | 2.536 | 3.700 | 5.310 | 6.957 | 7.795 |\nChâu Á luôn chiếm tỉ trọng dân số lớn nhất thế giới (chiếm 59,5% dân số toàn cầu năm 2020: 4.641 / 7.795 triệu người).",
        "metadata": {
            "type": "table",
            "title": "BẢNG 19.1. QUY MÔ DÂN SỐ THẾ GIỚI VÀ CÁC CHÂU LỤC GIAI ĐOẠN 1950 - 2020",
            "chapter": "Chương 8",
            "lesson": "Bài 19",
            "pdf_page": 57,
            "crop_filename": "page_56_table19_danso.png"
        }
    },
    # 12. Table 19.2 Độ tuổi
    {
        "id": "sgk10_p58_table19_2_dotuoi",
        "source_id": "sgk-dia-li-10-kntt",
        "source": "assets/sgk-dia-li-10-kntt-17627059007551086575955.pdf",
        "page": 58,
        "text": "BẢNG 19.2. CƠ CẤU DÂN SỐ THEO NHÓM TUỔI CỦA THẾ GIỚI GIAI ĐOẠN 1950 - 2020 (Đơn vị: %) (Trang 58):\n| Nhóm tuổi | Năm 1950 | Năm 1970 | Năm 1990 | Năm 2010 | Năm 2020 |\n|---|---|---|---|---|---|\n| Dưới 15 tuổi (0 - 14 tuổi) | 34,3 | 37,4 | 32,8 | 27,0 | 25,4 |\n| Từ 15 đến 64 tuổi | 60,6 | 57,3 | 61,0 | 65,3 | 65,3 |\n| Từ 65 tuổi trở lên | 5,1 | 5,3 | 6,2 | 7,7 | 9,3 |\nXu hướng: Tỉ trọng nhóm dưới 15 tuổi có xu hướng giảm liên tục từ 34,3% (1950) xuống 25,4% (2020), giảm 8,9%; tỉ trọng nhóm 65 tuổi trở lên tăng nhanh từ 5,1% lên 9,3%, cho thấy dân số thế giới đang già hóa.",
        "metadata": {
            "type": "table",
            "title": "BẢNG 19.2. CƠ CẤU DÂN SỐ THEO NHÓM TUỔI CỦA THẾ GIỚI GIAI ĐOẠN 1950 - 2020",
            "chapter": "Chương 8",
            "lesson": "Bài 19",
            "pdf_page": 59,
            "crop_filename": "page_58_table19_2_dotuoi.png"
        }
    },
    # 13. Chart Tháp dân số
    {
        "id": "sgk10_p59_chart_thapdanso",
        "source_id": "sgk-dia-li-10-kntt",
        "source": "assets/sgk-dia-li-10-kntt-17627059007551086575955.pdf",
        "page": 59,
        "text": "Hình 19.2. Các kiểu tháp dân số cơ bản (Trang 59):\nTháp dân số (tháp tuổi) thể hiện cơ cấu dân số theo tuổi và giới tính. Gồm 3 kiểu cơ bản:\n- Kiểu mở rộng: Đáy tháp rộng, đỉnh tháp nhọn, các cạnh thoải; thể hiện tỉ suất sinh cao, trẻ em nhiều, tuổi thọ trung bình thấp, dân số tăng nhanh (kết cấu dân số trẻ).\n- Kiểu thu hẹp: Đáy tháp hẹp lại, phần giữa phình to; thể hiện tỉ suất sinh có xu hướng giảm nhanh, tỉ lệ trẻ em giảm, tuổi thọ tăng lên (giai đoạn chuyển tiếp sang già hóa).\n- Kiểu ổn định: Đáy tháp và phần thân tháp gần như thẳng đứng, tương đương nhau; thể hiện tỉ suất sinh và tử đều thấp, tuổi thọ trung bình cao, tỉ lệ người già cao (kết cấu dân số già).",
        "metadata": {
            "type": "chart",
            "title": "Hình 19.2. Các kiểu tháp dân số cơ bản",
            "chapter": "Chương 8",
            "lesson": "Bài 19",
            "pdf_page": 60,
            "crop_filename": "page_59_chart_thapdanso.png"
        }
    },
    # 14. Text Đô thị hóa
    {
        "id": "sgk10_p60_text_dothikoa",
        "source_id": "sgk-dia-li-10-kntt",
        "source": "assets/sgk-dia-li-10-kntt-17627059007551086575955.pdf",
        "page": 60,
        "text": "Khái niệm và Đặc điểm của Đô thị hóa (Trang 60):\n1. Khái niệm:\n- Đô thị hóa là một quá trình kinh tế - xã hội mà biểu hiện là sự tăng nhanh về số lượng và quy mô của các điểm dân cư đô thị, sự tập trung dân cư trong các thành phố, đặc biệt là các thành phố lớn và sự phổ biến rộng rãi lối sống thành thị.\n2. Ba đặc điểm chính của đô thị hóa:\n- Dân số thành thị có xu hướng tăng nhanh trên toàn thế giới.\n- Dân cư tập trung ngày càng đông vào các thành phố lớn và cực lớn.\n- Lối sống thành thị phổ biến rộng rãi trong xã hội, lan tỏa dần về các vùng nông thôn.",
        "metadata": {
            "type": "text",
            "title": "Khái niệm và Đặc điểm của Đô thị hóa",
            "chapter": "Chương 8",
            "lesson": "Bài 20",
            "pdf_page": 61,
            "crop_filename": "page_60_text_dothikoa.png"
        }
    },
    # 15. Table 20 Đô thị hóa
    {
        "id": "sgk10_p61_table20_dothikoa",
        "source_id": "sgk-dia-li-10-kntt",
        "source": "assets/sgk-dia-li-10-kntt-17627059007551086575955.pdf",
        "page": 61,
        "text": "BẢNG 20. TỈ LỆ DÂN THÀNH THỊ CỦA THẾ GIỚI VÀ CÁC NHÓM NƯỚC GIAI ĐOẠN 1950 - 2020 (Đơn vị: %) (Trang 61):\n| Nhóm nước | Năm 1950 | Năm 1970 | Năm 1990 | Năm 2010 | Năm 2020 |\n|---|---|---|---|---|---|\n| Nhóm nước phát triển | 54,9 | 66,7 | 71,2 | 76,5 | 79,1 |\n| Nhóm nước đang phát triển | 17,9 | 24,7 | 34,7 | 46,2 | 51,7 |\n| Toàn thế giới | 29,6 | 36,6 | 43,0 | 51,7 | 56,2 |\nNhận xét: Tỉ lệ dân thành thị toàn thế giới tăng liên tục từ 29,6% năm 1950 lên 56,2% năm 2020. Năm 2020, nhóm nước phát triển có tỉ lệ dân thành thị là 79,1%, cao hơn 27,4% so với nhóm nước đang phát triển (51,7%).",
        "metadata": {
            "type": "table",
            "title": "BẢNG 20. TỈ LỆ DÂN THÀNH THỊ CỦA THẾ GIỚI VÀ CÁC NHÓM NƯỚC GIAI ĐOẠN 1950 - 2020",
            "chapter": "Chương 8",
            "lesson": "Bài 20",
            "pdf_page": 62,
            "crop_filename": "page_61_table20_dothikoa.png"
        }
    },
    # 16. Diagram Nguồn lực
    {
        "id": "sgk10_p63_diagram_nguonluc",
        "source_id": "sgk-dia-li-10-kntt",
        "source": "assets/sgk-dia-li-10-kntt-17627059007551086575955.pdf",
        "page": 63,
        "text": "Sơ đồ Các nguồn lực phát triển kinh tế (Trang 63):\nNguồn lực là tổng thể vị trí địa lí, các nguồn tài nguyên thiên nhiên, hệ thống tài sản quốc gia, nguồn nhân lực, đường lối chính sách, vốn và thị trường... có thể khai thác nhằm phục vụ phát triển kinh tế.\nPhân loại gồm ba nhóm chính:\n1. Vị trí địa lí: Vị trí tự nhiên, vị trí kinh tế, chính trị, giao thông... tạo thuận lợi hoặc khó khăn trong giao lưu, hợp tác.\n2. Nguồn lực tự nhiên: Đất, nước, khí hậu, sinh vật, khoáng sản... là cơ sở tự nhiên của quá trình sản xuất.\n3. Nguồn lực kinh tế - xã hội: Dân số và nguồn lao động, vốn đầu tư, khoa học - công nghệ, thị trường, đường lối chính sách... đóng vai trò quyết định đối với sự phát triển kinh tế.",
        "metadata": {
            "type": "diagram",
            "title": "Sơ đồ Các nguồn lực phát triển kinh tế",
            "chapter": "Chương 9",
            "lesson": "Bài 21",
            "pdf_page": 64,
            "crop_filename": "page_63_diagram_nguonluc.png"
        }
    },
    # 17. Chart Cơ cấu kinh tế
    {
        "id": "sgk10_p65_chart_cocaukinhte",
        "source_id": "sgk-dia-li-10-kntt",
        "source": "assets/sgk-dia-li-10-kntt-17627059007551086575955.pdf",
        "page": 65,
        "text": "Hình 21. Biểu đồ cơ cấu ngành kinh tế của nhóm nước phát triển và đang phát triển năm 2020 (Trang 65):\n- Nhóm nước phát triển: Nông nghiệp, lâm nghiệp, thuỷ sản chiếm 1,5%; Công nghiệp và xây dựng chiếm 24,0%; Dịch vụ chiếm 74,5%.\n- Nhóm nước đang phát triển: Nông nghiệp, lâm nghiệp, thuỷ sản chiếm 10,2%; Công nghiệp và xây dựng chiếm 32,8%; Dịch vụ chiếm 57,0%.\nNhận xét: Nhóm nước phát triển có tỉ trọng ngành dịch vụ vượt trội (74,5%) so với nhóm nước đang phát triển (57,0%), trong khi tỉ trọng nông nghiệp rất thấp (chỉ 1,5%).",
        "metadata": {
            "type": "chart",
            "title": "Hình 21. Biểu đồ cơ cấu ngành kinh tế của nhóm nước phát triển và đang phát triển năm 2020",
            "chapter": "Chương 9",
            "lesson": "Bài 21",
            "pdf_page": 66,
            "crop_filename": "page_65_chart_cocaukinhte.png"
        }
    },
    # 18. Table 24.1 Lúa gạo & Lúa mì
    {
        "id": "sgk10_p70_table24_1_luagao",
        "source_id": "sgk-dia-li-10-kntt",
        "source": "assets/sgk-dia-li-10-kntt-17627059007551086575955.pdf",
        "page": 70,
        "text": "BẢNG 24.1. SẢN LƯỢNG LÚA GẠO VÀ LÚA MÌ CỦA THẾ GIỚI GIAI ĐOẠN 2000 - 2019 (Đơn vị: triệu tấn) (Trang 70):\n| Cây lương thực | Năm 2000 | Năm 2005 | Năm 2010 | Năm 2015 | Năm 2019 |\n|---|---|---|---|---|---|\n| Lúa gạo | 599,4 | 634,2 | 701,1 | 741,4 | 755,5 |\n| Lúa mì | 585,8 | 626,9 | 653,7 | 741,7 | 765,8 |\nNhận xét: Cả sản lượng lúa gạo và lúa mì đều tăng liên tục từ năm 2000 đến 2019. Năm 2019, sản lượng lúa mì (765,8 triệu tấn) vượt qua sản lượng lúa gạo (755,5 triệu tấn) với mức chênh lệch 10,3 triệu tấn. Lúa gạo phân bố chủ yếu ở khu vực nhiệt đới gió mùa (châu Á), lúa mì phân bố chủ yếu ở vùng ôn đới.",
        "metadata": {
            "type": "table",
            "title": "BẢNG 24.1. SẢN LƯỢNG LÚA GẠO VÀ LÚA MÌ CỦA THẾ GIỚI GIAI ĐOẠN 2000 - 2019",
            "chapter": "Chương 10",
            "lesson": "Bài 24",
            "pdf_page": 71,
            "crop_filename": "page_70_table24_1_luagao.png"
        }
    },
    # 19. Table 25 Thủy sản
    {
        "id": "sgk10_p75_table25_thuysan",
        "source_id": "sgk-dia-li-10-kntt",
        "source": "assets/sgk-dia-li-10-kntt-17627059007551086575955.pdf",
        "page": 75,
        "text": "BẢNG 25. SẢN LƯỢNG THỦY SẢN THẾ GIỚI GIAI ĐOẠN 2000 - 2019 (Đơn vị: triệu tấn) (Trang 75):\n| Năm | Khai thác | Nuôi trồng | Tổng sản lượng |\n|---|---|---|---|\n| 2000 | 95,6 | 32,4 | 128,0 |\n| 2005 | 92,2 | 43,0 | 135,2 |\n| 2010 | 88,6 | 59,0 | 147,6 |\n| 2015 | 91,4 | 73,0 | 164,4 |\n| 2019 | 92,5 | 85,3 | 177,8 |\nNhận xét: Tổng sản lượng thủy sản tăng liên tục từ 128,0 triệu tấn (2000) lên 177,8 triệu tấn (2019). Sản lượng nuôi trồng tăng rất nhanh (gấp hơn 2,63 lần từ 32,4 lên 85,3 triệu tấn), trong khi sản lượng khai thác có xu hướng chững lại quanh mức 92 - 95 triệu tấn.",
        "metadata": {
            "type": "table",
            "title": "BẢNG 25. SẢN LƯỢNG THỦY SẢN THẾ GIỚI GIAI ĐOẠN 2000 - 2019",
            "chapter": "Chương 10",
            "lesson": "Bài 25",
            "pdf_page": 76,
            "crop_filename": "page_75_table25_thuysan.png"
        }
    },
    # 20. Text Ngành công nghiệp
    {
        "id": "sgk10_p78_text_congnghiep",
        "source_id": "sgk-dia-li-10-kntt",
        "source": "assets/sgk-dia-li-10-kntt-17627059007551086575955.pdf",
        "page": 78,
        "text": "Vai trò và Đặc điểm của Ngành Công nghiệp (Trang 78):\n1. Vai trò:\n- Tạo ra khối lượng của cải vật chất rất lớn cho xã hội; củng cố an ninh quốc phòng.\n- Cung cấp hầu hết các tư liệu sản xuất, xây dựng cơ sở vật chất - kĩ thuật cho tất cả các ngành kinh tế khác.\n- Tạo ra việc làm cho người lao động, nâng cao mức sống và thúc đẩy quá trình đô thị hóa.\n2. Đặc điểm:\n- Quá trình sản xuất công nghiệp gồm hai giai đoạn: Giai đoạn 1 là tác động vào đối tượng lao động để khai thác tài nguyên thiên nhiên; Giai đoạn 2 là chế biến nguyên liệu thành tư liệu sản xuất và vật phẩm tiêu dùng.\n- Sản xuất công nghiệp có tính chất tập trung cao độ và có sự phân công lao động xã hội sâu sắc cùng tính liên ngành cao.",
        "metadata": {
            "type": "text",
            "title": "Vai trò và Đặc điểm của Ngành Công nghiệp",
            "chapter": "Chương 11",
            "lesson": "Bài 28",
            "pdf_page": 79,
            "crop_filename": "page_78_text_congnghiep.png"
        }
    },
    # 21. Table 29.1 Năng lượng
    {
        "id": "sgk10_p82_table29_nangluong",
        "source_id": "sgk-dia-li-10-kntt",
        "source": "assets/sgk-dia-li-10-kntt-17627059007551086575955.pdf",
        "page": 82,
        "text": "BẢNG 29.1. SẢN LƯỢNG THAN, DẦU MỎ VÀ ĐIỆN CỦA THẾ GIỚI GIAI ĐOẠN 2000 - 2019 (Trang 82):\n| Năm | Than (triệu tấn) | Dầu mỏ (triệu tấn) | Điện (tỉ kWh) |\n|---|---|---|---|\n| 2000 | 4.757 | 3.606 | 15.500 |\n| 2005 | 6.035 | 3.921 | 18.300 |\n| 2010 | 7.429 | 4.028 | 21.500 |\n| 2015 | 7.915 | 4.362 | 24.300 |\n| 2019 | 8.049 | 4.478 | 27.000 |\nNhận xét: Sản lượng điện tăng nhanh nhất (tăng 1,74 lần từ 15.500 tỉ kWh lên 27.000 tỉ kWh). Sản lượng than tăng từ 4.757 lên 8.049 triệu tấn. Sản lượng dầu mỏ tăng từ 3.606 lên 4.478 triệu tấn. Các nước có sản lượng than lớn nhất là Trung Quốc, Ấn Độ, Hoa Kỳ; dầu mỏ lớn nhất là Hoa Kỳ, Nga, A-rập Xê-út.",
        "metadata": {
            "type": "table",
            "title": "BẢNG 29.1. SẢN LƯỢNG THAN, DẦU MỎ VÀ ĐIỆN CỦA THẾ GIỚI GIAI ĐOẠN 2000 - 2019",
            "chapter": "Chương 11",
            "lesson": "Bài 29",
            "pdf_page": 83,
            "crop_filename": "page_82_table29_nangluong.png"
        }
    },
    # 22. Chart Năng lượng 2019
    {
        "id": "sgk10_p84_chart_nangluong",
        "source_id": "sgk-dia-li-10-kntt",
        "source": "assets/sgk-dia-li-10-kntt-17627059007551086575955.pdf",
        "page": 84,
        "text": "Hình 29.2. Biểu đồ cơ cấu sử dụng năng lượng thế giới năm 2019 (Trang 84):\nCơ cấu sử dụng năng lượng toàn cầu năm 2019 (Đơn vị: %):\n- Dầu mỏ chiếm tỉ trọng lớn nhất: 33,1%\n- Than đá chiếm vị trí thứ hai: 27,0%\n- Khí tự nhiên chiếm: 24,2%\n- Thủy điện chiếm: 6,4%\n- Năng lượng tái tạo (gió, mặt trời, sinh khối): 5,0%\n- Năng lượng hạt nhân chiếm: 4,3%\nNhận xét: Năng lượng hóa thạch (dầu mỏ, than đá, khí tự nhiên) vẫn chiếm tỉ trọng áp đảo lên tới 84,3% tổng năng lượng tiêu thụ toàn cầu năm 2019.",
        "metadata": {
            "type": "chart",
            "title": "Hình 29.2. Biểu đồ cơ cấu sử dụng năng lượng thế giới năm 2019",
            "chapter": "Chương 11",
            "lesson": "Bài 29",
            "pdf_page": 85,
            "crop_filename": "page_84_chart_nangluong.png"
        }
    },
    # 23. Diagram Cơ cấu ngành dịch vụ
    {
        "id": "sgk10_p91_diagram_dichvu",
        "source_id": "sgk-dia-li-10-kntt",
        "source": "assets/sgk-dia-li-10-kntt-17627059007551086575955.pdf",
        "page": 91,
        "text": "Cơ cấu ngành dịch vụ (Trang 91):\nKhu vực dịch vụ có cơ cấu ngành hết sức đa dạng và phức tạp. Người ta thường chia dịch vụ thành 3 nhóm ngành chính:\n1. Dịch vụ kinh doanh: Bao gồm tài chính, ngân hàng, bảo hiểm, vận tải hàng hóa, bán buôn, bán lẻ, tư vấn pháp lí...\n2. Dịch vụ tiêu dùng: Bao gồm y tế, giáo dục, thể dục thể thao, du lịch, khách sạn, nhà hàng, dịch vụ cá nhân và cộng đồng...\n3. Dịch vụ công: Bao gồm hành chính công, thủ tục hành chính, dịch vụ an ninh, quốc phòng và các hoạt động đoàn thể.",
        "metadata": {
            "type": "diagram",
            "title": "Sơ đồ cơ cấu ngành dịch vụ",
            "chapter": "Chương 12",
            "lesson": "Bài 33",
            "pdf_page": 92,
            "crop_filename": "page_91_diagram_dichvu.png"
        }
    },
    # 24. Table 33 GDP Ngành kinh tế (Ảnh 2 của user)
    {
        "id": "sgk10_p92_table33_gdp",
        "source_id": "sgk-dia-li-10-kntt",
        "source": "assets/sgk-dia-li-10-kntt-17627059007551086575955.pdf",
        "page": 92,
        "text": "BẢNG 33. CƠ CẤU GDP THẾ GIỚI THEO NGÀNH KINH TẾ, NĂM 2000 VÀ NĂM 2019 (*) (Đơn vị: %) (Trang 92):\n| Năm | Nông nghiệp, lâm nghiệp và thuỷ sản | Công nghiệp và xây dựng | Dịch vụ |\n|---|---|---|---|\n| 2000 | 5,2 | 30,7 | 64,1 |\n| 2019 | 4,2 | 27,9 | 67,9 |\n(*) Không tính thuế sản phẩm trừ trợ cấp sản phẩm.\n\nNhận xét sự thay đổi tỉ trọng ngành dịch vụ:\n- Tỉ trọng ngành Dịch vụ chiếm vị trí áp đảo và tăng từ 64,1% (năm 2000) lên 67,9% (năm 2019), tăng thêm 3,8%.\n- Tỉ trọng Nông nghiệp, lâm nghiệp và thuỷ sản giảm từ 5,2% xuống 4,2% (giảm 1,0%).\n- Tỉ trọng Công nghiệp và xây dựng giảm mạnh nhất: từ 30,7% xuống 27,9% (giảm 2,8%).\nCâu hỏi ôn tập liên quan: Giao thông vận tải, tư vấn pháp lí, công chứng thuộc nhóm dịch vụ kinh doanh; bảo tàng, tư vấn sức khỏe, giáo dục thuộc nhóm dịch vụ tiêu dùng.",
        "metadata": {
            "type": "table",
            "title": "BẢNG 33. CƠ CẤU GDP THẾ GIỚI THEO NGÀNH KINH TẾ, NĂM 2000 VÀ NĂM 2019 (*)",
            "chapter": "Chương 12",
            "lesson": "Bài 33",
            "pdf_page": 93,
            "crop_filename": "page_92_table33_gdp.png"
        }
    },
    # 25. Map Hàng không & Đường biển (Ảnh 3 của user)
    {
        "id": "sgk10_p96_map_hangkhong_bien",
        "source_id": "sgk-dia-li-10-kntt",
        "source": "assets/sgk-dia-li-10-kntt-17627059007551086575955.pdf",
        "page": 96,
        "text": "Hình 34.6. Bản đồ mạng lưới đường biển và đường hàng không trên thế giới, năm 2019 (Trang 96-97):\n1. Tình hình phát triển và phân bố ngành hàng không:\n- Năm 2019, ngành hàng không thế giới vận chuyển được hơn 4,4 tỉ lượt hành khách.\n- Các tuyến bay sôi động nhất: Tuyến xuyên Đại Tây Dương nối châu Âu với châu Mỹ và các tuyến nối Hoa Kỳ với châu Á - Thái Bình Dương.\n- Bốn sân bay quốc tế vận chuyển hành khách lớn nhất năm 2019 gồm: Át-lan-ta (Hoa Kỳ), Bắc Kinh (Trung Quốc), Lốt An-giơ-lét (Hoa Kỳ), Đu-bai (Các Tiểu vương quốc A-rập Thống nhất).\n2. Đường biển:\n- Tuyến đường biển sôi động nhất kết nối châu Âu với châu Á - Thái Bình Dương và hai bờ Đại Tây Dương.\n- Các cảng biển lớn nhất năm 2019 đều nằm ở châu Á: Thượng Hải (Trung Quốc), Xin-ga-po, Ninh Ba - Chu Sơn (Trung Quốc), Thâm Quyến (Trung Quốc), Bu-san (Hàn Quốc).",
        "metadata": {
            "type": "map",
            "title": "Hình 34.6. Bản đồ mạng lưới đường biển và đường hàng không trên thế giới, năm 2019",
            "chapter": "Chương 12",
            "lesson": "Bài 34",
            "pdf_page": 97,
            "crop_filename": "page_96_map_hangkhong_bien.png"
        }
    },
    # 26. Table 34 Lượt khách hàng không
    {
        "id": "sgk10_p97_table34_hangkhong",
        "source_id": "sgk-dia-li-10-kntt",
        "source": "assets/sgk-dia-li-10-kntt-17627059007551086575955.pdf",
        "page": 97,
        "text": "BẢNG 34. SỐ LƯỢNG LƯỢT HÀNH KHÁCH VẬN CHUYỂN ĐƯỜNG HÀNG KHÔNG TRÊN THẾ GIỚI, GIAI ĐOẠN 2000 - 2019 (Trang 97):\n(Đơn vị: tỉ lượt người)\n| Năm | Năm 2000 | Năm 2010 | Năm 2019 |\n|---|---|---|---|\n| Số lượng hành khách | 1,9 | 2,6 | 4,4 |\nNhận xét: Số lượng hành khách vận chuyển bằng đường hàng không tăng liên tục và mạnh mẽ, từ 1,9 tỉ lượt người (năm 2000) lên 2,6 tỉ lượt người (năm 2010) và đạt 4,4 tỉ lượt người (năm 2019), tăng gấp hơn 2,3 lần trong vòng gần 20 năm, tăng thêm 2,5 tỉ lượt người.",
        "metadata": {
            "type": "table",
            "title": "BẢNG 34. SỐ LƯỢNG LƯỢT HÀNH KHÁCH VẬN CHUYỂN ĐƯỜNG HÀNG KHÔNG TRÊN THẾ GIỚI",
            "chapter": "Chương 12",
            "lesson": "Bài 34",
            "pdf_page": 98,
            "crop_filename": "page_97_table34_hangkhong.png"
        }
    },
    # 27. Sơ đồ tư duy Bưu chính viễn thông (Ảnh 1 của user)
    {
        "id": "sgk10_p98_diagram_buuchinh",
        "source_id": "sgk-dia-li-10-kntt",
        "source": "assets/sgk-dia-li-10-kntt-17627059007551086575955.pdf",
        "page": 98,
        "text": "SƠ ĐỒ TƯ DUY: VAI TRÒ CỦA BƯU CHÍNH VIỄN THÔNG (Trang 98):\n1. Với phát triển kinh tế (3 vai trò chính):\n- Cung ứng và truyền tải thông tin, vận chuyển bưu phẩm, bưu kiện góp phần tăng năng suất lao động.\n- Hiện đại hoá, thay đổi cách thức tổ chức nền kinh tế, thúc đẩy kinh tế phát triển.\n- Bản thân bưu chính viễn thông cũng là ngành dịch vụ mang lại giá trị kinh tế cao.\n2. Với các lĩnh vực khác (3 vai trò chính):\n- Đảm bảo giao lưu giữa các vùng, thúc đẩy quá trình hội nhập và toàn cầu hoá.\n- Tạo thuận lợi cho quản lí hành chính.\n- Nâng cao đời sống văn hoá, tinh thần trong xã hội.\n\nĐặc điểm ngành bưu chính viễn thông (mục b, Trang 98):\n- Gồm hai nhóm: bưu chính (vận chuyển thư, bưu phẩm, bưu kiện, hàng hoá,...) và viễn thông (dịch vụ gửi, truyền, nhận và xử lí thông tin giữa các đối tượng sử dụng).\n- Sản phẩm của bưu chính viễn thông là sự vận chuyển tin tức, bưu kiện, bưu phẩm, truyền dẫn thông tin điện tử,... từ nơi gửi đến nơi nhận.",
        "metadata": {
            "type": "diagram",
            "title": "SƠ ĐỒ TƯ DUY: VAI TRÒ CỦA BƯU CHÍNH VIỄN THÔNG VÀ ĐẶC ĐIỂM",
            "chapter": "Chương 12",
            "lesson": "Bài 35",
            "pdf_page": 99,
            "crop_filename": "page_98_diagram_buuchinh.png"
        }
    },
    # 28. Table 36 Du lịch
    {
        "id": "sgk10_p102_table36_dulich",
        "source_id": "sgk-dia-li-10-kntt",
        "source": "assets/sgk-dia-li-10-kntt-17627059007551086575955.pdf",
        "page": 102,
        "text": "BẢNG 36. SỐ LƯỢT KHÁCH DU LỊCH QUỐC TẾ VÀ DOANH THU DU LỊCH QUỐC TẾ TRÊN THẾ GIỚI GIAI ĐOẠN 2000 - 2019 (Trang 102):\n| Năm | Khách du lịch quốc tế (triệu lượt người) | Doanh thu du lịch quốc tế (tỉ USD) |\n|---|---|---|\n| 2000 | 682 | 475 |\n| 2005 | 809 | 679 |\n| 2010 | 953 | 927 |\n| 2015 | 1.189 | 1.196 |\n| 2019 | 1.460 | 1.482 |\nNhận xét: Số lượt khách du lịch quốc tế tăng từ 682 triệu lượt lên 1.460 triệu lượt (tăng 2,14 lần). Doanh thu du lịch quốc tế tăng từ 475 tỉ USD lên 1.482 tỉ USD (tăng 3,12 lần). Châu Âu là khu vực đón lượng khách du lịch và có doanh thu du lịch cao nhất thế giới.",
        "metadata": {
            "type": "table",
            "title": "BẢNG 36. SỐ LƯỢT KHÁCH DU LỊCH QUỐC TẾ VÀ DOANH THU DU LỊCH QUỐC TẾ TRÊN THẾ GIỚI",
            "chapter": "Chương 12",
            "lesson": "Bài 36",
            "pdf_page": 103,
            "crop_filename": "page_102_table36_dulich.png"
        }
    },
    # 29. Table 37 Xuất nhập khẩu
    {
        "id": "sgk10_p104_table37_thuongmai",
        "source_id": "sgk-dia-li-10-kntt",
        "source": "assets/sgk-dia-li-10-kntt-17627059007551086575955.pdf",
        "page": 104,
        "text": "BẢNG 37. TRỊ GIÁ XUẤT KHẨU VÀ NHẬP KHẨU HÀNG HÓA CỦA THẾ GIỚI GIAI ĐOẠN 2000 - 2019 (Đơn vị: tỉ USD) (Trang 104):\n| Năm | Xuất khẩu | Nhập khẩu | Tổng trị giá XNK |\n|---|---|---|---|\n| 2000 | 6.456 | 6.724 | 13.180 |\n| 2005 | 10.509 | 10.826 | 21.335 |\n| 2010 | 15.301 | 15.485 | 30.786 |\n| 2015 | 16.558 | 16.734 | 33.292 |\n| 2019 | 19.015 | 19.243 | 38.258 |\nNhận xét: Tổng trị giá xuất nhập khẩu hàng hóa thế giới tăng từ 13.180 tỉ USD (2000) lên 38.258 tỉ USD (2019), tăng gần gấp 3 lần (2,9 lần). Trong đó, năm 2019 xuất khẩu đạt 19.015 tỉ USD và nhập khẩu đạt 19.243 tỉ USD. Các nước đứng đầu về thương mại là Trung Quốc, Hoa Kỳ, Đức, Nhật Bản.",
        "metadata": {
            "type": "table",
            "title": "BẢNG 37. TRỊ GIÁ XUẤT KHẨU VÀ NHẬP KHẨU HÀNG HÓA CỦA THẾ GIỚI GIAI ĐOẠN 2000 - 2019",
            "chapter": "Chương 12",
            "lesson": "Bài 37",
            "pdf_page": 105,
            "crop_filename": "page_104_table37_thuongmai.png"
        }
    },
    # 30. Text Cán cân thương mại
    {
        "id": "sgk10_p105_text_thuongmai_can_can",
        "source_id": "sgk-dia-li-10-kntt",
        "source": "assets/sgk-dia-li-10-kntt-17627059007551086575955.pdf",
        "page": 105,
        "text": "Khái niệm Cán cân thương mại và Phân loại (Trang 105):\n- Cán cân thương mại là hiệu số giữa giá trị xuất khẩu và giá trị nhập khẩu hàng hóa, dịch vụ của một quốc gia trong một thời kỳ nhất định (thường là một năm).\n- Khi giá trị xuất khẩu lớn hơn giá trị nhập khẩu: cán cân thương mại dương, quốc gia đó xuất siêu.\n- Khi giá trị xuất khẩu nhỏ hơn giá trị nhập khẩu: cán cân thương mại âm, quốc gia đó nhập siêu.\n- Khi giá trị xuất khẩu bằng giá trị nhập khẩu: cán cân thương mại cân bằng.",
        "metadata": {
            "type": "text",
            "title": "Khái niệm Cán cân thương mại và Phân loại",
            "chapter": "Chương 12",
            "lesson": "Bài 37",
            "pdf_page": 106,
            "crop_filename": "page_105_text_thuongmai_can_can.png"
        }
    },
    # 31. Diagram Môi trường
    {
        "id": "sgk10_p108_diagram_moitruong",
        "source_id": "sgk-dia-li-10-kntt",
        "source": "assets/sgk-dia-li-10-kntt-17627059007551086575955.pdf",
        "page": 108,
        "text": "Môi trường và Tài nguyên thiên nhiên (Trang 108):\n- Môi trường sống của con người là tổng thể các điều kiện tự nhiên và nhân tạo bao quanh con người, có ảnh hưởng tới đời sống và sự phát triển của xã hội loài người. Gồm: môi trường tự nhiên, môi trường xã hội và môi trường nhân tạo.\n- Vai trò của môi trường: là không gian sống của con người; là nguồn cung cấp tài nguyên thiên nhiên; là nơi chứa đựng và đồng hóa các chất thải; là nơi lưu trữ và cung cấp thông tin.\n- Tài nguyên thiên nhiên phân loại theo thuộc tính tự nhiên (tài nguyên đất, nước, khí hậu, sinh vật, khoáng sản) hoặc theo công dụng kinh tế (tài nguyên nông nghiệp, công nghiệp, du lịch) và theo khả năng có thể bị hao kiệt (tài nguyên có thể phục hồi, không thể phục hồi, vô tận).",
        "metadata": {
            "type": "diagram",
            "title": "Môi trường sống và Tài nguyên thiên nhiên",
            "chapter": "Chương 13",
            "lesson": "Bài 39",
            "pdf_page": 109,
            "crop_filename": "page_108_diagram_moitruong.png"
        }
    },
    # 32. Text Tăng trưởng xanh
    {
        "id": "sgk10_p111_text_tangtruongxanh",
        "source_id": "sgk-dia-li-10-kntt",
        "source": "assets/sgk-dia-li-10-kntt-17627059007551086575955.pdf",
        "page": 111,
        "text": "Phát triển bền vững và Tăng trưởng xanh (Trang 111):\n- Phát triển bền vững là sự phát triển nhằm đáp ứng những nhu cầu của thế hệ hiện tại mà không làm tổn hại đến khả năng đáp ứng nhu cầu của các thế hệ tương lai trên cơ sở kết hợp chặt chẽ, hài hòa giữa ba trụ cột: tăng trưởng kinh tế, công bằng xã hội và bảo vệ môi trường.\n- Tăng trưởng xanh là phương thức phát triển kinh tế bền vững, nhấn mạnh vào việc thúc đẩy tăng trưởng và phát triển kinh tế, đồng thời bảo tồn các tài sản tự nhiên để tiếp tục cung cấp các tài nguyên và dịch vụ môi trường cho cuộc sống con người. Biểu hiện cụ thể: giảm phát thải khí nhà kính, chuyển dịch sang năng lượng tái tạo (gió, mặt trời), sử dụng tài nguyên hiệu quả và đẩy mạnh kinh tế tuần hoàn.",
        "metadata": {
            "type": "text",
            "title": "Phát triển bền vững và Tăng trưởng xanh",
            "chapter": "Chương 13",
            "lesson": "Bài 40",
            "pdf_page": 112,
            "crop_filename": "page_111_text_tangtruongxanh.png"
        }
    }
]

# Write chunks.json
chunks_file = BONUS_DIR / "chunks.json"
with open(chunks_file, "w", encoding="utf-8") as f:
    json.dump(chunks_data, f, ensure_ascii=False, indent=2)

print(f"Saved {len(chunks_data)} chunks to {chunks_file}")

# ----------------- 48 QUESTIONS (18 DEV + 30 TEST) -----------------
questions_data = [
    # ========== DEV SPLIT (15 Answered) ==========
    {
        "id": "b_dev_table_01",
        "split": "dev",
        "category": "table",
        "question": "Theo Bảng 19.2 (Trang 58), tỉ trọng nhóm dân số dưới 15 tuổi của thế giới giảm từ năm 1950 đến năm 2020 như thế nào?",
        "expected_answer": "Tỉ trọng nhóm dưới 15 tuổi giảm liên tục từ 34,3% (năm 1950) xuống 25,4% (năm 2020), giảm 8,9%.",
        "gold": [
            {
                "source_id": "sgk-dia-li-10-kntt",
                "page": 58,
                "evidence": "Tỉ trọng nhóm dưới 15 tuổi có xu hướng giảm liên tục từ 34,3% (1950) xuống 25,4% (2020), giảm 8,9%"
            }
        ]
    },
    {
        "id": "b_dev_table_02",
        "split": "dev",
        "category": "table",
        "question": "Theo Bảng 20 (Trang 61), năm 2020 tỉ lệ dân thành thị của nhóm nước phát triển cao hơn nhóm nước đang phát triển bao nhiêu phần trăm?",
        "expected_answer": "Năm 2020, tỉ lệ dân thành thị của nhóm nước phát triển (79,1%) cao hơn 27,4% so với nhóm nước đang phát triển (51,7%).",
        "gold": [
            {
                "source_id": "sgk-dia-li-10-kntt",
                "page": 61,
                "evidence": "Năm 2020, nhóm nước phát triển có tỉ lệ dân thành thị là 79,1%, cao hơn 27,4% so với nhóm nước đang phát triển (51,7%)."
            }
        ]
    },
    {
        "id": "b_dev_table_03",
        "split": "dev",
        "category": "table",
        "question": "Theo Bảng 25 (Trang 75), sản lượng nuôi trồng thủy sản của thế giới tăng gấp bao nhiêu lần từ năm 2000 đến năm 2019?",
        "expected_answer": "Sản lượng nuôi trồng thủy sản thế giới tăng gấp hơn 2,63 lần, từ 32,4 triệu tấn (năm 2000) lên 85,3 triệu tấn (năm 2019).",
        "gold": [
            {
                "source_id": "sgk-dia-li-10-kntt",
                "page": 75,
                "evidence": "Sản lượng nuôi trồng tăng rất nhanh (gấp hơn 2,63 lần từ 32,4 lên 85,3 triệu tấn)"
            }
        ]
    },
    {
        "id": "b_dev_diag_01",
        "split": "dev",
        "category": "diagram",
        "question": "Theo Hình 5.2 ở Trang 19, người ta quy định kinh tuyến nào làm đường chuyển ngày quốc tế và quy tắc đổi ngày khi đi qua kinh tuyến đó?",
        "expected_answer": "Lấy kinh tuyến 180 độ làm đường chuyển ngày quốc tế. Đi từ tây sang đông lùi lại 1 ngày lịch, đi từ đông sang tây tăng thêm 1 ngày lịch.",
        "gold": [
            {
                "source_id": "sgk-dia-li-10-kntt",
                "page": 19,
                "evidence": "Người ta quy định lấy kinh tuyến 180 độ đi qua giữa múi giờ số 12 ở Thái Bình Dương làm đường chuyển ngày quốc tế. Nếu đi từ tây sang đông qua kinh tuyến 180 độ thì lùi lại một ngày lịch; nếu đi từ đông sang tây qua kinh tuyến 180 độ thì tăng thêm một ngày lịch."
            }
        ]
    },
    {
        "id": "b_dev_diag_02",
        "split": "dev",
        "category": "diagram",
        "question": "Theo Lược đồ các mảng kiến tạo Hình 6.2 (Trang 23), thạch quyển được cấu tạo bởi 7 mảng kiến tạo lớn nào?",
        "expected_answer": "Bảy mảng kiến tạo lớn gồm: mảng Thái Bình Dương, mảng Ấn Độ - Ô-xtrây-li-a, mảng Âu - Á, mảng Bắc Mỹ, mảng Nam Mỹ, mảng Phi, mảng Nam Cực.",
        "gold": [
            {
                "source_id": "sgk-dia-li-10-kntt",
                "page": 23,
                "evidence": "Thạch quyển được cấu tạo bởi 7 mảng kiến tạo lớn gồm: mảng Thái Bình Dương, mảng Ấn Độ - Ô-xtrây-li-a, mảng Âu - Á, mảng Bắc Mỹ, mảng Nam Mỹ, mảng Phi, mảng Nam Cực."
            }
        ]
    },
    {
        "id": "b_dev_diag_03",
        "split": "dev",
        "category": "diagram",
        "question": "Dựa vào Sơ đồ ở Trang 63, các nguồn lực phát triển kinh tế được phân loại thành ba nhóm chính nào?",
        "expected_answer": "Ba nhóm chính gồm: Vị trí địa lí, Nguồn lực tự nhiên và Nguồn lực kinh tế - xã hội.",
        "gold": [
            {
                "source_id": "sgk-dia-li-10-kntt",
                "page": 63,
                "evidence": "Phân loại gồm ba nhóm chính:\n1. Vị trí địa lí: Vị trí tự nhiên, vị trí kinh tế, chính trị, giao thông... tạo thuận lợi hoặc khó khăn trong giao lưu, hợp tác.\n2. Nguồn lực tự nhiên: Đất, nước, khí hậu, sinh vật, khoáng sản... là cơ sở tự nhiên của quá trình sản xuất.\n3. Nguồn lực kinh tế - xã hội: Dân số và nguồn lao động, vốn đầu tư, khoa học - công nghệ, thị trường, đường lối chính sách..."
            }
        ]
    },
    {
        "id": "b_dev_chart_01",
        "split": "dev",
        "category": "chart",
        "question": "Dựa vào biểu đồ Hình 19.2 (Trang 59), hãy nêu đặc điểm hình dạng và ý nghĩa của kiểu tháp dân số mở rộng?",
        "expected_answer": "Kiểu mở rộng có đáy tháp rộng, đỉnh nhọn, các cạnh thoải; biểu hiện tỉ suất sinh cao, trẻ em nhiều, tuổi thọ trung bình thấp, dân số tăng nhanh (dân số trẻ).",
        "gold": [
            {
                "source_id": "sgk-dia-li-10-kntt",
                "page": 59,
                "evidence": "- Kiểu mở rộng: Đáy tháp rộng, đỉnh tháp nhọn, các cạnh thoải; thể hiện tỉ suất sinh cao, trẻ em nhiều, tuổi thọ trung bình thấp, dân số tăng nhanh (kết cấu dân số trẻ)."
            }
        ]
    },
    {
        "id": "b_dev_chart_02",
        "split": "dev",
        "category": "chart",
        "question": "Theo biểu đồ khí hậu Hình 10 (Trang 36), trạm Pa-lec-mô (I-ta-li-a) có đặc điểm nhiệt độ và lượng mưa mùa hạ như thế nào?",
        "expected_answer": "Tại Pa-lec-mô (cận nhiệt địa trung hải), mùa hạ khô nóng ít mưa với nhiệt độ tháng 7-8 cao nhất (25°C), mùa đông ấm áp mưa nhiều.",
        "gold": [
            {
                "source_id": "sgk-dia-li-10-kntt",
                "page": 36,
                "evidence": "Trạm Pa-lec-mô (I-ta-li-a - Kiểu khí hậu cận nhiệt địa trung hải): Nhiệt độ tháng 7-8 cao nhất (25°C), tháng 1 ấm áp (11°C). Lượng mưa năm 650 mm, mùa hạ khô nóng ít mưa, mùa đông mưa nhiều."
            }
        ]
    },
    {
        "id": "b_dev_chart_03",
        "split": "dev",
        "category": "chart",
        "question": "Dựa vào biểu đồ Hình 29.2 (Trang 84), ba nguồn năng lượng chiếm tỉ trọng lớn nhất trong cơ cấu sử dụng năng lượng thế giới năm 2019 là gì?",
        "expected_answer": "Ba nguồn năng lượng lớn nhất là: Dầu mỏ (33,1%), Than đá (27,0%) và Khí tự nhiên (24,2%).",
        "gold": [
            {
                "source_id": "sgk-dia-li-10-kntt",
                "page": 84,
                "evidence": "- Dầu mỏ chiếm tỉ trọng lớn nhất: 33,1%\n- Than đá chiếm vị trí thứ hai: 27,0%\n- Khí tự nhiên chiếm: 24,2%"
            }
        ]
    },
    {
        "id": "b_dev_multi_01",
        "split": "dev",
        "category": "multihop",
        "question": "Kết hợp Bảng 36 (Trang 102) và Bảng 37 (Trang 104), doanh thu du lịch quốc tế và tổng trị giá xuất nhập khẩu thế giới năm 2019 đạt bao nhiêu tỉ USD?",
        "expected_answer": "Năm 2019, doanh thu du lịch quốc tế đạt 1.482 tỉ USD và tổng trị giá xuất nhập khẩu hàng hóa thế giới đạt 38.258 tỉ USD.",
        "gold": [
            {
                "source_id": "sgk-dia-li-10-kntt",
                "page": 102,
                "evidence": "Doanh thu du lịch quốc tế tăng từ 475 tỉ USD lên 1.482 tỉ USD (tăng 3,12 lần)."
            }
        ]
    },
    {
        "id": "b_dev_multi_02",
        "split": "dev",
        "category": "multihop",
        "question": "Kết hợp Sơ đồ tư duy ở Trang 98 và Bảng 33 (Trang 92), ngành bưu chính viễn thông có sản phẩm là gì và thuộc nhóm ngành kinh tế có tỉ trọng GDP thế nào năm 2019?",
        "expected_answer": "Sản phẩm là sự vận chuyển tin tức, bưu kiện, bưu phẩm, truyền dẫn thông tin điện tử; thuộc ngành Dịch vụ chiếm 67,9% GDP thế giới năm 2019.",
        "gold": [
            {
                "source_id": "sgk-dia-li-10-kntt",
                "page": 98,
                "evidence": "Sản phẩm của bưu chính viễn thông là sự vận chuyển tin tức, bưu kiện, bưu phẩm, truyền dẫn thông tin điện tử,... từ nơi gửi đến nơi nhận."
            }
        ]
    },
    {
        "id": "b_dev_multi_03",
        "split": "dev",
        "category": "multihop",
        "question": "Kết hợp Bảng 29.1 (Trang 82) và Hình 29.2 (Trang 84), sản lượng than thế giới năm 2019 đạt bao nhiêu triệu tấn và than đá chiếm bao nhiêu phần trăm trong cơ cấu năng lượng?",
        "expected_answer": "Năm 2019, sản lượng than đạt 8.049 triệu tấn và than đá chiếm 27,0% trong cơ cấu sử dụng năng lượng thế giới.",
        "gold": [
            {
                "source_id": "sgk-dia-li-10-kntt",
                "page": 82,
                "evidence": "| 2019 | 8.049 | 4.478 | 27.000 |"
            }
        ]
    },
    {
        "id": "b_dev_text_01",
        "split": "dev",
        "category": "text",
        "question": "Theo nội dung bài 15 ở Trang 51, nguyên nhân chủ yếu tạo nên quy luật địa đới trên Trái Đất là gì?",
        "expected_answer": "Do dạng hình cầu của Trái Đất và góc chiếu của bức xạ mặt trời giảm dần từ xích đạo về hai cực, làm cho lượng bức xạ phân bố không đều.",
        "gold": [
            {
                "source_id": "sgk-dia-li-10-kntt",
                "page": 51,
                "evidence": "Nguyên nhân: Do dạng hình cầu của Trái Đất và góc chiếu của bức xạ mặt trời giảm dần từ xích đạo về hai cực, làm cho lượng bức xạ mặt trời phân bố không đều."
            }
        ]
    },
    {
        "id": "b_dev_text_02",
        "split": "dev",
        "category": "text",
        "question": "Theo mục b Trang 98, ngành bưu chính viễn thông bao gồm những nhóm nào và sản phẩm của ngành là gì?",
        "expected_answer": "Bao gồm hai nhóm: bưu chính và viễn thông. Sản phẩm là sự vận chuyển tin tức, bưu kiện, bưu phẩm, truyền dẫn thông tin điện tử,... từ nơi gửi đến nơi nhận.",
        "gold": [
            {
                "source_id": "sgk-dia-li-10-kntt",
                "page": 98,
                "evidence": "- Gồm hai nhóm: bưu chính (vận chuyển thư, bưu phẩm, bưu kiện, hàng hoá,...) và viễn thông (dịch vụ gửi, truyền, nhận và xử lí thông tin giữa các đối tượng sử dụng).\n- Sản phẩm của bưu chính viễn thông là sự vận chuyển tin tức, bưu kiện, bưu phẩm, truyền dẫn thông tin điện tử,... từ nơi gửi đến nơi nhận."
            }
        ]
    },
    {
        "id": "b_dev_text_03",
        "split": "dev",
        "category": "text",
        "question": "Theo bài 39 ở Trang 108, hãy nêu 4 vai trò của môi trường sống đối với con người?",
        "expected_answer": "Bốn vai trò gồm: là không gian sống; nguồn cung cấp tài nguyên thiên nhiên; nơi chứa đựng và đồng hóa chất thải; nơi lưu trữ và cung cấp thông tin.",
        "gold": [
            {
                "source_id": "sgk-dia-li-10-kntt",
                "page": 108,
                "evidence": "Vai trò của môi trường: là không gian sống của con người; là nguồn cung cấp tài nguyên thiên nhiên; là nơi chứa đựng và đồng hóa các chất thải; là nơi lưu trữ và cung cấp thông tin."
            }
        ]
    },

    # ========== TEST SPLIT (24 Answered) ==========
    # Nhóm 1: Bảng (6 câu)
    {
        "id": "b_test_table_01",
        "split": "test",
        "category": "table",
        "question": "Theo Bảng 33 (Trang 92), tỉ trọng của ngành Dịch vụ trong cơ cấu GDP thế giới năm 2019 đạt bao nhiêu phần trăm?",
        "expected_answer": "Năm 2019, tỉ trọng ngành Dịch vụ trong cơ cấu GDP thế giới đạt 67,9%.",
        "gold": [
            {
                "source_id": "sgk-dia-li-10-kntt",
                "page": 92,
                "evidence": "Tỉ trọng ngành Dịch vụ chiếm vị trí áp đảo và tăng từ 64,1% (năm 2000) lên 67,9% (năm 2019), tăng thêm 3,8%."
            }
        ]
    },
    {
        "id": "b_test_table_02",
        "split": "test",
        "category": "table",
        "question": "Theo Bảng 33, tỉ trọng của ngành Công nghiệp và xây dựng trong cơ cấu GDP thế giới thay đổi như thế nào giữa năm 2000 và năm 2019?",
        "expected_answer": "Tỉ trọng ngành Công nghiệp và xây dựng giảm từ 30,7% (năm 2000) xuống 27,9% (năm 2019), giảm 2,8%.",
        "gold": [
            {
                "source_id": "sgk-dia-li-10-kntt",
                "page": 92,
                "evidence": "Tỉ trọng Công nghiệp và xây dựng giảm mạnh nhất: từ 30,7% xuống 27,9% (giảm 2,8%)."
            }
        ]
    },
    {
        "id": "b_test_table_03",
        "split": "test",
        "category": "table",
        "question": "Theo Bảng 9, ở bán cầu Bắc, vĩ độ 70° có nhiệt độ trung bình năm và biên độ nhiệt độ năm là bao nhiêu độ C?",
        "expected_answer": "Ở vĩ độ 70° bán cầu Bắc, nhiệt độ trung bình năm là -10,4°C và biên độ nhiệt độ năm là 32,2°C.",
        "gold": [
            {
                "source_id": "sgk-dia-li-10-kntt",
                "page": 30,
                "evidence": "| 70° | -10,4 | 32,2 |"
            }
        ]
    },
    {
        "id": "b_test_table_04",
        "split": "test",
        "category": "table",
        "question": "Theo Bảng 19.1, châu lục nào có quy mô dân số lớn nhất thế giới năm 2020 và đạt bao nhiêu triệu người?",
        "expected_answer": "Châu Á có quy mô dân số lớn nhất năm 2020 đạt 4.641 triệu người (chiếm 59,5% dân số toàn cầu).",
        "gold": [
            {
                "source_id": "sgk-dia-li-10-kntt",
                "page": 56,
                "evidence": "Châu Á luôn chiếm tỉ trọng dân số lớn nhất thế giới (chiếm 59,5% dân số toàn cầu năm 2020: 4.641 / 7.795 triệu người)."
            }
        ]
    },
    {
        "id": "b_test_table_05",
        "split": "test",
        "category": "table",
        "question": "Theo Bảng 24.1, năm 2019 sản lượng lúa mì của thế giới vượt sản lượng lúa gạo bao nhiêu triệu tấn?",
        "expected_answer": "Năm 2019, sản lượng lúa mì (765,8 triệu tấn) vượt sản lượng lúa gạo (755,5 triệu tấn) là 10,3 triệu tấn.",
        "gold": [
            {
                "source_id": "sgk-dia-li-10-kntt",
                "page": 70,
                "evidence": "Năm 2019, sản lượng lúa mì (765,8 triệu tấn) vượt qua sản lượng lúa gạo (755,5 triệu tấn) với mức chênh lệch 10,3 triệu tấn."
            }
        ]
    },
    {
        "id": "b_test_table_06",
        "split": "test",
        "category": "table",
        "question": "Theo Bảng 29.1, sản lượng điện của thế giới tăng từ bao nhiêu lên bao nhiêu tỉ kWh trong giai đoạn 2000 - 2019?",
        "expected_answer": "Sản lượng điện thế giới tăng từ 15.500 tỉ kWh (năm 2000) lên 27.000 tỉ kWh (năm 2019), tăng 1,74 lần.",
        "gold": [
            {
                "source_id": "sgk-dia-li-10-kntt",
                "page": 82,
                "evidence": "Sản lượng điện tăng nhanh nhất (tăng 1,74 lần từ 15.500 tỉ kWh lên 27.000 tỉ kWh)."
            }
        ]
    },

    # Nhóm 2: Ảnh, Sơ đồ, Bản đồ (5 câu)
    {
        "id": "b_test_diag_01",
        "split": "test",
        "category": "diagram",
        "question": "Theo sơ đồ tư duy ở Trang 98, ngành bưu chính viễn thông có những vai trò chủ yếu nào đối với phát triển kinh tế?",
        "expected_answer": "Gồm 3 vai trò: cung ứng và truyền tải thông tin, vận chuyển bưu phẩm/kiện tăng năng suất lao động; hiện đại hoá, thay đổi cách tổ chức nền kinh tế; bản thân là ngành dịch vụ mang lại giá trị kinh tế cao.",
        "gold": [
            {
                "source_id": "sgk-dia-li-10-kntt",
                "page": 98,
                "evidence": "1. Với phát triển kinh tế (3 vai trò chính):\n- Cung ứng và truyền tải thông tin, vận chuyển bưu phẩm, bưu kiện góp phần tăng năng suất lao động.\n- Hiện đại hoá, thay đổi cách thức tổ chức nền kinh tế, thúc đẩy kinh tế phát triển.\n- Bản thân bưu chính viễn thông cũng là ngành dịch vụ mang lại giá trị kinh tế cao."
            }
        ]
    },
    {
        "id": "b_test_diag_02",
        "split": "test",
        "category": "diagram",
        "question": "Theo sơ đồ tư duy ở Trang 98, đối với các lĩnh vực khác, ngành bưu chính viễn thông đóng những vai trò gì?",
        "expected_answer": "Gồm 3 vai trò: đảm bảo giao lưu giữa các vùng, thúc đẩy hội nhập toàn cầu hoá; tạo thuận lợi cho quản lí hành chính; nâng cao đời sống văn hoá, tinh thần xã hội.",
        "gold": [
            {
                "source_id": "sgk-dia-li-10-kntt",
                "page": 98,
                "evidence": "2. Với các lĩnh vực khác (3 vai trò chính):\n- Đảm bảo giao lưu giữa các vùng, thúc đẩy quá trình hội nhập và toàn cầu hoá.\n- Tạo thuận lợi cho quản lí hành chính.\n- Nâng cao đời sống văn hoá, tinh thần trong xã hội."
            }
        ]
    },
    {
        "id": "b_test_diag_03",
        "split": "test",
        "category": "diagram",
        "question": "Dựa vào Hình 34.6 và nội dung trang 96, hãy kể tên 4 sân bay quốc tế vận chuyển hành khách lớn nhất thế giới năm 2019?",
        "expected_answer": "Bốn sân bay quốc tế lớn nhất năm 2019 là: Át-lan-ta (Hoa Kỳ), Bắc Kinh (Trung Quốc), Lốt An-giơ-lét (Hoa Kỳ), Đu-bai (Các Tiểu vương quốc A-rập Thống nhất).",
        "gold": [
            {
                "source_id": "sgk-dia-li-10-kntt",
                "page": 96,
                "evidence": "Bốn sân bay quốc tế vận chuyển hành khách lớn nhất năm 2019 gồm: Át-lan-ta (Hoa Kỳ), Bắc Kinh (Trung Quốc), Lốt An-giơ-lét (Hoa Kỳ), Đu-bai (Các Tiểu vương quốc A-rập Thống nhất)."
            }
        ]
    },
    {
        "id": "b_test_diag_04",
        "split": "test",
        "category": "diagram",
        "question": "Dựa vào Hình 34.6 và nội dung trang 96-97, các cảng biển có lượng hàng hóa lưu thông lớn nhất năm 2019 phân bố tập trung ở châu lục nào và gồm những cảng nào?",
        "expected_answer": "Các cảng biển lớn nhất năm 2019 đều nằm ở châu Á, gồm: Thượng Hải, Xin-ga-po, Ninh Ba - Chu Sơn, Thâm Quyến và Bu-san.",
        "gold": [
            {
                "source_id": "sgk-dia-li-10-kntt",
                "page": 96,
                "evidence": "Các cảng biển lớn nhất năm 2019 đều nằm ở châu Á: Thượng Hải (Trung Quốc), Xin-ga-po, Ninh Ba - Chu Sơn (Trung Quốc), Thâm Quyến (Trung Quốc), Bu-san (Hàn Quốc)."
            }
        ]
    },
    {
        "id": "b_test_diag_05",
        "split": "test",
        "category": "diagram",
        "question": "Theo sơ đồ cấu tạo vỏ Trái Đất ở Trang 17, vỏ Trái Đất gồm những tầng đá nào từ trên xuống dưới?",
        "expected_answer": "Gồm 3 tầng từ trên xuống: Tầng trầm tích ở trên cùng, Tầng granit ở giữa và Tầng badan ở dưới cùng.",
        "gold": [
            {
                "source_id": "sgk-dia-li-10-kntt",
                "page": 17,
                "evidence": "Sơ đồ cấu tạo vỏ Trái Đất (Trang 17):\n- Tầng trầm tích: Nằm ở trên cùng, do các vật liệu vụn, nhỏ bị nén chặt tạo thành; tầng này không liên tục và có độ dày không đều.\n- Tầng granit: Gồm các loại đá nhẹ (như đá granit và các loại đá có tính chất tương tự) tạo nên; lớp vỏ lục địa được cấu tạo chủ yếu bằng granit.\n- Tầng badan: Gồm các loại đá nặng hơn (như đá badan và các loại đá có tính chất tương tự) tạo nên; lớp vỏ đại dương cấu tạo chủ yếu bằng badan."
            }
        ]
    },

    # Nhóm 3: Biểu đồ (5 câu)
    {
        "id": "b_test_chart_01",
        "split": "test",
        "category": "chart",
        "question": "Dựa vào biểu đồ Hình 13 ở Trang 44, mùa lũ của sông Hồng tại trạm Hà Nội kéo dài trong những tháng nào và tháng nào đạt đỉnh lũ?",
        "expected_answer": "Mùa lũ kéo dài 5 tháng (tháng 6 đến tháng 10), đỉnh lũ vào tháng 8 trên 9.000 m³/s (khoảng 9.200 m³/s), chiếm khoảng 75% tổng lượng nước cả năm.",
        "gold": [
            {
                "source_id": "sgk-dia-li-10-kntt",
                "page": 44,
                "evidence": "Mùa lũ kéo dài 5 tháng (từ tháng 6 đến tháng 10), lưu lượng nước tháng cao nhất là tháng 8 (đạt trên 9.000 m³/s, đỉnh lũ khoảng 9.200 m³/s). Mùa lũ chiếm khoảng 75% tổng lượng nước cả năm."
            }
        ]
    },
    {
        "id": "b_test_chart_02",
        "split": "test",
        "category": "chart",
        "question": "Dựa vào biểu đồ nhiệt độ và lượng mưa Hình 10 (Trang 36), hãy nêu đặc điểm nhiệt độ tháng 1 và lượng mưa trung bình năm của trạm I-cu-xcơ (Nga)?",
        "expected_answer": "Tại trạm I-cu-xcơ, nhiệt độ tháng 1 thấp nhất xuống dưới -20°C (khoảng -21°C), lượng mưa trung bình năm thấp (410 mm) tập trung vào mùa hạ.",
        "gold": [
            {
                "source_id": "sgk-dia-li-10-kntt",
                "page": 36,
                "evidence": "Trạm I-cu-xcơ (Nga - Kiểu khí hậu ôn đới lục địa): Nhiệt độ tháng 7 cao nhất đạt khoảng 19°C, nhiệt độ tháng 1 thấp nhất xuống dưới -20°C (khoảng -21°C). Lượng mưa trung bình năm thấp (410 mm), mưa tập trung chủ yếu vào mùa hạ."
            }
        ]
    },
    {
        "id": "b_test_chart_03",
        "split": "test",
        "category": "chart",
        "question": "Dựa vào biểu đồ Hình 18 (Trang 54), tỉ suất gia tăng dân số tự nhiên của thế giới thay đổi như thế nào từ năm 1970 đến năm 2020?",
        "expected_answer": "Tỉ suất gia tăng dân số tự nhiên của thế giới giảm từ 2,08% (năm 1970) xuống 1,09% (năm 2020).",
        "gold": [
            {
                "source_id": "sgk-dia-li-10-kntt",
                "page": 54,
                "evidence": "Tỉ suất gia tăng dân số tự nhiên của thế giới có xu hướng giảm rõ rệt từ năm 1970 (2,08%) xuống còn 1,09% năm 2020."
            }
        ]
    },
    {
        "id": "b_test_chart_04",
        "split": "test",
        "category": "chart",
        "question": "Theo biểu đồ Hình 21 (Trang 65), cơ cấu ngành kinh tế của nhóm nước phát triển năm 2020 có tỉ trọng các ngành nông nghiệp, công nghiệp và dịch vụ lần lượt là bao nhiêu?",
        "expected_answer": "Nhóm nước phát triển năm 2020 có: Nông nghiệp chiếm 1,5%; Công nghiệp và xây dựng chiếm 24,0%; Dịch vụ chiếm 74,5%.",
        "gold": [
            {
                "source_id": "sgk-dia-li-10-kntt",
                "page": 65,
                "evidence": "Nhóm nước phát triển: Nông nghiệp, lâm nghiệp, thuỷ sản chiếm 1,5%; Công nghiệp và xây dựng chiếm 24,0%; Dịch vụ chiếm 74,5%."
            }
        ]
    },
    {
        "id": "b_test_chart_05",
        "split": "test",
        "category": "chart",
        "question": "Theo biểu đồ cơ cấu sử dụng năng lượng thế giới năm 2019 (Hình 29.2 Trang 84), nguồn năng lượng nào chiếm tỉ trọng lớn nhất và tỉ trọng đó là bao nhiêu?",
        "expected_answer": "Dầu mỏ chiếm tỉ trọng lớn nhất với 33,1% trong tổng cơ cấu sử dụng năng lượng toàn cầu năm 2019.",
        "gold": [
            {
                "source_id": "sgk-dia-li-10-kntt",
                "page": 84,
                "evidence": "- Dầu mỏ chiếm tỉ trọng lớn nhất: 33,1%\n- Than đá chiếm vị trí thứ hai: 27,0%"
            }
        ]
    },

    # Nhóm 4: Multi-hop (4 câu)
    {
        "id": "b_test_multi_01",
        "split": "test",
        "category": "multihop",
        "question": "Kết hợp số liệu Bảng 33 (Trang 92) và Bảng 34 (Trang 97), ngành dịch vụ và vận tải hành khách đường hàng không thế giới có xu hướng tăng trưởng như thế nào từ 2000 đến 2019?",
        "expected_answer": "Cả hai đều tăng mạnh: tỉ trọng ngành dịch vụ tăng từ 64,1% lên 67,9%, và lượt hành khách hàng không tăng từ 1,9 tỉ lên 4,4 tỉ lượt người.",
        "gold": [
            {
                "source_id": "sgk-dia-li-10-kntt",
                "page": 92,
                "evidence": "Tỉ trọng ngành Dịch vụ chiếm vị trí áp đảo và tăng từ 64,1% (năm 2000) lên 67,9% (năm 2019), tăng thêm 3,8%."
            }
        ]
    },
    {
        "id": "b_test_multi_02",
        "split": "test",
        "category": "multihop",
        "question": "Kết hợp Bảng 19.1 (Trang 56) và Bảng 20 (Trang 61), quy mô dân số và tỉ lệ dân thành thị toàn thế giới thay đổi như thế nào từ năm 1950 đến năm 2020?",
        "expected_answer": "Dân số thế giới tăng từ 2.536 triệu lên 7.795 triệu người, đồng thời tỉ lệ dân thành thị tăng từ 29,6% lên 56,2%.",
        "gold": [
            {
                "source_id": "sgk-dia-li-10-kntt",
                "page": 56,
                "evidence": "Toàn thế giới | 2.536 | 3.700 | 5.310 | 6.957 | 7.795 |"
            }
        ]
    },
    {
        "id": "b_test_multi_03",
        "split": "test",
        "category": "multihop",
        "question": "Dựa vào Sơ đồ cơ cấu ngành dịch vụ (Trang 91) và câu hỏi ôn tập ở Trang 92, các hoạt động giao thông vận tải, tư vấn pháp lí, bảo tàng và giáo dục được xếp vào những nhóm dịch vụ nào?",
        "expected_answer": "Giao thông vận tải và tư vấn pháp lí thuộc nhóm dịch vụ kinh doanh; bảo tàng và giáo dục thuộc nhóm dịch vụ tiêu dùng.",
        "gold": [
            {
                "source_id": "sgk-dia-li-10-kntt",
                "page": 92,
                "evidence": "Câu hỏi ôn tập liên quan: Giao thông vận tải, tư vấn pháp lí, công chứng thuộc nhóm dịch vụ kinh doanh; bảo tàng, tư vấn sức khỏe, giáo dục thuộc nhóm dịch vụ tiêu dùng."
            }
        ]
    },
    {
        "id": "b_test_multi_04",
        "split": "test",
        "category": "multihop",
        "question": "Kết hợp Bảng 24.1 (Trang 70) và Bảng 25 (Trang 75), hãy cho biết sản lượng lúa mì và sản lượng nuôi trồng thủy sản của thế giới năm 2019 đạt bao nhiêu triệu tấn?",
        "expected_answer": "Năm 2019, sản lượng lúa mì thế giới đạt 765,8 triệu tấn và sản lượng nuôi trồng thủy sản đạt 85,3 triệu tấn.",
        "gold": [
            {
                "source_id": "sgk-dia-li-10-kntt",
                "page": 70,
                "evidence": "| Lúa mì | 585,8 | 626,9 | 653,7 | 741,7 | 765,8 |"
            }
        ]
    },

    # Nhóm 5: Text (4 câu)
    {
        "id": "b_test_text_01",
        "split": "test",
        "category": "text",
        "question": "Khái niệm đô thị hóa được định nghĩa như thế nào trong bài 20 (Trang 60) sách giáo khoa Địa lí 10?",
        "expected_answer": "Đô thị hóa là một quá trình kinh tế - xã hội mà biểu hiện là sự tăng nhanh về số lượng và quy mô của các điểm dân cư đô thị, sự tập trung dân cư trong các thành phố, đặc biệt là các thành phố lớn và sự phổ biến rộng rãi lối sống thành thị.",
        "gold": [
            {
                "source_id": "sgk-dia-li-10-kntt",
                "page": 60,
                "evidence": "Đô thị hóa là một quá trình kinh tế - xã hội mà biểu hiện là sự tăng nhanh về số lượng và quy mô của các điểm dân cư đô thị, sự tập trung dân cư trong các thành phố, đặc biệt là các thành phố lớn và sự phổ biến rộng rãi lối sống thành thị."
            }
        ]
    },
    {
        "id": "b_test_text_02",
        "split": "test",
        "category": "text",
        "question": "Theo nội dung bài 28 ở Trang 78, quá trình sản xuất công nghiệp gồm có hai giai đoạn cơ bản nào?",
        "expected_answer": "Giai đoạn 1 là tác động vào đối tượng lao động để khai thác tài nguyên thiên nhiên; Giai đoạn 2 là chế biến nguyên liệu thành tư liệu sản xuất và vật phẩm tiêu dùng.",
        "gold": [
            {
                "source_id": "sgk-dia-li-10-kntt",
                "page": 78,
                "evidence": "Giai đoạn 1 là tác động vào đối tượng lao động để khai thác tài nguyên thiên nhiên; Giai đoạn 2 là chế biến nguyên liệu thành tư liệu sản xuất và vật phẩm tiêu dùng."
            }
        ]
    },
    {
        "id": "b_test_text_03",
        "split": "test",
        "category": "text",
        "question": "Theo nội dung bài 37 (Trang 105), cán cân thương mại là gì và khi nào một quốc gia được coi là xuất siêu?",
        "expected_answer": "Cán cân thương mại là hiệu số giữa giá trị xuất khẩu và giá trị nhập khẩu hàng hóa, dịch vụ. Khi giá trị xuất khẩu lớn hơn nhập khẩu thì gọi là xuất siêu (cán cân thương mại dương).",
        "gold": [
            {
                "source_id": "sgk-dia-li-10-kntt",
                "page": 105,
                "evidence": "Cán cân thương mại là hiệu số giữa giá trị xuất khẩu và giá trị nhập khẩu hàng hóa, dịch vụ của một quốc gia trong một thời kỳ nhất định (thường là một năm).\n- Khi giá trị xuất khẩu lớn hơn giá trị nhập khẩu: cán cân thương mại dương, quốc gia đó xuất siêu."
            }
        ]
    },
    {
        "id": "b_test_text_04",
        "split": "test",
        "category": "text",
        "question": "Thuật ngữ Tăng trưởng xanh được định nghĩa như thế nào trong bài 40 ở Trang 111?",
        "expected_answer": "Tăng trưởng xanh là phương thức phát triển kinh tế bền vững, nhấn mạnh vào việc thúc đẩy tăng trưởng và phát triển kinh tế, đồng thời bảo tồn các tài sản tự nhiên để tiếp tục cung cấp các tài nguyên và dịch vụ môi trường cho cuộc sống con người.",
        "gold": [
            {
                "source_id": "sgk-dia-li-10-kntt",
                "page": 111,
                "evidence": "Tăng trưởng xanh là phương thức phát triển kinh tế bền vững, nhấn mạnh vào việc thúc đẩy tăng trưởng và phát triển kinh tế, đồng thời bảo tồn các tài sản tự nhiên để tiếp tục cung cấp các tài nguyên và dịch vụ môi trường cho cuộc sống con người."
            }
        ]
    }
]

# Write questions.json
questions_file = BONUS_DIR / "questions.json"
with open(questions_file, "w", encoding="utf-8") as f:
    json.dump(questions_data, f, ensure_ascii=False, indent=2)

print(f"Saved {len(questions_data)} answerable questions to {questions_file}")

# Validate chunks against answerable questions per starter protocol!
with open(chunks_file, "r", encoding="utf-8") as f:
    chunks = json.load(f)

validate(chunks, [q for q in questions_data if q["split"] == "dev"])
validate(chunks, [q for q in questions_data if q["split"] == "test"])
print("Validation PASSED for both dev and test answerable questions!")


# ----------------- AGENT CASES (INCLUDING UNANSWERABLE / ABSTENTION) -----------------
agent_cases = []

# Add all answerable questions as search_and_answer cases
chunk_map = {c["id"]: c for c in chunks}
target_chunk_lookup = {
    "b_dev_table_01": "sgk10_p58_table19_2_dotuoi",
    "b_dev_table_02": "sgk10_p61_table20_dothikoa",
    "b_dev_table_03": "sgk10_p75_table25_thuysan",
    "b_dev_diag_01": "sgk10_p19_map_gio",
    "b_dev_diag_02": "sgk10_p23_map_kientao",
    "b_dev_diag_03": "sgk10_p63_diagram_nguonluc",
    "b_dev_chart_01": "sgk10_p59_chart_thapdanso",
    "b_dev_chart_02": "sgk10_p36_chart_bieudokhihau",
    "b_dev_chart_03": "sgk10_p84_chart_nangluong",
    "b_dev_multi_01": "sgk10_p102_table36_dulich",
    "b_dev_multi_02": "sgk10_p98_diagram_buuchinh",
    "b_dev_multi_03": "sgk10_p82_table29_nangluong",
    "b_dev_text_01": "sgk10_p51_text_quyluatdiadoi",
    "b_dev_text_02": "sgk10_p98_diagram_buuchinh",
    "b_dev_text_03": "sgk10_p108_diagram_moitruong",
    "b_test_table_01": "sgk10_p92_table33_gdp",
    "b_test_table_02": "sgk10_p92_table33_gdp",
    "b_test_table_03": "sgk10_p30_table9_nhietdo",
    "b_test_table_04": "sgk10_p56_table19_danso",
    "b_test_table_05": "sgk10_p70_table24_1_luagao",
    "b_test_table_06": "sgk10_p82_table29_nangluong",
    "b_test_diag_01": "sgk10_p98_diagram_buuchinh",
    "b_test_diag_02": "sgk10_p98_diagram_buuchinh",
    "b_test_diag_03": "sgk10_p96_map_hangkhong_bien",
    "b_test_diag_04": "sgk10_p96_map_hangkhong_bien",
    "b_test_diag_05": "sgk10_p17_diagram_votraidat",
    "b_test_chart_01": "sgk10_p44_chart_songhong",
    "b_test_chart_02": "sgk10_p36_chart_bieudokhihau",
    "b_test_chart_03": "sgk10_p54_chart_giatangdanso",
    "b_test_chart_04": "sgk10_p65_chart_cocaukinhte",
    "b_test_chart_05": "sgk10_p84_chart_nangluong",
    "b_test_multi_01": "sgk10_p92_table33_gdp",
    "b_test_multi_02": "sgk10_p56_table19_danso",
    "b_test_multi_03": "sgk10_p92_table33_gdp",
    "b_test_multi_04": "sgk10_p70_table24_1_luagao",
    "b_test_text_01": "sgk10_p60_text_dothikoa",
    "b_test_text_02": "sgk10_p78_text_congnghiep",
    "b_test_text_03": "sgk10_p105_text_thuongmai_can_can",
    "b_test_text_04": "sgk10_p111_text_tangtruongxanh"
}

for q in questions_data:
    agent_cases.append({
        "id": q["id"],
        "split": q["split"],
        "category": q["category"],
        "question": q["question"],
        "answerable": True,
        "expected_behavior": "search_and_answer",
        "target_chunk_id": target_chunk_lookup[q["id"]],
        "expected_answer": q["expected_answer"]
    })

# Add Dev Abstention Cases (3 cases)
dev_abs = [
    {
        "id": "b_dev_abs_01",
        "split": "dev",
        "category": "abstention",
        "question": "Chiến lược phát triển kinh tế biển Việt Nam đến năm 2030 theo Nghị quyết số 36-NQ/TW xác định những khâu đột phá nào?",
        "answerable": False,
        "expected_behavior": "search_and_abstain",
        "absence_reason": "Tài liệu SGK Địa lí 10 chỉ giảng dạy địa lí thế giới và tự nhiên đại cương, hoàn toàn không có nội dung Nghị quyết 36-NQ/TW về kinh tế biển Việt Nam."
    },
    {
        "id": "b_dev_abs_02",
        "split": "dev",
        "category": "abstention",
        "question": "Tiêu chí và thang điểm phân loại đô thị loại đặc biệt của Hà Nội và TP. Hồ Chí Minh theo Nghị quyết 1210/2016/UBTVQH13?",
        "answerable": False,
        "expected_behavior": "search_and_abstain",
        "absence_reason": "Tài liệu chỉ nêu khái niệm và đặc điểm chung của đô thị hóa thế giới, không có tiêu chí phân loại đô thị hành chính Việt Nam theo Nghị quyết 1210."
    },
    {
        "id": "b_dev_abs_03",
        "split": "dev",
        "category": "abstention",
        "question": "Phương pháp tính toán ma trận trọng số không gian Moran I bằng thư viện GeoPandas và PySAL trong phân tích GIS địa lí?",
        "answerable": False,
        "expected_behavior": "search_and_abstain",
        "absence_reason": "Tài liệu sách giáo khoa phổ thông không chứa kiến thức lập trình phân tích không gian GIS hay mã nguồn GeoPandas."
    }
]

# Add Test Abstention Cases (6 cases)
test_abs = [
    {
        "id": "b_test_abs_01",
        "split": "test",
        "category": "abstention",
        "question": "Chương trình phân vùng kinh tế trọng điểm Bắc Bộ của Việt Nam theo Nghị quyết 30-NQ/TW được triển khai cụ thể ra sao?",
        "answerable": False,
        "expected_behavior": "search_and_abstain",
        "absence_reason": "Tài liệu SGK Địa lí 10 Kết nối tri thức là chương trình địa lí đại cương thế giới, không dạy về quy hoạch vùng kinh tế trọng điểm Bắc Bộ lớp 12."
    },
    {
        "id": "b_test_abs_02",
        "split": "test",
        "category": "abstention",
        "question": "Mô hình phát triển kinh tế nông thôn theo tiêu chuẩn OCOP (Mỗi xã một sản phẩm) tại Đồng bằng sông Cửu Long gồm những bước nào?",
        "answerable": False,
        "expected_behavior": "search_and_abstain",
        "absence_reason": "Tài liệu không chứa thông tin về chương trình OCOP hay chính sách nông thôn mới tại Đồng bằng sông Cửu Long."
    },
    {
        "id": "b_test_abs_03",
        "split": "test",
        "category": "abstention",
        "question": "Công thức tính chỉ số phát triển con người hiệu chỉnh theo bất bình đẳng (IHDI) của UNDP áp dụng cho các nền kinh tế?",
        "answerable": False,
        "expected_behavior": "search_and_abstain",
        "absence_reason": "Tài liệu chỉ giới thiệu các chỉ số GDP, GNI cơ bản, hoàn toàn không trình bày công thức toán học chi tiết của chỉ số IHDI."
    },
    {
        "id": "b_test_abs_04",
        "split": "test",
        "category": "abstention",
        "question": "Quy hoạch chi tiết hướng tuyến đường sắt tốc độ cao Bắc - Nam khổ 1435 mm với tốc độ thiết kế 350 km/h được phê duyệt như thế nào?",
        "answerable": False,
        "expected_behavior": "search_and_abstain",
        "absence_reason": "Tài liệu chỉ phân tích mạng lưới đường biển và hàng không thế giới năm 2019, không có dự án đường sắt tốc độ cao Việt Nam."
    },
    {
        "id": "b_test_abs_05",
        "split": "test",
        "category": "abstention",
        "question": "Hiệp định Thương mại Tự do Việt Nam - EU (EVFTA) quy định lộ trình cắt giảm thuế quan xuất khẩu hàng dệt may như thế nào?",
        "answerable": False,
        "expected_behavior": "search_and_abstain",
        "absence_reason": "Tài liệu chỉ thảo luận về vai trò ngành thương mại và cán cân xuất nhập khẩu nói chung, không chứa điều khoản thuế quan EVFTA."
    },
    {
        "id": "b_test_abs_06",
        "split": "test",
        "category": "abstention",
        "question": "Mô hình mạng nơ-ron LSTM nào được dùng để dự báo lưu lượng dòng chảy sông Mê Công tại trạm Kratie trong mùa cạn?",
        "answerable": False,
        "expected_behavior": "search_and_abstain",
        "absence_reason": "Tài liệu chỉ giải thích chế độ nước sông tự nhiên, không đề cập đến mô hình trí tuệ nhân tạo hay thuật toán LSTM dự báo thủy văn."
    }
]

agent_cases.extend(dev_abs)
agent_cases.extend(test_abs)

cases_file = BONUS_DIR / "agent_cases.json"
with open(cases_file, "w", encoding="utf-8") as f:
    json.dump(agent_cases, f, ensure_ascii=False, indent=2)

print(f"Saved {len(agent_cases)} agent cases to {cases_file}")
print("Dev Cases count:", len([c for c in agent_cases if c["split"] == "dev"]))
print("Test Cases count:", len([c for c in agent_cases if c["split"] == "test"]))
