
def get_yes_no(prompt):
    while True:
        ans = input(prompt + " (y/n): ").strip().lower()
        if ans in ['y', 'n']:
            return ans == 'y'
        print("Chỉ nhập y hoặc n!")

# Bước 1: Nhập sát thương cơ bản
base_damage = float(input("Nhập sát thương cơ bản: "))

damage = base_damage

# Bước 2: Xét crit
if get_yes_no("Có crit không?"):
    damage *= 1.5

# Bước 3: Buff Cyrene
if get_yes_no("Có buff Cyrene không?"):
    damage *= 1.5

# Bước 4: Vũ khí blade
if get_yes_no("Có phải dùng vũ khí blade không?"):
    hp_base = float(input("Nhập HP cơ bản: "))
    damage += base_damage * (0.2 * hp_base / 100)  # 20% HP cơ bản thêm vào sát thương

print(f"Sát thương cuối cùng: {damage:.2f}")