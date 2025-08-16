from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.legends import Legend
import io
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

def generate_monthly_report(user, year, month, transactions, total_income, total_expenses, 
                          category_data, accounts, budgets, goals):
    # Create buffer
    buffer = io.BytesIO()
    
    # Create document
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1976D2'),
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#1976D2'),
        spaceAfter=12
    )
    
    # Title
    month_name = datetime(year, month, 1).strftime('%B %Y')
    elements.append(Paragraph(f'Financial Report - {month_name}', title_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # User info
    elements.append(Paragraph(f'{user.first_name} {user.last_name}', styles['Normal']))
    elements.append(Paragraph(f'Report Generated: {datetime.now().strftime("%B %d, %Y")}', styles['Normal']))
    elements.append(Spacer(1, 0.3*inch))
    
    # Summary Section
    elements.append(Paragraph('Monthly Summary', heading_style))
    
    summary_data = [
        ['', 'Amount'],
        ['Total Income', f'${total_income:,.2f}'],
        ['Total Expenses', f'${total_expenses:,.2f}'],
        ['Net Income', f'${total_income - total_expenses:,.2f}'],
        ['Transactions', str(len(transactions))]
    ]
    
    summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Category Breakdown
    elements.append(Paragraph('Category Breakdown', heading_style))
    
    # Create pie chart for expenses
    if category_data.get('expense'):
        expense_chart = create_pie_chart(category_data['expense'], 'Expense Categories')
        elements.append(expense_chart)
        elements.append(Spacer(1, 0.2*inch))
    
    # Category table
    category_table_data = [['Category', 'Type', 'Amount', 'Transactions']]
    
    for cat_type, categories in category_data.items():
        for cat_name, cat_info in categories.items():
            category_table_data.append([
                cat_name,
                cat_type.capitalize(),
                f'${cat_info["total"]:,.2f}',
                str(cat_info['count'])
            ])
    
    if len(category_table_data) > 1:
        cat_table = Table(category_table_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        cat_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(cat_table)
    
    elements.append(PageBreak())
    
    # Account Balances
    elements.append(Paragraph('Account Balances', heading_style))
    
    account_data = [['Account Name', 'Type', 'Balance']]
    total_balance = 0
    
    for account in accounts:
        account_data.append([
            account.account_name,
            account.account_type.capitalize(),
            f'${account.balance:,.2f}'
        ])
        total_balance += float(account.balance)
    
    account_data.append(['', 'Total:', f'${total_balance:,.2f}'])
    
    account_table = Table(account_data, colWidths=[3*inch, 2*inch, 2*inch])
    account_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (-2, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(account_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Budget Performance
    if budgets:
        elements.append(Paragraph('Budget Performance', heading_style))
        
        budget_data = [['Category', 'Budgeted', 'Spent', 'Remaining', 'Status']]
        
        for budget in budgets:
            # Calculate spent for this month
            month_spent = sum(
                abs(t.amount) for t in transactions 
                if t.category_id == budget.category_id and t.transaction_type == 'expense'
            )
            
            remaining = float(budget.budget_amount) - month_spent
            utilization = (month_spent / float(budget.budget_amount)) * 100 if budget.budget_amount > 0 else 0
            
            if utilization > 100:
                status = 'Over Budget'
            elif utilization >= 80:
                status = 'Near Limit'
            else:
                status = 'On Track'
            
            budget_data.append([
                budget.category.category_name,
                f'${budget.budget_amount:,.2f}',
                f'${month_spent:,.2f}',
                f'${remaining:,.2f}',
                status
            ])
        
        budget_table = Table(budget_data, colWidths=[2*inch, 1.3*inch, 1.3*inch, 1.3*inch, 1.5*inch])
        budget_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(budget_table)
        elements.append(Spacer(1, 0.3*inch))
    
    # Financial Goals
    if goals:
        elements.append(Paragraph('Financial Goals Progress', heading_style))
        
        goal_data = [['Goal', 'Target', 'Current', 'Progress', 'Target Date']]
        
        for goal in goals[:5]:  # Show top 5 goals
            progress = (float(goal.current_amount) / float(goal.target_amount)) * 100 if goal.target_amount > 0 else 0
            
            goal_data.append([
                goal.goal_name,
                f'${goal.target_amount:,.2f}',
                f'${goal.current_amount:,.2f}',
                f'{progress:.1f}%',
                goal.target_date.strftime('%m/%d/%Y') if goal.target_date else 'No target'
            ])
        
        goal_table = Table(goal_data, colWidths=[2.5*inch, 1.2*inch, 1.2*inch, 1*inch, 1.5*inch])
        goal_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(goal_table)
    
    # Build PDF
    doc.build(elements)
    
    return buffer

def create_pie_chart(data_dict, title):
    # Create matplotlib pie chart
    fig, ax = plt.subplots(figsize=(6, 4))
    
    labels = list(data_dict.keys())
    values = [info['total'] for info in data_dict.values()]
    
    # Create pie chart
    wedges, texts, autotexts = ax.pie(values, labels=labels, autopct='%1.1f%%', 
                                      startangle=90, textprops={'fontsize': 8})
    
    ax.set_title(title, fontsize=12, fontweight='bold')
    
    # Save to buffer
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', bbox_inches='tight', dpi=150)
    img_buffer.seek(0)
    plt.close()
    
    # Create ReportLab image
    img = Image(img_buffer, width=5*inch, height=3.3*inch)
    return img