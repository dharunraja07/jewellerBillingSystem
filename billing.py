def calculate_item(weight, gold_rate, wastage_percent, making_charge_total):
    gold_value = weight * gold_rate
    wastage_amount = gold_value * (wastage_percent / 100)

    total = gold_value + wastage_amount + making_charge_total

    return {
        "gold_value": gold_value,
        "wastage_amount": wastage_amount,
        "making_charge": making_charge_total,
        "total": total
    }