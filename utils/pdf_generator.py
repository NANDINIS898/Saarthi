from fpdf import FPDF
import os
from datetime import datetime

class PDF(FPDF):
    def header(self):
        # Add Saarthi branding at top-left with elegant styling
        self.set_font("DejaVu", 'B', 24)
        self.set_text_color(34, 139, 34)  # Forest Green
        self.set_xy(10, 10)
        self.cell(60, 10, "Saarthi", align="L")
        
        # Add tagline below Saarthi
        self.set_font("DejaVu", '', 9)
        self.set_text_color(100, 100, 100)
        self.set_xy(10, 18)
        self.cell(60, 5, "Your Financial Partner", align="L")
        
        # Add decorative line below header
        self.set_draw_color(34, 139, 34)
        self.set_line_width(0.8)
        self.line(10, 25, 200, 25)
        
        # Add date on top-right
        self.set_font("DejaVu", '', 10)
        self.set_text_color(80, 80, 80)
        self.set_xy(-60, 10)
        current_date = datetime.now().strftime("%B %d, %Y")
        self.cell(50, 5, current_date, align="R")

    def footer(self):
        # Decorative line above footer
        self.set_y(-25)
        self.set_draw_color(34, 139, 34)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y())
        
        # Company footer information
        self.set_y(-20)
        self.set_font("DejaVu", '', 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 4, "Saarthi Financial Services | www.saarthi.ai | support@saarthi.ai | 1800-123-456", align="C", ln=True)
        
        # Page number
        self.set_font("DejaVu", '', 9)
        self.set_text_color(120, 120, 120)
        self.cell(0, 4, f"Page {self.page_no()}", align="C")

    def add_section_title(self, title, color_r=0, color_g=70, color_b=140):
        """Add a styled section title"""
        self.set_font("DejaVu", 'B', 14)
        self.set_text_color(color_r, color_g, color_b)
        self.cell(0, 10, title, ln=True)
        self.ln(2)

    def add_horizontal_line(self, color_r=200, color_g=200, color_b=200):
        """Add a decorative horizontal line"""
        self.set_draw_color(color_r, color_g, color_b)
        self.set_line_width(0.3)
        current_y = self.get_y()
        self.line(10, current_y, 200, current_y)
        self.ln(5)


# Top of your file
from fpdf import FPDF
import os
from datetime import datetime

# ... rest of your PDF class

def generate_pdf(filename, name, loan, details):
    """
    Generate a professional loan sanction letter PDF with enhanced styling
    """
    # Ensure test folder exists
    output_path = os.path.join("test", filename)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    pdf = PDF()

    # Get absolute path to the font files relative to this script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    dejavu_regular = os.path.join(current_dir, "fonts", "DejaVuSans.ttf")
    dejavu_bold = os.path.join(current_dir, "fonts", "DejaVuSans-Bold.ttf")

    # Register fonts
    pdf.add_font("DejaVu", "", dejavu_regular)
    pdf.add_font("DejaVu", "B", dejavu_bold)

    pdf.add_page()
    
    # ... rest of your PDF generation code


    # MAIN TITLE with enhanced styling (aligned with header)
    pdf.ln(18)  # Reduced from 10 to align with header
    pdf.set_font("DejaVu", 'B', 22)
    pdf.set_text_color(0, 70, 140)  # Dark Blue
    pdf.cell(0, 10, "Loan Sanction Letter", ln=True, align="C")
    
    # Add decorative underline below title
    pdf.set_draw_color(0, 70, 140)
    pdf.set_line_width(0.5)
    title_line_y = pdf.get_y() - 2
    pdf.line(60, title_line_y, 150, title_line_y)
    # No spacing - subtitle immediately after line
    
    # Subtitle - positioned just below the title
    pdf.set_font("DejaVu", '', 11)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 5, "Official Loan Approval Document", ln=True, align="C")
    pdf.ln(8)  # Increased spacing to push reference lower

    # Reference number
    pdf.set_font("DejaVu", '', 10)
    pdf.set_text_color(80, 80, 80)
    ref_number = f"REF/SAARTHI/{datetime.now().strftime('%Y%m%d')}/{hash(name) % 10000:04d}"
    pdf.cell(0, 5, f"Reference No: {ref_number}", ln=True, align="R")
    pdf.ln(5)

    # GREETING
    pdf.set_font("DejaVu", 'B', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 6, f"Dear {name},")
    pdf.ln(2)

    # INTRO TEXT with better formatting
    pdf.set_font("DejaVu", '', 11)
    pdf.set_text_color(40, 40, 40)
    intro_text = "We are delighted to inform you that your loan application has been successfully approved! "
    intro_text += "Below are the comprehensive details of your sanctioned loan:"
    pdf.multi_cell(0, 6, intro_text)
    pdf.ln(5)

    # LOAN DETAILS SECTION with enhanced design
    pdf.add_section_title("Loan Details", 34, 139, 34)
    
    # Create a professional details box with gradient-like effect
    pdf.set_draw_color(34, 139, 34)
    pdf.set_fill_color(240, 255, 240)  # Very light green background
    pdf.set_line_width(1)

    # Main details box
    box_x = pdf.get_x()
    box_y = pdf.get_y()
    box_width = 180
    box_height = 65
    
    # Draw outer border
    pdf.rect(box_x, box_y, box_width, box_height, style='D')
    
    # Draw filled background
    pdf.set_fill_color(245, 252, 245)
    pdf.rect(box_x, box_y, box_width, box_height, style='F')
    
    # Add accent bar on left side
    pdf.set_fill_color(34, 139, 34)
    pdf.rect(box_x, box_y, 4, box_height, style='F')

    # Add loan details inside box with better formatting
    left_margin = box_x + 12
    current_y = box_y + 10
    line_height = 10
    
    # Format loan amount with commas
    loan_amount = float(str(loan['amount']).replace(',', ''))
    loan_amount_formatted = f"{loan_amount:,.2f}"

    
    # Loan Amount
    pdf.set_xy(left_margin, current_y)
    pdf.set_font("DejaVu", 'B', 13)
    pdf.set_text_color(34, 139, 34)
    pdf.cell(85, line_height, "Loan Amount:", ln=False)
    pdf.set_font("DejaVu", 'B', 13)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, line_height, f"₹{loan_amount_formatted}", ln=False)
    current_y += line_height
    
    # Tenure
    pdf.set_xy(left_margin, current_y)
    pdf.set_font("DejaVu", 'B', 13)
    pdf.set_text_color(34, 139, 34)
    pdf.cell(85, line_height, "Loan Tenure:", ln=False)
    pdf.set_font("DejaVu", '', 13)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, line_height, f"{loan['tenure']} years", ln=False)
    current_y += line_height
    
    # Interest Rate
    pdf.set_xy(left_margin, current_y)
    pdf.set_font("DejaVu", 'B', 13)
    pdf.set_text_color(34, 139, 34)
    pdf.cell(85, line_height, "Interest Rate:", ln=False)
    pdf.set_font("DejaVu", '', 13)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, line_height, f"{loan['interest']}% per annum", ln=False)
    current_y += line_height
    
    # Loan Type
    pdf.set_xy(left_margin, current_y)
    pdf.set_font("DejaVu", 'B', 13)
    pdf.set_text_color(34, 139, 34)
    pdf.cell(85, line_height, "Loan Type:", ln=False)
    pdf.set_font("DejaVu", '', 13)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, line_height, details.get('type', 'N/A'), ln=False)
    current_y += line_height

    # Convert loan amount and interest to float
    loan_amount = float(str(loan['amount']).replace(',', ''))
    interest_rate = float(str(loan['interest']).replace(',', ''))
    tenure_years = float(str(loan['tenure']).replace(',', ''))

    # EMI calculation
    principal = loan_amount
    rate = interest_rate / 100 / 12
    tenure_months = tenure_years * 12
    emi = principal * rate * (1 + rate)**tenure_months / ((1 + rate)**tenure_months - 1)

    # Format loan amount and EMI for display
    loan_amount_formatted = f"{loan_amount:,.2f}"
    emi_formatted = f"{emi:,.2f}"
 
    # Monthly EMI
    pdf.set_xy(left_margin, current_y)
    pdf.set_font("DejaVu", 'B', 13)
    pdf.set_text_color(34, 139, 34)
    pdf.cell(85, line_height, "Estimated Monthly EMI:", ln=False)
    pdf.set_font("DejaVu", 'B', 13)
    pdf.set_text_color(0, 70, 140)
    pdf.cell(0, line_height, f"₹{emi:,.2f}", ln=False)
    
    # Move cursor below the box
    pdf.ln(box_height - 45)

    # IMPORTANT NOTES SECTION
    pdf.ln(3)
    pdf.add_section_title("Important Information", 0, 70, 140)
    
    pdf.set_font("DejaVu", '', 10)
    pdf.set_text_color(60, 60, 60)
    
    notes = [
        "• This loan sanction is subject to the terms and conditions mentioned in the loan agreement.",
        "• Please submit all required documents within 15 days to proceed with disbursement.",
        "• EMI payments will commence from the first day of the month following disbursement.",
        "• Early repayment options are available with minimal processing charges."
    ]
    
    for note in notes:
        pdf.cell(0, 5, note, ln=True)
    
    pdf.ln(5)

    # CLOSING MESSAGE
    pdf.set_font("DejaVu", '', 11)
    pdf.set_text_color(40, 40, 40)
    closing_text = "Congratulations on your loan approval! We at Saarthi are committed to providing you with "
    closing_text += "transparent, trustworthy, and customer-centric financial services. Our team is here to "
    closing_text += "support you throughout your loan journey."
    pdf.multi_cell(0, 6, closing_text)
    pdf.ln(5)

    # CONTACT SECTION
    pdf.set_font("DejaVu", 'B', 11)
    pdf.set_text_color(34, 139, 34)
    pdf.cell(0, 6, "Need Assistance?", ln=True)
    
    # Add decorative line below "Need Assistance?"
    pdf.set_draw_color(34, 139, 34)
    pdf.set_line_width(0.3)
    line_y = pdf.get_y()
    pdf.line(10, line_y, 200, line_y)
    pdf.ln(5)
    
    pdf.set_font("DejaVu", '', 10)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 5, "Email: support@saarthi.ai  |  Phone: 1800-123-456  |  Website: www.saarthi.ai", ln=True)
    pdf.ln(6)

    # SIGNATURE SECTION
    pdf.set_font("DejaVu", 'B', 11)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 5, "Warm Regards,", ln=True)
    pdf.ln(1)
    pdf.set_font("DejaVu", 'B', 12)
    pdf.set_text_color(34, 139, 34)
    pdf.cell(0, 5, "Saarthi Financial Services Team", ln=True)

    # SAVE PDF
    pdf.output(output_path)
    print(f"✓ Professional PDF generated successfully!")
    print(f"✓ Saved at: {output_path}")
    return output_path


# Example usage:
if __name__ == "__main__":
    loan_info = {"amount": 500000, "tenure": 5, "interest": 7.5}
    details_info = {"type": "Personal Loan"}
    generate_pdf("loan_letter.pdf", "Harshit Mittal", loan_info, details_info)
