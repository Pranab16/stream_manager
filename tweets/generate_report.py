#!/usr/bin/env python
import json
import xlwt
import time
from tweets.models import TweetMention, TweetResponse, Account


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

        account = Account.objects.filter(screen_name=handle)

        wb = xlwt.Workbook()
        ws = wb.add_sheet('Twitter stats')
        headers = ['Account', 'Mention Count', 'Response Count', 'User Count', 'Avg Response Time']

        for i in len(headers):
            ws.write(0, i, headers[i])

        ws.write(1, 0, account.name)
        ws.write(1, 1, mention_count)
        ws.write(1, 2, response_count)
        ws.write(1, 3, user_count)
        ws.write(1, 4, avg_resp_time)

        file = open('report_'+account.name+str(int(time.time()))+'.xls', 'w+')
        wb.save(file)

    def create_same_category_report(self, handle):
        account = Account.objects.filter(screen_name=handle).first
        accounts = Account.objects.filter(category=account.category)
        mention_count = []
        response_count = []
        user_count = []
        avg_resp_time = []
        for idx, ant in enumerate(accounts):
            mention_count[idx], response_count[idx], user_count[idx], avg_resp_time[idx] = self.logic(ant.screen_name)

        wb = xlwt.Workbook()
        ws = wb.add_sheet('Twitter Same Category stats')
        headers = ['Account', 'Mention Count', 'Response Count', 'User Count', 'Avg Response Time']

        for i in len(headers):
            ws.write(0, i, headers[i])

        for i, account in enumerate(accounts):
            ws.write(i+1, 0, account.name)
            ws.write(i+1, 1, mention_count[i])
            ws.write(i+1, 2, response_count[i])
            ws.write(i+1, 3, user_count[i])
            ws.write(i+1, 4, avg_resp_time[i])

        file = open('same_category_report_'+account.name+str(int(time.time()))+'.xls', 'w+')
        wb.save(file)

    def create_diff_category_report(self, handle):
        account = Account.objects.filter(screen_name=handle).first
        accounts = Account.objects.exclude(category=account.category)
        mention_count = []
        response_count = []
        user_count = []
        avg_resp_time = []
        for idx, ant in enumerate(accounts):
            mention_count[idx], response_count[idx], user_count[idx], avg_resp_time[idx] = self.logic(ant.screen_name)

        wb = xlwt.Workbook()
        ws = wb.add_sheet('Twitter Same Category stats')
        headers = ['Account', 'Mention Count', 'Response Count', 'User Count', 'Avg Response Time']

        for i in len(headers):
            ws.write(0, i, headers[i])

        for i, account in enumerate(accounts):
            ws.write(i+1, 0, account.name)
            ws.write(i+1, 1, mention_count[i])
            ws.write(i+1, 2, response_count[i])
            ws.write(i+1, 3, user_count[i])
            ws.write(i+1, 4, avg_resp_time[i])

        file = open('different_category_report_'+account.name+str(int(time.time()))+'.xls', 'w+')
        wb.save(file)


