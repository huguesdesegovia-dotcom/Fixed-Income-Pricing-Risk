def bond_price(face_value, coupon_rate, years_to_maturity, yield_rate):
    coupon = face_value * coupon_rate
    price = 0

    for t in range(1, years_to_maturity + 1):
        price += coupon / (1 + yield_rate) ** t

    price += face_value / (1 + yield_rate) ** years_to_maturity

    return price

if __name__ == "__main__":
    F = 100
    c = 0.05
    T = 5
    y = 0.05

    price = bond_price(F, c, T, y)
    print("Bond price =", price)