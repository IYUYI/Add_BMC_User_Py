import openpyxl
from pyghmi.ipmi import command as ipmi_command

# 定义 BMC 账户信息
bmc_username = "myusername"
bmc_password = "MyPassword2024!"

# 读取 Excel 文件中的 IP 地址
def read_ip_addresses_from_excel(file_path, sheet_name):
    ip_addresses = []
    wb = openpyxl.load_workbook(file_path)
    sheet = wb[sheet_name]
    for row in sheet.iter_rows(values_only=True):
        ip_address = row[0]  # 假设 IP 地址在第一列
        ip_addresses.append(ip_address)
    return ip_addresses

# 添加 BMC 账户到指定的 IP 地址
def add_bmc_account(ip_address):
    try:
        with ipmi_command.Command(ip_address, bmc_username, bmc_password) as ipmicmd:
            # 添加账户的 IPMI 命令，这里需要根据 Pyghmi 的文档进行具体操作
            # 示例命令（具体命令取决于 BMC 的型号和支持的命令）
            # ipmicmd.set_user_privilege('bmc_username', 'bmc_password', 4)
            print(f"账户成功添加到 {ip_address}")
    except Exception as e:
        print(f"添加账户到 {ip_address} 失败：{str(e)}")

# 主程序
if __name__ == "__main__":
    file_path = "./ip-43.xlsx" # Excel 表格的工作表
    sheet_name = "Sheet1"   # Excel 表格的工作表名称

    ip_addresses = read_ip_addresses_from_excel(file_path, sheet_name)
    # 测试读取ip，并打印
    # 执行bmc账户植入计划
    for ip_address in ip_addresses:
        print(ip_address)
        #add_bmc_account(ip_address)
