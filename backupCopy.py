import os
import time
import zipfile
from libs.test_utils import get_root_path

# source = [os.path.join(get_root_path(),'element_selector'),
#           os.path.join(get_root_path(),'test_case'),
#           os.path.join(get_root_path(),'test_data'),
#           ]

source = [os.path.join(get_root_path())]

#如果不存在目标备份总目录则创建
target_dir = r'D:\automation_backUp'
if not os.path.exists(target_dir):
    os.mkdir(target_dir)
    print('成功创建备份目录 %s'%(target_dir))

#如果不存在目标备份”月“目录则创建
now1 = time.strftime('%Y%m')
target = os.path.join(target_dir,'automation_'+ now1)
if not os.path.exists(target):
    os.mkdir(target)
    print('成功创建备份目录 %s'%(target))

#得到目标备份压缩目录
now = time.strftime('%d %H%M%S')
target_1 = os.path.join(target,now+'.zip')

z = zipfile.ZipFile(target_1, 'w',zipfile.ZIP_DEFLATED)

for back_dir in source:
    for root,filedirs,files in os.walk(back_dir):
        # print('root:',root)
        # print('filedirs:',filedirs)
        # print('files:',files)
        for file in files:
            # z.write(os.path.join(root,file),file)
            # z.write(os.path.join(root,file),os.path.join(root.replace(back_dir,''),file))
            z.write(os.path.join(root,file),os.path.join(root.replace(get_root_path(),''),file))
z.close()
print('成功备份',source)
print('备份目录:',target_1)