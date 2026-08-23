def bond_price(face_value, coupon_rate, years_to_maturity, yield_rate):
    coupon = face_value * coupon_rate
    price = 0

    for t in range(1, years_to_maturity + 1):
        price += coupon / (1 + yield_rate) ** t

    price += face_value / (1 + yield_rate) ** years_to_maturity

    return price


def bond_ytm(price, face_value, coupon_rate, years_to_maturity):
    low = 0.0001
    high = 1.0
    tolerance = 1e-6

    while high - low > tolerance:
        mid = (low + high) / 2
        calculated_price = bond_price(face_value, coupon_rate, years_to_maturity, mid)

        if calculated_price > price:
            low = mid
        else:
            high = mid

    return (low + high) / 2


def macaulay_duration(face_value, coupon_rate, years_to_maturity, yield_rate):
    coupon = face_value * coupon_rate
    price = bond_price(face_value, coupon_rate, years_to_maturity, yield_rate)

    weighted_sum = 0
    for t in range(1, years_to_maturity + 1):
        cash_flow = coupon
        if t == years_to_maturity:
            cash_flow += face_value
        weighted_sum += t * cash_flow / (1 + yield_rate) ** t

    return weighted_sum / price


def modified_duration(face_value, coupon_rate, years_to_maturity, yield_rate):
    mac_dur = macaulay_duration(face_value, coupon_rate, years_to_maturity, yield_rate)
    return mac_dur / (1 + yield_rate)


def convexity(face_value, coupon_rate, years_to_maturity, yield_rate):
    coupon = face_value * coupon_rate
    price = bond_price(face_value, coupon_rate, years_to_maturity, yield_rate)

    weighted_sum = 0
    for t in range(1, years_to_maturity + 1):
        cash_flow = coupon
        if t == years_to_maturity:
            cash_flow += face_value
        weighted_sum += t * (t + 1) * cash_flow / (1 + yield_rate) ** t

    return weighted_sum / (price * (1 + yield_rate) ** 2)

if __name__ == "__main__":
    F = 100
    c = 0.05
    T = 5
    y = 0.05

    price = bond_price(F, c, T, y)
    print("Bond price =", price)

    ytm = bond_ytm(price, F, c, T)
    print("YTM =", ytm)

    mac_dur = macaulay_duration(F, c, T, y)
    mod_dur = modified_duration(F, c, T, y)
    print("Macaulay Duration =", mac_dur)
    print("Modified Duration =", mod_dur)
    conv = convexity(F, c, T, y)
    print("Convexity =", conv)