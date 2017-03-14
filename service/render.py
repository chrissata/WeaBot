# -- coding: utf-8 -
import sys
import sys

reload(sys)
sys.setdefaultencoding('utf8')
'''

{
  "results": [{
  "location": {
      "id": "C23NB62W20TF",
      "name": "西雅图",
      "country": "US",
      "timezone": "America/Los_Angeles",
      "timezone_offset": "-07:00"
  },
  "now": {
      "text": "多云", //天气现象文字
      "code": "4", //天气现象代码
      "temperature": "14", //温度，单位为c摄氏度或f华氏度
      "feels_like": "14", //体感温度，单位为c摄氏度或f华氏度
      "pressure": "1018", //气压，单位为mb百帕或in英寸
      "humidity": "76", //相对湿度，0~100，单位为百分比
      "visibility": "16.09", //能见度，单位为km公里或mi英里
      "wind_direction": "西北", //风向文字
      "wind_direction_degree": "340", //风向角度，范围0~360，0为正北，90为正东，180为正南，270为正西
      "wind_speed": "8.05", //风速，单位为km/h公里每小时或mph英里每小时
      "wind_scale": "2", //风力等级，请参考：http://baike.baidu.com/view/465076.htm
      "clouds": "90", //云量，范围0~100，天空被云覆盖的百分比 #目前不支持中国城市#
      "dew_point": "-12" //露点温度，请参考：http://baike.baidu.com/view/118348.htm #目前不支持中国城市#
  },
  "last_update": "2015-09-25T22:45:00-07:00" //数据更新时间（该城市的本地时间）
  }]
}
'''
def render_response(think_result, location, data_range):
    _, days = data_range
    return render_reply_daily(think_result, location, days)


def render_reply_daily(think_result, location, days):
    template = u"{loc}， ".format(loc=location)
    if len(think_result['results']) == 0:
        return template
    result = think_result['results'][0]
    weathers = result['daily']
    i = 0
    for w in weathers:
        if i >= days:
            break;
        i += 1
        template += u"{date} : 白天天气 {text_day}, 夜间天气 {text_night}, 最高温度 {high}°, 最低温度 {low}°\n".format(
                    date=w['date'],
                    text_day=w['text_day'],
                    text_night=w['text_night'],
                    high=w['high'],
                    low=w['low']
                    )
    return template


if __name__ == '__main__':
    pass
