# -*- coding: utf-8 -*-
"""
Created on Tue Jan 11 22:05:21 2022

@author: Test
"""

import list_morningstar_funds

eq_dataframe, error_pages = list_morningstar_funds.request_list_morningstar_funds(pageSize=10000)
list_morningstar_funds.save_to_JSON(eq_dataframe, 'morningstar_funds_dict')

