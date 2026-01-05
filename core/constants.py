# core/constants.py

EPS = 1e-6

RAW_NEEDED = [
    "BALANCE",
    "CREDIT_LIMIT",
    "PAYMENTS",
    "MINIMUM_PAYMENTS",
    "TENURE",
    "PURCHASES",
    "CASH_ADVANCE",
    "ONEOFF_PURCHASES",
    "INSTALLMENTS_PURCHASES",
    "BALANCE_FREQUENCY",
    "PURCHASES_FREQUENCY",
    "ONEOFF_PURCHASES_FREQUENCY",
    "PURCHASES_INSTALLMENTS_FREQUENCY",
    "CASH_ADVANCE_FREQUENCY",
    "CASH_ADVANCE_TRX",
    "PURCHASES_TRX",
    "PRC_FULL_PAYMENT",
]

# Nhãn cụm tiếng Việt
CLUSTER_LABELS_VI = {
    0: "Cụm 0 — Nhóm giá trị cao (chi tiêu mạnh, trả nợ tốt)",
    1: "Cụm 1 — Nhóm dùng thẻ thất thường (hạn mức cao, hành vi không đều)",
    2: "Cụm 2 — Nhóm ổn định (chi tiêu vừa phải, trả nợ đều)",
    3: "Cụm 3 — Nhóm rủi ro cao (trả nợ yếu / có xu hướng quay vòng)",
}

# Hành vi nâng cao
ADVANCED_HELP = {
    "BALANCE_FREQUENCY": "Tần suất cập nhật số dư (0–1). 1 = cập nhật thường xuyên.",
    "PURCHASES_FREQUENCY": "Tần suất phát sinh mua sắm (0–1). 1 = mua sắm thường xuyên.",
    "ONEOFF_PURCHASES_FREQUENCY": "Tần suất mua sắm một lần (0–1). 1 = thường xuyên mua 1 lần giá trị lớn.",
    "PURCHASES_INSTALLMENTS_FREQUENCY": "Tần suất mua trả góp (0–1). 1 = thường xuyên mua trả góp.",
    "CASH_ADVANCE_FREQUENCY": "Tần suất ứng/rút tiền mặt (0–1). 1 = rút tiền mặt thường xuyên.",
    "CASH_ADVANCE_TRX": "Số giao dịch rút tiền mặt (đếm số lần rút).",
    "PURCHASES_TRX": "Số giao dịch mua sắm (đếm số lần mua).",
    "PRC_FULL_PAYMENT": "Tỷ lệ thanh toán đủ toàn bộ dư nợ (0–1). 1 = luôn trả full.",
}

# Header mẫu cho input dán từ Excel
SAMPLE_HEADER = (
    "CUST_ID\tBALANCE\tBALANCE_FREQUENCY\tPURCHASES\tONEOFF_PURCHASES\tINSTALLMENTS_PURCHASES\t"
    "CASH_ADVANCE\tPURCHASES_FREQUENCY\tONEOFF_PURCHASES_FREQUENCY\tPURCHASES_INSTALLMENTS_FREQUENCY\t"
    "CASH_ADVANCE_FREQUENCY\tCASH_ADVANCE_TRX\tPURCHASES_TRX\tCREDIT_LIMIT\tPAYMENTS\t"
    "MINIMUM_PAYMENTS\tPRC_FULL_PAYMENT\tTENURE"
)
