from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import pagesizes
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase import pdfmetrics
from datetime import datetime
import os


def generate_invoice(customer_name, invoice_no, items, subtotal, cgst, sgst, grand_total):

    # ==============================
    # CREATE YEAR → MONTH FOLDER
    # ==============================
    now = datetime.now()
    year_folder = now.strftime("%Y")
    month_folder = now.strftime("%B")

    base_path = "invoices"
    full_folder_path = os.path.join(base_path, year_folder, month_folder)

    os.makedirs(full_folder_path, exist_ok=True)

    # Clean customer name (avoid space issues)
    clean_name = customer_name.replace(" ", "_")

    file_name = f"{now.strftime('%d-%m-%Y')}_INV-{invoice_no}_{clean_name}.pdf"
    file_path = os.path.join(full_folder_path, file_name)

    # ==============================
    # PAGE SETTINGS
    # ==============================
    left_margin = 30
    right_margin = 30
    top_margin = 30
    bottom_margin = 30

    doc = SimpleDocTemplate(
        file_path,
        pagesize=pagesizes.A4,
        rightMargin=right_margin,
        leftMargin=left_margin,
        topMargin=top_margin,
        bottomMargin=bottom_margin
    )

    elements = []
    styles = getSampleStyleSheet()

    page_width, page_height = pagesizes.A4
    usable_width = page_width - left_margin - right_margin

    # ==============================
    # REGISTER UNICODE FONT
    # ==============================
    pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
    font_name = 'STSong-Light'

    # ==============================
    # LOGO
    # ==============================
    logo_path = "logo.png"

    if os.path.exists(logo_path):
        logo = Image(logo_path)
        logo.drawHeight = 90
        logo.drawWidth = 200
        logo.hAlign = 'CENTER'
        elements.append(logo)
        elements.append(Spacer(1, 15))

    # ==============================
    # SHOP HEADER
    # ==============================
    shop_style = ParagraphStyle(
        name='ShopStyle',
        fontName=font_name,
        fontSize=20,
        alignment=1,
        spaceAfter=6
    )

    normal_style = ParagraphStyle(
        name='NormalStyle',
        fontName=font_name,
        fontSize=11,
        spaceAfter=2
    )

    elements.append(Paragraph("<b>Sri Kuberan Jewellery</b>", shop_style))
    elements.append(Spacer(1, 18))
    elements.append(Paragraph(
        "Address : No 5 Nellumandi Street , East Main Street , Pudukkottai",
        normal_style
    ))
    elements.append(Paragraph(
        "Mobile No : 7904602719 , 9865505371",
        normal_style
    ))

    elements.append(Spacer(1, 18))

    # ==============================
    # INVOICE INFO TABLE
    # ==============================
    info_data = [
        ["Invoice No:", invoice_no, "Date & Time:", now.strftime("%d-%m-%Y %H:%M:%S")],
        ["Customer Name:", customer_name, "", ""]
    ]

    info_table = Table(
        info_data,
        colWidths=[
            usable_width * 0.18,
            usable_width * 0.32,
            usable_width * 0.18,
            usable_width * 0.32
        ]
    )

    info_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), font_name),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    elements.append(info_table)
    elements.append(Spacer(1, 25))

    # ==============================
    # ITEM TABLE
    # ==============================
    data = [
        ["Item Name", "HUID", "Weight (g)", "Gold Rate", "Wastage %", "Sub Total"]
    ]

    for item in items:
        data.append([
            item.get("name", ""),
            item.get("huid", ""),
            f'{item["weight"]} g',
            f'{item["gold_rate"]:.2f}',
            f'{item["wastage"]}%',
            f'{item["total"]:.2f}'
        ])

    col_widths = [
        usable_width * 0.22,
        usable_width * 0.18,
        usable_width * 0.14,
        usable_width * 0.16,
        usable_width * 0.14,
        usable_width * 0.16,
    ]

    item_table = Table(data, colWidths=col_widths)

    item_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), font_name),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),
        ('ALIGN', (3, 1), (-1, -1), 'RIGHT'),
        ('ALIGN', (5, 1), (-1, -1), 'RIGHT'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
    ]))

    elements.append(item_table)
    elements.append(Spacer(1, 25))

    # ==============================
    # TOTAL SECTION
    # ==============================
    total_data = [
        ["Sub Total", f"{subtotal:.2f}"],
        ["CGST (1.5%)", f"{cgst:.2f}"],
        ["SGST (1.5%)", f"{sgst:.2f}"],
        ["Grand Total", f"Rs. {grand_total:.2f}"]
    ]

    total_width = usable_width * 0.45

    total_table = Table(
        total_data,
        colWidths=[total_width * 0.6, total_width * 0.4],
        hAlign='RIGHT'
    )

    total_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), font_name),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTSIZE', (0, 0), (-1, -2), 11),

        ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
        ('FONTSIZE', (0, -1), (-1, -1), 13),
    ]))

    elements.append(total_table)
    elements.append(Spacer(1, 40))

    # ==============================
    # FOOTER
    # ==============================
    elements.append(Paragraph("Thank you for shopping with us!", normal_style))

    # ==============================
    # OUTER BORDER
    # ==============================
    def draw_page_border(canvas, doc):
        margin = 15
        canvas.setLineWidth(2)
        canvas.rect(
            margin,
            margin,
            page_width - 2 * margin,
            page_height - 2 * margin
        )

    doc.build(
        elements,
        onFirstPage=draw_page_border,
        onLaterPages=draw_page_border
    )

    return file_path