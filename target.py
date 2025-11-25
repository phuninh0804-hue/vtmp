
monsters_hp = [100, 80, 120]  # máu của quái 1, 2, 3

def attack(monster_index, damage):
    idx = monster_index - 1
    if 0 <= idx < len(monsters_hp):
        if monsters_hp[idx] == 0:
            print(f"Quái số {monster_index} đã chết!")
            return
        monsters_hp[idx] -= damage
        if monsters_hp[idx] < 0:
            monsters_hp[idx] = 0
        print(f"Quái số {monster_index} bị trừ {damage} máu. Máu còn lại: {monsters_hp[idx]}")
    else:
        print("Quái không tồn tại!")

def all_monsters_dead():
    return all(hp == 0 for hp in monsters_hp)

while True:
    print("Trạng thái máu các quái:", monsters_hp)
    if all_monsters_dead():
        print("Tất cả quái đã chết. Kết thúc!")
        break
    try:
        monster = int(input(f"Chọn quái để tấn công (1-{len(monsters_hp)}): "))
        dmg = int(input("Nhập lượng sát thương: "))
        attack(monster, dmg)
    except ValueError:
        print("Vui lòng nhập số hợp lệ!")