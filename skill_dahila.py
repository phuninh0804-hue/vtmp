import random
import time

def slow_print(text, delay=0.03):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

# Kiểm tra tên nhân vật
def check_character():
    name = input("Hãy nhập đúng tên nhân vật để sử dụng skill: ").strip()
    if name.lower() == "dahila":
        slow_print("✔ Bạn đã nhập đúng tên nhân vật: Dahlia!\n")
        return True
    else:
        slow_print("✘ Sai tên! Chỉ đúng 'Dahlia' mới được kích hoạt skill.")
        return False

class Enemy:
    def __init__(self, name, hp, max_hp):
        self.name = name
        self.hp = hp
        self.max_hp = max_hp
        self.heo_tan = False

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0

    def apply_heo_tan(self):
        self.heo_tan = True
        slow_print(f"⛓ {self.name} nhận hiệu ứng 'Héo Tàn'!")

    def check_heo_tan(self, dahlia_attack):
        if self.heo_tan and self.hp <= self.max_hp * 0.1:
            slow_print(f"💀 {self.name} đã bị 'Héo Tàn' kích hoạt! Bị hạ gục lập tức!")
            self.hp = 0
            self.heo_tan = False
            return True
        return False

class Ally:
    def __init__(self, name):
        self.name = name
        self.dong_vu = False
        self.alive = True

    def apply_dong_vu(self):
        self.dong_vu = True
        slow_print(f"⭐ {self.name} nhận hiệu ứng 'Đồng Vũ'!")

    def remove_dong_vu(self):
        self.dong_vu = False

def simulate_skill():
    slow_print("🌙 Kích hoạt kỹ năng: Ai Đang Sợ Hãi Constance?\n", 0.04)
    allies = [Ally("Eve"), Ally("Mira"), Ally("Rex")]
    enemies = [Enemy("Goblin", 80, 100), Enemy("Ogre", 150, 200), Enemy("Spirit", 60, 80)]

    # Chọn đồng minh nhận Đồng Vũ
    print("Chọn đồng minh để nhận 'Đồng Vũ':")
    for i, ally in enumerate(allies):
        print(f"{i+1}. {ally.name}")
    ally_idx = int(input("Nhập số: ")) - 1
    chosen_ally = allies[ally_idx]
    chosen_ally.apply_dong_vu()

    effect_round = 1

    while True:
        slow_print(f"\n🌀 Hiệp {effect_round}:")
        if not chosen_ally.alive:
            slow_print(f"⚠ {chosen_ally.name} đã bị hạ gục!")
            chosen_ally.remove_dong_vu()
            slow_print("🔁 Dahlia phải mất 1 lượt để chọn lại 'Đồng Vũ'!")
            # Mất 1 lượt, chọn lại
            print("Chọn lại đồng minh để nhận 'Đồng Vũ':")
            for i, ally in enumerate(allies):
                if ally.alive:
                    print(f"{i+1}. {ally.name}")
            ally_idx = int(input("Nhập số: ")) - 1
            chosen_ally = allies[ally_idx]
            chosen_ally.apply_dong_vu()
            continue

        # Đồng minh tấn công
        target_list = [e for e in enemies if e.hp > 0]
        if not target_list:
            slow_print("🎉 Tất cả kẻ địch đã bị tiêu diệt! Kết thúc.")
            break

        target = random.choice(target_list)
        slow_print(f"{chosen_ally.name} tấn công {target.name}!", 0.04)
        basic_damage = 20
        extra = 0
        if chosen_ally.dong_vu and target.hp < target.max_hp * 0.75:
            extra = 10
            slow_print(f"🔥 \"Đồng Vũ\" hiệu lực! +10 sát thương vào {target.name}!", 0.04)
        total_damage = basic_damage + extra
        target.take_damage(total_damage)
        slow_print(f"💢 {target.name} mất {total_damage} máu (Còn lại: {target.hp}/{target.max_hp})", 0.04)

        if extra > 0:
            # Dahlia tấn công ngẫu nhiên và gắn Héo Tàn
            attack_enemy = random.choice(target_list)
            dahlia_dmg = 25
            slow_print(f" Dahlia tấn công ngẫu nhiên {attack_enemy.name} (gây {dahlia_dmg} sát thương)!", 0.04)
            attack_enemy.take_damage(dahlia_dmg)
            attack_enemy.apply_heo_tan()
            slow_print(f"{attack_enemy.name} còn {attack_enemy.hp}/{attack_enemy.max_hp} HP.", 0.04)
            # Kiểm tra hiệu ứng Héo Tàn
            for e in enemies:
                if e.check_heo_tan(lambda: 25):
                    # Nếu bị hạ gục bởi Héo Tàn, Dahlia lại phát động tấn công tương tự
                    next_targets = [enemy for enemy in enemies if enemy.hp > 0]
                    if next_targets:
                        chain_enemy = random.choice(next_targets)
                        slow_print(f"🌹 Dahlia tấn công dây chuyền: {chain_enemy.name} (25 sát thương)!", 0.04)
                        chain_enemy.take_damage(dahlia_dmg)
                        chain_enemy.apply_heo_tan()

        # Kiểm tra ally chết giả lập
        if random.random() < 0.2:
            slow_print(f"💢 {chosen_ally.name} bị tấn công phản đòn và gục ngã!")
            chosen_ally.alive = False

        effect_round += 1

        # Hiệu ứng kéo dài 1 hiệp
        chosen_ally.remove_dong_vu()
        slow_print(f"Hiệu ứng \"Đồng Vũ\" kết thúc cho {chosen_ally.name}.\n{'-'*40}")
        continue_run = input("Tiếp tục trận? (y/n): ").lower()
        if continue_run != 'y':
            break

if __name__ == "__main__":
    if check_character():
        simulate_skill()