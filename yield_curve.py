def bootstrap_spot_rates(bonds):
    spot_rates = []

    for i, bond in enumerate(bonds):
        maturity = bond["maturity"]
        coupon = bond["face_value"] * bond["coupon_rate"]
        price = bond["price"]
        face_value = bond["face_value"]

        known_cash_flows_pv = 0
        for t in range(1, maturity):
            known_cash_flows_pv += coupon / (1 + spot_rates[t - 1]) ** t

        final_cash_flow = coupon + face_value
        remaining_value = price - known_cash_flows_pv

        spot_rate = (final_cash_flow / remaining_value) ** (1 / maturity) - 1
        spot_rates.append(spot_rate)

    return spot_rates


if __name__ == "__main__":
    bonds = [
        {"maturity": 1, "coupon_rate": 0.0, "price": 96.15, "face_value": 100},
        {"maturity": 2, "coupon_rate": 0.06, "price": 100.50, "face_value": 100},
        {"maturity": 3, "coupon_rate": 0.05, "price": 97.80, "face_value": 100},
    ]

    rates = bootstrap_spot_rates(bonds)

    for i, rate in enumerate(rates, start=1):
        print(f"z{i} = {rate * 100:.2f}%")