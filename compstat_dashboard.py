# Created on Wed Mar 18 2020
# Author: Saravanan Somasundaram
# Purpose: query actuals and forecasts using CreditMaster

import os
import pandas as pd
import datetime
import numpy as np
import cx_Oracle
import boto3
import logging
import base64
import email_util as eu

logging.basicConfig(level=os.environ.get('LOG_LEVEL', 'DEBUG'))
log = logging.getLogger(__name__)

def run_compstat_dashboard():
    # corpcredit credentials
    _cc_db_user = os.environ.get('CC_DB_USER')
    _cc_db_host = os.environ.get('CC_DB_HOST')

    log.debug("_cc_db_user: %s", _cc_db_user)
    log.debug("_cc_db_host: %s", _cc_db_host)

    # dm_corp credentials
    _dm_corp_db_user = os.environ.get('DM_CORP_DB_USER')
    _dm_corp_db_dsn = os.environ.get('DM_CORP_DB_HOST')

    log.debug("_dm_corp_db_user: %s", _dm_corp_db_user)
    log.debug("_dm_corp_db_dsn: %s", _dm_corp_db_dsn)

    session = boto3.Session(region_name='us-east-1')
    ssm = session.client('ssm')
    corpcredit = ssm.get_parameter(
        Name='oracloud-corpcredit-db-password', WithDecryption=True)
    _cc_db_password_encoded = corpcredit['Parameter']['Value']
    log.debug("_cc_db_password_encoded: [REDACTED]")
    _cc_db_password = base64.b64decode(_cc_db_password_encoded)


    dmcorp = ssm.get_parameter(
        Name='oracloud-dmcorp-db-password', WithDecryption=True)
    _dm_corp_db_password_encoded = dmcorp['Parameter']['Value']
    log.debug("_dm_corp_db_password_encoded: [REDACTED]")
    _dm_corp_db_password = base64.b64decode(_dm_corp_db_password_encoded)

    _s3_bucket_name = os.environ.get('S3_BUCKET_NAME')
    log.debug("_s3_bucket_name: %s", _s3_bucket_name)
    bucket_name = _s3_bucket_name

    corp_credit_un = _cc_db_user
    corp_credit_pw = _cc_db_password
    corp_credit_dsn = _cc_db_host

    dmcorp_un = _dm_corp_db_user
    dmcorp_pw = _dm_corp_db_password
    dmcorp_dsn = _dm_corp_db_dsn

    ###########################################################################################################################################
    ##############################Start of getPortfolio########################################################################################
    ###########################################################################################################################################
    # connect to corpcredit database
    sql = """select credit_master.* from corpcredit.credit_master where actv_flg = 'Y'"""
    cn = cx_Oracle.connect(corp_credit_un, corp_credit_pw, corp_credit_dsn)
    d_CM = pd.read_sql(sql, cn)

    # connect to dmcorp database
    sql = """SELECT DM_CORP.AGNT.AGNT_ID, DM_CORP.AGNT.ULT_AGNT_ID, DM_CORP.AGNT.ULT_AGNT_NM FROM DM_CORP.AGNT"""
    dm = cx_Oracle.connect(dmcorp_un, dmcorp_pw, dmcorp_dsn)
    d_Mart = pd.read_sql(sql, dm)
    ###########################################################################################################################################

    d_CM['AGNT_ID'] = d_CM['AGNT_ID'].astype('float64')

    #merge CM and DM_CORP
    d_CM = d_CM.merge(d_Mart, on = 'AGNT_ID', how='left')

    # capture all unique FDR nicknames
    cfin = d_CM[d_CM['NCKNM'].isin(d_CM['CFIN_PRNT_NCKNM'])]
    cfin = cfin.drop_duplicates(['NCKNM'], keep='first')
    cfin['FDR_NCKNM'] = None
    cfin['FDR_NCKNM'] = cfin['NCKNM']

    sub = d_CM[~d_CM['NCKNM'].isin(cfin['CFIN_PRNT_NCKNM'])]
    sub['FDR_NCKNM'] = None
    sub['FDR_NCKNM'] = sub['NCKNM']
    # fdr = cfin.append(sub, ignore_index=True)
    fdr = pd.concat([cfin, sub])

    sub = d_CM[~d_CM['CFIN_PRNT_NCKNM'].isin(d_CM['NCKNM'])]
    sub['FDR_NCKNM'] = None
    sub['FDR_NCKNM'] = sub['CFIN_PRNT_NCKNM']
    # fdr = fdr.append(sub, ignore_index=True)
    fdr = pd.concat([fdr, sub])

    fdr = fdr.drop_duplicates(['FDR_NCKNM'], keep='first')
    fdr = fdr[fdr['FDR_NCKNM'].notnull()]

    ###########################################################################################################################################
    # export

    d = '{:%Y-%m-%d}'.format(datetime.datetime.now())
    loc = '/tmp/'
    filenamecm = loc + 'credit_master_' + d + '.csv'
    log.debug("filenamecm: %s", filenamecm)
    fdr.to_csv(filenamecm, index=False)

    ############################END OF TBD#############################
    ###########################################################################################################################################
    ##############################End of getPortfolio##########################################################################################
    ###########################################################################################################################################


    ###########################################################################################################################################
    ##############################Start of getFDR##############################################################################################
    ###########################################################################################################################################


    def getFdr(NickList, fdrId, startYear, endYear, Cohort=False, tgtCurrencyCode="USD", tgtScale=1000000, write_csvs=False, templateName="GLOBAL CORPORATES", curConversion=True, region='Global'):

        import logging.config
        from datetime import date, datetime
        from zeep import Client, Settings
        import numpy as np
        import pandas as pd
        import time
        import datetime as dt
        from pandas import Series
        import os
        import requests
        import zeep
        from collections import OrderedDict
        import json

        true_start_time = time.time()
        start_time = time.time()

        # location details
        _fdr_link = os.environ.get('FDR_LINK')
        _fdr_url = os.environ.get('FDR_URL')

        log.debug("FDR_LINK: %s", _fdr_link)
        log.debug("FDR_URL: %s", _fdr_url)

        loginkey = ssm.get_parameter(Name='login_key', WithDecryption=True)
        _login_key_encoded = loginkey['Parameter']['Value']
        log.debug("_login_key_encoded: [REDACTED]")

        fdr = _fdr_link
        settings = Settings(strict=False)
        client = Client(fdr, settings=settings)
        login = _login_key_encoded
        fdr_dict = pd.read_csv("FdrDictionary - " +
                               templateName + ".csv", encoding='ISO-8859-1')
        targetCurrencyCode = tgtCurrencyCode
        targetScale = tgtScale

        loc = '/tmp/'
        # load tickers
        if type(NickList) == str:
            my_nicks = pd.read_csv(loc+NickList, encoding='ISO-8859-1')
        # Taking smaller subset for testing purposes
        # my_nicks = my_nicks[0:10]

        ###############################################################################
        # Check to make sure parameters were entered correctly
        ###############################################################################

        if type(startYear) != int:
            print("Please enter an integer for startYear.")
            return None

        if type(endYear) != int:
            print("Please enter an integer for endYear.")
            return None

        if type(Cohort) != bool:
            print("Please enter True or False for Cohort.")
            return None

        if type(NickList) != list and type(NickList) != str:
            print("NickList must be a string or a list.")
            return None

        if type(fdrId) != list and type(fdrId) != str:
            print("fdrId must be a string or a list.")
            return None

        if type(tgtScale) != int:
            print("Please enter an integer for tgtScale.")
            return None

        if endYear < startYear:
            print("endYear cannot be before startYear.")
            return None

        if type(write_csvs) != bool:
            print("Please enter True or False for write_csvs.")
            return None

        if type(curConversion) != bool:
            print("Please enter True or False for curConversion.")
            return None

        if templateName != "UniCOR" and templateName != "GLOBAL CORPORATES":
            print("Please enter 'UniCOR' or 'GLOBAL CORPORATES' for template.")
            return None

        # Plan to add list of currency codes to make sure a real code is being entered

        ###############################################################################
        # get template id
        ###############################################################################
        templates = client.service.getTemplateBusinessList(
            UserLoginBase64=login, productCode='ALL')
        for template in templates:
            if template['name'] == templateName and template['stateId'] == 1:
                tmpltBusID = template['templateId']

        ###############################################################################
        # get nickname ids
        ###############################################################################

        if type(NickList) == list:
            nicknames = NickList
        else:
            nicknames = list(my_nicks.FDR_NCKNM)
        # nicknames = list(my_nicks.FDRNickname)
        nicknames = list(set(nicknames))
        nicks = client.service.getNicknameIds(
            UserLoginBase64=login, nicknames=nicknames)
        nicknames = {i.nicknameId: i.nickname for i in nicks}

        ###############################################################################
        # get statement Master ID's
        ###############################################################################
        result = []
        result_nickname = []
        result_nickname2 = []

        for i in range(len(list(nicknames.keys()))):
            temp_result = client.service.getStatementListByNickname(
                login, list(nicknames.keys())[i], tmpltBusID, "All")
            for data in range(len(temp_result)):
                result_nickname.append(list(nicknames.keys())[i])
                result_nickname2.append(list(nicknames.values())[i])
                result.append(temp_result[data])

        df = pd.DataFrame()

        list_stmntMstrId = []
        list_statementDate = []
        list_periodDuration = []
        list_periodTypeId = []

        for data in result:
            list_stmntMstrId.append(data['stmntMstrId'])
            list_statementDate.append(data['statementDate'])
            list_periodDuration.append(data['periodDuration'])
            list_periodTypeId.append(data['periodTypeId'])

        df['stmntMstrId'] = list_stmntMstrId
        df['statementDate'] = list_statementDate
        df['periodDuration'] = list_periodDuration
        df['periodTypeId'] = list_periodTypeId

        df["statementDate"] = pd.to_datetime(df['statementDate'], utc=True)
        # df["statementYear"] = df["statementDate"].dt.year

        # Adding Nicknames
        df["Nickname ID"] = result_nickname
        df["Nickname"] = result_nickname2

        # Create new column, "STMNT_DT_day", that denotes the day of the statement date
        df["STMNT_DT_day"] = pd.DatetimeIndex(df["statementDate"]).day
        # Create new column, "STMNT_DT_month", that denotes the month of the statement date
        df["STMNT_DT_month"] = pd.DatetimeIndex(df["statementDate"]).month
        # Create new column, "STMNT_DT_year", that denotes the year of the statement date and change to numeric from character
        df["STMNT_DT_year"] = pd.DatetimeIndex(df["statementDate"]).year

        # Create new column, "lfsq_quarter", that determines the corresponding
        # financial quarter.  The following logic is used:
        # 4Q begins Nov 15 and ends Dec 31   ## Step 1 use Q4 and Statement Year
        #   as default
        # 3Q begins Aug 15 and ends Nov 14   ## Step 2 adjust for prior to Nov
        # 2Q begins May 15 and ends Aug 14   ## Step 3 adjust for prior to Aug
        # 1Q begins Feb 15 and ends May 14   ## Step 4 adjust for prior to May
        # 4Q begins Jan 1  and ends Feb 14   ## Step 5 adjust for prior to Feb (both year and quarter)

        df["lfsq_year"] = df["STMNT_DT_year"]

        def changeYear(df):
            if df["STMNT_DT_month"] < 2 or (df["STMNT_DT_month"] <= 2 and df["STMNT_DT_day"] < 15):
                return df["lfsq_year"]-1
            else:
                return df["lfsq_year"]

        df["lfsq_year"] = df.apply(changeYear, axis=1)

        if startYear == endYear:

            df = df[df["lfsq_year"] == startYear]
        elif endYear == 0:
            df = df[df["lfsq_year"] >= startYear]
        else:
            df = df[df["lfsq_year"] > startYear-1]
            df = df[df["lfsq_year"] < endYear + 1]

        df = df[df['periodDuration'] == 12]
        df = df[df['periodTypeId'] == 0]

        stmntMstrIdList = list(df['stmntMstrId'].unique())

        stmntMstrIdList = [int(x) for x in stmntMstrIdList]

        print("Time Elapsed: Get stmntMstrId's: ", time.time() - start_time)

        start_time = time.time()

        ###############################################################################
        # Getting meta data using getStatementListByNickname call
        ###############################################################################

        for i in range(len(result)):
            result[i] = zeep.helpers.serialize_object(result[i])
            result[i] = dict(result[i])
            for j in result[i].keys():
                if j.endswith('Date') and pd.isnull(result[i][j]) == False:
                    result[i][j] = str(result[i][j].date())

        meta_df = pd.json_normalize(result)


        meta_df = meta_df[['scaleId', 'currencyId', 'statementTypeId', 'analistReviewed',
                           'pblshFlg', 'lstChngDate', 'lstModUser', 'stmntMstrId']]
        meta_df.columns = ['scaleId', 'currencyId', 'statementTypeId', 'analistReviewed',
                           'pblshFlg', 'lastChangeDate', 'lastChangedBy', 'stmntMstrId']

        df = pd.merge(left=df, right=meta_df, on="stmntMstrId", how="left")

        print("Time Elapsed: Organizing metadata: ", time.time() - start_time)

        start_time = time.time()


        ###############################################################################
        ### skip USD if converting to reduce memory used
        ###############################################################################
        if curConversion == True:
            df = df[df['currencyId'] != 163]
            stmntMstrIdList = pd.DataFrame(stmntMstrIdList)
            stmntMstrIdList.columns = ['stmntMstrId']
            stmntMstrIdList = stmntMstrIdList[stmntMstrIdList['stmntMstrId'].isin(df['stmntMstrId'])]
            stmntMstrIdList = list(df['stmntMstrId'].unique())
            stmntMstrIdList = [int(x) for x in stmntMstrIdList]


        ###############################################################################
        # REST API
        ###############################################################################

        fdrUrl = _fdr_url
        uName = os.environ.get('USERNAME')

        if type(fdrId) == str:
            fdrId = pd.read_csv(fdrId, encoding='ISO-8859-1')
            fdrIds = list(fdrId.fdrID)
        else:
            fdrIds = fdrId

        # NC: Add total debt with equity credit
        if templateName == "GLOBAL CORPORATES" and 11010 not in fdrIds:
            fdrIds.append(11010)
        if templateName == "UniCOR" and 200200 not in fdrIds:
            fdrIds.append(200200)

        # Get FDR detail information from FDR Web Service
        payload = {'userId': uName,
                   'tmpltBusId': tmpltBusID,
                   'stmntMstrIdList': stmntMstrIdList,
                   'idList': fdrIds,
                   'idType': 'FDRID',
                   'includeOffsetInfo': 'true'}

        # payload = {'userId': os.environ['USERNAME'],
        #           'tmpltBusId': tmpltBusID,
        #           'stmntMstrIdList': stmntMstrIdList,
        #           'idList': fdrIds,
        #           'idType': 'FDRID',
        #           'includeOffsetInfo': 'true'}

        r = requests.post(fdrUrl, json=payload)

        d = r.json()

        print("Time Elapsed: Running REST API: ", time.time() - start_time)

        start_time = time.time()

        ###############################################################################
        # Formatting Full Statements from REST API
        ###############################################################################

        if templateName == 'UniCOR':
            final_table = pd.json_normalize(d['statementMasterList'], 'statementDetailList', ['fiscalYear', 'periodDuration', 'periodTypeId', 'statementDate', 'statementTypeId', 'stmntMstrId'])\
                .pivot(index='stmntMstrId', columns='fdrId', values='adjustedValue')
        else:
            final_table = pd.json_normalize(d['statementMasterList'], 'statementDetailList', ['fiscalYear', 'periodDuration', 'periodTypeId', 'statementDate', 'statementTypeId', 'stmntMstrId'])\
                .pivot(index='stmntMstrId', columns='fdrId', values='finalValue')

        print("Time Elapsed: Organizing REST API Data: ", time.time() - start_time)

        start_time = time.time()

        ###############################################################################
        # Merging REST API with meta data
        ###############################################################################

        combinedDf = pd.merge(left=final_table, right=df, on="stmntMstrId",
                              how="left", suffixes=("_details", "_masters"))

        # if templateName == 'UniCOR':
        #     for i in combinedDf.columns.values:
        #         if i in fdrIds:
        #             combinedDf[i] = [j.replace(",","") for j in combinedDf[i]]
        #             combinedDf[i] = combinedDf[i].astype('float64')

        ###############################################################################
        # adding scale
        ###############################################################################

        def addScale(row):
            if row['scaleId'] ==0:
                return 1
            if row['scaleId']==1:
                return 10
            if row['scaleId'] == 2:
                return 100
            if row['scaleId'] == 3:
                return 1000
            if row['scaleId'] == 4:
                return 1000000
            if row['scaleId'] == 5:
                return 1000000000

        # adding the function values
        combinedDf['SourceScale'] = combinedDf.apply(addScale, axis=1)

        # we are making it standard millions
        combinedDf['TargetScale'] = targetScale
        combinedDf['scaleConver'] = combinedDf['SourceScale'] / \
            combinedDf['TargetScale']
        # Not elegant at all.. if i could jsut multiply by a list
        # fdrIdListNonRatio =[10280,10730,11090,11240,25160,25230,26300,25300,26320,15000,26380,25360,26420,11010,11370,121880,2101,2102,2103,2104,2105,2106,2107,2111,10440,10391,11450,14990,15180]

        # only those 3 ratios in combinedDf

        fdrRatioDict = fdr_dict.set_index("FDR Id")["Ratio"].to_dict()
        fdrIdListNonRatio = []

        for i in fdrIds:
            if fdrRatioDict[i] == False:
                fdrIdListNonRatio.append(i)

        # fdrIdListNonRatio=[10280,10730]
        for x in fdrIdListNonRatio:
            combinedDf[x] = combinedDf[x] * combinedDf['scaleConver']

        ###############################################################################
        # add exchange rates - conversion happens in R script
        ###############################################################################

        # NC: Tweaked these lines a bit bc they were acting up. Might be bc of a new Pandas version
        # get statement dates for which I need an FX rate
        targetDates = list(pd.to_datetime(combinedDf['statementDate']))
        targetDates = [i for i in targetDates if i <
                       datetime.now(targetDates[0].tzinfo)]

        targetDates = set(targetDates)

        # convert currency ID to letter ID
        currency = client.service.getLookups(login, "CURRENCY")
        curr_dic = {}
        for curr in currency:
            curr_dic.update({curr['id']: curr['code']})

        # create a unique set of currencyy codes based on the data frame supplied
        letterIdList = []
        for cid in set(combinedDf['currencyId']):
            letterIdList.append(curr_dic[cid])

        # for each statement date, run the methods below to collect the necessary conversion data
        dateList = []
        valueList = []
        targetList = []
        sourceList = []
        fxTypeList = []

        # below is more explicit. Don't need to make assumptions if API returns data needed
        for d in targetDates:
            average = client.service.getAverageExchangeRateForMultipleCurrency(
                login, targetCurrencyCode, letterIdList, d, 12)
            for i in average:
                # we invert this rate b/c the way the
                valueList.append(1/i['rate'])
                # FDR API is set up you can't pass multiple targets so in order to
                # minimize the number of calls to the API we are using the source
                # list parameter as the target list
                # dateList.append(i['rateDate']) #looks like this is broken- only returns todays date
                dateList.append(d)
                targetList.append(i['sourceCurrencyCd'])
                sourceList.append(i['targetCurrencyCd'])
                fxTypeList.append("Average")
            spot = client.service.getExchangeRateForMultipleCurrency(
                login, targetCurrencyCode, letterIdList, d)
            for i in spot:
                # we invert this rate b/c the way the
                valueList.append(1/i['rate'])
                # FDR API is set up you can't pass multiple targets so in order to
                # minimize the number of calls to the API we are using the source
                # list parameter as the target list
                dateList.append(i['rateDate'])
                targetList.append(i['sourceCurrencyCd'])
                sourceList.append(i['targetCurrencyCd'])
                fxTypeList.append("Spot")

        fxRef = pd.DataFrame({'Date': dateList,
                              'FX_Type': fxTypeList,
                              'Source': sourceList,
                              'Target': targetList,
                              'Value': valueList})
        # repeatDateList=np.repeat(dateList,len(letterIdList))
        # d={'Average Rate':pd.Series(averageList), 'Spot Rate':pd.Series(spotList), 'Statement Date': pd.Series(repeatDateList), 'Source Currency':
        #    pd.Series(letterIdList*len(dateList)),'Target Currency': pd.Series([targetCurrencyCode]*len(dateList)*len(letterIdList))}
        # fxDf_new =pd.DataFrame(d)

        if write_csvs == True:
            fxRef.to_csv(loc + "ReferenceTable.csv",
                         index=False)

        # LOAD FDR DATA
        curr_dict = pd.read_csv("CurrencyDict.csv", encoding='ISO-8859-1')
        fx_dict = fxRef  # 12/11: No need to call csv if we already have the data frame

        # standarize the date, remove hours, minutes and seconds
        fx_dict["Date"] = pd.to_datetime(fx_dict["Date"], utc=True).dt.date

        # rename columns, more make sense names ? rename columns from Python FDR data to match legacy R script
        combinedDf = combinedDf.rename(index=str, columns={"statementDate": "STMNT_DT",
                                                           "scaleId": "SCALE_ID",
                                                           "currencyId": "CRNCY_ID",
                                                           "periodDuration": "PRD_DUR_ID",
                                                           "periodTypeId": "PRD_TYP_ID",
                                                           "lastChangeDate": "CHG_DT",
                                                           "lastChangedBy": "CHG_USR",
                                                           "Nickname": "NCKNM"})

        # create a new column ("STMNT_TYP_DESC")
        combinedDf["STMNT_TYP_DESC"] = combinedDf["statementTypeId"].apply(
            lambda x: "Original" if x == 0 else(
                "Forecast" if x == 3 else(
                    "Restated" if x == 1 else
                    "UNKNOWN")))

        combinedDf = pd.concat([combinedDf[combinedDf["STMNT_TYP_DESC"] == "Original"],
                                combinedDf[combinedDf["STMNT_TYP_DESC"] == "Forecast"], combinedDf[combinedDf["STMNT_TYP_DESC"] == "Restated"]])

        # replace this w/ setnames next time
        # maybe there is another way.. this part is ugly, for fdr_dict, FdrId value starts with X, so remove the x, form [1:]

        # convert columns name value to str
        # combinedDf.columns=combinedDf.columns.astype(str)

        # Adds correct column names
    #    nameMatch=Series(fdr_dict["Item Description"].values,index=fdr_dict["FDR Id"]).to_dict()
    #    nameMatchx={}
    #    for i in nameMatch:
    #        nameMatchx[i]=nameMatch[i]
    #
    #    combinedDf=combinedDf.rename(nameMatchx,axis=1)

        ###############################################################################
        # Removing Duplicates and Bad Data
        ###############################################################################

        # NC: Added for data quality purposes
        # LM removed 9/20/21
        # if templateName == "GLOBAL CORPORATES":
        #    combinedDf = combinedDf[pd.isnull(combinedDf[11010]) == False]

        combinedDf = combinedDf.sort_values(by=["STMNT_DT", "CHG_DT"])
        combinedDf = combinedDf.drop_duplicates(
            subset=["NCKNM", "lfsq_year", "STMNT_TYP_DESC"], keep="last")

        # Counts occurences of each NCKNM and fiscal year combo
        groupBydf = combinedDf.groupby(
            ["NCKNM", "lfsq_year"]).size().reset_index(name='N')
        # Adds N variable to FDR Data
        newFdr = pd.merge(combinedDf, groupBydf, on=[
                          "NCKNM", "lfsq_year"], how="inner")
        dupes_groups = groupBydf[groupBydf['N'] >= 2]
        dupes_dic = pd.merge(combinedDf, dupes_groups, on=[
                             "NCKNM", "lfsq_year"], how="inner")
        clean_fdr = newFdr[newFdr['N'] < 2]

        # Re-adds more current statement for duplicates
        for i in range(len(dupes_groups.index)):
            temp_dt = pd.merge(dupes_dic, pd.DataFrame(
                dupes_groups.iloc[i:i+1])[["NCKNM", "lfsq_year"]], on=["NCKNM", "lfsq_year"], how="inner")

            if len(temp_dt["STMNT_TYP_DESC"].unique()) == 1:
                # clean_fdr = clean_fdr.append(
                #     temp_dt[temp_dt["CHG_DT"] == temp_dt["CHG_DT"].max()])
                clean_fdr = pd.concat([clean_fdr, temp_dt[temp_dt["CHG_DT"] == temp_dt["CHG_DT"].max()]])
            else:
                temp_dt = temp_dt[temp_dt["STMNT_TYP_DESC"] != 'Forecast']
                if "Restated" in temp_dt.values:
                    # clean_fdr = clean_fdr.append(
                    #     temp_dt[temp_dt["STMNT_TYP_DESC"] == "Restated"])
                    clean_fdr = pd.concat([clean_fdr, temp_dt[temp_dt["STMNT_TYP_DESC"] == "Restated"]])
                else:
                    # clean_fdr = clean_fdr.append(
                    #     temp_dt[temp_dt["CHG_DT"] == temp_dt["CHG_DT"].max()])
                    clean_fdr = pd.concat([clean_fdr, temp_dt[temp_dt["CHG_DT"] == temp_dt["CHG_DT"].max()]])

        # check no more duplicate statements

        groupBydf2 = clean_fdr.groupby(
            ["NCKNM", "lfsq_year"]).size().reset_index(name='N2')

        if groupBydf2[groupBydf2["N2"] >= 2].empty == True:
            print("\nNo duplicate statements\n")
        else:
            print("\nSTILL DUPLICATE STATEMENTS!!!")

        ###########################################################
        # Cohort Section
        ###########################################################

        # CREATE COHORT
        if Cohort == True:
            for i in range(startYear, endYear+1):
                if i == startYear:
                    testVec = pd.DataFrame(
                        clean_fdr[clean_fdr["lfsq_year"] == i]["NCKNM"])
                    finalVec = testVec
                else:
                    testVec = pd.DataFrame(
                        clean_fdr[clean_fdr["lfsq_year"] == i]["NCKNM"])
                    finalVec = pd.merge(
                        left=testVec, right=finalVec, on="NCKNM", how="inner")

            final_fdr = pd.merge(clean_fdr, finalVec, on="NCKNM", how="inner")

        if Cohort == False:
            final_fdr = clean_fdr

        ###################################################################
        # Performing currency conversion
        ###################################################################
        if curConversion == False:
            final_fdr["CRNCY"] = [curr_dic[i] for i in final_fdr["CRNCY_ID"]]
            final_fdr["STMNT_DT"] = final_fdr["STMNT_DT"].dt.date

        if curConversion == True:
            # input target/common currency
            tgtCur = tgtCurrencyCode

            # Getting Currency abbreviation for input currency
            final_fdr["CRNCY"] = [curr_dic[i] for i in final_fdr["CRNCY_ID"]]

            # add tgt cur column
            final_fdr["tgtCRNCY"] = tgtCur

            # create a key to merge conversion rates
            fx_dict["CRNCY_KEY"] = fx_dict["Date"].map(
                str)+fx_dict["Source"]+fx_dict["Target"]
            final_fdr["CRNCY_KEY"] = (final_fdr["STMNT_DT"].dt.date).map(
                str)+final_fdr["CRNCY"]+tgtCur

            # merge in fx value
            fx_dict = fx_dict.drop_duplicates(keep="first")
            merged_fdr = pd.merge(
                final_fdr, fx_dict[fx_dict["FX_Type"] == 'Spot'], on="CRNCY_KEY", how="left")
            merged_fdr = merged_fdr.rename(
                index=str, columns={"Value": "FX_Value"})
            merged_fdr = merged_fdr.drop(
                ["Date", "FX_Type", "Source", "Target"], axis=1)

            # delete the overlap columns after merge
            merged_fdr2 = pd.merge(
                merged_fdr, fx_dict[fx_dict["FX_Type"] == 'Average'], on="CRNCY_KEY", how="left", suffixes=('', '_y'))
            merged_fdr2 = merged_fdr2.drop(
                ["Date", "FX_Type", "Source", "Target"], axis=1)
            merged_fdr2 = merged_fdr2.rename(
                index=str, columns={"Value": "FXavg_Value"})
            # Moving to end
            # overlap_cols=[x for x in merged_fdr2.columns[merged_fdr2.columns.str.endswith('_y')]]
            # merged_fdr2=merged_fdr2.drop(overlap_cols,axis=1)

            # create a key to merge conversion rates a second time- but only the forecasts without matches
            fx_spot_fcast = fx_dict[fx_dict["Date"] == dt.date(dt.datetime.today().year-1,12,31)]
            fx_spot_fcast = fx_spot_fcast[fx_spot_fcast["FX_Type"] == "Spot"]
            fx_avg_fcast = fx_dict[fx_dict["Date"] == dt.date(dt.datetime.today().year-1,12,31)]
            fx_avg_fcast = fx_avg_fcast[fx_avg_fcast["FX_Type"] == "Average"]

            merged_fdr2["CRNCY_KEY2"] = merged_fdr2["CRNCY"] + \
                merged_fdr2["tgtCRNCY"]
            fx_spot_fcast["CRNCY_KEY2"] = fx_spot_fcast["Source"] + \
                fx_spot_fcast["Target"]
            fx_avg_fcast["CRNCY_KEY2"] = fx_avg_fcast["Source"] + \
                fx_avg_fcast["Target"]

            merged_fdr3 = pd.merge(merged_fdr2, fx_avg_fcast,
                                   on="CRNCY_KEY2", how="left", suffixes=('', '_y'))
            merged_fdr3 = merged_fdr3.drop(
                ["Date", "FX_Type", "Source", "Target", "CRNCY_KEY_y"], axis=1)

            merged_fdr4 = pd.merge(merged_fdr3, fx_spot_fcast,
                                   on="CRNCY_KEY2", how="left", suffixes=('', '_y'))
            merged_fdr4 = merged_fdr4.drop(
                ["Date", "FX_Type", "Source", "Target", "CRNCY_KEY_y"], axis=1)

            merged_fdr4 = merged_fdr4.rename(
                index=str, columns={"Value": "Last FXavg_Value", "Value_y": "Last FX_Value"})

            # Should prevent chained assignment warning for following for loop
            pd.options.mode.chained_assignment = None

            for i in range(len(merged_fdr4)):

                if np.isnan(merged_fdr4["FX_Value"][i]) == True:
                    merged_fdr4["FX_Value"].iloc[i] = merged_fdr4["Last FX_Value"].iloc[i]

                if np.isnan(merged_fdr4["FXavg_Value"][i]) == True:
                    merged_fdr4["FXavg_Value"].iloc[i] = merged_fdr4["Last FXavg_Value"].iloc[i]

            merged_fdr4 = merged_fdr4.drop(
                ["Last FXavg_Value", "Last FX_Value"], axis=1)

            final_fdr = merged_fdr4

            final_fdr["STMNT_DT"] = final_fdr["STMNT_DT"].dt.date

            # if missing FX_value prob b/c forecast. Add latest forecast
            # def fillNullSpot(df):
            #    if df["FX_Value"]==np.nan and df["CRNCY"]==df["tgtCRNCY"]:
            #        return 1
            #    else:
            #        return df["FX_Value"]
            #
            # def fillNullAvg(df):
            #    if df["FXavg_Value"]==np.nan and df["CRNCY"]==df["tgtCRNCY"]:
            #        return 1
            #    else:
            #        return df["FXavg_Value"]
            #
            # merged_fdr2["FX_Value"]=merged_fdr2.apply(fillNullSpot,axis=1)
            # merged_fdr2["FXavg_Value"]=merged_fdr2.apply(fillNullAvg,axis=1)

            # create a key to merge conversion rates a second time- but only the forecasts without matches

            # this add 12-31-17 fx rates to forecasts statements

            ###############################################################################
            # Performing FX conversion
            ###############################################################################

            fdrConvTypeDict = fdr_dict.set_index(
                "FDR Id")["Conversion Type"].to_dict()

            for i in fdrIdListNonRatio:
                if fdrConvTypeDict[i] == "Spot":
                    final_fdr[i] = final_fdr[i]*final_fdr["FX_Value"]
                if fdrConvTypeDict[i] == "Average":
                    final_fdr[i] = final_fdr[i]*final_fdr["FXavg_Value"]

        ###############################################################################
        # Adding correct column names and deleting overlaps
        ###############################################################################

        nameMatch = Series(fdr_dict["Item Description"].values,
                           index=fdr_dict["FDR Id"]).to_dict()
        nameMatchx = {}
        for i in nameMatch:
            nameMatchx[i] = nameMatch[i]

        final_fdr = final_fdr.rename(nameMatchx, axis=1)

        overlap_cols = [
            x for x in final_fdr.columns[final_fdr.columns.str.endswith('_y')]]
        final_fdr = final_fdr.drop(overlap_cols, axis=1)

        # Removes ID columns for cleaner reporting purposes
        final_fdr = final_fdr.drop(["PRD_DUR_ID", "PRD_TYP_ID", "CRNCY_ID",
                                    "statementTypeId", "SCALE_ID", "N"], axis=1)

        final_fdr = final_fdr.drop_duplicates()

        if write_csvs == True and curConversion == False:
            final_fdr.to_csv(loc + region + "_fdr_data.csv",
                             index=False)

        if write_csvs == True and curConversion == True:
            final_fdr.to_csv(loc + region + "_fdr_USD_data.csv",
                             index=False)

        end_time = time.time()
        print("Time Elapsed (Rest of code): ", end_time - start_time)
        print("Time Elapsed (Total): ", time.time() - true_start_time)

        final_fdr = final_fdr.drop_duplicates(keep="last")

        return final_fdr

    ###############################################################################
        # If not passing in Nickname List or FDR ID List, create here
    ###############################################################################


    # Function Calls
    ###############################################################################
    # location details
    d = '{:%Y-%m-%d}'.format(datetime.datetime.now())

    year = int(datetime.datetime.now().year)
    start_year = year - 5
    end_year = year + 3

    filenamecmread = loc + 'credit_master_' + d + '.csv'
    log.debug("filenamecmread: %s", filenamecmread)
    my_nicks = pd.read_csv(filenamecmread, encoding='ISO-8859-1')

    region = 'LATAM'

    nicknames = my_nicks[my_nicks['GEO_SGMNT'] == region]
    nicknames = list(nicknames.FDR_NCKNM)
    fdrData = getFdr(NickList = nicknames,fdrId = 'fdrIDs.csv',
                     startYear = start_year, endYear = end_year, templateName = "GLOBAL CORPORATES",
                     curConversion= False, Cohort = False,tgtCurrencyCode = "USD",write_csvs = True, region = region)

    fdrData = getFdr(NickList = nicknames,fdrId = 'fdrIDs.csv',
                     startYear = start_year, endYear = end_year, templateName = "GLOBAL CORPORATES",
                     curConversion= True, Cohort = False,tgtCurrencyCode = "USD",write_csvs = True, region = region)

    region = 'APAC'
    nicknames = my_nicks[my_nicks['GEO_SGMNT'] == region]
    nicknames = list(nicknames.FDR_NCKNM)
    fdrData = getFdr(NickList = nicknames,fdrId = 'fdrIDs.csv',
                     startYear = start_year, endYear = end_year, templateName = "GLOBAL CORPORATES",
                     curConversion= False, Cohort = False,tgtCurrencyCode = "USD",write_csvs = True, region = region)

    fdrData = getFdr(NickList = nicknames,fdrId = 'fdrIDs.csv',
                     startYear = start_year, endYear = end_year, templateName = "GLOBAL CORPORATES",
                     curConversion= True, Cohort = False,tgtCurrencyCode = "USD",write_csvs = True, region = region)

    region = 'EMEA'
    nicknames = my_nicks[my_nicks['GEO_SGMNT'] == region]
    nicknames = list(nicknames.FDR_NCKNM)
    fdrData = getFdr(NickList = nicknames,fdrId = 'fdrIDs.csv',
                     startYear = start_year, endYear = end_year, templateName = "GLOBAL CORPORATES",
                     curConversion= False, Cohort = False,tgtCurrencyCode = "USD",write_csvs = True, region = region)

    fdrData = getFdr(NickList = nicknames,fdrId = 'fdrIDs.csv',
                     startYear = start_year, endYear = end_year, templateName = "GLOBAL CORPORATES",
                     curConversion= True, Cohort = False,tgtCurrencyCode = "USD",write_csvs = True, region = region)

    region = 'NorthAmerica'
    nicknames = my_nicks[my_nicks['GEO_SGMNT'] == region]
    nicknames = list(nicknames.FDR_NCKNM)
    fdrData = getFdr(NickList = nicknames,fdrId = 'fdrIDs.csv',
                     startYear = start_year, endYear = end_year, templateName = "GLOBAL CORPORATES",
                     curConversion= False, Cohort = False,tgtCurrencyCode = "USD",write_csvs = True, region = region)

    fdrData = getFdr(NickList = nicknames,fdrId = 'fdrIDs.csv',
                     startYear = start_year, endYear = end_year, templateName = "GLOBAL CORPORATES",
                     curConversion= True, Cohort = False,tgtCurrencyCode = "USD",write_csvs = True, region = region)

    ###########################################################################################################################################
    ##############################End of getFDR################################################################################################
    ###########################################################################################################################################


    ###########################################################################################################################################
    ##############################Start of mergeData###########################################################################################
    ###########################################################################################################################################

    # location details

    d = '{:%Y-%m-%d}'.format(datetime.datetime.now())

    # read in cm
    d_CM = pd.read_csv(filenamecmread, encoding='ISO-8859-1')


    #read in global corp data (converted)
    d = pd.read_csv(loc+'NorthAmerica_fdr_USD_data.csv', encoding='ISO-8859-1')
    d_FDR = d
    d = pd.read_csv(loc+'EMEA_fdr_USD_data.csv', encoding='ISO-8859-1')
    # d_FDR = d_FDR.append(d, ignore_index=True)
    d_FDR = pd.concat([d_FDR, d])
    d = pd.read_csv(loc+'APAC_fdr_USD_data.csv', encoding='ISO-8859-1')
    # d_FDR = d_FDR.append(d, ignore_index=True)
    d_FDR = pd.concat([d_FDR, d])
    d = pd.read_csv(loc+'LATAM_fdr_USD_data.csv', encoding='ISO-8859-1')
    # d_FDR = d_FDR.append(d, ignore_index=True)
    d_FDR = pd.concat([d_FDR, d])

    #read in global corp data (not converted)
    d = pd.read_csv(loc+'NorthAmerica_fdr_data.csv', encoding='ISO-8859-1')
    # d_FDR = d_FDR.append(d, ignore_index=True)
    d_FDR = pd.concat([d_FDR, d])
    d = pd.read_csv(loc+'EMEA_fdr_data.csv', encoding='ISO-8859-1')
    # d_FDR = d_FDR.append(d, ignore_index=True)
    d_FDR = pd.concat([d_FDR, d])
    d = pd.read_csv(loc+'APAC_fdr_data.csv', encoding='ISO-8859-1')
    # d_FDR = d_FDR.append(d, ignore_index=True)
    d_FDR = pd.concat([d_FDR, d])
    d = pd.read_csv(loc+'LATAM_fdr_data.csv', encoding='ISO-8859-1')
    # d_FDR = d_FDR.append(d, ignore_index=True)
    d_FDR = pd.concat([d_FDR, d])

    #merge
    all_data = d_CM.merge(d_FDR, left_on = 'FDR_NCKNM', right_on= 'NCKNM')

    #remove old forecasts
    all_data = all_data[~((all_data['lfsq_year'] < 2019) & (all_data['STMNT_TYP_DESC'] == 'Forecast'))]

    #identify cohort of last five years
    for i in range(2015,2023):
        if i == 2015:
            testVec = all_data[(all_data["lfsq_year"] == i)]
            finalVec = testVec
        else:
            testVec = all_data[(all_data["lfsq_year"] == i)]
            finalVec = finalVec[finalVec['FDR_NCKNM'].isin(testVec['FDR_NCKNM'])]

    all_data['COHORT'] = None
    all_data.loc[(all_data['FDR_NCKNM'].isin(finalVec['FDR_NCKNM'])),'COHORT'] = 'TRUE'

    #identify Credit Parents
    all_data['CREDIT_PRNT'] = None
    all_data.loc[all_data['AGNT_ID'] == (all_data['CREDIT_PRNT_ID']),'CREDIT_PRNT'] = 'TRUE'

    #identify Committee Parents
    all_data['CMT_PRNT'] = None
    all_data.loc[all_data['AGNT_ID'] == (all_data['CMT_PRNT_ID']),'CMT_PRNT'] = 'TRUE'

    #identify Consolidated Financial Parents
    all_data['CON_FIN_PRNT'] = None
    all_data.loc[all_data['NCKNM_x'] == (all_data['CFIN_PRNT_NCKNM']),'CON_FIN_PRNT'] = 'TRUE'

    ##############################################################################################################################

    #identify outliers

    #filter to USD data only
    all_data.loc[all_data['tgtCRNCY'] == 'USD','CRNCY'] = 'USD'
    usd_data = all_data[(all_data['CRNCY'] == 'USD')]
    usd_data['FX_CONV'] = 'USD'

    usd_data['REV_OUTLIER'] = None
    lower_bm = np.percentile(usd_data['Gross Revenue'], 20)
    usd_data.loc[usd_data['Gross Revenue'] <= lower_bm,'REV_OUTLIER'] = '20th percentile'

    higher_bm = np.percentile(usd_data['Gross Revenue'], 80)
    usd_data.loc[usd_data['Gross Revenue'] >= higher_bm,'REV_OUTLIER'] = '80th percentile'

    lower_bm = np.percentile(usd_data['Gross Revenue'], 15)
    usd_data.loc[usd_data['Gross Revenue'] <= lower_bm,'REV_OUTLIER'] = '15th percentile'

    higher_bm = np.percentile(usd_data['Gross Revenue'], 85)
    usd_data.loc[usd_data['Gross Revenue'] >= higher_bm,'REV_OUTLIER'] = '85th percentile'

    lower_bm = np.percentile(usd_data['Gross Revenue'], 10)
    usd_data.loc[usd_data['Gross Revenue'] <= lower_bm,'REV_OUTLIER'] = '10th percentile'

    higher_bm = np.percentile(usd_data['Gross Revenue'], 90)
    usd_data.loc[usd_data['Gross Revenue'] >= higher_bm,'REV_OUTLIER'] = '90th percentile'

    lower_bm = np.percentile(usd_data['Gross Revenue'], 5)
    usd_data.loc[usd_data['Gross Revenue'] <= lower_bm,'REV_OUTLIER'] = '5th percentile'

    higher_bm = np.percentile(usd_data['Gross Revenue'], 95)
    usd_data.loc[usd_data['Gross Revenue'] >= higher_bm,'REV_OUTLIER'] = '95th percentile'

    usd_data.loc[usd_data['REV_OUTLIER'].isnull(),'REV_OUTLIER'] = 'Not an Outlier'

    usd_data['EBITDA_OUTLIER'] = None
    lower_bm = np.percentile(usd_data['Operating EBITDA (Before Income from Associates)'], 20)
    usd_data.loc[usd_data['Operating EBITDA (Before Income from Associates)'] <= lower_bm,'EBITDA_OUTLIER'] = '20th percentile'

    higher_bm = np.percentile(usd_data['Operating EBITDA (Before Income from Associates)'], 80)
    usd_data.loc[usd_data['Operating EBITDA (Before Income from Associates)'] >= higher_bm,'EBITDA_OUTLIER'] = '80th percentile'

    lower_bm = np.percentile(usd_data['Operating EBITDA (Before Income from Associates)'], 15)
    usd_data.loc[usd_data['Operating EBITDA (Before Income from Associates)'] <= lower_bm,'EBITDA_OUTLIER'] = '15th percentile'

    higher_bm = np.percentile(usd_data['Operating EBITDA (Before Income from Associates)'], 85)
    usd_data.loc[usd_data['Operating EBITDA (Before Income from Associates)'] >= higher_bm,'EBITDA_OUTLIER'] = '85th percentile'

    lower_bm = np.percentile(usd_data['Operating EBITDA (Before Income from Associates)'], 10)
    usd_data.loc[usd_data['Operating EBITDA (Before Income from Associates)'] <= lower_bm,'EBITDA_OUTLIER'] = '10th percentile'

    higher_bm = np.percentile(usd_data['Operating EBITDA (Before Income from Associates)'], 90)
    usd_data.loc[usd_data['Operating EBITDA (Before Income from Associates)'] >= higher_bm,'EBITDA_OUTLIER'] = '90th percentile'

    lower_bm = np.percentile(usd_data['Operating EBITDA (Before Income from Associates)'], 5)
    usd_data.loc[usd_data['Operating EBITDA (Before Income from Associates)'] <= lower_bm,'EBITDA_OUTLIER'] = '5th percentile'

    higher_bm = np.percentile(usd_data['Operating EBITDA (Before Income from Associates)'], 95)
    usd_data.loc[usd_data['Operating EBITDA (Before Income from Associates)'] >= higher_bm,'EBITDA_OUTLIER'] = '95th percentile'

    usd_data.loc[usd_data['EBITDA_OUTLIER'].isnull(),'EBITDA_OUTLIER'] = 'Not an Outlier'

    usd_data['DEBT_OUTLIER'] = None
    lower_bm = np.percentile(usd_data['Total Debt with Equity Credit'], 20)
    usd_data.loc[usd_data['Total Debt with Equity Credit'] <= lower_bm,'DEBT_OUTLIER'] = '20th percentile'

    higher_bm = np.percentile(usd_data['Total Debt with Equity Credit'], 80)
    usd_data.loc[usd_data['Total Debt with Equity Credit'] >= higher_bm,'DEBT_OUTLIER'] = '80th percentile'

    lower_bm = np.percentile(usd_data['Total Debt with Equity Credit'], 15)
    usd_data.loc[usd_data['Total Debt with Equity Credit'] <= lower_bm,'DEBT_OUTLIER'] = '15th percentile'

    higher_bm = np.percentile(usd_data['Total Debt with Equity Credit'], 85)
    usd_data.loc[usd_data['Total Debt with Equity Credit'] >= higher_bm,'DEBT_OUTLIER'] = '85th percentile'

    lower_bm = np.percentile(usd_data['Total Debt with Equity Credit'], 10)
    usd_data.loc[usd_data['Total Debt with Equity Credit'] <= lower_bm,'DEBT_OUTLIER'] = '10th percentile'

    higher_bm = np.percentile(usd_data['Total Debt with Equity Credit'], 90)
    usd_data.loc[usd_data['Total Debt with Equity Credit'] >= higher_bm,'DEBT_OUTLIER'] = '90th percentile'

    lower_bm = np.percentile(usd_data['Total Debt with Equity Credit'], 5)
    usd_data.loc[usd_data['Total Debt with Equity Credit'] <= lower_bm,'DEBT_OUTLIER'] = '5th percentile'

    higher_bm = np.percentile(usd_data['Total Debt with Equity Credit'], 95)
    usd_data.loc[usd_data['Total Debt with Equity Credit'] >= higher_bm,'DEBT_OUTLIER'] = '95th percentile'

    usd_data.loc[usd_data['DEBT_OUTLIER'].isnull(),'DEBT_OUTLIER'] = 'Not an Outlier'

    usd_data = usd_data[['AGNT_ID','AGNT_NM','ULT_AGNT_ID','ULT_AGNT_NM','CFIN_PRNT_NCKNM','CON_FIN_PRNT','TEAM_NM','SUB_SCTR_NM','SUP_ANLYST','DATA_ANLYST','PRIM_ANLYST','MRKT_SCTR_4','FDR_NCKNM','GEO_SGMNT',
    'CNTRY_OPER', 'LT_FC_IDR', 'LT_FC_OUTLOOK', 'LT_FC_RTNG_PRODUCT', 'LT_LC_IDR', 'LT_LC_RTNG_PRODUCT', 'NT_FC_LT_IDR', 'NT_FC_LT_RTNG_PRODUCT',
    'stmntMstrId', 'STMNT_DT', 'lfsq_year','STMNT_TYP_DESC', 'analistReviewed','pblshFlg','CRNCY','FX_CONV', 'FX_Value','FXavg_Value',
    'Gross Revenue','Revenue Growth (%)','Operating EBITDA (Before Income from Associates)','Operating EBITDA Margin (%)','Operating EBITDA (After Associates and Minorities)',
    'Rental Expense ','Operating EBITDAR','Operating EBITDAR Margin (%)','Operating EBITDAR after associates and minorities ','Operating EBIT','Operating EBIT Margin (%)',
    'Gross Interest Expense','Net Income','Readily Available Cash and Equivalents','Net Working Capital (Fitch-Defined)','Short-Term Debt','Total Debt with Equity Credit',
    'Senior Secured Debt','Senior Unsecured Debt','Subordinated Debt','Other Debt','Equity Credit','Total Adjusted Debt with Equity Credit ','Off Balance Sheet Debt ',
    'Net Debt ','Operating EBITDA ','Cash Interest Paid','Cash interest received ','Cash Tax','Funds Flow from Operations','FFO Margin (%)','Change in Working Capital',
    'Cash Flow from Operations (Fitch Defined)','Capital Expenditure','Capital Intensity (Capex/Revenue) %','Common Dividends','Free Cash Flow','Free Cash Flow Margin (%)',
    'Net Acquisitions and Divestitures','FFO Interest Coverage (x)','FFO Fixed Charge Coverage (x)','Operating EBITDAR/Interest Paid + Rents (x)',
    'Operating EBITDAR/Net Interest Paid + Rents (x)','Operating EBITDA/Interest Paid (x)','Total Adjusted Debt/Operating EBITDAR (x)',
    'Total Adjusted Net Debt/Operating EBITDAR (x)','Total Debt with Equity Credit/Operating EBITDA (x)','Total Net Debt With Equity Credit/Operating EBITDA (x)',
    'FFO Adjusted Leverage (x)','FFO Adjusted Net Leverage (x)', 'FFO Leverage (x)', 'FFO Net Leverage  (x)',
    'Pretax Income (Including Associate Income/Loss) ','Dividends Received Less Dividends Paid to Minorities (Inflow/(Out)flow)','Other Items Before FFO ',
    'Total Non-Operating/Non-Recurring Cash Flow','Other Investing and Financing Cash Flow Items ','Net Debt Proceeds','Net Equity Proceeds','Total Change in Cash','COGS (excluding D&A) ',
    'Gross Profit ','S,G&A (excluding D&A) ','Lease Equivalent Debt ',
    'COHORT','CREDIT_PRNT','CMT_PRNT',
    'REV_OUTLIER', 'EBITDA_OUTLIER','DEBT_OUTLIER', 'CHG_DT','CHG_USR']]

    ##############################################################################################################################
    #read in reporting currency

    reporting_data = all_data[(all_data['tgtCRNCY'] != 'USD')]

    #remove old forecasts
    reporting_data = reporting_data[~((reporting_data['lfsq_year'] < 2019) & (reporting_data['STMNT_TYP_DESC'] == 'Forecast'))]

    reporting_data['FX_CONV'] = 'Reporting Currency'
    reporting_data['FX_Value'] = None
    reporting_data['FXavg_Value'] = None
    reporting_data['REV_OUTLIER'] = None
    reporting_data['EBITDA_OUTLIER'] = None
    reporting_data['DEBT_OUTLIER'] = None

    reporting_data = reporting_data[['AGNT_ID','AGNT_NM','ULT_AGNT_ID','ULT_AGNT_NM','CFIN_PRNT_NCKNM', 'CON_FIN_PRNT','TEAM_NM','SUB_SCTR_NM','SUP_ANLYST','DATA_ANLYST','PRIM_ANLYST','MRKT_SCTR_4','FDR_NCKNM','GEO_SGMNT',
    'CNTRY_OPER', 'LT_FC_IDR', 'LT_FC_OUTLOOK', 'LT_FC_RTNG_PRODUCT', 'LT_LC_IDR', 'LT_LC_RTNG_PRODUCT', 'NT_FC_LT_IDR', 'NT_FC_LT_RTNG_PRODUCT',
    'stmntMstrId', 'STMNT_DT', 'lfsq_year','STMNT_TYP_DESC', 'analistReviewed','pblshFlg','CRNCY','FX_CONV', 'FX_Value','FXavg_Value',
    'Gross Revenue','Revenue Growth (%)','Operating EBITDA (Before Income from Associates)','Operating EBITDA Margin (%)','Operating EBITDA (After Associates and Minorities)',
    'Rental Expense ','Operating EBITDAR','Operating EBITDAR Margin (%)','Operating EBITDAR after associates and minorities ','Operating EBIT','Operating EBIT Margin (%)',
    'Gross Interest Expense','Net Income','Readily Available Cash and Equivalents','Net Working Capital (Fitch-Defined)','Short-Term Debt','Total Debt with Equity Credit',
    'Senior Secured Debt','Senior Unsecured Debt','Subordinated Debt','Other Debt','Equity Credit','Total Adjusted Debt with Equity Credit ','Off Balance Sheet Debt ',
    'Net Debt ','Operating EBITDA ','Cash Interest Paid','Cash interest received ','Cash Tax','Funds Flow from Operations','FFO Margin (%)','Change in Working Capital',
    'Cash Flow from Operations (Fitch Defined)','Capital Expenditure','Capital Intensity (Capex/Revenue) %','Common Dividends','Free Cash Flow','Free Cash Flow Margin (%)',
    'Net Acquisitions and Divestitures','FFO Interest Coverage (x)','FFO Fixed Charge Coverage (x)','Operating EBITDAR/Interest Paid + Rents (x)',
    'Operating EBITDAR/Net Interest Paid + Rents (x)','Operating EBITDA/Interest Paid (x)','Total Adjusted Debt/Operating EBITDAR (x)',
    'Total Adjusted Net Debt/Operating EBITDAR (x)','Total Debt with Equity Credit/Operating EBITDA (x)','Total Net Debt With Equity Credit/Operating EBITDA (x)',
    'FFO Adjusted Leverage (x)','FFO Adjusted Net Leverage (x)', 'FFO Leverage (x)', 'FFO Net Leverage  (x)',
    'Pretax Income (Including Associate Income/Loss) ','Dividends Received Less Dividends Paid to Minorities (Inflow/(Out)flow)','Other Items Before FFO ',
    'Total Non-Operating/Non-Recurring Cash Flow','Other Investing and Financing Cash Flow Items ','Net Debt Proceeds','Net Equity Proceeds','Total Change in Cash','COGS (excluding D&A) ',
    'Gross Profit ','S,G&A (excluding D&A) ','Lease Equivalent Debt ',
    'COHORT','CREDIT_PRNT','CMT_PRNT',
    'REV_OUTLIER', 'EBITDA_OUTLIER','DEBT_OUTLIER','CHG_DT','CHG_USR']]

    #merge
    # final_data = reporting_data.append(usd_data)
    final_data = pd.concat([reporting_data, usd_data])

    #clean
    final_data['LT_FC_IDR'] = final_data['LT_FC_IDR'].values.astype(str)
    final_data['LT_FC_IDR'] = final_data['LT_FC_IDR'].str.replace(r"\(.*\)","")
    final_data.loc[final_data['LT_FC_IDR'] == 'NR','LT_FC_IDR'] = None
    final_data.loc[final_data['LT_FC_IDR'] == 'WD','LT_FC_IDR'] = None

    final_data['LT_LC_IDR'] = final_data['LT_LC_IDR'].values.astype(str)
    final_data['LT_LC_IDR'] = final_data['LT_LC_IDR'].str.replace(r"\(.*\)","")
    final_data.loc[final_data['LT_LC_IDR'] == 'NR','LT_LC_IDR'] = None
    final_data.loc[final_data['LT_LC_IDR'] == 'WD','LT_LC_IDR'] = None

    spec_grade = ['AAA', 'AA+', 'AA', 'AA-', 'A+', 'A', 'A-', 'BBB+', 'BBB', 'BBB-']
    final_data.loc[(final_data['LT_FC_IDR'].isin(spec_grade)) | (final_data['LT_LC_IDR'].isin(spec_grade)),'GRADE'] = 'Investment Grade'
    final_data.loc[(~final_data['LT_FC_IDR'].isin(spec_grade)) | (~final_data['LT_LC_IDR'].isin(spec_grade)),'GRADE'] = 'Speculative Grade'
    final_data.loc[final_data['GRADE'].isnull(),'GRADE'] = 'NA'

    final_data.loc[final_data['LT_FC_IDR'].isnull(), 'LT_FC_IDR'] = 'NA'
    final_data.loc[final_data['LT_LC_IDR'].isnull(), 'LT_LC_IDR'] = 'NA'

    final_data.loc[final_data['analistReviewed'] == False, 'analistReviewed'] = 'Not Reviewed'
    final_data.loc[final_data['analistReviewed'] == True, 'analistReviewed'] = 'Reviewed'

    final_data.loc[final_data['pblshFlg'] == False, 'pblshFlg'] = 'Not Published'
    final_data.loc[final_data['pblshFlg'] == True, 'pblshFlg'] = 'Published'


    final_data.to_csv(loc + 'data.csv', index = False)

    log.debug("Upload files to S3")
    s3 = boto3.resource('s3')

    for filename in os.listdir("/tmp"):
        if filename == "data.csv":
            destination = "compstatsdashboard/" + filename
            log.debug("Uploaded file to S3" + filename)
            s3.meta.client.upload_file(
                "/tmp/" + filename, bucket_name, destination)
            continue
        else:
            continue
    ###########################################################################################################################################
    ##############################End of mergeData#############################################################################################
    ###########################################################################################################################################


# Entry point
try:
    run_compstat_dashboard()
except Exception as e:
    log.debug(f'Error while running script:{e}')
    eu.email_on_error()