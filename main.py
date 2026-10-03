import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta


def to_number(text):
    return float(text.strip().replace(",", "."))


class XAUUSDApp:
    def __init__(self, root):
        self.root = root
        self.root.title("XAUUSD — 1-Matematik Strategiya")
        self.root.geometry("950x720")
        self.root.minsize(800, 600)

        title = tk.Label(
            root,
            text="XAUUSD — 1-MATEMATIK STRATEGIYA",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=(12, 8))

        frame = tk.Frame(root)
        frame.pack(fill="both", expand=True, padx=15, pady=5)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        self.output = tk.Text(
            frame,
            font=("Consolas", 11),
            wrap="word",
            yscrollcommand=scrollbar.set
        )
        self.output.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.output.yview)

        self.entry_frame = tk.Frame(root)
        self.entry_frame.pack(fill="x", padx=15, pady=(5, 12))

        self.question = tk.Label(
            self.entry_frame,
            text="",
            font=("Arial", 12, "bold")
        )
        self.question.pack(side="left")

        self.entry = tk.Entry(
            self.entry_frame,
            width=20,
            font=("Arial", 13)
        )
        self.entry.pack(side="left", padx=(12, 0))
        self.entry.bind("<Return>", lambda event: self.next_step())

        self.start_process()

    def write(self, text=""):
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)

    def start_process(self):
        self.step = 1
        self.analysis_time = None
        self.three_hours_before = None
        self.three_hours_after = None
        self.current_price = None
        self.historical_mid = None
        self.high_price = None
        self.low_price = None

        self.output.delete("1.0", tk.END)

        self.write("=" * 78)
        self.write("XAUUSD — 1-MATEMATIK STRATEGIYA")
        self.write("=" * 78)
        self.write("")
        self.write("Har bir amal Enter tugmasi bilan tasdiqlanadi.")
        self.write("Narxlar uchun nuqta yoki vergul ishlatish mumkin.")
        self.write("Masalan: 4184.46 yoki 4184,46")
        self.write("")

        self.question.config(text="Analiz qilinadigan vaqtni kiriting (HH:MM):")
        self.entry.config(state="normal")
        self.entry.delete(0, tk.END)
        self.entry.focus()

    def next_step(self):
        value = self.entry.get().strip()

        if not value:
            messagebox.showwarning("Xatolik", "Qiymatni kiriting.")
            return

        if self.step == 1:
            try:
                analysis_time = datetime.strptime(value, "%H:%M")
            except ValueError:
                messagebox.showerror(
                    "Xatolik",
                    "Vaqtni HH:MM ko‘rinishida kiriting.\nMasalan: 14:30"
                )
                return

            self.analysis_time = analysis_time
            self.three_hours_before = analysis_time - timedelta(hours=3)
            self.three_hours_after = analysis_time + timedelta(hours=3)

            self.write(f"Analiz qilinadigan vaqt: {analysis_time.strftime('%H:%M')}")
            self.write(
                f"3 soat oldingi vaqt:       "
                f"{self.three_hours_before.strftime('%H:%M')}"
            )
            self.write(
                f"3 soat keyingi vaqt:       "
                f"{self.three_hours_after.strftime('%H:%M')}"
            )
            self.write("")

            self.question.config(text="1. Joriy real XAUUSD narxi:")
            self.step = 2

        elif self.step in (2, 3, 4, 5):
            try:
                number = to_number(value)
            except ValueError:
                messagebox.showerror(
                    "Xatolik",
                    "Raqamni to‘g‘ri kiriting.\nMasalan: 4184.46 yoki 4184,46"
                )
                return

            self.entry.delete(0, tk.END)

            if self.step == 2:
                self.current_price = number
                self.write(
                    f"1. Joriy real XAUUSD narxi: {self.current_price:.2f}"
                )
                self.question.config(
                    text="2. 3 soat oldingi tarixiy boshlang‘ich narxning o‘rtasi:"
                )
                self.step = 3

            elif self.step == 3:
                self.historical_mid = number
                self.write(
                    f"2. 3 soat oldingi tarixiy boshlang‘ich narxning o‘rtasi: "
                    f"{self.historical_mid:.2f}"
                )
                self.question.config(
                    text="3. 3 soat ichidagi ENG YUQORI narx:"
                )
                self.step = 4

            elif self.step == 4:
                self.high_price = number
                self.write(
                    f"3. 3 soat ichidagi ENG YUQORI narx: "
                    f"{self.high_price:.2f}"
                )
                self.question.config(
                    text="4. 3 soat ichidagi ENG PAST narx:"
                )
                self.step = 5

            elif self.step == 5:
                self.low_price = number
                self.write(
                    f"4. 3 soat ichidagi ENG PAST narx: "
                    f"{self.low_price:.2f}"
                )
                self.calculate()

    def calculate(self):
        movement = self.high_price - self.low_price
        future_supply = self.current_price + movement
        future_demand = self.current_price - movement
        future_range = future_supply - future_demand
        pips = future_range * 100

        self.write("")
        self.write("=" * 78)
        self.write("5. HISOB-KITOB")
        self.write("=" * 78)
        self.write("")
        self.write(
            f"{self.high_price:.2f} - {self.low_price:.2f} = {movement:.2f}"
        )
        self.write(f"3 soatlik harakat: {movement:.2f}")
        self.write("")
        self.write(
            f"KELAJAK TAKLIF: "
            f"{self.current_price:.2f} + {movement:.2f} = {future_supply:.2f}"
        )
        self.write(
            f"KELAJAK TALAB:  "
            f"{self.current_price:.2f} - {movement:.2f} = {future_demand:.2f}"
        )
        self.write("")
        self.write(
            f"KELAJAK ICHKI UMUMIY HARAKAT: "
            f"{future_supply:.2f} - {future_demand:.2f} = {future_range:.2f}"
        )
        self.write(f"PIPS: {future_range:.2f} × 100 = {pips:.0f} pips")

        self.write("")
        self.write("=" * 78)
        self.write("6. YAKUNIY NATIJA — KELAJAK REAL NARXI UCHUN ANALIZ")
        self.write("=" * 78)
        self.write("")
        self.write(f"Analiz vaqti:                         {self.analysis_time.strftime('%H:%M')}")
        self.write(f"3 soat oldingi vaqt:                  {self.three_hours_before.strftime('%H:%M')}")
        self.write(f"3 soat keyingi vaqt:                  {self.three_hours_after.strftime('%H:%M')}")
        self.write("")
        self.write(f"Joriy real narx:                      {self.current_price:.2f}")
        self.write(f"3 soat oldingi tarixiy o‘rta narx:    {self.historical_mid:.2f}")
        self.write(f"3 soatlik ENG YUQORI narx:            {self.high_price:.2f}")
        self.write(f"3 soatlik ENG PAST narx:              {self.low_price:.2f}")
        self.write("")
        self.write(f"Kelajak TAKLIF narxi:                 {future_supply:.2f}")
        self.write(f"Kelajak TALAB narxi:                  {future_demand:.2f}")
        self.write(f"Kelajak ichki umumiy harakat:         {future_range:.2f}")
        self.write(f"Hisoblangan harakat:                  {pips:.0f} pips")
        self.write("")
        self.write("=" * 78)
        self.write("1-matematik strategiya hisob-kitobi tugadi.")
        self.write("=" * 78)

        self.question.config(text="Yangi hisob uchun Enter bosing:")
        self.entry.delete(0, tk.END)
        self.entry.config(state="normal")
        self.entry.focus()
        self.entry.bind("<Return>", self.restart_once)

    def restart_once(self, event=None):
        self.entry.unbind("<Return>")
        self.entry.bind("<Return>", lambda event: self.next_step())
        self.start_process()


if __name__ == "__main__":
    root = tk.Tk()
    XAUUSDApp(root)
    root.mainloop()
