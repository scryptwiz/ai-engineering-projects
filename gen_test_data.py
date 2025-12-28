import random
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import black, gray


def create_messy_pdf(filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # --- PAGE 1: Basic Info (Slightly Rotated) ---

    # Simulate a bad scan by rotating the entire page context slightly
    c.translate(width / 2, height / 2)
    c.rotate(2)  # Rotate 2 degrees counter-clockwise
    c.translate(-width / 2, -height / 2)

    # Header
    c.setFont("Helvetica-Bold", 24)
    c.drawString(100, 700, "INSURANCE CLAIM FORM")

    # Form Field: Policy Number
    c.setFont("Helvetica", 12)
    c.drawString(100, 650, "Policy Number:")
    # Simulate "Typewritten" data
    c.setFont("Courier-Bold", 14)
    c.drawString(220, 650, "POL-8842-XJ9")

    # Form Field: Claimant Name
    c.setFont("Helvetica", 12)
    c.drawString(100, 600, "Claimant Name:")
    # Simulate "Handwritten" data (using a script-like standard font if avail, or just italic)
    c.setFont("Times-Italic", 16)
    c.drawString(220, 600, "Sarah J. Connor")

    # Form Field: Claim Type (Checkbox style)
    c.setFont("Helvetica", 12)
    c.drawString(100, 550, "Type of Claim:")
    c.rect(210, 550, 10, 10)
    c.drawString(230, 550, "Accident")
    c.rect(310, 550, 10, 10, fill=1)  # Filled box
    c.drawString(330, 550, "Theft")

    # Add some "noise" / dirt lines
    c.setStrokeColor(gray)
    c.line(50, 400, 550, 410)  # Random scratch line

    c.showPage()  # Finish Page 1

    # --- PAGE 2: Details & Amount (Messy) ---

    # Header
    c.setFont("Helvetica-Bold", 18)
    c.drawString(100, 700, "Incident Details")

    # Description
    c.setFont("Times-Roman", 12)
    text = "I parked my car at the mall. When I returned, the window was broken."
    c.drawString(100, 650, text)

    # The Money Shot (Total Amount)
    # Let's make this hard: Put it in a box, slightly off-center
    c.rect(350, 100, 150, 50)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(360, 135, "TOTAL CLAIM AMOUNT")

    # The value
    c.setFont("Courier-Bold", 20)
    c.drawString(380, 110, "$ 4,500.00")

    # Date (Handwritten style at bottom)
    c.setFont("Times-Italic", 12)
    c.drawString(100, 100, "Date: 2024-01-15")

    c.save()
    print(f"Successfully created: {filename}")


if __name__ == "__main__":
    create_messy_pdf("messy_claim.pdf")
