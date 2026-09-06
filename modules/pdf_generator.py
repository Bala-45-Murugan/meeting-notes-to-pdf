from fpdf import FPDF


class MeetingPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, "Meeting Notes", align="R")
        self.ln(4)
        self.set_draw_color(0, 102, 204)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(6)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def section_title(self, title: str):
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(0, 102, 204)
        self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(0, 102, 204)
        self.set_line_width(0.3)
        self.line(10, self.get_y(), 80, self.get_y())
        self.ln(3)

    def body_text(self, text: str):
        self.set_font("Helvetica", "", 11)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 6, text)
        self.ln(2)

    def bullet_list(self, items: list[str]):
        self.set_font("Helvetica", "", 11)
        self.set_text_color(40, 40, 40)
        for item in items:
            self.cell(6, 6, "-")
            self.multi_cell(0, 6, item)
            self.ln(1)
        self.ln(2)

    def check_page_break(self, h: int = 20):
        if self.get_y() + h > self.h - 25:
            self.add_page()


def generate_pdf(data: dict, output_path: str):
    pdf = MeetingPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=25)
    pdf.add_page()

    title = data.get("title", "Meeting Notes")
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(30, 30, 30)
    pdf.multi_cell(0, 12, title)
    pdf.ln(2)

    meta_parts = []
    if data.get("date"):
        meta_parts.append(f"Date: {data['date']}")
    if data.get("attendees"):
        meta_parts.append(f"Attendees: {', '.join(data['attendees'])}")
    if meta_parts:
        pdf.set_font("Helvetica", "I", 10)
        pdf.set_text_color(100, 100, 100)
        pdf.multi_cell(0, 6, " | ".join(meta_parts))
        pdf.ln(6)

    if data.get("summary"):
        pdf.check_page_break(30)
        pdf.section_title("Summary")
        pdf.body_text(data["summary"])

    if data.get("discussion_points"):
        pdf.check_page_break(20 + len(data["discussion_points"]) * 8)
        pdf.section_title("Key Discussion Points")
        pdf.bullet_list(data["discussion_points"])

    if data.get("decisions"):
        pdf.check_page_break(20 + len(data["decisions"]) * 8)
        pdf.section_title("Decisions Made")
        pdf.bullet_list(data["decisions"])

    if data.get("action_items"):
        pdf.check_page_break(20 + len(data["action_items"]) * 8)
        pdf.section_title("Action Items")
        pdf.bullet_list(data["action_items"])

    if data.get("next_steps"):
        pdf.check_page_break(20 + len(data["next_steps"]) * 8)
        pdf.section_title("Next Steps")
        pdf.bullet_list(data["next_steps"])

    pdf.output(output_path)
