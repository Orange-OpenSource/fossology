#!/usr/bin/env python
#
# Copyright 2020
# SPDX-License-Identifier: GPL-2.0
# Author: Darshan Kansagara <kansagara.darshan97@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 2 as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import psycopg2
import os

# Reading the db config file
DB_CONFIG_FILE = "/usr/local/etc/fossology/Db.conf"
CONFIG_STATIC = dict()
# parse DB_CONFIG_FILE
with open(DB_CONFIG_FILE, mode="r") as dbf:
    config_entry = dbf.readline()
    while config_entry:
        config_entry = config_entry.split("=")
        CONFIG_STATIC[config_entry[0]] = config_entry[1].strip().replace(";", "")
        config_entry = dbf.readline()

# produces "conf1=val1 conf2=val2 conf3=val3 ..."
config = " ".join(["=".join(config) for config in CONFIG_STATIC.items()])

connection = psycopg2.connect(config)

def _query(connection, query, single=True):
    try : 
        cur = connection.cursor()
        cur.execute(query)
        result = cur.fetchone() if single else cur.fetchall()
        return result
    except :
        print("Error in executing the query : "+ query)


#fetching FossDash URL from DB
query = "select * from sysconfig where variablename='FossDashReportingAPIUrl'"
fossdash_url_record = _query(connection,query)
if fossdash_url_record == None :
    print("No record found with variable name FossDashReportingAPIUrl")
else :
    # print("record = ", fossdash_url_record)
    # print("type = ", type(fossdash_url_record))
    fossdash_url = fossdash_url_record[2]
    print("conf_value_fossDash_URL = ", fossdash_url)

    try :
        # Writting FossDash URL into fossdash.conf file
        f = open("/usr/local/etc/fossology/fossdash.conf", "w+")
        f.write("FOSSDASH_URL="+fossdash_url)
        f.close()
    except Exception as e :
        print("Exception occured in run_me.py")
        print(e)
    finally:
        f.close()

# #fetching FossDash Script Cron Schedule from DB
# query = "select * from sysconfig where variablename='FossDashScriptCronSchedule'"
# fossdash_cron_schedule_record =  _query(connection,query)
# if fossdash_url_record == None :
#     print("No record found with variable name FossDashScriptCronSchedule")
# else :
#     # print("record = ", fossdash_cron_schedule_record)
#     fossdash_cron_schedule = fossdash_cron_schedule_record[2]
#     print("conf_value_fossDash_URL = ", fossdash_cron_schedule)

#     try:
#         # Writting cron schedule data into cron job file
#         f = open("/etc/cron.d/fossology", "w+")
#         # file content would be  = */1 * * * * root /fossology/fossdash-publish.run >> /tmp/fossdash.log 2>&1
#         # Fix me : Here we need to give give installation path of script
#         f.write(fossdash_cron_schedule + " root /fossology/fossdash-publish.run >> /tmp/fossdash.log 2>&1")
#         f.write("\n")
#         f.close()
#     except Exception as e :
#         print("Exception occured in run_me.py")
#         print(e)
#     finally:
#         f.close()

if connection:
    connection.close()
