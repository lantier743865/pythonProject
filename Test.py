# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import os

from androguard.misc import AnalyzeAPK
from androguard.core.androconf import load_api_specific_resource_module

path = r"/Users/wuxiaolong/project/qianshou-android"
out_path = r"/Users/didi/PycharmProjects/findLocationManagerApi/"
files = []
path_list = os.listdir(path)
path_list.sort()
for name in path_list:
    if os.path.isfile(os.path.join(path, name)):
        files.append(name)


def main():
    for apkFile in files:
        file_name = os.path.splitext(apkFile)[0]
        print(apkFile)
        if apkFile.startswith('.'):
            continue
        out = AnalyzeAPK(path + '/' + apkFile)
        a = out[0]
        d = out[1]
        dx = out[2]

        app_name = a.get_app_name()
        pkg = a.get_package()
        v_n = a.get_androidversion_name()

        api_inside_filename = os.path.join(out_path, file_name + "_扫描结果.txt")
        api_inside_file = open(api_inside_filename, 'w', encoding='utf-8')

        calling_pkg_dict = {}
        care_method1 = ['requestLocationUpdates', 'removeUpdates', 'getLastKnownLocation', 'requestSingleUpdate',
                        'addNmeaListener', 'addGpsStatusListener']
        care_method = ['getAllCellInfo', 'getConnectionInfo', 'startScan', 'getScanResults', 'requestCellInfoUpdate',
                       'getCellLocation']

        care_method2 = ['requestLocationUpdates','removeLocationUpdates']

        # class_name = 'Lcom/didichuxing/bigdata/dp/locsdk/DIDILocationManager;'
        class_name = 'Landroid/location/LocationManager;'

        # 1.获取定位方法外部调用
        api_inside_file.write(app_name + "、" + pkg + "、" + v_n + "：\n\n")
        api_inside_file.write("------------------------------系统定位Api外部调用函数如下------------------------------：\n\n")
        for meth in dx.classes[class_name].get_methods():
            inside = "系统函数 " + str(meth.name) + '\n'
            if meth.name in care_method1:
                api_inside_file.write(inside)
                for _, call, _ in meth.get_xref_from():
                    class_name = str(call.class_name)
                    if not class_name.startswith('Lcom/didichuxing/bigdata/dp') \
                        and not class_name.startswith('Lcom/didi/vdr') \
                        and not class_name.startswith('Landroidx') \
                        and not class_name.startswith('Lcom/didi/flp'):
                            class_name = '.'.join(class_name.split('/')).replace('L', '')
                            calling = '    调用类 ->' + class_name + ' 方法名： ' + str(call.name) + '\n'
                            package_name = '.'.join(class_name.split('.')[:4])
                            calling_pkg_dict['包名 -> ' + package_name] = ''
                            api_inside_file.write(calling)

        api_inside_file.write("\n")
        api_inside_file.write("检测出的包名如下：\n")

        for pkg in calling_pkg_dict:
            api_inside_file.write("    " + pkg + "\n")
        api_inside_file.write("------------------------------系统定位Api外部调用函数如上------------------------------：\n\n")

        calling_pkg_dict.clear()

        api_inside_file.write("\n")
        api_inside_file.write("\n")
        api_inside_file.write("\n")
        api_inside_file.write("------------------------------Didi定位Api外部调用函数如下------------------------------：\n\n")
        if 'Landroid/net/wifi/WifiManager;' in dx.classes:
            for meth in dx.classes['Landroid/net/wifi/WifiManager;'].get_methods():
                inside = "Location " + str(meth.name) + '\n'
                # if meth.name in care_method:
                api_inside_file.write(inside)
                for _, call, _ in meth.get_xref_from():
                    class_name = str(call.class_name)
                    if not class_name.startswith('Lcom/didichuxing/bigdata/dp'):
                        calling = '    调用类 ->' + class_name + ' 方法名： ' + str(call.name) + '\n'
                        package_name = "/".join(class_name.split("/")[:3])
                        calling_pkg_dict['包名 -> ' + package_name] = ''
                        api_inside_file.write(calling)

        if 'Landroid/telephony/TelephonyManager;' in dx.classes:
            for meth in dx.classes['Landroid/telephony/TelephonyManager;'].get_methods():
                inside = "Location " + str(meth.name) + '\n'
                # if meth.name in care_method:
                api_inside_file.write(inside)
                for _, call, _ in meth.get_xref_from():
                    class_name = str(call.class_name)
                    if not class_name.startswith('Lcom/didichuxing/bigdata/dp'):
                        calling = '    调用类 ->' + class_name + ' 方法名： ' + str(call.name) + '\n'
                        package_name = "/".join(class_name.split("/")[:3])
                        calling_pkg_dict['包名 -> ' + package_name] = ''
                        api_inside_file.write(calling)

        api_inside_file.write("\n")
        api_inside_file.write("检测出的包名如下：\n")

        for pkg in calling_pkg_dict:
            api_inside_file.write("    " + pkg + "\n")
        api_inside_file.write("------------------------------Didi定位Api外部调用函数如上------------------------------：\n\n")

        api_inside_file.close()
        # 2.api和权限映射
        # api_perm_filename = os.path.join(out_path, file_name + "_api-perm.txt")
        # api_perm_file = open(api_perm_filename, 'w', encoding='utf-8')
        # permissionMap = load_api_specific_resource_module('api_permission_mappings')
        # for meth_analysis in dx.get_methods():
        #     meth = meth_analysis.get_method()
        #     name = meth.get_class_name() + "-" + meth.get_name() + "-" + str(
        #         meth.get_descriptor())
        #     for k, v in permissionMap.items():
        #         if name == k:
        #             result = str(meth) + ' : ' + str(v)
        #             api_perm_file.write(result + '\n')
        # api_perm_file.close()
        print("扫描结束")


if __name__ == '__main__':
    main()