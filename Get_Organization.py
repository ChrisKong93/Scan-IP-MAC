def get_mac_organization(macaddr='48:5f:99:a2:0d:47'):
    # print(macaddr)
    # exit()
    macaddrp = macaddr[0:8]
    Organization = ''
    addr = ''
    with open('./oui.txt', encoding='UTF-8') as f:
        lines = f.readlines()  # 调用文件的 readline()方法
        i = 0
    for line in lines:
        if i < 3:
            # print(line)
            pass
        else:
            if macaddrp == line[0:8]:
                # print(macaddrp)
                # print(line)
                l = line.replace(' ', '')
                # print(line)
                l = l.replace('	', '')
                Organization = l[13:-1]
                # print(l[13:-1])
                # print(lines[i + 1])
                addr = lines[i + 2].strip()
                # print(lines[i + 2].strip())
                break
            # elif macaddrp.replace('-', '') == line[0:6]:
            #     print(line)
            #     break
        i += 1
    return Organization, addr


if __name__ == '__main__':
    macaddr = '00-01-6C-06-A6-29'
    Organization = get_mac_organization(macaddr)
    # 打印需要的字段
    print('mac地址：' + macaddr + '\t' + '组织：' + Organization)
