# WFTD_bot, a Python bot designed to interact with Slack
---

Created May 2016, last updated May 2016

---

**Purpose:** WFTD\_bot, or "Words For The Day Bot”, was created to function in a communal writer’s group, tracking how many words each member wrote on their stories.  Writers can update their totals at any point during the day, and WFTD\_bot captures these numbers and record them in log files.  WFTD\_bot can, upon request, also provide various statistics, such as current words for the day (WFTD) recorded, WFTD counts for a previous day, and overall averages and totals for the month or current calendar year.

**Language:** WFTD_bot is coded entirely in Python.

**Packages and interfacing:** WFTD_bot uses several Python packages, with the most important being slackclient.  This package allows for easier structuring of API calls, needed for the Python program to interface with the Slack hangout, both for posting messages and retrieving activity to collect values.

WFTD_bot also uses the following Python packages: time, re, os, datetime, string, random

**Log files:** In order to reduce the amount of memory used by the Python program, and to allow for analysis of statistics with outside programs, WFTD\_bot records all information in CSV (comma separated values) log files.  WFTD_bot creates a unique log file for each user, in which WFTD counts are recorded along with the time and date of that message being posted to the Slack group.

---

## Interacting with WFTD_bot

WFTD\_bot looks for particular word combinations in messages.  Most messages also require that the bot’s unique ID be used, which is done by tagging the bot in the message with “@wftd_bot”.

| Keyword(s)     | Bot tagged? | Result                              |
| -------------- | :---------: | ----------------------------------- |
| Hello          | Yes         | Says hello to the bot.  |
| +(number)      | No          | Adds that number to the user’s WFTD, written in log file |
| WFTD           | Yes         | Bot prints user’s current day total |
| WFTM           | Yes         | Bot prints user’s monthly word total|
| WFTY           | Yes         | Bot prints user’s yearly word total |
| WFTD, yesterday| Yes         | Bot prints user’s WFTD for the previous day (if available) |
| WFTD, @other_user | Yes | Bot prints WFTD for specified (tagged) user. |
| average, month | Yes         | Bot prints user's average WFTD for the current month |
| average, year  | Yes         | Bot prints user's average WFTD for the current year, including zero days |
| average, year, nonzero | Yes | Bot prints user's average WFTD for the year, calculated based only on days when the user had at least 1 WFTD entry |
| election      | Yes          | This one's a secret; try it yourself! |



