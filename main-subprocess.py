import openpyxl
import subprocess

# 读取 Excel 文件中的 BMC IP、用户名和密码
def read_bmc_credentials_from_excel(file_path, sheet_name):
    bmcs = []
    wb = openpyxl.load_workbook(file_path)
    sheet = wb[sheet_name]
    for row in sheet.iter_rows(values_only=True):
        bmc_ip = row[0]
        bmc_user = row[1]
        bmc_password = row[2]
        bmcs.append((bmc_ip, bmc_user, bmc_password))
    return bmcs

# 使用ipmitool添加BMC账户密码
def add_bmc_credentials(bmc):
    # 本机创建新用户流程参考
    # ipmitool -I lanplus -H 172.100.70.43 -U admin -P mypassword user set name 9 mytest
    # ipmitool -I lanplus -H 172.100.70.43 -U admin -P mypassword user set password 9 mypassword2020!
    # ipmitool -I lanplus -H 172.100.70.43 -U admin -P mypassword user priv 9 4
    # ipmitool -I lanplus -H 172.100.70.43 -U admin -P mypassword user enable 9
    # ipmitool -I lanplus -H 172.100.70.43 -U admin -P mypassword channel set access 1 9 callin=on ipmi=on link=on
    # ipmitool -I lanplus -H 172.100.70.43 -U mytest -P mypassword user list

    # 构造ipmitool命令
    add_name = f"ipmitool -I lanplus -H {bmc[0]} -U {bmc[1]} -P {bmc[2]} user set name {bmc_id} {bmc_name}"
    print(add_name)
    # 执行命令
    subprocess.run(add_name, shell=True, capture_output=True, text=True)
    # 构造ipmitool命令
    add_password = f"ipmitool -I lanplus -H {bmc[0]} -U {bmc[1]} -P {bmc[2]} user set password {bmc_id} {bmc_password}"
    print(add_password)
    # 执行命令
    subprocess.run(add_password, shell=True, capture_output=True, text=True)
    # 构造ipmitool命令
    add_priv = f"ipmitool -I lanplus -H {bmc[0]} -U {bmc[1]} -P {bmc[2]} user priv {bmc_id} {bmc_priv}"
    print(add_priv)
    # 执行命令
    subprocess.run(add_priv, shell=True, capture_output=True, text=True)
    # 构造ipmitool命令
    enable = f"ipmitool -I lanplus -H {bmc[0]} -U {bmc[1]} -P {bmc[2]} user enable {bmc_id}"
    print(enable)
    # 执行命令
    subprocess.run(enable, shell=True, capture_output=True, text=True)
    # 构造ipmitool命令
    channel = f"ipmitool -I lanplus -H {bmc[0]} -U {bmc[1]} -P {bmc[2]} channel setaccess 1 {bmc_id} callin=on ipmi=on link=on"
    print(channel)
    # 执行命令
    subprocess.run(channel, shell=True, capture_output=True, text=True)
    # 构造ipmitool命令
    check= f"ipmitool -I lanplus -H {bmc[0]} -U {bmc_name} -P {bmc_password} user list"
    print(check)
    # 执行命令
    result = subprocess.run(check, shell=True, capture_output=True, text=True)
    # 检查执行结果
    if result.returncode == 0:
        print(f"成功为IP地址 {bmc[0]} 添加BMC账户密码。")
    else:
        print(f"无法为IP地址 {bmc[0]} 添加BMC账户密码。错误信息：{result.stderr}")

# 主程序
if __name__ == "__main__":
    file_path = "./ip-43.xlsx"      # Excel 表格的工作表
    sheet_name = "Sheet1"           # Excel 表格的工作表名称
    bmc_id = 8                    # 范围1-16 建议使用不常用的数字
    bmc_name = "mye8"             # 新账户名
    bmc_password = "mypassword"   # 新账户密码
    bmc_priv = 4                  # 新账户级别
    # 读取 Excel 文件中的 BMC IP、用户名和密码
    bmcs = read_bmc_credentials_from_excel(file_path, sheet_name)
    # 对表格中的主机新增账户和密码
    for bmc in bmcs:
        print(bmc[0],bmc[1],bmc[2])
        add_bmc_credentials(bmc)
