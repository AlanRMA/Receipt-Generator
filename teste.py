from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def create_receipt(filename, service_provider, client, total_value, date, data, logo_path):
    # Define o tamanho da página e margens
    page_width = 8.5 * inch
    page_height = 11 * inch
    margin = 0.5 * inch
    doc = SimpleDocTemplate(filename, pagesize=(page_width, page_height),
                            rightMargin=margin, leftMargin=margin,
                            topMargin=margin, bottomMargin=margin)
    
    # Define o estilo para o texto
    styles = getSampleStyleSheet()
    style_normal = styles['Normal']
    
    # Estilo para o prestador de serviços
    style_provider = ParagraphStyle(
        name='ProviderStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14
    )
    
    # Estilo para as tabelas de informações fixas
    style_fixed_info = ParagraphStyle(
        name='FixedInfoStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12
    )

    # Define a largura da tabela
    table_width = 7.5 * inch

    # Adiciona o logo
    try:
        logo = Image(logo_path, width=1.5 * inch, height=1.5 * inch)  # Ajusta o tamanho do logo
    except IOError:
        print(f"Não foi possível abrir o arquivo de imagem: {logo_path}")
        logo = Spacer(1.5 * inch, 1.5 * inch)  # Usa um espaço se a imagem não estiver disponível

    # Cria a tabela para os dados fixos e logo
    info_table_data = [
        [Table([
            [Paragraph(f"<b>Prestador(a) de serviço:</b> {service_provider}", style_provider)],
            [Paragraph(f"<b>Cliente:</b> {client}", style_fixed_info)],
            [Paragraph(f"<b>Valor total:</b> R$ {total_value:.2f}", style_fixed_info)],
            [Paragraph(f"<b>Data:</b> {date}", style_fixed_info)]
        ], colWidths=[table_width/2.0]), logo]
    ]

    # Cria a tabela para os dados fixos e o logo
    info_table = Table(info_table_data, colWidths=[table_width/2.0, table_width/2.0])
    info_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6)
    ]))

    # Define a tabela para os itens
    items_data = [
        ["Ref", "Descrição", "Serviço", "Valor"]
    ]
    
    for item in data:
        ref, desc, service, val = item
        items_data.append([ref, desc, service, f"R$ {val:.2f}"])

    # Cria a tabela para os itens
    items_table = Table(items_data, colWidths=[table_width/4.0]*4, rowHeights=[0.4*inch] * len(items_data))
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4)
    ]))

    # Cria a lista de elementos para o PDF
    elements = [
        info_table,
        Spacer(1, 0.5*inch),  # Espaço entre a tabela de informações e a tabela de itens
        items_table,
        Spacer(1, 0.2*inch)  # Espaço entre a tabela de itens e o final do PDF
    ]
    doc.build(elements)

# Informações fixas
service_provider = "Rosania"
client = "LOH"
total_value = 150.75
date = "18/07/2024"

# Itens (referência, descrição, serviço, valor)
data = [
    ("001", "Macaquinho\nDescrição longa", "Vestido", 100.00),
    ("002", "Short\nDescrição longa", "Verão", 50.75),
    ("003", "Blusa\nDescrição longa", "Outono", 80.00)
] * 5

# Caminho para a imagem do logo
logo_path = "logo.png"

# Cria o recibo
create_receipt("recibo.pdf", service_provider, client, total_value, date, data, logo_path)
