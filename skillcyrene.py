import time
import random

def slow_print(text, delay=0.03):
    for ch in text:
        print(ch, end='', flush=True)
        time.sleep(delay)
    print()

def check_character():
    name = input("Hãy nhập đúng tên nhân vật để sử dụng kỹ năng: ").strip()
    if name.lower() == "cyrene":
        slow_print("✔ Bạn đã nhập đúng tên nhân vật: Cyrene!\n", 0.03)
        return True
    else:
        slow_print("✘ Sai tên! Chỉ đúng 'Cyrene' mới được kích hoạt skill!", 0.03)
        return False

class Enemy:
    def __init__(self, name, max_hp):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0

class Ally:
    def __init__(self, name):
        self.name = name
        self.buff = False
        self.is_chrysos_activated = False

    def activate_chrysos(self):
        # Được người chơi xác nhận là hậu duệ Chrysos
        self.is_chrysos_activated = True

    def deactivate_chrysos(self):
        self.is_chrysos_activated = False

    def apply_buff(self):
        self.buff = True
        slow_print(f"🌟 {self.name} nhận buff: +50% sát thương & gây sát thương theo %HP địch!", 0.035)
        if self.is_chrysos_activated:
            slow_print(f"💛 {self.name} là Hậu Duệ Chrysos! Kích hoạt hiệu ứng đặc biệt!", 0.04)

    def remove_buff(self):
        self.buff = False
        self.deactivate_chrysos()

class CyreneSkill:
    def __init__(self, allies, enemies):
        self.charge = 0
        self.activated = False
        self.buff_target = None
        self.buff_rounds = 0
        self.allies = allies
        self.enemies = enemies

    def action(self, actor_name):
        self.charge += 1
        slow_print(f"⚡ {actor_name} hành động! Năng lượng Cyrene: {self.charge}/12", 0.025)

    def can_activate(self):
        return self.charge >= 12 and not self.activated

    def activate(self):
        slow_print("\n🌼 Cyrene kích hoạt 'Người Yêu Dấu'!", 0.033)
        slow_print("✨ Toàn đội có thể kích hoạt Skill hoặc Passive mà không cần điều kiện (chỉ 1 lần/trận)!", 0.034)
        self.charge = 0
        self.activated = True
        for ally in self.allies:
            slow_print(f"✨ {ally.name}: Có thể kích hoạt Skill hoặc Passive tự do trong lượt này!", 0.02)
        # Bổ sung hỏi buff bằng tên và xác nhận là hậu duệ Chrysos
        print("\nCác đồng minh trên sân:")
        for a in self.allies:
            print("-", a.name)
        while True:
            buff_name = input("Nhập tên nhân vật bạn muốn buff: ").strip()
            found = None
            for a in self.allies:
                if a.name.lower() == buff_name.lower():
                    found = a
                    break
            if not found:
                print("Không tìm thấy tên đồng minh. Hãy nhập lại đúng tên.")
                continue
            yn = input(f"Nhân vật \"{found.name}\" có phải là Hậu Duệ Chrysos không? (y/n): ").strip().lower()
            if yn == "y":
                found.activate_chrysos()
            else:
                found.deactivate_chrysos()
            self.buff_target = found
            found.apply_buff()
            self.buff_rounds = 3
            break

    def ally_attack(self, ally, enemy):
        base_dmg = 22
        if ally.buff:
            extra = int(base_dmg * 0.5)
            percent = 2 + max(0, (enemy.max_hp - 93)//7)
            hp_dmg = int(enemy.max_hp * percent / 100)
            total = base_dmg + extra + hp_dmg
            slow_print(f"🔥 {ally.name} (buffed): {base_dmg}+{extra}(+50% buff)+{hp_dmg}({percent}%HP) = {total} sát thương!", 0.04)
            if ally.is_chrysos_activated:
                slow_print(f"💫 Hiệu ứng đặc biệt: {ally.name} phát ánh sáng Chrysos và lực sát thương mạnh mẽ vang vọng!", 0.04)
            enemy.take_damage(total)
        else:
            slow_print(f"{ally.name} tấn công thường {enemy.name}, gây {base_dmg} sát thương.", 0.026)
            enemy.take_damage(base_dmg)
        slow_print(f"🩸 {enemy.name}: {enemy.hp}/{enemy.max_hp}\n", 0.02)

    def end_turn(self):
        # Giảm buff nếu có
        if self.buff_target and self.buff_target.buff:
            self.buff_rounds -= 1
            if self.buff_rounds == 0:
                slow_print(f"⏳ Buff trên {self.buff_target.name} đã hết tác dụng.", 0.03)
                self.buff_target.remove_buff()
                self.buff_target = None

def simulate_skill():
    allies = [
        Ally("Alice"),
        Ally("Bob"),
        Ally("Hậu Duệ Chrysos - Irios")
    ]
    enemies = [
        Enemy("Goblin", 120),
        Enemy("Guardian", 170),
        Enemy("Spirit", 105)
    ]
    cyrene = "Cyrene"
    skill = CyreneSkill(allies, enemies)
    turn = 1
    while True:
        slow_print(f"\n=== Hiệp {turn} ===", 0.042)
        # Mỗi khi đồng đội và Cyrene lần lượt hành động
        for actor in [cyrene] + [a.name for a in allies if a.buff or random.random() > 0.22]:
            skill.action(actor)
            if skill.can_activate():
                activate = input("\nKích hoạt 'Người Yêu Dấu'? (y/n): ").lower()
                if activate == 'y':
                    skill.activate()
                    break

        # đồng đội tấn công
        for ally in allies:
            if ally.buff or random.random() > 0.3:
                targets = [e for e in enemies if e.hp > 0]
                if not targets:
                    break
                target = random.choice(targets)
                skill.ally_attack(ally, target)

        skill.end_turn()
        if all(e.hp == 0 for e in enemies):
            slow_print("🎊 Toàn bộ kẻ địch đã bị đánh bại! Kết thúc trận.\n", 0.033)
            break
        turn += 1
        if input("Tiếp tục hiệp mới? (y/n): ").lower() != "y":
            break

if __name__ == "__main__":
    print("== Mô phỏng skill Người Yêu Dấu của Cyrene ==")
    if check_character():
        simulate_skill()