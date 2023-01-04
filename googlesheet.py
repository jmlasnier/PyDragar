import re

import gspread
from oauth2client.service_account import ServiceAccountCredentials


def get_worksheet(sheet_id):
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    return client.open_by_key(sheet_id).sheet1


def copy_source_spreadsheet():
    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    new_ss = client.copy(file_id='1yq2TX19iwdCo2Zs3NAnanseSe4O-YVYJORqhyUedpA4')
    return new_ss.id


def add_to_sold_units(cover_id, nb_same_cover):
    sheet = get_worksheet("1FbiPW_wVv2_MgdHaq3R23bSY9XE2gg91dyFHY-q2rHI")  # -------------
    cell = sheet.find(cover_id)
    if cell is None:
        cell = sheet.find('RMX-XX')
    sheet.update_cell(cell.row, cell.col + 1, int(sheet.cell(cell.row, cell.col + 1).value) + nb_same_cover)
    print("added 1 sold unit to: ", cover_id, " in 1FbiPW_wVv2_MgdHaq3R23bSY9XE2gg91dyFHY-q2rHI")


def std_remove_from_inventory(cover_id, nb_same_cover):
    sheet_id = "1mkNrHdHcS44TUIVerOXZ-bSweqSz5qw3ZhJbj218hQs"  # -------------
    sheet = get_worksheet(sheet_id)
    complete_set = ["PS1-DR", "PS1-AR", "PS1-NI", "PS1-GI", "PS1-DI", "PS1-AI", "RS1-GR", "RS1-NR"]
    double_plate_set_integrated = ["RS1-AI", "RS1-DI", "RS1-GI", "RS1-NI"]
    top_plus_bandes_set = []
    double_plate_set_retractable = ["RS1-DR", "RS1-AR"]
    if cover_id in complete_set:
        cell = sheet.find(cover_id)
        sheet.update_cell(cell.row, cell.col + 1, int(sheet.cell(cell.row, cell.col + 1).value) - nb_same_cover)
        print("removed 1 unit : ", cover_id, " in", sheet_id)
    elif cover_id in top_plus_bandes_set:
        pedestrian_code = str(cover_id).replace("R", "P", 1)
        cell = sheet.find(pedestrian_code)
        sheet.update_cell(cell.row, cell.col + 1, int(sheet.cell(cell.row, cell.col + 1).value) - nb_same_cover)
        cell = sheet.find("Bandes")
        sheet.update_cell(cell.row, cell.col + 1, int(sheet.cell(cell.row, cell.col + 1).value) - nb_same_cover)
        print("removed 1 ", pedestrian_code, " and 1 bandes in", sheet_id)
    elif cover_id in double_plate_set_integrated:
        pedestrian_code = str(cover_id).replace("R", "P", 1)
        cell = sheet.find(pedestrian_code)
        sheet.update_cell(cell.row, cell.col + 1, int(sheet.cell(cell.row, cell.col + 1).value) - nb_same_cover)
        cell = sheet.find("PS1-AI")
        sheet.update_cell(cell.row, cell.col + 1, int(sheet.cell(cell.row, cell.col + 1).value) - nb_same_cover)
        print("removed 1 ", pedestrian_code, " and 1 PS1-AI in", sheet_id)
    elif cover_id in double_plate_set_retractable:
        pedestrian_code = str(cover_id).replace("R", "P", 1)
        cell = sheet.find(pedestrian_code)
        sheet.update_cell(cell.row, cell.col + 1, int(sheet.cell(cell.row, cell.col + 1).value) - nb_same_cover)
        cell = sheet.find("PS1-AR")
        sheet.update_cell(cell.row, cell.col + 1, int(sheet.cell(cell.row, cell.col + 1).value) - nb_same_cover)
        print("removed 1 ", pedestrian_code, " and 1 PS1-AR in", sheet_id)


def log_custom_cover(po_number, price_this_cover, cover_id, nb_same_cover):
    sheet = get_worksheet("1ll8PBRPfuSoyz96teXryVYi6vOCjRQR50zzWxUaRlvk")
    empty_row = len(list(filter(None, sheet.col_values(1)))) + 1
    sheet.update_cell(empty_row, 1, po_number)
    sheet.update_cell(empty_row, 2, cover_id)
    sheet.update_cell(empty_row, 3, price_this_cover)
    sheet.update_cell(empty_row, 4, nb_same_cover)
    print("added data to row ", empty_row, " in 1ll8PBRPfuSoyz96teXryVYi6vOCjRQR50zzWxUaRlvk")


# def save_custom_info_for_future_shipping(client_order_id, client_email, client_name, client_adr):
#     sheet = get_worksheet("19P6OjdqSQ98K6nn2rIDe5qB3GKNIfOn8iKgDblyObws")
#     empty_row = len(list(filter(None, sheet.col_values(1)))) + 1
#     sheet.update_cell(empty_row, 1, client_order_id)
#     sheet.update_cell(empty_row, 2, client_email)
#     sheet.update_cell(empty_row, 3, client_name)
#     sheet.update_cell(empty_row, 4, client_adr)
#     print("save future info to row ", empty_row, " in 19P6OjdqSQ98K6nn2rIDe5qB3GKNIfOn8iKgDblyObws")


def get_custom_shipping_info_for_label(order_id):
    sheet_pending = get_worksheet("19P6OjdqSQ98K6nn2rIDe5qB3GKNIfOn8iKgDblyObws")
    order_row = sheet_pending.find(order_id).row
    email = sheet_pending.cell(order_row, 2).value
    name = sheet_pending.cell(order_row, 3).value
    address = sheet_pending.cell(order_row, 4).value

    sheet_pending.update_cell(order_row, 7, "retreived")

    sheet_custom = get_worksheet("1ll8PBRPfuSoyz96teXryVYi6vOCjRQR50zzWxUaRlvk")
    order_rrow = sheet_custom.find(order_id).row
    dim1 = float(str(sheet_custom.cell(order_rrow, 3).value).replace(",", "."))
    dim2 = float(str(sheet_custom.cell(order_rrow, 4).value).replace(",", "."))
    dim3 = float(str(sheet_custom.cell(order_rrow, 5).value).replace(",", "."))
    weight = float(str(sheet_custom.cell(order_rrow, 8).value).replace(",", "."))

    print("retrieved shipping info for order ", order_id)

    return [email, name, address, order_id, dim1, dim2, dim3, weight]


def save_std_sale_repartition(order_id, vente, cost):
    sheet = get_worksheet("1uXbnH4u3Kaq8KXc5E64Furmo39WfxBGaa0nphrz3Su0")  # --------
    empty_row = len(list(filter(None, sheet.col_values(1)))) + 1
    sheet.update_cell(empty_row, 1, order_id)
    sheet.update_cell(empty_row, 2, vente)
    sheet.update_cell(empty_row, 3, cost)
    print("added sale to row ", empty_row, " in 1uXbnH4u3Kaq8KXc5E64Furmo39WfxBGaa0nphrz3Su0")


def write_shipping_price_std(sheet_id, price):
    sheet = get_worksheet(sheet_id)
    sheet.update_cell(7, 1, re.sub(r"\.", ",", price))
    print("updated shipping price in ", sheet_id)


def write_shipping_price_custom(order_id, price):
    sheet = get_worksheet("1ll8PBRPfuSoyz96teXryVYi6vOCjRQR50zzWxUaRlvk")
    row = sheet.find(order_id).row
    sheet.update_cell(row, 10, price)
    print("updated custom shipping price to row ", row, "in 1ll8PBRPfuSoyz96teXryVYi6vOCjRQR50zzWxUaRlvk")


def log_shipping_cost(shipping_price):
    sheet = get_worksheet("1QSWhIPCDNcEqmsOcldTqzvGNvZbfhR7kweM3pGur58k")
    ship_col = sheet.find("postes canada").col
    empty_row = len(list(filter(None, sheet.col_values(ship_col)))) + 1
    sheet.update_cell(empty_row, ship_col, shipping_price)
    print("logged shipping cost to row ", empty_row, " in 1QSWhIPCDNcEqmsOcldTqzvGNvZbfhR7kweM3pGur58k")


def log_client(name, email):
    sheet = get_worksheet("14vHKH_m48MxZfA93PSof4Ohk4B4tanTdxscrIlkj4js")
    empty_row = len(list(filter(None, sheet.col_values(1)))) + 1
    sheet.update_cell(empty_row, 1, name)
    sheet.update_cell(empty_row, 2, email)
    print("logged client to row ", empty_row, "in 14vHKH_m48MxZfA93PSof4Ohk4B4tanTdxscrIlkj4js")


# test eh
if __name__ == "__main__":
    log_client("ss12.22", "dnusnfus")
