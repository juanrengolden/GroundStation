import cartopy.io.img_tiles as cimgt
'''
天地图：https://vgimap.tianditu.gov.cn/
参考:https://cloud.tencent.com/developer/article/1709627
'''
# 天地图相关
#天地图矢量
class TDT_vec(cimgt.GoogleWTS):
    def _image_url(self, tile):
        x, y, z = tile
        #请自行在天地图申请key，用于地图生成
        key = ''
        url = 'http://t0.tianditu.gov.cn/DataServer?T=vec_w&x=%s&y=%s&l=%s&tk=%s' % (x, y, z, key)
        return url

# 天地图遥感
class TDT_img(cimgt.GoogleWTS):
    def _image_url(self, tile):
        x, y, z = tile
        key = ''
        url = 'http://t0.tianditu.gov.cn/DataServer?T=img_w&x=%s&y=%s&l=%s&tk=%s' % (x, y, z, key)
        return url

# 天地图地形
class TDT_ter(cimgt.GoogleWTS):
    def _image_url(self, tile):
        x, y, z = tile
        key = ''
        url = 'http://t0.tianditu.gov.cn/DataServer?T=ter_w&x=%s&y=%s&l=%s&tk=%s' % (x, y, z, key)
        return url