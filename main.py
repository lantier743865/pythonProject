# This is a sample Python script.
import os


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    path = r"/Users/wuxiaolong/project/qianshou-android"
    out_path = r"/Users/didi/PycharmProjects/findLocationManagerApi/"
    files = []
    path_list = os.listdir(path)
    path_list.sort()
    for name in path_list:
        if os.path.isfile(os.path.join(path, name)):
            files.append(name)

    print(f'Hi, {files}')  # Press ⌘F8 to toggle the breakpoint.

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
