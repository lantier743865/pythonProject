# This is a sample Python script.
import os

project_android_path = "/Users/wuxiaolong/project/qianshou-android"
project_ios_path = "/Users/wuxiaolong/project/qianshou-ios"
tracking_class_name_with_package_java = "com.tantan.x.track.Tracking;"
tracking_class_name_with_package_kt = "com.tantan.x.track.Tracking"
tracking_class_name = "Tracking"
tracking_method_name_map = {
    "sendMC": [],
    "sendMV": [],
    "sendPV": [],
    "sendSC": [],
    "sendUBC": [],
    "sendMS": [],
    "sendBO": [],
    "sendBP": [],
    "createPageHelper": [],
}
# 此处必须加方法返回值，否则会匹配代码调用处的pageId()、this.pageId()、act().pageId()、getPageId()
page_id_java_method_name_pageId = "String pageId()"
# fun getPageId(): String
# override fun pageId() = "p_matchmaker_purchase_page"

page_id_kt_method_name_getPageId = "fun getPageId()"
page_id_kt_method_name_pageId = "fun pageId()"
page_id_kt_method_name_pageId_one_line = "fun pageId() ="

valid_pid_map = {

}

invalid_pid_map = {

}

valid_eid_map = {

}

invalid_eid_map = {

}

eid_file = open('eid.txt', mode='w')
pid_file = open('pid.txt', mode='w')



def find_all_file_with_suffix(dir, suffix, fl):
    for f in os.listdir(dir):  # 遍历整个文件夹
        path = os.path.join(dir, f)
        if os.path.isfile(path):  # 判断是否为一个文件，排除文件夹
            if f.endswith(suffix):
                if not path.__contains__("/build"):
                    fl.append(dir + "/" + f)
        elif os.path.isdir(path):
            new_dir = path
            find_all_file_with_suffix(new_dir, suffix, fl)
    return fl

pid_rule = '"p_'
eid_rule = '"e_'
def find_all_id_method(f):
    file = open(f, "r")
    lines = file.readlines()
    for line in lines:
        # print('line->' + format(line))
        if line.__contains__(pid_rule):
            count = line.count(pid_rule)
            if count > 0:
                index = line.find(pid_rule)
                temp = line[index:]
                params = temp.split('"')
                if count == 1:
                    pid = params[1]
                    if pid in invalid_pid_map:
                        valid_pid_map[pid] += 1
                    else:
                        valid_pid_map[pid] = 1
                else:
                    for pid in params:
                        if pid.__contains__('p_'):
                            if pid in invalid_pid_map:
                                valid_pid_map[pid] += 1
                            else:
                                valid_pid_map[pid] = 1

        if line.__contains__(eid_rule):
            count = line.count(eid_rule)
            if count > 0:
                index = line.find(eid_rule)
                temp = line[index:]
                params = temp.split('"')
                if count == 1:
                    eid = params[1]
                    if eid in valid_eid_map:
                        valid_eid_map[eid] += 1
                    else:
                        valid_eid_map[eid] = 1
                else:
                    for eid in params:
                        if eid.__contains__('e_'):
                            if eid in valid_eid_map:
                                valid_eid_map[eid] += 1
                            else:
                                valid_eid_map[eid] = 1


# 此方法已废弃，只维护 find_all_kt_track_method
def find_all_java_track_method(f):
    file = open(f, "r")
    lines = file.readlines()
    is_need_go_ahead = False
    for line in lines:
        if line.strip().endswith(tracking_class_name_with_package_java):
            is_need_go_ahead = True
            break
    if is_need_go_ahead:
        for line in lines:
            if line.__contains__(tracking_class_name):
                for key, value in tracking_method_name_map.items():
                    if line.__contains__(key):
                        # 总体切割
                        temp = line.strip().split(',')
                        if len(temp) < 2:
                            print('此处换行了，请手动处理->'+f)
                        else:
                            # 去除代码行前后空格
                            subStr = temp[0].strip()
                            # count = methodAndPage.count('(')
                            # 存在pageid从方法调用情况
                            index = subStr.find('(')
                            # 找出类名和方法名
                            classAndMethod = subStr[0:index]
                            params = classAndMethod.split('.')
                            className = params[0]
                            methodName = params[1]

                            # 算出pid
                            pidTemp = subStr[index + 1:]
                            pidParams = pidTemp.split('"')
                            if len(pidParams) > 1:
                                # 这种才是正常情况，用双引号包裹的
                                pid = pidParams[1]

                                if pid in valid_pid_map:
                                    valid_pid_map[pid] += 1
                                else:
                                    valid_pid_map[pid] = 1

                            else:
                                pid = pidParams[0]
                                if pid in invalid_pid_map:
                                    invalid_pid_map[pid] += 1
                                else:
                                    invalid_pid_map[pid] = 1
                                # print('此处pid不能直接使用，请手动处理')

                            # 算出eid
                            eidTemp = temp[1]
                            # print('temp->' + format(temp))
                            # print('eidTemp->' + format(eidTemp))
                            eidParams = eidTemp.split('"')
                            if len(eidParams) > 1:
                                # 这种才是正常情况，用双引号包裹的
                                eid = eidParams[1]
                                if eid in valid_eid_map:
                                    valid_eid_map[eid] += 1
                                else:
                                    valid_eid_map[eid] = 1
                            else:
                                eid = eidParams[0]
                                if eid in invalid_eid_map:
                                    invalid_eid_map[eid] += 1
                                else:
                                    invalid_eid_map[eid] = 1
                                # print('此处eid不能直接使用，请手动处理')

                            print('pid->' + pid)
                            print('eid->' + eid)
                            eid_file.write(eid+'\n')
                            pid_file.write(pid+'\n')
                        break
                        # print('line->' + format(line))
                        # temp = line.split('.')
                        # className = temp[0].strip()
                        # otherParams = temp[1].split(',')
                        # methodAndPage = otherParams[0].split("(")
                        # methodName = methodAndPage[0]
                        # pageId = methodAndPage[1]
                        # print('otherParams->' + format(otherParams))
                        # eid = otherParams[1]
                        # print('类名->' + className)
                        # print('方法名->' + methodName)
                        # if methodName.__eq__("createPageHelper"):
                        #     print('pid->' + pageId)
                        # else:
                        #     print('pid->'+pageId)
                        #     print('eid->'+eid)


def find_pageid_method(f):
    file = open(f, "r")
    lines = file.readlines()
    is_need_go_ahead = False
    for line in lines:
        if line.strip().endswith(tracking_class_name_with_package_kt) or line.strip().endswith(tracking_class_name_with_package_java):
            is_need_go_ahead = True
            break
    if is_need_go_ahead:
        line_feed = False
        has_get_page_id = False
        has_page_id_java = False
        has_page_id_kt = False
        pid = ''
        for line in lines:
            if line_feed:
                line_feed = False
                if has_page_id_java:
                    index = line.find('return')
                    temp = line[index+6:]
                    pid_params = temp.split('"')
                    if len(pid_params) > 2:
                        pid = pid_params[1]
                    if pid in invalid_pid_map:
                        valid_pid_map[pid] += 1
                    else:
                        valid_pid_map[pid] = 1
                if has_page_id_kt:
                    pid_params = line.split('"')
                    # print('pid_params->' + format(pid_params))
            # print('line->' + format(line))

            # print('__contains__->' + format(line.strip().__contains__(page_id_kt_method_name_pageId_one_line)))
            if line.strip().__contains__(page_id_kt_method_name_pageId_one_line):
                pid_params = line.split('"')
                if len(pid_params) > 2:
                    pid = pid_params[1]
                print('pid->' + format(pid))
                if pid in invalid_pid_map:
                    valid_pid_map[pid] += 1
                else:
                    valid_pid_map[pid] = 1
                break
            if line.__contains__(page_id_java_method_name_pageId):
                line_feed = True
                has_page_id_java = True
            if line.__contains__(page_id_kt_method_name_getPageId) :
                line_feed = True
                has_get_page_id = True
            if line.__contains__(page_id_kt_method_name_pageId):
                line_feed = True
                has_page_id_kt = True
                print('line_feed->' + format(line_feed))
            else:
                line_feed = False

def find_all_kt_track_method(f):
    file = open(f, "r")
    lines = file.readlines()
    is_need_go_ahead = False
    for line in lines:
        if line.strip().endswith(tracking_class_name_with_package_kt) or line.strip().endswith(tracking_class_name_with_package_java):
            is_need_go_ahead = True
            break
    if is_need_go_ahead:

        line_feed = False
        compose_str = ''
        for line in lines:
            if line_feed:
                line_feed = False
                compose_str += line
                # print('换行字符串->' + compose_str)
            else:
                compose_str = line

            if compose_str.__contains__(tracking_class_name):
                dealLine = compose_str
                index = compose_str.find(tracking_class_name)
                if index != -1:
                    dealLine = compose_str[index:]
                line = dealLine


                for key, value in tracking_method_name_map.items():
                    if line.__contains__(key):
                        # 总体切割
                        temp = line.strip().split(',')
                        if len(temp) < 2:
                            line_feed = True
                            print(''
                                  '->' + format(line_feed))
                            continue
                        else:
                            # 去除代码行前后空格
                            line_feed = False
                            subStr = temp[0].strip()
                            # count = methodAndPage.count('(')
                            # 存在pageid从方法调用情况
                            index = subStr.find('(')
                            # 找出类名和方法名
                            classAndMethod = subStr[0:index]
                            params = classAndMethod.split('.')
                            className = params[0]
                            methodName = params[1]

                            # 算出pid
                            pidTemp = subStr[index+1:]
                            pidParams = pidTemp.strip().split('"')
                            if len(pidParams) > 1:
                                # 这种才是正常情况，用双引号包裹的
                                pid = pidParams[1]

                                if pid in valid_pid_map:
                                    valid_pid_map[pid] += 1
                                else:
                                    valid_pid_map[pid] = 1

                            else:
                                pid = pidParams[0]
                                if pid in invalid_pid_map:
                                    invalid_pid_map[pid] += 1
                                else:
                                    invalid_pid_map[pid] = 1
                                # print('此处pid不能直接使用，请手动处理')

                            # 算出eid
                            eidTemp = temp[1]
                            # print('temp->' + format(temp))
                            # print('eidTemp->' + format(eidTemp))
                            eidParams = eidTemp.split('"')
                            if len(eidParams) > 1:
                                # 这种才是正常情况，用双引号包裹的
                                eid = eidParams[1]
                                if pid in valid_eid_map:
                                    valid_eid_map[eid] += 1
                                else:
                                    invalid_eid_map[eid] = 1
                            else:
                                eid = eidParams[0]
                                if pid in invalid_eid_map:
                                    invalid_eid_map[pid] += 1
                                else:
                                    invalid_eid_map[pid] = 1
                                # print('此处eid不能直接使用，请手动处理')



                            print('pid->' + pid)
                            print('eid->' + eid)
                            eid_file.write(eid + '\n')
                            pid_file.write(pid + '\n')
                        break



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    kt_file_list = []
    java_file_list = []


    for f_java in find_all_file_with_suffix(project_android_path, ".java", java_file_list):
        # print("java->" + f_java)
        find_all_id_method(f_java)
    for f_kt in find_all_file_with_suffix(project_android_path, ".kt", java_file_list):
        # print("f_kt->" + f_kt)
        find_all_id_method(f_kt)
    # for f_kt in find_all_file_with_suffix(project_ios_path, ".swift", java_file_list):
    #     # print("f_kt->" + f_kt)
    #     find_all_id_method(f_kt)
    # #
    # for f_kt in find_all_file_with_suffix(project_android_path, ".kt", kt_file_list):
    #     # print("kt->" + f_kt)
    #     find_all_kt_track_method(f_kt)
    # for f_kt in find_all_file_with_suffix(project_android_path, ".java", java_file_list):
    #     # print("kt->" + f_kt)
    #     find_all_kt_track_method(f_kt)

    valid_pid_key_count = 0
    valid_pid_count = 0
    invalid_pid_key_count = 0
    invalid_pid_count = 0
    pid_key_count = 0
    pid_count = 0

    for (key, value) in valid_pid_map.items():
        valid_pid_key_count += 1
        valid_pid_count += valid_pid_map[key]
        pid_file.write(key + '\n')
    for (key, value) in invalid_pid_map.items():
        invalid_pid_key_count += 1
        invalid_pid_count += invalid_pid_map[key]

    print('valid_pid_key_count->' + format(valid_pid_key_count))
    print('valid_pid_count->' + format(valid_pid_count))

    # print('invalid_pid_key_count->' + format(invalid_pid_key_count))
    # print('invalid_pid_count->' + format(invalid_pid_count))

    pid_key_count = valid_pid_key_count + invalid_pid_key_count
    pid_count = valid_pid_count + invalid_pid_count

    # print('pid_key_count->' + format(pid_key_count))
    # print('pid_count->' + format(pid_count))

    valid_eid_key_count = 0
    valid_eid_count = 0
    invalid_eid_key_count = 0
    invalid_eid_count = 0
    eid_key_count = 0
    eid_count = 0

    for (key, value) in valid_eid_map.items():
        valid_eid_key_count += 1
        valid_eid_count += valid_eid_map[key]
        eid_file.write(key + '\n')
    for (key, value) in invalid_eid_map.items():
        invalid_eid_key_count += 1
        invalid_eid_count += invalid_eid_map[key]

    print('valid_eid_key_count->' + format(valid_eid_key_count))
    print('valid_eid_count->' + format(valid_eid_count))

    # print('invalid_eid_key_count->' + format(invalid_eid_key_count))
    # print('invalid_eid_count->' + format(invalid_eid_count))

    eid_key_count = valid_eid_key_count + invalid_eid_key_count
    eid_count = valid_eid_count + invalid_eid_count

    # print('eid_key_count->' + format(eid_key_count))
    # print('eid_count->' + format(eid_count))
    key_count = eid_key_count + pid_key_count
    id_count = eid_count + pid_count
    # print('valid_eid_map->' + format(valid_eid_map))
    print('key_count->' + format(key_count))
    print('id_count->' + format(id_count))






    # find_all_java_track_method(
    #     "/Users/wuxiaolong/project/qianshou-android/app/src/main/java/com/tantan/x/dating/ui/VideoChatActivity.java")
    # find_all_kt_track_method("/Users/wuxiaolong/project/qianshou-android/app/src/main/java/com/tantan/x/apm/TrackWrapper.kt")
    # find_all_kt_track_method("/Users/wuxiaolong/project/qianshou-android/app/src/main/java/com/tantan/x/vip/MVipBuyBannerAdapter.kt")
    # find_all_kt_track_method("/Users/wuxiaolong/project/qianshou-android/app/src/main/java/com/tantan/x/group/binder/FeedGroupViewBinder.kt")
    # find_all_kt_track_method("/Users/wuxiaolong/project/qianshou-android/app/src/main/java/com/tantan/x/group/binder/NotifyLikeViewBinder.kt")
    # find_all_kt_track_method("/Users/wuxiaolong/project/qianshou-android/app/src/main/java/com/tantan/x/likecard/favoriteguide/FavoriteGuideAct.kt")
    # find_all_kt_track_method("/Users/wuxiaolong/project/qianshou-android/app/src/main/java/com/tantan/x/like/ui/LikeItemBinder.kt")
    # find_all_java_track_method("/Users/wuxiaolong/project/qianshou-android/app/src/main/java/com/tantan/x/main/recommends/recommend/view/swipe/NewSwipeCardGroup.java")

    # find_all_kt_track_method("/Users/wuxiaolong/project/qianshou-android/app/src/main/java/com/tantan/x/dating/ui/VideoChatActivity.java")
    # find_pageid_method("/Users/wuxiaolong/project/qianshou-android/app/src/main/java/com/tantan/x/dating/ui/VideoChatActivity.java")
    # find_pageid_method("/Users/wuxiaolong/project/qianshou-android/app/src/main/java/com/tantan/x/vip/MVipBuyAct.kt")
    # find_all_id_method("/Users/wuxiaolong/project/qianshou-ios/tantan-x/Source/Payment/Managers/IAPManager.swift")
    # find_all_id_method("Users/wuxiaolong/project/qianshou-ios/tantan-x/Source/ChatV2/Flower[收花列表]/Controllers/ConversationFlowersViewController.swift")
    # find_all_id_method("/Users/wuxiaolong/project/qianshou-ios/tantan-x/Source/ChatV2/Flower\[收花列表\]/Controllers/ConversationFlowersViewController.swift")
    # find_all_id_method("/Users/wuxiaolong/project/qianshou-android/app/src/main/java/com/tantan/x/register/address/SelectAddressDialog.kt")


    # print('valid_pid_map->' + format(valid_pid_map))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

# TODO: 再查找pageId()方法
