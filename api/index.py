from flask import Flask, request, send_file, jsonify
import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

app = Flask(__name__)

@app.route('/')
def serve_index():
    return send_file('public/index.html')

@app.route('/create-receipt', methods=['POST'])
def create_receipt():
    data = request.json
    service_provider = data.get('service_provider', '')
    client = data.get('client', '')
    date = data.get('date', '')
    items = data.get('items', [])

    if not service_provider or not client or not date or not items:
        return jsonify({'error': 'Dados insuficientes'}), 400

    total_value = sum(item.get('value', 0) for item in items)

    # Define o tamanho da página e margens
    page_width = 8.5 * inch
    page_height = 11 * inch
    margin = 0.5 * inch
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=(page_width, page_height),
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

    # Cria a tabela para os dados fixos e logo (substituindo logo por espaço em branco)
    info_table_data = [
        [Table([
            [Paragraph(f"<b>Prestador(a) de serviço:</b> {service_provider}", style_provider)],
            [Paragraph(f"<b>Cliente:</b> {client}", style_fixed_info)],
            [Paragraph(f"<b>Valor total:</b> R$ {total_value:.2f}", style_fixed_info)],
            [Paragraph(f"<b>Data:</b> {date}", style_fixed_info)]
        ], colWidths=[table_width/2.0]), Spacer(1.5 * inch, 1.5 * inch)]  # Espaço em branco no lugar do logo
    ]

    # Cria a tabela para os dados fixos
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
        ["Referência", "Descrição", "Serviço", "Valor"]
    ]
    
    for item in items:
        ref = item.get('ref', '')
        description = item.get('description', '')
        service = item.get('service', '')
        value = item.get('value', 0)
        items_data.append([ref, description, service, f"R$ {value:.2f}"])

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

    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='recibo.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)