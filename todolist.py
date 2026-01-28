import sqlite3
import os
from datetime import datetime, timedelta
import json

# Database setup
DATABASE_FILE = "tasks.db"

class TodoApp:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.setup_database()
    
    def setup_database(self):
        """Create database and tables if they don't exist"""
        self.conn = sqlite3.connect(DATABASE_FILE)
        self.cursor = self.conn.cursor()
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                deadline TEXT NOT NULL,
                priority TEXT DEFAULT 'Normal',
                status TEXT DEFAULT 'Belum Selesai',
                created_at TEXT NOT NULL
            )
        ''')
        
        self.conn.commit()
    
    def add_task(self, title, deadline, priority="Normal"):
        """Add a new task to the database"""
        try:
            # Validate deadline format (YYYY-MM-DD)
            datetime.strptime(deadline, "%Y-%m-%d")
            
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            self.cursor.execute('''
                INSERT INTO tasks (title, deadline, priority, created_at)
                VALUES (?, ?, ?, ?)
            ''', (title, deadline, priority, created_at))
            
            self.conn.commit()
            print(f"✓ Task '{title}' berhasil ditambahkan!")
            return True
        except ValueError:
            print("✗ Format deadline tidak valid! Gunakan format YYYY-MM-DD")
            return False
        except Exception as e:
            print(f"✗ Terjadi kesalahan: {e}")
            return False
    
    def get_all_tasks(self):
        """Retrieve all tasks from database"""
        try:
            self.cursor.execute('SELECT id, title, deadline, priority, status FROM tasks ORDER BY deadline ASC')
            return self.cursor.fetchall()
        except Exception as e:
            print(f"✗ Terjadi kesalahan saat mengambil data: {e}")
            return []
    
    def check_reminders(self):
        """Check for tasks with deadline within 1 day"""
        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)
        
        try:
            self.cursor.execute('''
                SELECT id, title, deadline FROM tasks 
                WHERE deadline <= ? AND status = 'Belum Selesai'
                ORDER BY deadline ASC
            ''', (tomorrow.strftime("%Y-%m-%d"),))
            
            reminders = self.cursor.fetchall()
            return reminders
        except Exception as e:
            print(f"✗ Terjadi kesalahan: {e}")
            return []
    
    def display_tasks(self):
        """Display all tasks in a list view"""
        tasks = self.get_all_tasks()
        
        if not tasks:
            print("\n📋 Belum ada tugas. Tambahkan tugas baru!\n")
            return
        
        print("\n" + "="*80)
        print("📋 DAFTAR TUGAS")
        print("="*80)
        
        for task in tasks:
            task_id, title, deadline, priority, status = task
            
            # Calculate days until deadline
            try:
                deadline_date = datetime.strptime(deadline, "%Y-%m-%d").date()
                days_left = (deadline_date - datetime.now().date()).days
                
                if days_left < 0:
                    days_info = f"Terlambat {abs(days_left)} hari"
                elif days_left == 0:
                    days_info = "Hari ini!"
                elif days_left == 1:
                    days_info = "Besok!"
                else:
                    days_info = f"{days_left} hari lagi"
            except:
                days_info = "N/A"
            
            # Set priority emoji
            priority_emoji = {
                "Tinggi": "🔴",
                "Normal": "🟡",
                "Rendah": "🟢"
            }.get(priority, "🟡")
            
            # Set status icon
            status_icon = "✓" if status == "Selesai" else "○"
            
            print(f"\n[{task_id}] {status_icon} {title}")
            print(f"    Deadline: {deadline} ({days_info})")
            print(f"    Prioritas: {priority_emoji} {priority}")
            print(f"    Status: {status}")
    
    def display_reminders(self):
        """Display tasks that need reminders"""
        reminders = self.check_reminders()
        
        if reminders:
            print("\n" + "🔔 "*20)
            print("⚠️  PENGINGAT: Tugas-tugas yang akan jatuh tempo!")
            print("🔔 "*20)
            
            for reminder_id, title, deadline in reminders:
                try:
                    deadline_date = datetime.strptime(deadline, "%Y-%m-%d").date()
                    days_left = (deadline_date - datetime.now().date()).days
                    
                    if days_left < 0:
                        print(f"❌ Sudah terlambat: {title} (Deadline: {deadline})")
                    elif days_left == 0:
                        print(f"⏰ HARI INI: {title} (Deadline: {deadline})")
                    else:
                        print(f"⏱️  Sisa {days_left} hari: {title} (Deadline: {deadline})")
                except:
                    pass
            
            print("🔔 "*20 + "\n")
    
    def complete_task(self, task_id):
        """Mark a task as completed"""
        try:
            self.cursor.execute('UPDATE tasks SET status = ? WHERE id = ?', ("Selesai", task_id))
            self.conn.commit()
            print(f"✓ Tugas dengan ID {task_id} sudah ditandai selesai!")
            return True
        except Exception as e:
            print(f"✗ Terjadi kesalahan: {e}")
            return False
    
    def delete_task(self, task_id):
        """Delete a task from database"""
        try:
            self.cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            self.conn.commit()
            print(f"✓ Tugas dengan ID {task_id} sudah dihapus!")
            return True
        except Exception as e:
            print(f"✗ Terjadi kesalahan: {e}")
            return False
    
    def edit_task(self, task_id, title=None, deadline=None, priority=None):
        """Edit task details"""
        try:
            if title:
                self.cursor.execute('UPDATE tasks SET title = ? WHERE id = ?', (title, task_id))
            if deadline:
                datetime.strptime(deadline, "%Y-%m-%d")
                self.cursor.execute('UPDATE tasks SET deadline = ? WHERE id = ?', (deadline, task_id))
            if priority:
                self.cursor.execute('UPDATE tasks SET priority = ? WHERE id = ?', (priority, task_id))
            
            self.conn.commit()
            print(f"✓ Tugas dengan ID {task_id} sudah diperbarui!")
            return True
        except ValueError:
            print("✗ Format deadline tidak valid! Gunakan format YYYY-MM-DD")
            return False
        except Exception as e:
            print(f"✗ Terjadi kesalahan: {e}")
            return False
    
    def export_tasks(self, filename="tasks_export.json"):
        """Export tasks to JSON file"""
        try:
            tasks = self.get_all_tasks()
            export_data = []
            
            for task in tasks:
                export_data.append({
                    "id": task[0],
                    "title": task[1],
                    "deadline": task[2],
                    "priority": task[3],
                    "status": task[4]
                })
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            
            print(f"✓ Data sudah diekspor ke {filename}")
            return True
        except Exception as e:
            print(f"✗ Terjadi kesalahan saat mengekspor: {e}")
            return False
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()


def display_menu():
    """Display main menu"""
    print("\n" + "="*50)
    print("     📋 APLIKASI TO-DO LIST")
    print("="*50)
    print("1. ➕ Tambah Tugas")
    print("2. 👀 Lihat Semua Tugas")
    print("3. ✓ Tandai Selesai")
    print("4. 🗑️  Hapus Tugas")
    print("5. ✏️  Edit Tugas")
    print("6. 📤 Export Tugas (JSON)")
    print("7. ❌ Keluar")
    print("="*50)


def main():
    """Main application loop"""
    app = TodoApp()
    
    print("\n🎉 Selamat datang di Aplikasi To-Do List!")
    
    while True:
        # Check and display reminders
        app.display_reminders()
        
        display_menu()
        choice = input("Pilih menu (1-7): ").strip()
        
        if choice == "1":
            print("\n" + "-"*50)
            title = input("Masukkan judul tugas: ").strip()
            if not title:
                print("✗ Judul tugas tidak boleh kosong!")
                continue
            
            deadline = input("Masukkan deadline (YYYY-MM-DD): ").strip()
            
            print("Pilih prioritas:")
            print("1. Tinggi (🔴)")
            print("2. Normal (🟡)")
            print("3. Rendah (🟢)")
            priority_choice = input("Pilih (1-3) [default: 2 - Normal]: ").strip()
            
            priority_map = {"1": "Tinggi", "2": "Normal", "3": "Rendah"}
            priority = priority_map.get(priority_choice, "Normal")
            
            app.add_task(title, deadline, priority)
        
        elif choice == "2":
            app.display_tasks()
        
        elif choice == "3":
            app.display_tasks()
            try:
                task_id = int(input("Masukkan ID tugas yang sudah selesai: "))
                app.complete_task(task_id)
            except ValueError:
                print("✗ ID harus berupa angka!")
        
        elif choice == "4":
            app.display_tasks()
            try:
                task_id = int(input("Masukkan ID tugas yang akan dihapus: "))
                confirm = input("Yakin hapus tugas ini? (y/n): ").lower()
                if confirm == 'y':
                    app.delete_task(task_id)
            except ValueError:
                print("✗ ID harus berupa angka!")
        
        elif choice == "5":
            app.display_tasks()
            try:
                task_id = int(input("Masukkan ID tugas yang akan diedit: "))
                
                print("\nApa yang ingin diedit?")
                print("1. Judul")
                print("2. Deadline")
                print("3. Prioritas")
                print("4. Semua")
                
                edit_choice = input("Pilih (1-4): ").strip()
                
                new_title = None
                new_deadline = None
                new_priority = None
                
                if edit_choice in ["1", "4"]:
                    new_title = input("Masukkan judul baru: ").strip()
                
                if edit_choice in ["2", "4"]:
                    new_deadline = input("Masukkan deadline baru (YYYY-MM-DD): ").strip()
                
                if edit_choice in ["3", "4"]:
                    print("Pilih prioritas:")
                    print("1. Tinggi")
                    print("2. Normal")
                    print("3. Rendah")
                    priority_choice = input("Pilih (1-3): ").strip()
                    priority_map = {"1": "Tinggi", "2": "Normal", "3": "Rendah"}
                    new_priority = priority_map.get(priority_choice)
                
                app.edit_task(task_id, new_title, new_deadline, new_priority)
            except ValueError:
                print("✗ Input tidak valid!")
        
        elif choice == "6":
            filename = input("Masukkan nama file (default: tasks_export.json): ").strip()
            if not filename:
                filename = "tasks_export.json"
            app.export_tasks(filename)
        
        elif choice == "7":
            print("\n👋 Terima kasih telah menggunakan Aplikasi To-Do List!")
            app.close()
            break
        
        else:
            print("✗ Pilihan tidak valid! Silakan coba lagi.")


if __name__ == "__main__":
    main()
