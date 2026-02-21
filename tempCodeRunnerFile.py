
        total_data,
        colWidths=[total_width * 0.6, total_width * 0.4],
        hAlign='RIGHT'
    )

    total_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), font_name),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTSIZE', (0, 0), (-1, -2), 11),

        # Grand Total Highlight (Aligned Properly)
        ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),