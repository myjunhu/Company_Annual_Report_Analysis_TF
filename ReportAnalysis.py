#!/usr/bin/env python  
# _*_ coding:utf-8 _*_  
#  
# @Version : 1.0  
# @Time    : 2019/7/10
# @Author  : 圈圈烃
# @File    : ReportAnalysis
# @Description:
#
#
import os
import jieba
import jieba.analyse
import csv
import re

rule1 = ['环保理念', '环保方针', '环保政策', '环保制度', ]
rule2 = ['环保管理部门', '污染控制部门', '环保管理岗位', '环保内控', ]
rule3 = ['环保目标', '环保措施', ]
rule4 = ['环境认证', '环境管理体系', ]
rule5 = ['清洁生产', ]
rule6 = ['培训', '教育', '环保教育', '环保培训', ]
rule7 = ['环境专利', '环保专利', '环保课题', ]
rule8 = ['自愿协议', ]
rule9 = ['荣誉称号', ]
rule10 = ['同时设计', '同时施工', '同时投产']
# "================================================"
rule11 = ['资源消耗', '资源节约', '节约资源', '节约', '消耗', '资源', ]
rule12 = ['GDP能耗', ]
# "================================================"
rule13 = ['废水', '污水', ]
rule14 = ['废气', ]
rule15 = ['毒性', ]
rule16 = ['噪声', '粉尘', ]
rule17 = ['固废', '处理', '处置', ]
rule18 = ['回收', '废品', '利用', '削减', '清理']
# "================================================"
rule19 = ['环保研发费', '环保创新费', '节能投入', '环境研发', '创新', '节能']
rule20 = ['环保治理', '环保工程', '环保借款', '环境工程', '环境治理']
rule21 = ['环保诉讼', '环保罚款', '环保缴费', '环保人工费', '环境缴费', '环境费用', '环境罚款']
rule22 = ['环保设备', '环保设施建设与运营费', '环保监测', ]
rule23 = ['排污费', '绿化费', '保护费']
rule24 = ['环保拨款', '环保补助', '税收减免', '环保补贴', ]
rule25 = ['环保奖励', ]
rule26 = ['环境福利', ]
rule27 = ['环境风险', '对策', '环保要求']
# "================================================"
ruleList = [rule1, rule2, rule3, rule4, rule5,
            rule6, rule7, rule8, rule9, rule10,
            rule11, rule12, rule13, rule14, rule15,
            rule16, rule17, rule18, rule19, rule20,
            rule21, rule22, rule23, rule24, rule25,
            rule26, rule27, ]


def scoreRuleJieba(path):
    with open(path, 'r', encoding='utf-8') as fr:
        content = fr.read().replace('\n', '').replace(' ', '')
    print(content)
    keywords = jieba.analyse.textrank(content, topK=20, withWeight=True)
    for item in keywords:
        print(item[0], item[1])


def scoreRule(path):
    scoreList = list()
    with open(path, 'r', encoding='utf-8') as fr:
        content = fr.read().replace('\n', '').replace(' ', '')
    for rule in ruleList:
        score = 0
        for keword in rule:
            if keword in content:
                score += 1
        scoreList.append(score)
    # print(scoreList)
    # print("总分：%d" % (sum(scoreList)))
    return sum(scoreList)


def eachFile(path):
    """批量读取txt进行赋值"""
    data = list([['999999', '2012', '2013', '2014', '2015', '2016', '2017', '2018']])
    fileNames = os.listdir(path)
    for file in fileNames:
        newDir = path + '/' + file
        if os.path.isfile(newDir):
            print(newDir.split('/')[-1] + '得分情况：')
            score = scoreRule(newDir)  # 打分函数
            data = write_csv(data, newDir, score)
        else:
            eachFile(newDir)
    with open("2018年报合集_score.csv", "a", newline="", encoding='utf_8_sig') as fw:
        f_csv = csv.writer(fw)
        for row in data:
            f_csv.writerow(row)
        print("csv写入成功...")


def write_csv(data, filePath, score):
    #  ['000000', '2012', '2013', '2014', '2015', '2016', '2017', '2018']
    yearList = ['999999', '2012', '2013', '2014', '2015', '2016', '2017', '2018']
    rows = ['000000', '', '', '', '', '', '', '']
    stockCode = re.findall(r'([0|3|6|9][0-9]{5})[-|\u4e00-\u9fa5|A-Za-z|\s]', filePath)[0]
    stockIndex = 0
    for j in range(len(data)):
        if stockCode in data[j][0]:
            stockIndex = j
            data[j][0] = str(stockCode) + '\r'
            break
    if stockIndex == 0:
        rows[0] = str(stockCode) + '\r'
        for i in range(8):
            if yearList[i] in filePath:
                rows[i] = str(score)
                break
        data.append(rows)
    else:
        for i in range(8):
            if yearList[i] in filePath:
                data[stockIndex][i] = str(score)
                break
    # print(data)
    return data


def main():
    path = r'F:\\Users\\QQT\\Documents\\Python Projects\\Company_Annual_Report_Analysis_TF\\TxT'
    path = r'G:\BaiduNetdiskDownload\TXT\可持续发展报告'
    path = r'G:\BaiduNetdiskDownload\TXT\社会责任报告'
    path = r'G:\BaiduNetdiskDownload\TXT\年报合集'
    path = r'G:\BaiduNetdiskDownload\TXT\年报\2018'
    # path = r'E:\QuanQTing Files\Documents\Code\Python Project\Company_Annual_Report_Analysis_TF\TxT'
    # path = r'F:\Users\QQT\Documents\Python Projects\Company_Annual_Report_Analysis_TF\TxT\社会责任报告\000027深圳能源\000027深圳能源：2014年度社会责任报告.txt'
    # path = r'F:\Users\QQT\Documents\Python Projects\Company_Annual_Report_Analysis_TF\TxT\年报数据\000027深圳能源\000027深圳能源2014年年度报告-20150327.txt'
    # scoreRule(path)
    eachFile(path)


if __name__ == '__main__':
    main()
    # write_csv(filePath="000004国农科技2012年年度报告-20130420.txt", score=2)
