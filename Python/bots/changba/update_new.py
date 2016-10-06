#!/usr/bin/env python
# -*- coding: utf-8 -*-
from changba import *

def main():
    with open('./cfg/config.ini', 'r') as ifs:
        uid = ifs.readline().strip('\n')
    with open('./cfg/%s.log' % uid, 'r') as ifs:
        latestid = ifs.readline().strip('\n')
    userid, worknum, nick_name = get_userid_and_worknum(uid)
    work_list = get_work_list(userid, worknum, latestid)
    prefix = make_sure_output_path(nick_name)

    if work_list:
        with open('./cfg/%s.log' % uid, 'w') as ofs:
            ofs.write(work_list[0]['workid'] + '\n')
        download_list(work_list, prefix)
    print 'updated %d songs' % len(work_list)

if __name__ == '__main__':
    main()

