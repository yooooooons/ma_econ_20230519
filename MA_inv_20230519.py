#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
import pyupbit
import datetime
import pandas as pd
import numpy as np
import warnings
import traceback

warnings.filterwarnings('ignore')

#from scipy.signal import savgol_filter
#from scipy.signal import savitzky_golay

#import matplotlib.pyplot as plt


# In[2]:


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)


# In[3]:


# 전체 자산 중 몇 % 자산을 투자할 것인가?

invest_ratio = 0.015   # 보유 금액의 최대 몇 % 를 투자할것인가 (예> 0.1 <-- 보유금액 10% 투자) 


# In[4]:


transaction_fee_ratio = 0.0005   # 거래 수수료 비율

time_factor = 9   # 클라우드 서버와 한국과의 시차

check_currency = 'KRW'


# In[5]:


#업비트 계정 설정

access_key = "ixWxT1mblIf6FJ7afaS3MLZ1eyovfIcTwSapB2VD"
secret_key = "Fll2k01gQthoKrdAhjcTFcYrh0o7Dejtzp4J6J0R"

upbit = pyupbit.Upbit(access_key, secret_key)


# In[6]:


candle_type = '60min'
#candle_type = 'day'

if candle_type == '1min' :
    candle_adapt = 'minute1'
    time_unit = 1
elif candle_type == '3min' :
    candle_adapt = 'minute3'
    time_unit = 3
elif candle_type == '5min' :
    candle_adapt = 'minute5'
    time_unit = 5
elif candle_type == '10min' :
    candle_adapt = 'minute10'
    time_unit = 10
elif candle_type == '15min' :
    candle_adapt = 'minute15'
    time_unit = 15
elif candle_type == '30min' :
    candle_adapt = 'minute30'
    time_unit = 30
elif candle_type == '60min' :
    candle_adapt = 'minute60'
    time_unit = 60
elif candle_type == '240min' :
    candle_adapt = 'minute240'
    time_unit = 240
elif candle_type == 'day' :
    candle_adapt = 'day'
    time_unit = (60 * 24)
elif candle_type == 'month' :
    candle_adapt = 'month'
    time_unit = 60 * 24 * 30


# In[7]:


# Test setting
vol_duration = 12
buy_price_up_unit = 1


# In[8]:


# 투자 대상 코인 및 설정값

BTC_0_dic = {'type' : 'type_1', 'coin_No' : 0, 'ma_duration_long' : 70, 'ma_duration_mid' : 35, 'ma_duration_short' : 15, 'ratio_ema_long_rise' : 1.000, 'ratio_ema_mid_rise' : 1.0002, 'successive_rise' : 2, 'ratio_ema_mid_long' : 0.99, 'ratio_vol_curr_prior' : 0.8,              'diff_m_l_factor' : 0.005, 'diff_vol_aver' : 1.5, 'under_long_duration' : 20, 'recent_vol_duration' : 10, 'ratio_sell' : 0.9991, 'add_ratio_sell' : 0.0006, 'sell_method_vol_cri' : 0.5, 'ratio_diff_ema_mid' : 0.008, 'ratio_sell_forced' : 0.07,              'bought_state' : 0, 'bought_price' : 0.0}

ETH_1_dic = {'type' : 'type_1', 'coin_No' : 1, 'ma_duration_long' : 70, 'ma_duration_mid' : 35, 'ma_duration_short' : 15, 'ratio_ema_long_rise' : 1.000, 'ratio_ema_mid_rise' : 1.0003, 'successive_rise' : 2, 'ratio_ema_mid_long' : 0.99, 'ratio_vol_curr_prior' : 0.8,              'diff_m_l_factor' : 0.001, 'diff_vol_aver' : 2.0, 'under_long_duration' : 20, 'recent_vol_duration' : 10, 'ratio_sell' : 0.9993, 'add_ratio_sell' : 0.0005, 'sell_method_vol_cri' : 0.4, 'ratio_diff_ema_mid' : 0.005, 'ratio_sell_forced' : 0.07,              'bought_state' : 0, 'bought_price' : 0.0}

ETC_5_dic = {'type' : 'type_1', 'coin_No' : 5, 'ma_duration_long' : 100, 'ma_duration_mid' : 35, 'ma_duration_short' : 15, 'ratio_ema_long_rise' : 1.0001, 'ratio_ema_mid_rise' : 1.0003, 'successive_rise' : 2, 'ratio_ema_mid_long' : 0.98, 'ratio_vol_curr_prior' : 0.8,              'diff_m_l_factor' : 0.01, 'diff_vol_aver' : 1.5, 'under_long_duration' : 20, 'recent_vol_duration' : 10, 'ratio_sell' : 0.9993, 'add_ratio_sell' : 0.0003, 'sell_method_vol_cri' : 0.5, 'ratio_diff_ema_mid' : 0.007, 'ratio_sell_forced' : 0.07,              'bought_state' : 0, 'bought_price' : 0.0}

WAVES_7_dic = {'type' : 'type_1', 'coin_No' : 7, 'ma_duration_long' : 100, 'ma_duration_mid' : 35, 'ma_duration_short' : 15, 'ratio_ema_long_rise' : 1.0001, 'ratio_ema_mid_rise' : 1.0003, 'successive_rise' : 2, 'ratio_ema_mid_long' : 0.985, 'ratio_vol_curr_prior' : 1.0,                'diff_m_l_factor' : 0.015, 'diff_vol_aver' : 1.5, 'under_long_duration' : 20, 'recent_vol_duration' : 10, 'ratio_sell' : 0.9993, 'add_ratio_sell' : 0.0003, 'sell_method_vol_cri' : 0.7, 'ratio_diff_ema_mid' : 0.007, 'ratio_sell_forced' : 0.1,                'bought_state' : 0, 'bought_price' : 0.0}

ARK_14_dic = {'type' : 'type_1', 'coin_No' : 14, 'ma_duration_long' : 100, 'ma_duration_mid' : 35, 'ma_duration_short' : 15, 'ratio_ema_long_rise' : 1.0001, 'ratio_ema_mid_rise' : 1.0003, 'successive_rise' : 2, 'ratio_ema_mid_long' : 0.985, 'ratio_vol_curr_prior' : 1.0,               'diff_m_l_factor' : 0.01, 'diff_vol_aver' : 2.0, 'under_long_duration' : 20, 'recent_vol_duration' : 10, 'ratio_sell' : 0.9991, 'add_ratio_sell' : 0.0003, 'sell_method_vol_cri' : 0.5, 'ratio_diff_ema_mid' : 0.008, 'ratio_sell_forced' : 0.07,               'bought_state' : 0, 'bought_price' : 0.0}

BTG_21_dic = {'type' : 'type_1', 'coin_No' : 21, 'ma_duration_long' : 100, 'ma_duration_mid' : 35, 'ma_duration_short' : 15, 'ratio_ema_long_rise' : 1.0001, 'ratio_ema_mid_rise' : 1.0003, 'successive_rise' : 2, 'ratio_ema_mid_long' : 0.985, 'ratio_vol_curr_prior' : 1.0,               'diff_m_l_factor' : 0.01, 'diff_vol_aver' : 1.5, 'under_long_duration' : 20, 'recent_vol_duration' : 10, 'ratio_sell' : 0.9993, 'add_ratio_sell' : 0.0005, 'sell_method_vol_cri' : 0.7, 'ratio_diff_ema_mid' : 0.007, 'ratio_sell_forced' : 0.07,               'bought_state' : 0, 'bought_price' : 0.0}

MLK_61_dic = {'type': 'type_1', 'coin_No': 61, 'ma_duration_long': 100, 'ma_duration_mid': 35, 'ma_duration_short': 15, 'ratio_ema_long_rise': 1.0001, 'ratio_ema_mid_rise': 1.0003, 'successive_rise': 2, 'ratio_ema_mid_long': 0.98, 'ratio_vol_curr_prior': 0.6,               'diff_m_l_factor': 0.015, 'diff_vol_aver': 1.5, 'under_long_duration': 20, 'recent_vol_duration': 10, 'ratio_sell': 0.9993, 'add_ratio_sell': 0.0005, 'sell_method_vol_cri': 0.7, 'ratio_diff_ema_mid': 0.008, 'ratio_sell_forced': 0.07,               'bought_state' : 0, 'bought_price' : 0.0}

LOOM_30_dic = {'type': 'type_1', 'coin_No': 30, 'ma_duration_long': 100, 'ma_duration_mid': 35, 'ma_duration_short': 15, 'ratio_ema_long_rise': 1.0, 'ratio_ema_mid_rise': 1.0003, 'successive_rise': 2, 'ratio_ema_mid_long': 0.985, 'ratio_vol_curr_prior': 0.8,                'diff_m_l_factor': 0.015, 'diff_vol_aver': 2.0, 'under_long_duration': 20, 'recent_vol_duration': 10, 'ratio_sell': 0.9991, 'add_ratio_sell': 0.0003, 'sell_method_vol_cri': 0.5, 'ratio_diff_ema_mid': 0.008, 'ratio_sell_forced': 0.07,                'bought_state': 0, 'bought_price': 0.0}

ARK_14_dic = {'type': 'type_1', 'coin_No': 14, 'ma_duration_long': 100, 'ma_duration_mid': 35, 'ma_duration_short': 15, 'ratio_ema_long_rise': 1.0001, 'ratio_ema_mid_rise': 1.0004, 'successive_rise': 2, 'ratio_ema_mid_long': 0.98, 'ratio_vol_curr_prior': 1.0,               'diff_m_l_factor': 0.01, 'diff_vol_aver': 2.0, 'under_long_duration': 20, 'recent_vol_duration': 10, 'ratio_sell': 0.9993, 'add_ratio_sell': 0.0003, 'sell_method_vol_cri': 0.5, 'ratio_diff_ema_mid': 0.008, 'ratio_sell_forced': 0.07,               'bought_state': 0, 'bought_price': 0.0}

ZRX_29_dic = {'type': 'type_1', 'coin_No': 29, 'ma_duration_long': 100, 'ma_duration_mid': 35, 'ma_duration_short': 15, 'ratio_ema_long_rise': 1.0001, 'ratio_ema_mid_rise': 1.0003, 'successive_rise': 2, 'ratio_ema_mid_long': 0.985, 'ratio_vol_curr_prior': 1.0,               'diff_m_l_factor': 0.015, 'diff_vol_aver': 1.5, 'under_long_duration': 20, 'recent_vol_duration': 10, 'ratio_sell': 0.9993, 'add_ratio_sell': 0.0005, 'sell_method_vol_cri': 0.7, 'ratio_diff_ema_mid': 0.008, 'ratio_sell_forced': 0.1,               'bought_state': 0, 'bought_price': 0.0}


# In[9]:


LIST_target = [BTC_0_dic, ETH_1_dic, ETC_5_dic, WAVES_7_dic, ARK_14_dic, BTG_21_dic, MLK_61_dic, LOOM_30_dic, ARK_14_dic, ZRX_29_dic]


# In[10]:


len(LIST_target)


# In[11]:



# 코인번호로 코인 명칭 추출
tickers = pyupbit.get_tickers()

LIST_coin_KRW = []

for i in range (0, len(tickers), 1):
    if tickers[i][0:3] == 'KRW':
        LIST_coin_KRW.append(tickers[i])

LIST_check_coin_currency = []

for i in range (0, len(LIST_coin_KRW), 1):
    LIST_check_coin_currency.append(LIST_coin_KRW[i][4:])

LIST_check_coin_currency_2 = []

for i in range (0, len(LIST_check_coin_currency), 1) :
    temp = 'KRW-' + LIST_check_coin_currency[i]
    LIST_check_coin_currency_2.append(temp)


# In[12]:


# 매수 최소단위 산출

def unit_value_calc (DF_test) :
    unit_factor = 0
    unit_value = 0
        
    if DF_test['open'][-1] >= 1000000 :  # 200만원 이상은 거래단위가 1000원, 100~200만원은 거래단위가 500원이지만 편의상 200만원 이상과 함께 처리
        unit_factor = -3
        unit_value = 1000
    elif DF_test['open'][-1] >= 100000 :
        unit_factor = -2
        unit_value = 50
    elif DF_test['open'][-1] >= 10000 :
        unit_factor = -1
        unit_value = 10
    elif DF_test['open'][-1] >= 1000 :
        unit_factor = -1
        unit_value = 5
    elif DF_test['open'][-1] >= 100 :
        unit_factor = 0
        unit_value = 1
    else :
        unit_factor = 1
        unit_value = 0.1
    
    print ('DF_test[open][-1] : {0}  /  unit_factor : {1}  /  unit_value : {2}'.format(DF_test['open'][-1], unit_factor, unit_value))
        
    return unit_value


# In[13]:


# 몇건의 과거 이력을 참조할 것인가

candle_count = round((60/time_unit) * 24 * 100)


# In[14]:


# 잔고 조회, 현재가 조회 함수 정의

def get_balance(target_currency):   # 현급 잔고 조회
    """잔고 조회"""
    balances = upbit.get_balances()   # 통화단위, 잔고 등이 Dictionary 형태로 balance에 저장
    for b in balances:
        if b['currency'] == target_currency:   # 화폐단위('KRW', 'KRW-BTC' 등)에 해당하는 잔고 출력
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_balance_locked(target_currency):   # 거래가 예약되어 있는 잔고 조회
    """잔고 조회"""
    balances = upbit.get_balances()   # 통화단위, 잔고 등이 Dictionary 형태로 balance에 저장
    for b in balances:
        if b['currency'] == target_currency:   # 화폐단위('KRW', 'KRW-BTC' 등)에 해당하는 잔고 출력
            if b['locked'] is not None:
                return float(b['locked'])
            else:
                return 0
    return 0

def get_avg_buy_price(target_currency):   # 거래가 예약되어 있는 잔고 조회
    """평균 매수가 조회"""
    balances = upbit.get_balances()   # 통화단위, 잔고 등이 Dictionary 형태로 balance에 저장
    for b in balances:
        if b['currency'] == target_currency:   # 화폐단위('KRW', 'KRW-BTC' 등)에 해당하는 잔고 출력
            if b['avg_buy_price'] is not None:
                return float(b['avg_buy_price'])
            else:
                return 0
    return 0

'''
def get_current_price(invest_coin):
    """현재가 조회"""
    #return pyupbit.get_orderbook(tickers=invest_coin)[0]["orderbook_units"][0]["ask_price"]
    return pyupbit.get_current_price(invest_coin)
'''
#price = pyupbit.get_current_price("KRW-BTC")


# In[15]:


upbit.get_balances()


# In[16]:


# 매수/매도 함수 정의

def buy_sell_normal (dic_target) :
    
    coin_inv = LIST_check_coin_currency_2[dic_target['coin_No']]
    print ('\n\nCheking coin is :', coin_inv) 
    
    DF_check = pyupbit.get_ohlcv(LIST_check_coin_currency_2[dic_target['coin_No']], count=candle_count, interval=candle_adapt)
    
    DF_check['ratio_prior_to_cur'] = DF_check['open'] / DF_check['open'].shift(1)
    
    DF_check['ema_long'] = DF_check['open'].ewm(span = dic_target['ma_duration_long'], adjust=False).mean()
    DF_check['ema_mid'] = DF_check['open'].ewm(span = dic_target['ma_duration_mid'], adjust=False).mean()
    DF_check['ema_short'] = DF_check['open'].ewm(span = dic_target['ma_duration_short'], adjust=False).mean()
    
    DF_check['ratio_ema_long'] = DF_check['ema_long'] / DF_check['ema_long'].shift(1)
    
    DF_check['fall_check'] = 0
    DF_check.loc[(DF_check['ratio_ema_long'] < 1), 'fall_check'] = 1
    
    DF_check['ratio_ema_mid'] = DF_check['ema_mid'] / DF_check['ema_mid'].shift(1)
    
    DF_check['rise_check_mid'] = 0
    DF_check.loc[(DF_check['ratio_ema_mid'] > 1), 'rise_check_mid'] = 1
    
    DF_check['ratio_ema_short'] = DF_check['ema_short'] / DF_check['ema_short'].shift(1)
    
    DF_check['rise_check_short'] = 0
    DF_check.loc[(DF_check['ratio_ema_short'] > 1), 'rise_check_short'] = 1
    
    DF_check['diff_m_l'] = DF_check['ema_mid'] - DF_check['ema_long']
    
    DF_check['mid_under_long'] = 0
    DF_check.loc[(DF_check['diff_m_l'] > 0), 'mid_under_long'] = 1
    
    DF_check['vol_amount'] = 0.0
    
    DF_check.loc[(DF_check['volume'] >= (2.0 * DF_check.sort_values('volume', ascending=False).tail(round(0.9 * len(DF_check)))['volume'].mean())), 'vol_amount'] = 2.0
    DF_check.loc[(DF_check['volume'] < (2.0 * DF_check.sort_values('volume', ascending=False).tail(round(0.9 * len(DF_check)))['volume'].mean())) &                  (DF_check['volume'] >= (1.8 * DF_check.sort_values('volume', ascending=False).tail(round(0.9 * len(DF_check)))['volume'].mean())), 'vol_amount'] = 1.8
    DF_check.loc[(DF_check['volume'] < (1.8 * DF_check.sort_values('volume', ascending=False).tail(round(0.9 * len(DF_check)))['volume'].mean())) &                  (DF_check['volume'] >= (1.6 * DF_check.sort_values('volume', ascending=False).tail(round(0.9 * len(DF_check)))['volume'].mean())), 'vol_amount'] = 1.6
    DF_check.loc[(DF_check['volume'] < (1.6 * DF_check.sort_values('volume', ascending=False).tail(round(0.9 * len(DF_check)))['volume'].mean())) &                  (DF_check['volume'] >= (1.4 * DF_check.sort_values('volume', ascending=False).tail(round(0.9 * len(DF_check)))['volume'].mean())), 'vol_amount'] = 1.4
    DF_check.loc[(DF_check['volume'] < (1.4 * DF_check.sort_values('volume', ascending=False).tail(round(0.9 * len(DF_check)))['volume'].mean())) &                  (DF_check['volume'] >= (1.2 * DF_check.sort_values('volume', ascending=False).tail(round(0.9 * len(DF_check)))['volume'].mean())), 'vol_amount'] = 1.2
    DF_check.loc[(DF_check['volume'] < (1.2 * DF_check.sort_values('volume', ascending=False).tail(round(0.9 * len(DF_check)))['volume'].mean())) &                  (DF_check['volume'] >= (1.0 * DF_check.sort_values('volume', ascending=False).tail(round(0.9 * len(DF_check)))['volume'].mean())), 'vol_amount'] = 1.0
    DF_check.loc[(DF_check['volume'] < (1.0 * DF_check.sort_values('volume', ascending=False).tail(round(0.9 * len(DF_check)))['volume'].mean())) &                  (DF_check['volume'] >= (0.8 * DF_check.sort_values('volume', ascending=False).tail(round(0.9 * len(DF_check)))['volume'].mean())), 'vol_amount'] = 0.8
    DF_check.loc[(DF_check['volume'] < (0.8 * DF_check.sort_values('volume', ascending=False).tail(round(0.9 * len(DF_check)))['volume'].mean())) &                  (DF_check['volume'] >= (0.6 * DF_check.sort_values('volume', ascending=False).tail(round(0.9 * len(DF_check)))['volume'].mean())), 'vol_amount'] = 0.6
    DF_check.loc[(DF_check['volume'] < (0.6 * DF_check.sort_values('volume', ascending=False).tail(round(0.9 * len(DF_check)))['volume'].mean())) &                  (DF_check['volume'] >= (0.4 * DF_check.sort_values('volume', ascending=False).tail(round(0.9 * len(DF_check)))['volume'].mean())), 'vol_amount'] = 0.4
    DF_check.loc[(DF_check['volume'] < (0.4 * DF_check.sort_values('volume', ascending=False).tail(round(0.9 * len(DF_check)))['volume'].mean())) &                  (DF_check['volume'] >= (0.2 * DF_check.sort_values('volume', ascending=False).tail(round(0.9 * len(DF_check)))['volume'].mean())), 'vol_amount'] = 0.2
    
    DF_check['recent_vol_aver'] = 0.0
    
    for k in range(0, len(DF_check), 1):
        DF_check['recent_vol_aver'][k] = DF_check.iloc[(k - dic_target['recent_vol_duration']): k]['vol_amount'].sum()
        
    print ('DF_check :\n', DF_check)


    # Buy / Sell logic
    
    if dic_target['bought_state'] == 0 :   # 매수가 없는 상태라면 
        
        '''
        print('DF_check[ratio_ema_long][-3] : {0} / [-2] : {1} / [-1] : {2}   >   criteria : {3}'.format(DF_check['ratio_ema_long'][-3], DF_check['ratio_ema_long'][-2], DF_check['ratio_ema_long'][-1], dic_target['ratio_ema_long_rise']))
        print('DF_check[ratio_ema_mid][-1] : {0}   >   criteria : {1}'.format(DF_check['ratio_ema_mid'][-1], dic_target['ratio_ema_mid_rise']))
        print('DF_check.iloc[-dic_target[successive_rise] : ][rise_check_short].sum() : {0}   >=    (dic_target[successive_rise] - 1) : {1}'.format(DF_check.iloc[-dic_target['successive_rise'] : ]['rise_check_short'].sum(), (dic_target['successive_rise'] - 1)))
        print('(DF_check[ema_mid][-1] / DF_check[ema_long][-1]) : {0}   >   dic_target[ratio_ema_mid_long] : {1}'.format((DF_check['ema_mid'][-1] / DF_check['ema_long'][-1]), dic_target['ratio_ema_mid_long']))
        print('DF_check[volume][-2] : {0}   >=   (dic_target[ratio_vol_curr_prior] * DF_check.iloc[-4 : -2][volume].mean()) : {1}'.format(DF_check['volume'][-2], (dic_target['ratio_vol_curr_prior'] * DF_check.iloc[-4 : -2]['volume'].mean())))
        print('DF_check.iloc[-(dic_target[under_long_duration] + 1) : -1][mid_under_long].sum() : {0}   ==   0'.format(DF_check.iloc[-(dic_target['under_long_duration'] + 1) : -1]['mid_under_long'].sum()))
        print('(-DF_check.loc[DF_check.iloc[-(dic_target[under_long_duration] + 1) : -1][diff_m_l].idxmin()][diff_m_l] : {0}   >   (dic_target[diff_m_l_factor] * DF_check[open][-1]) : {1}'.\
              format((-DF_check.loc[DF_check.iloc[-(dic_target['under_long_duration'] + 1) : -1]['diff_m_l'].idxmin()]['diff_m_l'], (dic_target['diff_m_l_factor'] * DF_check['open'][-1]))))
        print('(DF_check.loc[DF_check.iloc[-6 : -2][recent_vol_aver].idxmax()][recent_vol_aver] - DF_check[recent_vol_aver][-2]) : {0}   >   dic_target[diff_vol_aver] : {1}'.\
              format((DF_check.loc[DF_check.iloc[-6 : -2]['recent_vol_aver'].idxmax()]['recent_vol_aver'] - DF_check['recent_vol_aver'][-2]), dic_target['diff_vol_aver']))
        '''
        
        print('DF_check[ratio_ema_long][-3] & [-2] & [-1] > criteria _____ {0} & {1} & {2} > {3}'.format(DF_check['ratio_ema_long'][-3], DF_check['ratio_ema_long'][-2], DF_check['ratio_ema_long'][-1], dic_target['ratio_ema_long_rise']))
        print('DF_check[ratio_ema_mid][-1] > criteria _____ {0} > {1}'.format(DF_check['ratio_ema_mid'][-1], dic_target['ratio_ema_mid_rise']))
        print('DF_check.iloc[-dic_target[successive_rise] : ][rise_check_short].sum() >= (dic_target[successive_rise] - 1) _____ {0} >= {1}'.format(DF_check.iloc[-dic_target['successive_rise'] : ]['rise_check_short'].sum(), (dic_target['successive_rise'] - 1)))
        print('(DF_check[ema_mid][-1] / DF_check[ema_long][-1]) : {0} > dic_target[ratio_ema_mid_long] _____ {0} > {1}'.format((DF_check['ema_mid'][-1] / DF_check['ema_long'][-1]), dic_target['ratio_ema_mid_long']))
        print('DF_check[volume][-2] >= (dic_target[ratio_vol_curr_prior] * DF_check.iloc[-4 : -2][volume].mean()) _____ {0} > {1}'.format(DF_check['volume'][-2], (dic_target['ratio_vol_curr_prior'] * DF_check.iloc[-4 : -2]['volume'].mean())))
        print('DF_check.iloc[-(dic_target[under_long_duration] + 1) : -1][mid_under_long].sum() == 0 _____ {0} == 0'.format(DF_check.iloc[-(dic_target['under_long_duration'] + 1) : -1]['mid_under_long'].sum()))
        print('(-DF_check.loc[DF_check.iloc[-(dic_target[under_long_duration] + 1) : -1][diff_m_l].idxmin()][diff_m_l] > (dic_target[diff_m_l_factor] * DF_check[open][-1]) _____ {0} > {1}'.              format(-DF_check.loc[DF_check.iloc[-(dic_target['under_long_duration'] + 1) : -1]['diff_m_l'].idxmin()]['diff_m_l'], (dic_target['diff_m_l_factor'] * DF_check['open'][-1])))
        print('(DF_check.loc[DF_check.iloc[-6 : -2][recent_vol_aver].idxmax()][recent_vol_aver] - DF_check[recent_vol_aver][-2]) > dic_target[diff_vol_aver] _____ {0} > {1}'.              format((DF_check.loc[DF_check.iloc[-6 : -2]['recent_vol_aver'].idxmax()]['recent_vol_aver'] - DF_check['recent_vol_aver'][-2]), dic_target['diff_vol_aver']))        
               
        
        if (DF_check['ratio_ema_long'][-3] > dic_target['ratio_ema_long_rise']) and (DF_check['ratio_ema_long'][-2] > dic_target['ratio_ema_long_rise']) and (DF_check['ratio_ema_long'][-1] > dic_target['ratio_ema_long_rise']) and (DF_check['ratio_ema_mid'][-1] > dic_target['ratio_ema_mid_rise']) and         (DF_check.iloc[-dic_target['successive_rise'] : ]['rise_check_short'].sum() >= (dic_target['successive_rise'] - 1)) and         ((DF_check['ema_mid'][-1] / DF_check['ema_long'][-1]) > dic_target['ratio_ema_mid_long']) and         (DF_check['volume'][-2] >= (dic_target['ratio_vol_curr_prior'] * DF_check.iloc[-4 : -2]['volume'].mean())) and         (DF_check.iloc[-(dic_target['under_long_duration'] + 1) : -1]['mid_under_long'].sum() == 0) and (-DF_check.loc[DF_check.iloc[-(dic_target['under_long_duration'] + 1) : -1]['diff_m_l'].idxmin()]['diff_m_l'] > (dic_target['diff_m_l_factor'] * DF_check['open'][-1])) and         ((DF_check.loc[DF_check.iloc[-6 : -2]['recent_vol_aver'].idxmax()]['recent_vol_aver'] - DF_check['recent_vol_aver'][-2]) < dic_target['diff_vol_aver']) :
            
            print ('$$$$$ [{0}] buying_transaction is coducting $$$$$'.format(coin_inv))
            
            investable_budget = (get_balance(check_currency) + upbit.get_amount('ALL')) * invest_ratio
            buying_volume = (investable_budget * (1 - transaction_fee_ratio)) / pyupbit.get_current_price(coin_inv)
            currrent_price = pyupbit.get_current_price(coin_inv)
            print ('\ncurrent_price : ', currrent_price)
            buyable_price = currrent_price + (buy_price_up_unit * unit_value_calc(DF_check))
            print ('investable_budget : {0} / currrent_price : {1} / buying_volume : {2}'.format(investable_budget, currrent_price, buying_volume))
            
            #transaction_buy = upbit.buy_market_order(coin_inv, investable_budget)   # 시장가로 매수
            transaction_buy1 = upbit.buy_limit_order(coin_inv, buyable_price, buying_volume)   # 지정가로 매수
            time.sleep(30)            
            print ('buy_1ST_transaction_result :', transaction_buy1)
            print ('time : {0}  /  buying_target_volume : {1}  /  bought_volume_until_now : {2}'.format((datetime.datetime.now() + datetime.timedelta(seconds = (time_factor*3600))), buying_volume, get_balance(coin_inv[4:])))
            
            transaction_buy_cancel1 = upbit.cancel_order(transaction_buy1['uuid'])
            
            dic_target['bought_state'] = 1
            dic_target['buy_signal_flag'] = 1
            

                        
    # 매수상태 점검
        
    if get_balance(coin_inv[4:]) > 0 :
        dic_target['bought_state'] = 1
        print ('bought_state_in mid check : {0}'.format(dic_target['bought_state']))
    else :
        dic_target['bought_state'] = 0
        print ('bought_state_in mid check : {0}'.format(dic_target['bought_state']))
            
        
    # 매도 영역
    if dic_target['bought_state'] == 1 :   # 매수가 되어 있는 상태라면
            
        print ('Now : ', datetime.datetime.now() + datetime.timedelta(seconds = (time_factor * 3600)))
            
        # 일반 매도 (거래량이 어느정도 유지될 때)  
        print('Cheking Normal selling with Normal volume')
        print('DF_check[volume][-2] >= (dic_target[sell_method_vol_cri] * DF_check.iloc[-5 : -2][volume].mean()) _____ {0} >= {1}'.format(DF_check['volume'][-2], (dic_target['sell_method_vol_cri'] * DF_check.iloc[-5 : -2]['volume'].mean())))
        print('DF_check.iloc[-10 : ][ratio_ema_long].mean() < dic_target[ratio_sell] _____ {0} < {1}'.format(DF_check.iloc[-10 : ]['ratio_ema_long'].mean(), dic_target['ratio_sell']))
                      
        if ((DF_check['volume'][-2] >= (dic_target['sell_method_vol_cri'] * DF_check.iloc[-5 : -2]['volume'].mean())) and (DF_check.iloc[-10 : ]['ratio_ema_long'].mean() < dic_target['ratio_sell'])) :
            transaction_sell = upbit.sell_market_order(coin_inv, get_balance(coin_inv[4:]))   # 시장가에 매도
            time.sleep(5)
            print ('\nnow :', (datetime.datetime.now() + datetime.timedelta(seconds = (time_factor * 3600))))
            print ('sell_transaction_result_by_ NORMAL Selling with Normal Volume :', transaction_sell)
                
            dic_target['bought_state'] = 0
                
            time.sleep(5)
                
                
        # 일반 매도 (거래량이 저조할 때)
        print('Cheking Normal selling with LOW volume')
        print('DF_check[volume][-2] < (dic_target[sell_method_vol_cri] * DF_check.iloc[(-5) : -2][volume].mean() _____ {0} < {1}'.format(DF_check['volume'][-2], (dic_target['sell_method_vol_cri'] * DF_check.iloc[(-5) : -2]['volume'].mean())))
        print('DF_check[ratio_ema_long][-1] < (dic_target[ratio_sell] + dic_target[add_ratio_sell]) _____ {0} < {1}'.format(DF_check['ratio_ema_long'][-1], (dic_target['ratio_sell'] + dic_target['add_ratio_sell'])))
            
        if (get_balance(coin_inv[4:]) > 0) and         (DF_check['volume'][-2] < (dic_target['sell_method_vol_cri'] * DF_check.iloc[(-5) : -2]['volume'].mean())) and (DF_check['ratio_ema_long'][-1] < (dic_target['ratio_sell'] + dic_target['add_ratio_sell'])) :
            transaction_sell = upbit.sell_market_order(coin_inv, get_balance(coin_inv[4:]))   # 시장가에 매도
            time.sleep(5)
            print ('\nnow :', (datetime.datetime.now() + datetime.timedelta(seconds = (time_factor * 3600))))
            print ('sell_transaction_result_by_ NORMAL Selling with Low Volume :', transaction_sell)
                
            dic_target['bought_state'] = 0
                
            time.sleep(5)
                

        # 급격하게 하락할때 (거래량이 저조할 때)
        print('Cheking radical falling with LOW volume')
        print('DF_check[volume][-2] < (dic_target[sell_method_vol_cri] * DF_check.iloc[-5 : -2][volume].mean()) _____ {0} < {1}'.format(DF_check['volume'][-2], (dic_target['sell_method_vol_cri'] * DF_check.iloc[-5 : -2]['volume'].mean())))
        print('(DF_check.loc[DF_check.iloc[-6 : -1][ema_mid].idxmax()][ema_mid] - DF_check[ema_mid][-1]) > (dic_target[ratio_diff_ema_mid] * DF_check[open][-1]) _____ {0} > {1}'.              format((DF_check.loc[DF_check.iloc[-6 : -1]['ema_mid'].idxmax()]['ema_mid'] - DF_check['ema_mid'][-1]), (dic_target['ratio_diff_ema_mid'] * DF_check['open'][-1])))
            
        if (get_balance(coin_inv[4:]) > 0) and         (DF_check['volume'][-2] < (dic_target['sell_method_vol_cri'] * DF_check.iloc[-5 : -2]['volume'].mean())) and ((DF_check.loc[DF_check.iloc[-6 : -1]['ema_mid'].idxmax()]['ema_mid'] - DF_check['ema_mid'][-1]) > (dic_target['ratio_diff_ema_mid'] * DF_check['open'][-1])) :
            transaction_sell = upbit.sell_market_order(coin_inv, get_balance(coin_inv[4:]))   # 시장가에 매도
            time.sleep(5)
            print ('\nnow :', (datetime.datetime.now() + datetime.timedelta(seconds = (time_factor * 3600))))
            print ('sell_transaction_result_by_ radical falling :', transaction_sell)
                
            dic_target['bought_state'] = 0
                
            time.sleep(5)


# In[ ]:


while True:
    try:
        now = datetime.datetime.now() + datetime.timedelta(seconds=(time_factor * 3600))  # 클라우드 서버와 한국과의 시간차이 보정 (9시간)
        print('\n', now)

        if (0 < (now.minute % time_unit) <= 3) & (0 < (now.second % 60) <= 59):  # N시:01:00초 ~ N시:01:15초 사이 시각이면
            balances = upbit.get_balances()
            print('current_aseet_status\n', balances)

            for i in range(0, len(LIST_target), 1):
                buy_sell_check = buy_sell_normal(LIST_target[i])
                time.sleep(5)

        # 손실율이 임계수준을 초과하였을때 강제 매도
        for k in range(0, len(LIST_target), 1):
            coin_inv_2 = LIST_check_coin_currency_2[LIST_target[k]['coin_No']]
            print('Cheking coin is :', coin_inv_2)

            if LIST_target[k]['bought_state'] == 1:
                print('Cheking radical falling over criteria Loss with coin :', coin_inv_2)
                print(
                    '(pyupbit.get_current_price(coin_inv_2) / get_avg_buy_price(LIST_check_coin_currency[LIST_target[k][coin_No]])) < (1 - LIST_target[k][ratio_sell_forced]) ____ {0} < {1}'. \
                    format((pyupbit.get_current_price(coin_inv_2) / get_avg_buy_price(
                        LIST_check_coin_currency[LIST_target[k]['coin_No']])), (1 - LIST_target[k]['ratio_sell_forced'])))

                if ((pyupbit.get_current_price(coin_inv_2) / get_avg_buy_price(
                        LIST_check_coin_currency[LIST_target[k]['coin_No']])) < (1 - LIST_target[k]['ratio_sell_forced'])):
                    transaction_sell = upbit.sell_market_order(coin_inv, get_balance(coin_inv[4:]))  # 시장가에 매도
                    time.sleep(5)
                    print('\nnow :', (datetime.datetime.now() + datetime.timedelta(seconds=(time_factor * 3600))))
                    print('sell_transaction_result_by_ radical falling :', transaction_sell)

                    LIST_target[k]['bought_state'] = 0

                    time.sleep(5)

        time.sleep(5)

    except :
        print ('Error has occured!!!')
        err_msg = traceback.format_exc()
        print(err_msg)


# In[ ]:




