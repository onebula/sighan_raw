#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 22:56:08 2019

@author: kuangchen
"""

import regex
from bs4 import BeautifulSoup
from opencc import OpenCC

from file_io import save_data_list

cc = OpenCC('t2s')
def convert(text):
    #return cc.convert(text)
    return text

def transform_2013(html_string):
    soup = BeautifulSoup(html_string, 'lxml')
    error_texts = []
    correct_texts = []
    sentences = soup.find_all('p')
    mistakes = soup.find_all('mistake')
    for sentence in sentences:
        text = sentence.get_text().strip()
        error_text = convert(text)
        correct_text = error_text[:]
        for mistake in mistakes:
            location = int(mistake.get('wrong_position', '0').strip()) - 1
            if location == -1:
                continue
            error = convert(mistake.wrong.get_text().strip())
            correct = convert(mistake.correct.get_text().strip())
            st = location - len(error)
            ed = location + len(error)
            # 校准位置
            location_r = error_text.find(error, max(0, st - 5), ed + 5)
            if location_r == -1:
                # 精确匹配无法找到，尝试模糊匹配
                m = regex.search(ur'(?:%s){s<=1}'%(error), error_text)
                if m is not None:
                    location_r = m.start()
                    error = m[0]
            st = location_r
            ed = location_r + len(error)
            # 核对校准结果，否则进行一次全局替换
            if error_text[st:ed] == error:
                correct_text = correct_text[:st] + correct + correct_text[ed:]
            else:
                print(error_text)
                print(location)
                print(error)
                correct_text = correct_text.replace(error, correct, 1)
        if len(error_text) != len(correct_text):
            print(text)
        error_texts.append(error_text)
        correct_texts.append(correct_text)
    return error_texts, correct_texts

def process_2013(data_file, samples_num=-1):
    error_texts = []
    correct_texts = []
    with open(data_file, 'r') as f:
        idx = 0
        lines = []
        for line in f:
            try:
                content = line.decode('utf8').strip()
            except Exception as e:
                print line
                print e
                continue
            if '<DOC' in content and idx % 100 == 0:
                print(idx)
            if samples_num > 0 and idx >= samples_num:
                break
            if '</DOC>' in content:
                idx += 1
                errors, corrects = transform_2013(''.join(lines))
                error_texts += errors
                correct_texts += corrects
                lines = []
            else:
                lines.append(content)
    return error_texts, correct_texts

def transform_html(html_string):
    soup = BeautifulSoup(html_string, 'lxml')
    error_texts = []
    correct_texts = []
    sentences = soup.find_all('passage')
    mistakes = soup.find_all('mistake')
    for sentence in sentences:
        text_id = sentence.get('id', '')
        text = sentence.get_text().strip()
        error_text = convert(text)
        correct_text = error_text[:]
        for mistake in mistakes:
            if mistake.get('id', '') == text_id:
                location = int(mistake.get('location', '0').strip()) - 1
                if location == -1:
                    continue
                error = convert(mistake.wrong.get_text().strip())
                correct = convert(mistake.correction.get_text().strip())                    
                st = location - len(error)
                ed = location + len(error) + 1
                # 校准位置
                location_r = error_text.find(error, max(0, st), ed)
                if location_r == -1:
                    # 精确匹配无法找到，尝试模糊匹配
                    if len(error) > 1:
                        m = regex.search(ur'(?:%s){s<=1}'%(error), error_text)
                        if m is not None:
                            if error == m[0]:
                                location_r = m.start()
                            else:
                                print 'type1'
                                print error_text
                                print error
                        else:
                            print 'type2'
                            print error_text
                            print error
                    else:
                        print 'type3'
                        print st
                        print ed
                        print error_text
                        print error
                st = location_r
                ed = location_r + len(error)
                # 核对校准结果，否则进行一次全局替换
                if error_text[st:ed] == error:
                    correct_text = correct_text[:st] + correct + correct_text[ed:]
                else:
                    print(error_text)
                    print(location)
                    print(error)
                    correct_text = correct_text.replace(error, correct, 1)
        if len(error_text) != len(correct_text):
            print 'type4'
            print(text)
        if error_text == correct_text:
            print 'type5'            
            print text
        error_texts.append(error_text)
        correct_texts.append(correct_text)
    return error_texts, correct_texts

def process_html(data_file, samples_num=-1):
    error_texts = []
    correct_texts = []
    with open(data_file, 'r') as f:
        idx = 0
        lines = []
        for line in f:
            try:
                content = line.decode('utf8').strip()
            except Exception as e:
                print line
                print e
                continue
            if '<ESSAY' in content and idx % 100 == 0:
                print(idx)
            if samples_num > 0 and idx >= samples_num:
                break
            if '</ESSAY>' in content:
                idx += 1
                errors, corrects = transform_html(''.join(lines))
                error_texts += errors
                correct_texts += corrects
                lines = []
            else:
                lines.append(content)
    return error_texts, correct_texts

def process_truth(doc_file, truth_file):
    error_texts = []
    correct_texts = []
    with open(doc_file, 'r') as f1:
        with open(truth_file, 'r') as f2:
            for line1, line2 in zip(f1, f2):
                try:
                    doc = regex.split('[ \t]', line1.decode('utf8').strip())
                except Exception as e:
                    print line1
                    print e
                    continue
                try:
                    truth = line2.decode('utf8').strip().split(', ')
                except Exception as e:
                    print line2
                    print e
                    continue
                text_id = doc[0]
                text = ''.join(doc[1:])
                text_id = regex.findall(u'\((NID|pid)=(.*)\)', text_id)[0][1]
                error_text = convert(text)
                correct_text = error_text[:]
                truth_id = truth[0]
                if truth_id == text_id:
                    for i in range(1, len(truth), 2):
                        if int(truth[i]) == 0:
                            continue
                        st = int(truth[i]) - 1
                        ed = st + 1
                        error = error_text[st:ed]
                        correct = convert(truth[i+1])
                        if error == correct:
                            print text
                            print text[st:ed]
                            print truth[i+1]
                        correct_text = correct_text[0:st] + correct + correct_text[ed:]
                    error_texts.append(error_text)
                    correct_texts.append(correct_text)
                else:
                    print(truth_id, text_id)
    return error_texts, correct_texts

def cal_diff(error_texts, correct_texts):
    print('Error texts num: {}, ave len: {:.2f}'.format(len(error_texts), sum([len(text) for text in error_texts])*1.0/len(error_texts)))
    print('Correct texts num: {}, ave len: {:.2f}'.format(len(correct_texts), sum([len(text) for text in correct_texts])*1.0/len(correct_texts)))
    diff_num = 0
    error_num = 0
    for i, (error_text, correct_text) in enumerate(zip(error_texts, correct_texts)):
        if len(error_text) != len(correct_text):
            print('Length of {}-th text is different'.format(i))
        if error_text != correct_text:
            diff_num += 1
        for error, correct in zip(error_text, correct_text):
            if error != correct:
                error_num += 1
    print('Diffs num: {}'.format(diff_num))
    print('Errors num: {}'.format(error_num))

if __name__ == '__main__':
    
    '''
    # train
    '''
    
    raw_error_texts1, raw_correct_texts1 = process_2013('sighan7csc_release1.0/SampleSet/Bakeoff2013_SampleSet_WithError_00001-00350.txt')
    raw_error_texts2, raw_correct_texts2 = process_2013('sighan7csc_release1.0/SampleSet/Bakeoff2013_SampleSet_WithoutError_10001-10350.txt')
    error_texts = raw_error_texts1 + raw_error_texts2
    correct_texts = raw_correct_texts1 + raw_correct_texts2
    cal_diff(error_texts, correct_texts)
    save_data_list(error_texts, 'train13_error.txt', sep = '')
    save_data_list(correct_texts, 'train13_correct.txt', sep = '')
    
    
    raw_error_texts1, raw_correct_texts1 = process_html('clp14csc_release1.1/Training/B1_training.sgml')
    raw_error_texts2, raw_correct_texts2 = process_html('clp14csc_release1.1/Training/C1_training.sgml')
    error_texts = raw_error_texts1 + raw_error_texts2
    correct_texts = raw_correct_texts1 + raw_correct_texts2
    cal_diff(error_texts, correct_texts)
    save_data_list(error_texts, 'train14_error.txt', sep = '')
    save_data_list(correct_texts, 'train14_correct.txt', sep = '')
    
    
    raw_error_texts1, raw_correct_texts1 = process_html('sighan8csc_release1.0/Training/SIGHAN15_CSC_A2_Training.sgml')
    raw_error_texts2, raw_correct_texts2 = process_html('sighan8csc_release1.0/Training/SIGHAN15_CSC_B2_Training.sgml')
    error_texts = raw_error_texts1 + raw_error_texts2
    correct_texts = raw_correct_texts1 + raw_correct_texts2
    cal_diff(error_texts, correct_texts)
    save_data_list(error_texts, 'train15_error.txt', sep = '')
    save_data_list(correct_texts, 'train15_correct.txt', sep = '')
    
    '''
    # test
    '''
    
    error_texts, correct_texts = process_truth('sighan7csc_release1.0/FinalTest/FinalTest_SubTask2.txt', 'sighan7csc_release1.0/FinalTest/FinalTest_SubTask2_Truth.txt')
    cal_diff(error_texts, correct_texts)
    save_data_list(error_texts, 'test13_error.txt', sep = '')
    save_data_list(correct_texts, 'test13_correct.txt', sep = '')
    
    error_texts, correct_texts = process_truth('clp14csc_release1.1/Test/CLP14_CSC_TestInput.txt', 'clp14csc_release1.1/Test/CLP14_CSC_TestTruth.txt')
    cal_diff(error_texts, correct_texts)
    save_data_list(error_texts, 'test14_error.txt', sep = '')
    save_data_list(correct_texts, 'test14_correct.txt', sep = '')
    
    error_texts, correct_texts = process_truth('sighan8csc_release1.0/Test/SIGHAN15_CSC_TestInput.txt', 'sighan8csc_release1.0/Test/SIGHAN15_CSC_TestTruth.txt')
    cal_diff(error_texts, correct_texts)
    save_data_list(error_texts, 'test15_error.txt', sep = '')
    save_data_list(correct_texts, 'test15_correct.txt', sep = '')
    