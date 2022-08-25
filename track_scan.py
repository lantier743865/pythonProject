# This is a sample Python script.
import os

project_path = "/Users/wuxiaolong/project/qianshou-android"
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

valid_pid_map = {

}

invalid_pid_map = {

}

valid_eid_map = {

}

invalid_eid_map = {

}



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
                                if pid in valid_eid_map:
                                    valid_eid_map[pid] += 1
                                else:
                                    invalid_eid_map[pid] = 1
                            else:
                                eid = eidParams[0]
                                if pid in invalid_eid_map:
                                    invalid_eid_map[pid] += 1
                                else:
                                    invalid_eid_map[pid] = 1
                                # print('此处eid不能直接使用，请手动处理')

                            # print('pid->' + pid)
                            # print('eid->' + eid)
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



def find_all_kt_track_method(f):
    file = open(f, "r")
    lines = file.readlines()
    is_need_go_ahead = False
    for line in lines:
        if line.strip().endswith(tracking_class_name_with_package_kt):
            is_need_go_ahead = True
            break
    if is_need_go_ahead:

        line_feed = False
        compose_str = ''
        for line in lines:
            if line_feed:
                line_feed = False
                compose_str += line
                print('换行字符串->' + compose_str)
            else:
                compose_str = line

            if line.__contains__(tracking_class_name):
                dealLine = line
                index = line.find(tracking_class_name)
                if index != -1:
                    dealLine = line[index:]
                line = dealLine


                for key, value in tracking_method_name_map.items():
                    if line.__contains__(key):
                        # 总体切割
                        temp = line.strip().split(',')
                        if len(temp) < 2:
                            line_feed = True
                            print('此处换行了，请手动处理->' + format(line_feed))
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
                                if pid in valid_eid_map:
                                    valid_eid_map[pid] += 1
                                else:
                                    invalid_eid_map[pid] = 1
                            else:
                                eid = eidParams[0]
                                if pid in invalid_eid_map:
                                    invalid_eid_map[pid] += 1
                                else:
                                    invalid_eid_map[pid] = 1
                                # print('此处eid不能直接使用，请手动处理')



                            print('pid->' + pid)
                            print('eid->' + eid)
                        break



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    kt_file_list = []
    java_file_list = []


    # for f_java in find_all_file_with_suffix(project_path, ".java", java_file_list):
    #     # print("java->" + f_java)
    #     find_all_java_track_method(f_java)
    # #
    # for f_kt in find_all_file_with_suffix(project_path, ".kt", kt_file_list):
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
    for (key, value) in invalid_pid_map.items():
        invalid_pid_key_count += 1
        invalid_pid_count += invalid_pid_map[key]

    # print('valid_pid_key_count->' + format(valid_pid_key_count))
    # print('valid_pid_count->' + format(valid_pid_count))
    #
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
    for (key, value) in invalid_eid_map.items():
        invalid_eid_key_count += 1
        invalid_eid_count += invalid_eid_map[key]

    # print('valid_eid_key_count->' + format(valid_eid_key_count))
    # print('valid_eid_count->' + format(valid_eid_count))
    #
    # print('invalid_eid_key_count->' + format(invalid_eid_key_count))
    # print('invalid_eid_count->' + format(invalid_eid_count))

    eid_key_count = valid_eid_key_count + invalid_eid_key_count
    eid_count = valid_eid_count + invalid_eid_count

    # print('eid_key_count->' + format(eid_key_count))
    # print('eid_count->' + format(eid_count))
    # print('valid_eid_map->' + format(valid_eid_map))

    # find_all_java_track_method(
    #     "/Users/wuxiaolong/project/qianshou-android/app/src/main/java/com/tantan/x/dating/ui/VideoChatActivity.java")
    # find_all_kt_track_method("/Users/wuxiaolong/project/qianshou-android/app/src/main/java/com/tantan/x/apm/TrackWrapper.kt")
    # find_all_kt_track_method("/Users/wuxiaolong/project/qianshou-android/app/src/main/java/com/tantan/x/vip/MVipBuyBannerAdapter.kt")
    # find_all_kt_track_method("/Users/wuxiaolong/project/qianshou-android/app/src/main/java/com/tantan/x/group/binder/FeedGroupViewBinder.kt")
    # find_all_kt_track_method("/Users/wuxiaolong/project/qianshou-android/app/src/main/java/com/tantan/x/group/binder/NotifyLikeViewBinder.kt")
    # find_all_kt_track_method("/Users/wuxiaolong/project/qianshou-android/app/src/main/java/com/tantan/x/likecard/favoriteguide/FavoriteGuideAct.kt")
    find_all_kt_track_method("/Users/wuxiaolong/project/qianshou-android/app/src/main/java/com/tantan/x/like/ui/LikeItemBinder.kt")
    # find_all_java_track_method("/Users/wuxiaolong/project/qianshou-android/app/src/main/java/com/tantan/x/main/recommends/recommend/view/swipe/NewSwipeCardGroup.java")
    # find_all_java_track_method("/Users/wuxiaolong/project/qianshou-android/app/src/main/java/com/tantan/x/dating/ui/VideoChatActivity.java")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/