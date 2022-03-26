# -*- coding: utf-8 -*-
import os
import shutil
import logging
import subprocess

logging.basicConfig(format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
                    level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)


def merge_ts_2_mp4(ts_dir, mp4_path, remain_ts=True, sort_key=lambda x: int(x[:-3])):
    """
    使用 ffmpeg 将碎片ts文件合并并转换为 mp4
    使用要求：本地已安装 ffmpeg 并已配置到环境变量
    :param ts_dir: 碎片ts文件的路径
    :param mp4_path: 转换后 mp4 的路径，如 data/1.mp4
    :param remain_ts: 成功生成 mp4 后是否保留原始 ts 路径
    :param sort_key: 文件名排序方式，默认排序方式处理如: 1.ts;13.ts;22.ts;789.ts等
    :return:
    """
    file_li = [i for i in os.listdir(ts_dir) if i.endswith('.ts')]
    file_li.sort(key=sort_key)
    file_li_str = '|'.join(file_li)
    mp4_path = os.path.join(ts_dir, mp4_path)
    cmd_li = ['ffmpeg', '-i', f'"concat:{file_li_str}"', '-c', 'copy', f'"{mp4_path}"', '-y']
    subprocess.call(' '.join(cmd_li), shell=True, cwd=ts_dir)
    if not os.path.exists(mp4_path):
        logger.error(f'[{ts_dir}] 生成 mp4 失败 [{mp4_path}]')
        return False
    if not remain_ts:
        logger.info(f'删除来源 ts 路径：{ts_dir}')
        shutil.rmtree(ts_dir, ignore_errors=True)
    logger.info(f'[{ts_dir}] 成功生成 mp4 [{mp4_path}]')
    return True
