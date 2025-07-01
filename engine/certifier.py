from fpdf import FPDF

class Certifier:
    """
    Aggregates results and generates a PDF certification report.
    """
    def __init__(self, output_path):
        self.output_path = output_path

    def generate_report(self, organization, scroll_results, fork_results, reflection):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, f"Certification Report: {organization}", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.ln(5)
        pdf.cell(0, 10, f"Score: {reflection['score']}/100", ln=True)
        pdf.ln(5)
        pdf.cell(0, 10, "Scroll Results:", ln=True)
        for title, res in scroll_results.items():
            status = "PASS" if res["passed"] else "FAIL"
            pdf.cell(0, 8, f"{title} ({res['requirement']}): {status}", ln=True)
        pdf.ln(3)
        pdf.cell(0, 10, "Fork Results:", ln=True)
        for desc, passed in fork_results.items():
            status = "PASS" if passed else "FAIL"
            pdf.cell(0, 8, f"{desc}: {status}", ln=True)
        pdf.output(self.output_path)
        return self.output_path
