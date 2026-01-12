from __future__ import annotations


def validate_city(city: str) -> str:
    """
    Kiểm tra và chuẩn hoá tên thành phố người dùng nhập.
    - Không được rỗng
    - Xoá khoảng trắng đầu/cuối
    - Gom nhiều khoảng trắng liên tiếp thành 1 khoảng trắng
    """
    c = city.strip()
    if not c:
        raise ValueError("Tên thành phố không được để trống.")

    # "  Ho   Chi   Minh  " -> "Ho Chi Minh"
    c = " ".join(c.split())
    return c
