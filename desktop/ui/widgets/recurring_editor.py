import customtkinter as ctk
from datetime import datetime
from typing import List

class RecurringEditor(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry("400x450")
        self.title("Повторяющееся событие")
        self.resizable(False, False)
        self.frequencies = {"Ежедневно": "DAILY", "Еженедельно": "WEEKLY", "Ежемесячно": "MONTHLY", "Ежегодно": "YEARLY"}
        self.days = ["MO", "TU", "WE", "TH", "FR", "SA", "SU"]
        self.selected_days = set()
        self.exceptions = []
        self.rrule_result = None

        ctk.CTkLabel(self, text="Частота").pack(pady=(10, 2), padx=15, fill="x")
        self.freq_box = ctk.CTkComboBox(self, values=list(self.frequencies.keys()), command=self._on_freq_change)
        self.freq_box.set("Ежедневно")
        self.freq_box.pack(padx=15, pady=2, fill="x")

        self.interval_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.interval_frame.pack(fill="x", padx=15, pady=5)
        ctk.CTkLabel(self.interval_frame, text="Каждый").pack(side="left")
        self.interval_entry = ctk.CTkEntry(self.interval_frame, width=40)
        self.interval_entry.insert(0, "1")
        self.interval_entry.pack(side="left", padx=5)
        self.interval_label = ctk.CTkLabel(self.interval_frame, text="дней")
        self.interval_label.pack(side="left")

        self.days_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.days_frame.pack(fill="x", padx=15, pady=5)
        self.day_checkboxes = {}
        for i, day in enumerate(self.days):
            cb = ctk.CTkCheckBox(self.days_frame, text=day, width=30, command=lambda d=day: self._toggle_day(d))
            cb.grid(row=0, column=i, padx=2)
            self.day_checkboxes[day] = cb
        self.days_frame.pack_forget()

        ctk.CTkLabel(self, text="Завершается").pack(pady=(5, 2), padx=15, fill="x")
        self.end_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.end_frame.pack(fill="x", padx=15, pady=2)
        self.end_var = ctk.StringVar(value="never")
        ctk.CTkRadioButton(self.end_frame, text="Никогда", variable=self.end_var, value="never").pack(side="left")
        ctk.CTkRadioButton(self.end_frame, text="После", variable=self.end_var, value="count").pack(side="left", padx=5)
        self.count_entry = ctk.CTkEntry(self.end_frame, width=40)
        self.count_entry.insert(0, "10")
        self.count_entry.pack(side="left", padx=2)
        ctk.CTkRadioButton(self.end_frame, text="Дата", variable=self.end_var, value="date").pack(side="left", padx=5)
        self.date_entry = ctk.CTkEntry(self.end_frame, width=80)
        self.date_entry.insert(0, "2026-12-31")
        self.date_entry.pack(side="left")

        ctk.CTkLabel(self, text="Исключить даты (ГГГГ-ММ-ДД)").pack(pady=(5, 2), padx=15, fill="x")
        self.exc_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.exc_frame.pack(fill="x", padx=15, pady=2)
        self.exc_entry = ctk.CTkEntry(self.exc_frame)
        self.exc_entry.pack(side="left", expand=True, fill="x", padx=5)
        ctk.CTkButton(self.exc_frame, text="Добавить", width=40, command=self._add_exception).pack(side="left")
        self.exc_list = ctk.CTkTextbox(self, height=60)
        self.exc_list.pack(fill="x", padx=15, pady=5)

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=15, pady=10)
        ctk.CTkButton(btn_frame, text="Отмена", command=self.destroy).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Сохранить", command=self._save).pack(side="right", padx=5)

    def _on_freq_change(self, val):
        if val == "Еженедельно":
            self.days_frame.pack(fill="x", padx=15, pady=5)
            self.interval_label.configure(text="недель")
        elif val == "Ежемесячно":
            self.days_frame.pack_forget()
            self.interval_label.configure(text="месяцев")
        else:
            self.days_frame.pack_forget()
            self.interval_label.configure(text="дней")

    def _toggle_day(self, day):
        cb = self.day_checkboxes[day]
        if cb.get() == 1:
            self.selected_days.add(day)
        else:
            self.selected_days.discard(day)

    def _add_exception(self):
        try:
            date_str = self.exc_entry.get().strip()
            datetime.strptime(date_str, "%Y-%m-%d")
            if date_str not in self.exceptions:
                self.exceptions.append(date_str)
                self.exc_list.insert("end", date_str + "\n")
            self.exc_entry.delete(0, "end")
        except ValueError:
            pass

    def _save(self):
        freq = self.frequencies[self.freq_box.get()]
        interval = self.interval_entry.get() or "1"
        parts = [f"FREQ={freq}", f"INTERVAL={interval}"]
        if freq == "WEEKLY" and self.selected_days:
            parts.append(f"BYDAY={','.join(sorted(self.selected_days))}")
        end_type = self.end_var.get()
        if end_type == "count":
            parts.append(f"COUNT={self.count_entry.get() or '10'}")
        elif end_type == "date":
            parts.append(f"UNTIL={self.date_entry.get().replace('-', '')}T000000Z")
        if self.exceptions:
            parts.append(f"EXDATE={','.join(self.exceptions)}")
        self.rrule_result = ";".join(parts)
        self.destroy()

    def get_result(self):
        return self.rrule_result