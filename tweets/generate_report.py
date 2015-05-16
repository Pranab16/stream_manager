#!/usr/bin/env python
import json
import xlwt
from tweets.models import TweetMention, TweetResponse


class GenerateReport():
    def __init__(self):
        pass

    def logic(self, handle):
        mentions = TweetMention.objects.filter(account__screen_name=handle)
        mention_count = mentions.count
        user_count = mentions.distinct('user_id_str')
        response_count = 0
        avg_resp_time = 0
        resp_time = []
        for mention in mentions:
            if mention.retweeted:
                res = TweetResponse.objects.filter(account__screen_name=handle, reply_id_str=mention.id_str).first
                if res is not None:
                    response_count += 1
                    resp_time.append(res.created_at - mention.created_at)
                    avg_resp_time = (avg_resp_time + (res.created_at - mention.created_at)) / response_count

        resp_time.sort()

        return mention_count, response_count, user_count, avg_resp_time

    def create_report(self, handle):
        mention_count, response_count, user_count, avg_resp_time = self.logic(handle)

        wb = xlwt.Workbook()
        ws = wb.add_sheet('A Test Sheet')
        headers = ['Mention Count', 'Response Count', 'User Count', 'Avg Response Time']

        for i in len(headers):
            ws.write(0, i, headers[i])
        


        ws.write(0, 0, 1234.56)
        ws.write(1, 0, datetime.now())
        ws.write(2, 0, 1)
        ws.write(2, 1, 1)
        ws.write(2, 2, xlwt.Formula("A3+B3"))

        wb.save('example.xls')


