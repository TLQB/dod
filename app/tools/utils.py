import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import xlsxwriter

def number_to_char(number):
    if 1 <= number <= 26:
        return chr(number + 64)
    else:
        raise ValueError("Number must be between 1 and 26")

def get_sheet_names(file):
    """Returns the list of sheet names in the Excel file."""
    excel_file = pd.ExcelFile(file)
    return excel_file.sheet_names

def get_all_brands(file):
    """Returns a sorted list of unique brands in the Excel file."""
    all_sheets = pd.read_excel(file, sheet_name=None)
    unique_brands = set()
    for s_name, sheet_data in all_sheets.items():
        if "Brand" in sheet_data.columns:
            unique_brands.update(sheet_data["Brand"].dropna().unique())
    return sorted(unique_brands)

def get_column_names(file):
    """Returns the list of column names in the first sheet of the Excel file."""
    df = pd.read_excel(file, sheet_name=0)  # Read the first sheet to get column names
    return df.columns.tolist()

def process_and_export_data(
    input_file_path,
    output_file_path,
    selected_columns,
    sheet_name_checked,
    brand_checked,
):
    all_sheets = pd.read_excel(input_file_path, sheet_name=None)
    with pd.ExcelWriter(output_file_path, engine="xlsxwriter") as writer:
        for index, (s_name, sheet_data) in enumerate(all_sheets.items()):
            if s_name not in sheet_name_checked:
                continue

            color = [
                "green",
                "purple",
                "yellow",
                "pink",
                "black",
                "white",
                "red",
                "blue",
            ]
            df = sheet_data
            # Loại bỏ các row có 'Last Selling Price' bằng 0
            df_filtered = df.query("`Last Selling Price` != 0")

            # Sắp xếp DataFrame theo cột 'Sales QTY' từ lớn đến bé
            df_sorted = df_filtered.sort_values(by="Sales QTY", ascending=False)

            # [
            #     'No.',
            #     'Search Period',
            #     'Category',
            #     'Brand',
            #     'Shop',
            #     'Corner Name',
            #     'Item',
            #     'Class',
            #     'Subclass',
            #     'Ref No.',
            #     'Product Name',
            #     'Product Code',
            #     'Inv.-In\nYear',
            #     'B/L Mgt ID',
            #     'Valid Date',
            #     'Inv. In Date',
            #     'Size',
            #     'Color',
            #     'Volume',
            #     'Material',
            #     'Gender',
            #     'Line',
            #     'Source Code',
            #     'Season',
            #     'General/Refund',
            #     'Currency Code Supply',
            #     'Cost',
            #     'Last Selling Price',
            #     'Offline Sales QTY',
            #     'Online Sales QTY',
            #     'Special Sales QTY',
            #     'Sales QTY',
            #     'Offline Revenues',
            #     'Online Revenues',
            #     'Special Sales Total Sale Amount',
            #     'Sales Amount',
            #     'Offline Net Sales',
            #     'Online Net Sales',
            #     'Special Sales Net Sales',
            #     'Sales(Net)',
            #     '입국장 재고수량',
            #     'Inv. QTY',
            #     'Stock Price'
            # ]
            grouped_totals = (
                df_sorted.groupby("Brand")
                .agg(
                    {
                        "Search Period": lambda x: "",
                        "Category": lambda x: "",
                        "Shop": lambda x: "",
                        "Corner Name": lambda x: "",
                        "Item": lambda x: "",
                        "Class": lambda x: "",
                        "Subclass": lambda x: "",
                        "Product Code": lambda x: "",
                        "Inv.-In\nYear": lambda x: "",
                        "Valid Date": lambda x: "",
                        "Size": lambda x: "",
                        "Color": lambda x: "",
                        "Material": lambda x: "",
                        "Gender": lambda x: "",
                        "Season": lambda x: "",
                        "General/Refund": lambda x: "",
                        "Currency Code Supply": lambda x: "",
                        "Cost": lambda x: "",
                        "Offline Net Sales": "sum",
                        "Online Net Sales": "sum",
                        "Last Selling Price": lambda x: "",
                        "Sales QTY": "sum",
                        "Sales Amount": "sum",
                        "Inv. QTY": "sum",
                        "Stock Price": "sum",
                    }
                )
                .reset_index()
            )

            for branch_name, branch_data in df_sorted.groupby("Brand"):
                if branch_name not in brand_checked:
                    continue
                # Add a new column for row numbers and restart from 1 for each sheet
                branch_data["No."] = range(1, len(branch_data) + 1)

                branch_total = grouped_totals[
                    grouped_totals["Brand"] == branch_name
                ]
                branch_total["No."] = ""
                branch_total["Ref No."] = ""
                branch_total["Product Name"] = "Total"

                branch_data_with_total = pd.concat(
                    [
                        branch_total[selected_columns],
                        branch_data[selected_columns],
                    ]
                )

                sheet_name = branch_name + "_" + s_name

                branch_data_with_total.to_excel(
                    writer,
                    sheet_name=sheet_name,
                    index=False,
                    startrow=2,
                    header=False,
                )

                # Get the Worksheet object and write the caption
                worksheet = writer.sheets[sheet_name]

                worksheet.set_tab_color(color[index])

                # Get the current month and year
                # current_month_year = datetime.now().strftime("%b %Y")
                # Tính tháng trước đó
                previous_month = datetime.now() - relativedelta(months=1)
                previous_month_year = previous_month.strftime("%b %Y")

                if s_name.startswith("DNDT"):
                    place = "DA NANG DOWNTOWN"
                elif s_name.startswith("NTAP"):
                    place = "NHA TRANG AIRPORT"
                elif s_name.startswith("DNAP"):
                    place = "DA NANG AIRPORT"
                else:
                    place = "All"

                title = f"{branch_name} MONTHLY SALES REPORT \n {previous_month_year} {place}"

                # Set title format
                title_format = writer.book.add_format(
                    {
                        "bold": True,
                        "font_size": 11,
                        "align": "center",
                        "valign": "vcenter",
                    }
                )
                title_format.set_text_wrap()
                worksheet.set_row(0, worksheet.default_row_height * 2)

                # Write the title in the first row
                for col_num, value in enumerate(selected_columns):
                    worksheet.write(1, col_num, value, title_format)

                char = number_to_char(len(selected_columns))

                # Center the title in the merged cells
                range_title = "A1" + ":" + str(char) + "1"
                worksheet.merge_range(range_title, title, title_format)

                # Auto-resize row height based on content
                for i, col in enumerate(selected_columns):
                    max_len = max(
                        [
                            len(str(value))
                            for value in branch_data_with_total[col]
                        ]
                    )
                    worksheet.set_column(i, i, max_len + 2)  # Set column width
                # Tô màu xám cho hàng tổng
                border_format = writer.book.add_format({"border": 1})

                max_row = len(branch_data_with_total)
                max_col = len(selected_columns)

                range_header = "A2" + ":" + str(char) + "2"
                worksheet.conditional_format(
                    range_header,
                    {
                        "type": "no_blanks",
                        "format": writer.book.add_format(
                            {
                                "bg_color": "#778899",
                                "font_color": "#FFFFFF",
                            }
                        ),
                    },
                )

                range_total = "A3" + ":" + str(char) + "3"
                worksheet.conditional_format(
                    range_total,
                    {
                        "type": "formula",
                        "criteria": "=TRUE",
                        "format": writer.book.add_format(
                            {"bg_color": "#D3D3D3"}
                        ),
                    },
                )

                worksheet.conditional_format(
                    xlsxwriter.utility.xl_range(
                        1, 0, max_row + 1, max_col - 1
                    ),  # Phạm vi ô (hàng, cột, hàng_cuối, cột_cuối)
                    {"type": "no_blanks", "format": border_format},
                )
                # Add bold formatting to the "Total" row
                bold_format = writer.book.add_format({"bold": True})
                worksheet.set_row(1, 30)
                worksheet.set_row(2, cell_format=bold_format)

                # Center the "No." column
                center_format = writer.book.add_format({"align": "center"})
                worksheet.set_column(
                    0, 0, 3, center_format
                )  # Set width and alignment for "Row Number" column

                # Format numerical columns with commas
                num_format = writer.book.add_format({"num_format": "#,##0"})
                for col in [
                    "Last Selling Price",
                    "Sales QTY",
                    "Sales Amount",
                    "Inv. QTY",
                ]:
                    col_idx = selected_columns.index(col)
                    worksheet.set_column(col_idx, col_idx, 15, num_format)

                worksheet.set_row(2, 15, num_format)
                worksheet.set_row(1, 14)